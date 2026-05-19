#!/usr/bin/env python3
"""SQLite backend helpers for the AAN Reddit reference corpus."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List, Optional

SCHEMA_VERSION = "1.0"


def connect_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = NORMAL")
    connection.execute("PRAGMA temp_store = MEMORY")
    connection.execute("PRAGMA mmap_size = 268435456")
    return connection


def init_db(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS corpus_meta (
            meta_key TEXT PRIMARY KEY,
            meta_value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sources (
            source_id TEXT PRIMARY KEY,
            enabled INTEGER NOT NULL,
            platform TEXT,
            source_family TEXT,
            source_kind TEXT,
            subreddit TEXT,
            notes TEXT,
            source_json TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS source_listing_modes (
            source_id TEXT NOT NULL,
            listing_index INTEGER NOT NULL,
            sort TEXT NOT NULL,
            time_filter TEXT NOT NULL,
            max_posts INTEGER,
            PRIMARY KEY (source_id, listing_index),
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS collection_runs (
            run_id TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            collection_name TEXT,
            description TEXT,
            config_path TEXT NOT NULL,
            output_dir TEXT NOT NULL,
            db_path TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            status TEXT NOT NULL,
            max_posts_override INTEGER,
            max_comments_override INTEGER,
            no_comments INTEGER NOT NULL,
            defaults_json TEXT NOT NULL,
            selected_source_ids_json TEXT NOT NULL,
            errors_json TEXT,
            summary_json TEXT,
            posts_count INTEGER DEFAULT 0,
            comments_count INTEGER DEFAULT 0,
            links_count INTEGER DEFAULT 0,
            reference_hints_count INTEGER DEFAULT 0,
            fetch_requests_count INTEGER DEFAULT 0,
            error_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS run_sources (
            run_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            status TEXT NOT NULL,
            error_type TEXT,
            error_message TEXT,
            posts_count INTEGER DEFAULT 0,
            comments_count INTEGER DEFAULT 0,
            links_count INTEGER DEFAULT 0,
            reference_hints_count INTEGER DEFAULT 0,
            fetch_requests_count INTEGER DEFAULT 0,
            PRIMARY KEY (run_id, source_id),
            FOREIGN KEY (run_id) REFERENCES collection_runs(run_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fetch_requests (
            fetch_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            sort TEXT NOT NULL,
            time_filter TEXT NOT NULL,
            request_url TEXT NOT NULL,
            returned_children INTEGER NOT NULL,
            after_fullname TEXT,
            FOREIGN KEY (run_id) REFERENCES collection_runs(run_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS reddit_posts (
            reddit_post_id TEXT PRIMARY KEY,
            fullname TEXT,
            subreddit TEXT NOT NULL,
            source_id TEXT NOT NULL,
            author TEXT,
            title TEXT,
            selftext TEXT,
            permalink TEXT NOT NULL,
            domain TEXT,
            outbound_url TEXT,
            is_self INTEGER,
            over_18 INTEGER,
            spoiler INTEGER,
            stickied INTEGER,
            link_flair_text TEXT,
            created_utc REAL,
            first_seen_run_id TEXT NOT NULL,
            last_seen_run_id TEXT NOT NULL,
            first_seen_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL,
            current_score INTEGER,
            current_upvote_ratio REAL,
            current_num_comments INTEGER,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE RESTRICT,
            FOREIGN KEY (first_seen_run_id) REFERENCES collection_runs(run_id) ON DELETE RESTRICT,
            FOREIGN KEY (last_seen_run_id) REFERENCES collection_runs(run_id) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS post_observations (
            observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            reddit_post_id TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            sort TEXT NOT NULL,
            time_filter TEXT NOT NULL,
            score INTEGER,
            upvote_ratio REAL,
            num_comments INTEGER,
            observed_at TEXT NOT NULL,
            distribution_policy TEXT,
            storage_policy TEXT,
            notes TEXT,
            UNIQUE (run_id, source_id, reddit_post_id, sort, time_filter),
            FOREIGN KEY (run_id) REFERENCES collection_runs(run_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE,
            FOREIGN KEY (reddit_post_id) REFERENCES reddit_posts(reddit_post_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS reddit_comments (
            reddit_comment_id TEXT PRIMARY KEY,
            reddit_post_id TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            source_id TEXT NOT NULL,
            parent_id TEXT,
            author TEXT,
            body TEXT,
            permalink TEXT NOT NULL,
            depth INTEGER,
            created_utc REAL,
            first_seen_run_id TEXT NOT NULL,
            last_seen_run_id TEXT NOT NULL,
            first_seen_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL,
            current_score INTEGER,
            FOREIGN KEY (reddit_post_id) REFERENCES reddit_posts(reddit_post_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE RESTRICT,
            FOREIGN KEY (first_seen_run_id) REFERENCES collection_runs(run_id) ON DELETE RESTRICT,
            FOREIGN KEY (last_seen_run_id) REFERENCES collection_runs(run_id) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS comment_observations (
            observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            reddit_comment_id TEXT NOT NULL,
            reddit_post_id TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            score INTEGER,
            observed_at TEXT NOT NULL,
            UNIQUE (run_id, source_id, reddit_comment_id),
            FOREIGN KEY (run_id) REFERENCES collection_runs(run_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE,
            FOREIGN KEY (reddit_comment_id) REFERENCES reddit_comments(reddit_comment_id) ON DELETE CASCADE,
            FOREIGN KEY (reddit_post_id) REFERENCES reddit_posts(reddit_post_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS extracted_links (
            link_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            reddit_post_id TEXT NOT NULL,
            reddit_comment_id TEXT,
            source_type TEXT NOT NULL,
            url TEXT NOT NULL,
            domain TEXT,
            post_permalink TEXT,
            comment_permalink TEXT,
            FOREIGN KEY (run_id) REFERENCES collection_runs(run_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE,
            FOREIGN KEY (reddit_post_id) REFERENCES reddit_posts(reddit_post_id) ON DELETE CASCADE,
            FOREIGN KEY (reddit_comment_id) REFERENCES reddit_comments(reddit_comment_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS reference_hints (
            reference_hint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            reddit_post_id TEXT NOT NULL,
            reddit_comment_id TEXT,
            source_type TEXT NOT NULL,
            hint_kind TEXT NOT NULL,
            hint_value TEXT NOT NULL,
            evidence TEXT,
            post_permalink TEXT,
            comment_permalink TEXT,
            FOREIGN KEY (run_id) REFERENCES collection_runs(run_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE,
            FOREIGN KEY (reddit_post_id) REFERENCES reddit_posts(reddit_post_id) ON DELETE CASCADE,
            FOREIGN KEY (reddit_comment_id) REFERENCES reddit_comments(reddit_comment_id) ON DELETE CASCADE
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS posts_fts USING fts5(
            reddit_post_id UNINDEXED,
            title,
            selftext,
            tokenize = 'unicode61'
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS comments_fts USING fts5(
            reddit_comment_id UNINDEXED,
            body,
            tokenize = 'unicode61'
        );

        CREATE INDEX IF NOT EXISTS idx_posts_source_subreddit ON reddit_posts(source_id, subreddit);
        CREATE INDEX IF NOT EXISTS idx_posts_last_seen ON reddit_posts(last_seen_at);
        CREATE INDEX IF NOT EXISTS idx_post_observations_run ON post_observations(run_id, source_id);
        CREATE INDEX IF NOT EXISTS idx_comments_post ON reddit_comments(reddit_post_id);
        CREATE INDEX IF NOT EXISTS idx_comments_last_seen ON reddit_comments(last_seen_at);
        CREATE INDEX IF NOT EXISTS idx_comment_observations_run ON comment_observations(run_id, source_id);
        CREATE INDEX IF NOT EXISTS idx_links_run ON extracted_links(run_id, source_id);
        CREATE INDEX IF NOT EXISTS idx_links_domain ON extracted_links(domain);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_links_unique ON extracted_links(
            run_id, source_id, reddit_post_id, IFNULL(reddit_comment_id, ''), source_type, url
        );
        CREATE INDEX IF NOT EXISTS idx_reference_hints_run ON reference_hints(run_id, source_id);
        CREATE INDEX IF NOT EXISTS idx_reference_hints_kind_value ON reference_hints(hint_kind, hint_value);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_reference_hints_unique ON reference_hints(
            run_id, source_id, reddit_post_id, IFNULL(reddit_comment_id, ''), source_type,
            hint_kind, hint_value, IFNULL(evidence, '')
        );
        """
    )
    connection.execute(
        "INSERT INTO corpus_meta(meta_key, meta_value) VALUES(?, ?) ON CONFLICT(meta_key) DO UPDATE SET meta_value=excluded.meta_value",
        ("schema_version", SCHEMA_VERSION),
    )
    connection.commit()


def sync_sources(connection: sqlite3.Connection, sources: Iterable[dict], updated_at: str) -> None:
    for source in sources:
        connection.execute(
            """
            INSERT INTO sources (
                source_id, enabled, platform, source_family, source_kind,
                subreddit, notes, source_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET
                enabled=excluded.enabled,
                platform=excluded.platform,
                source_family=excluded.source_family,
                source_kind=excluded.source_kind,
                subreddit=excluded.subreddit,
                notes=excluded.notes,
                source_json=excluded.source_json,
                updated_at=excluded.updated_at
            """,
            (
                source["source_id"],
                1 if source.get("enabled") else 0,
                source.get("platform"),
                source.get("source_family"),
                source.get("source_kind"),
                source.get("subreddit"),
                source.get("notes"),
                json.dumps(source, ensure_ascii=False, sort_keys=True),
                updated_at,
            ),
        )
        connection.execute("DELETE FROM source_listing_modes WHERE source_id = ?", (source["source_id"],))
        for index, listing_mode in enumerate(source.get("listing_modes", [])):
            connection.execute(
                """
                INSERT INTO source_listing_modes (source_id, listing_index, sort, time_filter, max_posts)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    source["source_id"],
                    index,
                    listing_mode["sort"],
                    listing_mode.get("time_filter") or "",
                    listing_mode.get("max_posts"),
                ),
            )
    connection.commit()


def insert_run(connection: sqlite3.Connection, *, run_id: str, collection_name: Optional[str], description: Optional[str],
               config_path: str, output_dir: str, db_path: str, started_at: str, status: str,
               max_posts_override: Optional[int], max_comments_override: Optional[int],
               no_comments: bool, defaults: dict, source_ids: List[str]) -> None:
    connection.execute(
        """
        INSERT INTO collection_runs (
            run_id, schema_version, collection_name, description, config_path, output_dir, db_path,
            started_at, status, max_posts_override, max_comments_override, no_comments,
            defaults_json, selected_source_ids_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            SCHEMA_VERSION,
            collection_name,
            description,
            config_path,
            output_dir,
            db_path,
            started_at,
            status,
            max_posts_override,
            max_comments_override,
            1 if no_comments else 0,
            json.dumps(defaults, ensure_ascii=False, sort_keys=True),
            json.dumps(source_ids, ensure_ascii=False),
        ),
    )
    connection.commit()


def upsert_post(connection: sqlite3.Connection, post: dict, observed_at: str) -> None:
    connection.execute(
        """
        INSERT INTO reddit_posts (
            reddit_post_id, fullname, subreddit, source_id, author, title, selftext, permalink, domain,
            outbound_url, is_self, over_18, spoiler, stickied, link_flair_text, created_utc,
            first_seen_run_id, last_seen_run_id, first_seen_at, last_seen_at,
            current_score, current_upvote_ratio, current_num_comments
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(reddit_post_id) DO UPDATE SET
            fullname=excluded.fullname,
            subreddit=excluded.subreddit,
            source_id=excluded.source_id,
            author=excluded.author,
            title=excluded.title,
            selftext=excluded.selftext,
            permalink=excluded.permalink,
            domain=excluded.domain,
            outbound_url=excluded.outbound_url,
            is_self=excluded.is_self,
            over_18=excluded.over_18,
            spoiler=excluded.spoiler,
            stickied=excluded.stickied,
            link_flair_text=excluded.link_flair_text,
            created_utc=excluded.created_utc,
            last_seen_run_id=excluded.last_seen_run_id,
            last_seen_at=excluded.last_seen_at,
            current_score=excluded.current_score,
            current_upvote_ratio=excluded.current_upvote_ratio,
            current_num_comments=excluded.current_num_comments
        """,
        (
            post["reddit_post_id"],
            post.get("fullname"),
            post["subreddit"],
            post["source_id"],
            post.get("author"),
            post.get("title"),
            post.get("selftext"),
            post["permalink"],
            post.get("domain"),
            post.get("url"),
            _bool_int(post.get("is_self")),
            _bool_int(post.get("over_18")),
            _bool_int(post.get("spoiler")),
            _bool_int(post.get("stickied")),
            post.get("link_flair_text"),
            post.get("created_utc"),
            post["run_id"],
            post["run_id"],
            observed_at,
            observed_at,
            post.get("score"),
            post.get("upvote_ratio"),
            post.get("num_comments"),
        ),
    )
    connection.execute(
        """
        INSERT INTO post_observations (
            run_id, source_id, reddit_post_id, subreddit, sort, time_filter, score,
            upvote_ratio, num_comments, observed_at, distribution_policy, storage_policy, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(run_id, source_id, reddit_post_id, sort, time_filter) DO UPDATE SET
            score=excluded.score,
            upvote_ratio=excluded.upvote_ratio,
            num_comments=excluded.num_comments,
            observed_at=excluded.observed_at,
            distribution_policy=excluded.distribution_policy,
            storage_policy=excluded.storage_policy,
            notes=excluded.notes
        """,
        (
            post["run_id"],
            post["source_id"],
            post["reddit_post_id"],
            post["subreddit"],
            post["sort"],
            post.get("time_filter") or "",
            post.get("score"),
            post.get("upvote_ratio"),
            post.get("num_comments"),
            observed_at,
            post.get("distribution_policy"),
            post.get("storage_policy"),
            post.get("notes"),
        ),
    )
    connection.execute("DELETE FROM posts_fts WHERE reddit_post_id = ?", (post["reddit_post_id"],))
    connection.execute(
        "INSERT INTO posts_fts (reddit_post_id, title, selftext) VALUES (?, ?, ?)",
        (post["reddit_post_id"], post.get("title") or "", post.get("selftext") or ""),
    )


def upsert_comment(connection: sqlite3.Connection, comment: dict, observed_at: str) -> None:
    connection.execute(
        """
        INSERT INTO reddit_comments (
            reddit_comment_id, reddit_post_id, subreddit, source_id, parent_id, author, body,
            permalink, depth, created_utc, first_seen_run_id, last_seen_run_id,
            first_seen_at, last_seen_at, current_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(reddit_comment_id) DO UPDATE SET
            reddit_post_id=excluded.reddit_post_id,
            subreddit=excluded.subreddit,
            source_id=excluded.source_id,
            parent_id=excluded.parent_id,
            author=excluded.author,
            body=excluded.body,
            permalink=excluded.permalink,
            depth=excluded.depth,
            created_utc=excluded.created_utc,
            last_seen_run_id=excluded.last_seen_run_id,
            last_seen_at=excluded.last_seen_at,
            current_score=excluded.current_score
        """,
        (
            comment["comment_id"],
            comment["post_id"],
            comment["subreddit"],
            comment["source_id"],
            comment.get("parent_id"),
            comment.get("author"),
            comment.get("body"),
            comment["permalink"],
            comment.get("depth"),
            comment.get("created_utc"),
            comment["run_id"],
            comment["run_id"],
            observed_at,
            observed_at,
            comment.get("score"),
        ),
    )
    connection.execute(
        """
        INSERT INTO comment_observations (
            run_id, source_id, reddit_comment_id, reddit_post_id, subreddit, score, observed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(run_id, source_id, reddit_comment_id) DO UPDATE SET
            score=excluded.score,
            observed_at=excluded.observed_at
        """,
        (
            comment["run_id"],
            comment["source_id"],
            comment["comment_id"],
            comment["post_id"],
            comment["subreddit"],
            comment.get("score"),
            observed_at,
        ),
    )
    connection.execute("DELETE FROM comments_fts WHERE reddit_comment_id = ?", (comment["comment_id"],))
    connection.execute(
        "INSERT INTO comments_fts (reddit_comment_id, body) VALUES (?, ?)",
        (comment["comment_id"], comment.get("body") or ""),
    )


def insert_link(connection: sqlite3.Connection, link: dict) -> None:
    connection.execute(
        """
        INSERT OR IGNORE INTO extracted_links (
            run_id, source_id, subreddit, reddit_post_id, reddit_comment_id,
            source_type, url, domain, post_permalink, comment_permalink
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            link["run_id"],
            link["source_id"],
            link["subreddit"],
            link["post_id"],
            link.get("comment_id"),
            link["source_type"],
            link["url"],
            link.get("domain"),
            link.get("post_permalink"),
            link.get("comment_permalink"),
        ),
    )


def insert_reference_hint(connection: sqlite3.Connection, hint: dict) -> None:
    connection.execute(
        """
        INSERT OR IGNORE INTO reference_hints (
            run_id, source_id, subreddit, reddit_post_id, reddit_comment_id, source_type,
            hint_kind, hint_value, evidence, post_permalink, comment_permalink
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            hint["run_id"],
            hint["source_id"],
            hint["subreddit"],
            hint["post_id"],
            hint.get("comment_id"),
            hint["source_type"],
            hint["kind"],
            hint["value"],
            hint.get("evidence"),
            hint.get("post_permalink"),
            hint.get("comment_permalink"),
        ),
    )


def insert_fetch_log(connection: sqlite3.Connection, run_id: str, source_id: str, fetch_log: Iterable[dict]) -> int:
    count = 0
    for row in fetch_log:
        connection.execute(
            """
            INSERT INTO fetch_requests (
                run_id, source_id, sort, time_filter, request_url, returned_children, after_fullname
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                source_id,
                row["sort"],
                row.get("time_filter") or "",
                row["url"],
                row["returned_children"],
                row.get("after"),
            ),
        )
        count += 1
    return count


def finalize_run(connection: sqlite3.Connection, *, run_id: str, finished_at: str, status: str,
                 summary: dict, errors: List[dict], source_counts: Dict[str, dict]) -> None:
    fetch_requests_count = sum(counts.get("fetch_requests", 0) for counts in source_counts.values())
    posts_count = sum(counts.get("posts", 0) for counts in source_counts.values())
    comments_count = sum(counts.get("comments", 0) for counts in source_counts.values())
    links_count = sum(counts.get("links", 0) for counts in source_counts.values())
    reference_hints_count = sum(counts.get("reference_hints", 0) for counts in source_counts.values())

    for source_id, counts in source_counts.items():
        connection.execute(
            """
            INSERT INTO run_sources (
                run_id, source_id, status, error_type, error_message,
                posts_count, comments_count, links_count, reference_hints_count, fetch_requests_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_id, source_id) DO UPDATE SET
                status=excluded.status,
                error_type=excluded.error_type,
                error_message=excluded.error_message,
                posts_count=excluded.posts_count,
                comments_count=excluded.comments_count,
                links_count=excluded.links_count,
                reference_hints_count=excluded.reference_hints_count,
                fetch_requests_count=excluded.fetch_requests_count
            """,
            (
                run_id,
                source_id,
                counts.get("status", "completed"),
                counts.get("error_type"),
                counts.get("error_message"),
                counts.get("posts", 0),
                counts.get("comments", 0),
                counts.get("links", 0),
                counts.get("reference_hints", 0),
                counts.get("fetch_requests", 0),
            ),
        )

    connection.execute(
        """
        UPDATE collection_runs
        SET finished_at = ?,
            status = ?,
            summary_json = ?,
            errors_json = ?,
            posts_count = ?,
            comments_count = ?,
            links_count = ?,
            reference_hints_count = ?,
            fetch_requests_count = ?,
            error_count = ?
        WHERE run_id = ?
        """,
        (
            finished_at,
            status,
            json.dumps(summary, ensure_ascii=False, sort_keys=True),
            json.dumps(errors, ensure_ascii=False),
            posts_count,
            comments_count,
            links_count,
            reference_hints_count,
            fetch_requests_count,
            len(errors),
            run_id,
        ),
    )
    connection.commit()


def _bool_int(value: Optional[bool]) -> Optional[int]:
    if value is None:
        return None
    return 1 if value else 0
