#!/usr/bin/env python3
"""Collect reference-only Reddit data for AAN research support."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from reddit_reference_db import (
    connect_db,
    finalize_run,
    init_db,
    insert_fetch_log,
    insert_link,
    insert_reference_hint,
    insert_run,
    sync_sources,
    upsert_comment,
    upsert_post,
)

SCHEMA_VERSION = "1.1"
URL_RE = re.compile(r"https?://[^\s)\]}>\"']+")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
PMID_URL_RE = re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/?", re.IGNORECASE)
ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", re.IGNORECASE)
ARXIV_TEXT_RE = re.compile(r"\barXiv:([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)\b", re.IGNORECASE)
PMCID_URL_RE = re.compile(r"pmc\.ncbi\.nlm\.nih\.gov/articles/(PMC\d+)/?", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/reddit_reference_sources.json", help="Path to collector config JSON")
    parser.add_argument("--output-dir", default="data/reddit", help="Base output directory")
    parser.add_argument("--db-path", default=None, help="Path to sqlite database (default: <output-dir>/reddit_reference.sqlite)")
    parser.add_argument("--source-id", action="append", dest="source_ids", help="Only collect the specified source_id (repeatable)")
    parser.add_argument("--max-posts-override", type=int, default=None, help="Override per-listing max_posts for validation/smaller runs")
    parser.add_argument("--max-comments-override", type=int, default=None, help="Override max_comments_per_post for validation/smaller runs")
    parser.add_argument("--no-comments", action="store_true", help="Skip per-post comment collection")
    parser.add_argument("--listing-sort", action="append", dest="listing_sorts", help="Only collect listing modes whose sort matches this value (repeatable)")
    parser.add_argument("--since-date", default=None, help="Only keep posts/comments created on or after this UTC date (YYYY-MM-DD)")
    parser.add_argument("--pause-seconds-override", type=float, default=None, help="Override pause_between_requests_seconds for slower/politer runs")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_since_date(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def json_dump(path: Path, payload: dict) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def jsonl_dump(path: Path, rows: Iterable[dict]) -> int:
    ensure_dir(path.parent)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def parse_retry_after(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    try:
        seconds = float(value)
    except ValueError:
        return None
    return max(seconds, 0.0)


def fetch_json(
    url: str,
    user_agent: str,
    timeout: int,
    *,
    max_attempts: int = 4,
    retry_backoff_seconds: float = 15.0,
    retry_statuses: Optional[Iterable[int]] = None,
) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    retry_statuses = set(retry_statuses or {429, 500, 502, 503, 504})
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in retry_statuses or attempt >= max_attempts:
                raise
            retry_after = parse_retry_after(exc.headers.get("Retry-After"))
            sleep_seconds = retry_after if retry_after is not None else retry_backoff_seconds * attempt
            time.sleep(sleep_seconds)
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt >= max_attempts:
                raise
            time.sleep(retry_backoff_seconds * attempt)
    if last_error:
        raise last_error
    raise RuntimeError(f"Failed to fetch {url}")


def listing_url(base_url: str, subreddit: str, sort: str, limit: int, after: Optional[str], time_filter: Optional[str]) -> str:
    params = {"limit": str(limit), "raw_json": "1"}
    if after:
        params["after"] = after
    if time_filter:
        params["t"] = time_filter
    return f"{base_url}/r/{subreddit}/{sort}.json?{urllib.parse.urlencode(params)}"


def comments_url(base_url: str, permalink: str, limit: int, sort: str) -> str:
    params = urllib.parse.urlencode({"limit": str(limit), "sort": sort, "raw_json": "1"})
    return f"{base_url}{permalink}.json?{params}"


def normalize_url(url: str) -> str:
    return url.rstrip(".,;:!?)\"")


def extract_urls(text: Optional[str]) -> List[str]:
    if not text:
        return []
    seen: List[str] = []
    for match in URL_RE.findall(text):
        url = normalize_url(match)
        if url not in seen:
            seen.append(url)
    return seen


def extract_reference_hints(text: Optional[str], urls: Iterable[str]) -> List[dict]:
    hints: List[dict] = []
    seen = set()

    def add(kind: str, value: str, evidence: str) -> None:
        key = (kind, value)
        if key in seen:
            return
        seen.add(key)
        hints.append({"kind": kind, "value": value, "evidence": evidence})

    if text:
        for match in DOI_RE.findall(text):
            add("doi", match, match)
        for match in ARXIV_TEXT_RE.findall(text):
            add("arxiv", match, match)

    for url in urls:
        pmid_match = PMID_URL_RE.search(url)
        if pmid_match:
            add("pmid", pmid_match.group(1), url)
        pmcid_match = PMCID_URL_RE.search(url)
        if pmcid_match:
            add("pmcid", pmcid_match.group(1), url)
        arxiv_match = ARXIV_URL_RE.search(url)
        if arxiv_match:
            add("arxiv", arxiv_match.group(1), url)
        for doi_match in DOI_RE.findall(url):
            add("doi", doi_match, url)

    return hints


def flatten_comment_tree(children: List[dict], *, post_id: str, post_permalink: str, subreddit: str, source_id: str, run_id: str, max_comments: int) -> List[dict]:
    rows: List[dict] = []

    def walk(nodes: List[dict], depth: int) -> None:
        for node in nodes:
            if len(rows) >= max_comments:
                return
            if node.get("kind") != "t1":
                continue
            data = node.get("data", {})
            body = data.get("body") or ""
            urls = extract_urls(body)
            rows.append(
                {
                    "run_id": run_id,
                    "source_id": source_id,
                    "subreddit": subreddit,
                    "post_id": post_id,
                    "comment_id": data.get("id"),
                    "parent_id": data.get("parent_id"),
                    "depth": depth,
                    "author": data.get("author"),
                    "score": data.get("score"),
                    "created_utc": data.get("created_utc"),
                    "permalink": f"https://www.reddit.com{data.get('permalink', post_permalink)}",
                    "body": body,
                    "urls": urls,
                    "reference_hints": extract_reference_hints(body, urls),
                }
            )
            replies = data.get("replies")
            if isinstance(replies, dict):
                walk(replies.get("data", {}).get("children", []), depth + 1)
            if len(rows) >= max_comments:
                return

    walk(children, 0)
    return rows


def collect_listing(source: dict, defaults: dict, args: argparse.Namespace, run_id: str) -> Tuple[List[dict], List[dict], List[dict], List[dict], List[dict]]:
    base_url = defaults["base_url"].rstrip("/")
    timeout = int(defaults["request_timeout_seconds"])
    pause_seconds = args.pause_seconds_override if args.pause_seconds_override is not None else float(defaults["pause_between_requests_seconds"])
    retry_backoff_seconds = float(defaults.get("retry_backoff_seconds", max(15.0, pause_seconds * 5)))
    max_request_attempts = int(defaults.get("max_request_attempts", 4))
    user_agent = defaults["user_agent"]
    collect_comments = bool(defaults.get("collect_comments", True)) and not args.no_comments
    max_comments = args.max_comments_override or int(defaults.get("max_comments_per_post", 20))
    limit_per_request = min(int(defaults.get("max_posts_per_listing", 75)), 100)
    since_utc = parse_since_date(args.since_date)

    posts: List[dict] = []
    comments: List[dict] = []
    links: List[dict] = []
    reference_hints: List[dict] = []
    fetch_log: List[dict] = []
    seen_post_ids = set()

    subreddit = source["subreddit"]
    notes = source.get("notes")

    listing_modes = source.get("listing_modes", [])
    if args.listing_sorts:
        allowed_sorts = set(args.listing_sorts)
        listing_modes = [mode for mode in listing_modes if mode.get("sort") in allowed_sorts]

    for listing_mode in listing_modes:
        sort = listing_mode["sort"]
        time_filter = listing_mode.get("time_filter")
        remaining = args.max_posts_override or int(listing_mode.get("max_posts", defaults.get("max_posts_per_listing", 75)))
        after = None

        while remaining > 0:
            batch_limit = min(limit_per_request, remaining, 100)
            url = listing_url(base_url, subreddit, sort, batch_limit, after, time_filter)
            payload = fetch_json(
                url,
                user_agent=user_agent,
                timeout=timeout,
                max_attempts=max_request_attempts,
                retry_backoff_seconds=retry_backoff_seconds,
            )
            children = payload.get("data", {}).get("children", [])
            after = payload.get("data", {}).get("after")
            fetch_log.append({"url": url, "sort": sort, "time_filter": time_filter, "returned_children": len(children), "after": after})

            if not children:
                break

            stop_paging_new = False
            kept_in_batch = 0
            for child in children:
                data = child.get("data", {})
                post_id = data.get("id")
                created_utc = data.get("created_utc")
                if since_utc is not None and created_utc is not None and created_utc < since_utc:
                    if sort == "new" and not time_filter:
                        stop_paging_new = True
                    continue
                if post_id in seen_post_ids:
                    continue
                seen_post_ids.add(post_id)
                kept_in_batch += 1
                body = data.get("selftext") or ""
                post_urls = extract_urls(body)
                outbound_url = data.get("url_overridden_by_dest")
                if not outbound_url and not data.get("is_self"):
                    outbound_url = data.get("url")
                if outbound_url and outbound_url.startswith("/"):
                    outbound_url = f"https://www.reddit.com{outbound_url}"
                all_urls = list(post_urls)
                if outbound_url and outbound_url not in all_urls:
                    all_urls.append(outbound_url)
                hints = extract_reference_hints(body, all_urls)
                post_row = {
                    "run_id": run_id,
                    "source_id": source["source_id"],
                    "subreddit": subreddit,
                    "sort": sort,
                    "time_filter": time_filter,
                    "source_kind": source.get("source_kind"),
                    "distribution_policy": defaults.get("distribution_policy", "no_distribution"),
                    "storage_policy": defaults.get("storage_policy"),
                    "notes": notes,
                    "reddit_post_id": data.get("id"),
                    "fullname": data.get("name"),
                    "title": data.get("title"),
                    "author": data.get("author"),
                    "created_utc": data.get("created_utc"),
                    "score": data.get("score"),
                    "upvote_ratio": data.get("upvote_ratio"),
                    "num_comments": data.get("num_comments"),
                    "permalink": f"https://www.reddit.com{data.get('permalink')}",
                    "domain": data.get("domain"),
                    "is_self": data.get("is_self"),
                    "over_18": data.get("over_18"),
                    "spoiler": data.get("spoiler"),
                    "stickied": data.get("stickied"),
                    "link_flair_text": data.get("link_flair_text"),
                    "url": outbound_url,
                    "selftext": body,
                    "urls": all_urls,
                    "reference_hints": hints,
                }
                posts.append(post_row)

                for url_value in all_urls:
                    links.append(
                        {
                            "run_id": run_id,
                            "source_id": source["source_id"],
                            "subreddit": subreddit,
                            "post_id": data.get("id"),
                            "comment_id": None,
                            "source_type": "post_outbound_url" if outbound_url == url_value else "post_text_url",
                            "url": url_value,
                            "domain": urllib.parse.urlparse(url_value).netloc.lower() or None,
                            "post_permalink": post_row["permalink"],
                        }
                    )

                for hint in hints:
                    reference_hints.append(
                        {
                            "run_id": run_id,
                            "source_id": source["source_id"],
                            "subreddit": subreddit,
                            "post_id": data.get("id"),
                            "comment_id": None,
                            "source_type": "post",
                            **hint,
                            "post_permalink": post_row["permalink"],
                        }
                    )

                if collect_comments and data.get("permalink"):
                    comment_payload = fetch_json(
                        comments_url(base_url, data["permalink"], max_comments, defaults.get("comment_sort", "top")),
                        user_agent=user_agent,
                        timeout=timeout,
                        max_attempts=max_request_attempts,
                        retry_backoff_seconds=retry_backoff_seconds,
                    )
                    if isinstance(comment_payload, list) and len(comment_payload) > 1:
                        comment_rows = flatten_comment_tree(
                            comment_payload[1].get("data", {}).get("children", []),
                            post_id=data.get("id"),
                            post_permalink=post_row["permalink"],
                            subreddit=subreddit,
                            source_id=source["source_id"],
                            run_id=run_id,
                            max_comments=max_comments,
                        )
                        if since_utc is not None:
                            comment_rows = [row for row in comment_rows if row.get("created_utc") is None or row["created_utc"] >= since_utc]
                        comments.extend(comment_rows)
                        for comment in comment_rows:
                            for url_value in comment["urls"]:
                                links.append(
                                    {
                                        "run_id": run_id,
                                        "source_id": source["source_id"],
                                        "subreddit": subreddit,
                                        "post_id": data.get("id"),
                                        "comment_id": comment["comment_id"],
                                        "source_type": "comment_url",
                                        "url": url_value,
                                        "domain": urllib.parse.urlparse(url_value).netloc.lower() or None,
                                        "post_permalink": post_row["permalink"],
                                        "comment_permalink": comment["permalink"],
                                    }
                                )
                            for hint in comment["reference_hints"]:
                                reference_hints.append(
                                    {
                                        "run_id": run_id,
                                        "source_id": source["source_id"],
                                        "subreddit": subreddit,
                                        "post_id": data.get("id"),
                                        "comment_id": comment["comment_id"],
                                        "source_type": "comment",
                                        **hint,
                                        "post_permalink": post_row["permalink"],
                                        "comment_permalink": comment["permalink"],
                                    }
                                )
                    time.sleep(pause_seconds)

            remaining -= kept_in_batch
            if stop_paging_new or not after:
                break
            time.sleep(pause_seconds)

    return posts, comments, links, reference_hints, fetch_log


def summarize(posts: List[dict], comments: List[dict], links: List[dict], reference_hints: List[dict], sources: List[dict], run_id: str, started_at: str, finished_at: str, errors: List[dict], db_path: str) -> dict:
    subreddits = sorted({post["subreddit"] for post in posts})
    top_domains = Counter()
    for link in links:
        parsed = urllib.parse.urlparse(link["url"])
        if parsed.netloc:
            top_domains[parsed.netloc.lower()] += 1
    reference_kind_counts = Counter(hint["kind"] for hint in reference_hints)
    return {
        "run_id": run_id,
        "schema_version": SCHEMA_VERSION,
        "started_at": started_at,
        "finished_at": finished_at,
        "db_path": db_path,
        "source_ids": [source["source_id"] for source in sources],
        "subreddits": subreddits,
        "counts": {
            "posts": len(posts),
            "comments": len(comments),
            "links": len(links),
            "reference_hints": len(reference_hints),
            "errors": len(errors),
        },
        "top_domains": [{"domain": domain, "count": count} for domain, count in top_domains.most_common(20)],
        "reference_kind_counts": dict(reference_kind_counts),
        "errors": errors,
    }


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    output_dir = Path(args.output_dir)
    db_path = Path(args.db_path) if args.db_path else output_dir / "reddit_reference.sqlite"
    config = load_json(config_path)
    defaults = config.get("defaults", {})
    all_sources = config.get("sources", [])
    enabled_sources = [source for source in all_sources if source.get("enabled")]
    if args.source_ids:
        requested = set(args.source_ids)
        enabled_sources = [source for source in enabled_sources if source.get("source_id") in requested]
    if not enabled_sources:
        raise SystemExit("No enabled sources selected")

    run_id = make_run_id()
    started_at = iso_now()
    snapshot_dir = output_dir / "snapshots" / run_id
    runs_dir = output_dir / "runs"
    ensure_dir(snapshot_dir)
    ensure_dir(runs_dir)

    connection = connect_db(db_path)
    init_db(connection)
    sync_sources(connection, all_sources, updated_at=started_at)
    insert_run(
        connection,
        run_id=run_id,
        collection_name=config.get("collection_name"),
        description=config.get("description"),
        config_path=str(config_path),
        output_dir=str(output_dir),
        db_path=str(db_path),
        started_at=started_at,
        status="running",
        max_posts_override=args.max_posts_override,
        max_comments_override=args.max_comments_override,
        no_comments=args.no_comments,
        defaults=defaults,
        source_ids=[source["source_id"] for source in enabled_sources],
    )

    all_posts: List[dict] = []
    all_comments: List[dict] = []
    all_links: List[dict] = []
    all_reference_hints: List[dict] = []
    fetch_logs: Dict[str, List[dict]] = {}
    errors: List[dict] = []
    source_counts: Dict[str, dict] = {source["source_id"]: {"status": "completed", "posts": 0, "comments": 0, "links": 0, "reference_hints": 0, "fetch_requests": 0} for source in enabled_sources}

    for source in enabled_sources:
        source_id = source["source_id"]
        try:
            posts, comments, links, reference_hints, fetch_log = collect_listing(source, defaults, args, run_id)
            fetch_logs[source_id] = fetch_log
            source_counts[source_id].update(
                {
                    "posts": len(posts),
                    "comments": len(comments),
                    "links": len(links),
                    "reference_hints": len(reference_hints),
                    "fetch_requests": len(fetch_log),
                }
            )
            all_posts.extend(posts)
            all_comments.extend(comments)
            all_links.extend(links)
            all_reference_hints.extend(reference_hints)

            observed_at = iso_now()
            with connection:
                inserted_fetches = insert_fetch_log(connection, run_id, source_id, fetch_log)
                source_counts[source_id]["fetch_requests"] = inserted_fetches
                for post in posts:
                    upsert_post(connection, post, observed_at)
                for comment in comments:
                    upsert_comment(connection, comment, observed_at)
                for link in links:
                    insert_link(connection, link)
                for hint in reference_hints:
                    insert_reference_hint(connection, hint)
        except urllib.error.HTTPError as exc:
            error_row = {"source_id": source_id, "error_type": "HTTPError", "message": str(exc)}
            errors.append(error_row)
            source_counts[source_id].update({"status": "error", "error_type": "HTTPError", "error_message": str(exc)})
        except urllib.error.URLError as exc:
            error_row = {"source_id": source_id, "error_type": "URLError", "message": str(exc)}
            errors.append(error_row)
            source_counts[source_id].update({"status": "error", "error_type": "URLError", "error_message": str(exc)})
        except Exception as exc:  # pragma: no cover
            error_row = {"source_id": source_id, "error_type": exc.__class__.__name__, "message": str(exc)}
            errors.append(error_row)
            source_counts[source_id].update({"status": "error", "error_type": exc.__class__.__name__, "error_message": str(exc)})

    finished_at = iso_now()
    summary = summarize(
        all_posts,
        all_comments,
        all_links,
        all_reference_hints,
        enabled_sources,
        run_id,
        started_at,
        finished_at,
        errors,
        str(db_path),
    )

    posts_count = jsonl_dump(snapshot_dir / "posts.jsonl", all_posts)
    comments_count = jsonl_dump(snapshot_dir / "comments.jsonl", all_comments)
    links_count = jsonl_dump(snapshot_dir / "links.jsonl", all_links)
    hints_count = jsonl_dump(snapshot_dir / "reference_hints.jsonl", all_reference_hints)
    json_dump(snapshot_dir / "summary.json", summary)
    json_dump(snapshot_dir / "fetch_log.json", fetch_logs)
    json_dump(
        runs_dir / f"{run_id}.json",
        {
            "run_id": run_id,
            "schema_version": SCHEMA_VERSION,
            "config_path": str(config_path),
            "output_dir": str(output_dir),
            "db_path": str(db_path),
            "source_ids": [source["source_id"] for source in enabled_sources],
            "started_at": started_at,
            "finished_at": finished_at,
            "counts": {
                "posts": posts_count,
                "comments": comments_count,
                "links": links_count,
                "reference_hints": hints_count,
                "errors": len(errors),
            },
            "summary_path": str(snapshot_dir / "summary.json"),
            "snapshot_dir": str(snapshot_dir),
        },
    )

    finalize_run(connection, run_id=run_id, finished_at=finished_at, status="completed_with_errors" if errors else "completed", summary=summary, errors=errors, source_counts=source_counts)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
