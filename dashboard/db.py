from __future__ import annotations

import sqlite3
from typing import Iterable, Sequence


DEFAULT_DB_PATH = "data/reddit/reddit_reference.sqlite"


class ManagedConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback):  # type: ignore[override]
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def connect_db(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, factory=ManagedConnection)
    conn.row_factory = sqlite3.Row
    return conn


def _placeholders(values: Sequence[str]) -> str:
    return ", ".join("?" for _ in values)


def get_collection_summaries(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    query = """
    WITH latest_runs AS (
        SELECT rs1.*
        FROM run_sources rs1
        WHERE NOT EXISTS (
            SELECT 1
            FROM run_sources rs2
            WHERE rs2.source_id = rs1.source_id
              AND rs2.run_id > rs1.run_id
        )
    )
    SELECT
        s.source_id,
        s.enabled,
        s.subreddit,
        s.notes,
        (
            SELECT COUNT(*)
            FROM reddit_posts rp
            WHERE rp.source_id = s.source_id
        ) AS post_count,
        (
            SELECT COUNT(*)
            FROM reddit_comments rc
            WHERE rc.source_id = s.source_id
        ) AS comment_count,
        latest_runs.status AS latest_status,
        latest_runs.posts_count AS latest_posts_count,
        latest_runs.comments_count AS latest_comments_count,
        latest_runs.links_count AS latest_links_count,
        latest_runs.reference_hints_count AS latest_reference_hints_count,
        latest_runs.error_type,
        NULL AS latest_finished_at,
        MAX(
            COALESCE((SELECT MAX(rp.last_seen_at) FROM reddit_posts rp WHERE rp.source_id = s.source_id), ''),
            COALESCE((SELECT MAX(rc.last_seen_at) FROM reddit_comments rc WHERE rc.source_id = s.source_id), '')
        ) AS last_seen_at
    FROM sources s
    LEFT JOIN latest_runs ON latest_runs.source_id = s.source_id
    ORDER BY s.source_id COLLATE NOCASE ASC
    """
    return list(conn.execute(query))


def get_feed_posts(
    conn: sqlite3.Connection,
    source_ids: Sequence[str],
    *,
    limit: int = 25,
    offset: int = 0,
) -> list[sqlite3.Row]:
    if not source_ids:
        raise ValueError("source_ids must not be empty")

    placeholders = _placeholders(source_ids)
    query = f"""
    SELECT
        reddit_post_id,
        source_id,
        subreddit,
        title,
        author,
        selftext,
        permalink,
        domain,
        outbound_url,
        created_utc,
        last_seen_at,
        current_score,
        current_num_comments
    FROM reddit_posts
    WHERE source_id IN ({placeholders})
    ORDER BY created_utc DESC, reddit_post_id DESC
    LIMIT ? OFFSET ?
    """
    params = [*source_ids, limit, offset]
    return list(conn.execute(query, params))


def get_post_detail(conn: sqlite3.Connection, reddit_post_id: str) -> dict[str, object] | None:
    post = conn.execute(
        """
        SELECT
            reddit_post_id,
            source_id,
            subreddit,
            title,
            author,
            selftext,
            permalink,
            domain,
            outbound_url,
            created_utc,
            last_seen_at,
            current_score,
            current_num_comments
        FROM reddit_posts
        WHERE reddit_post_id = ?
        """,
        (reddit_post_id,),
    ).fetchone()
    if post is None:
        return None

    comments = list(
        conn.execute(
            """
            SELECT
                reddit_comment_id,
                reddit_post_id,
                source_id,
                subreddit,
                author,
                body,
                permalink,
                depth,
                created_utc,
                last_seen_at,
                current_score
            FROM reddit_comments
            WHERE reddit_post_id = ?
            ORDER BY created_utc ASC, reddit_comment_id ASC
            """,
            (reddit_post_id,),
        )
    )
    links = list(
        conn.execute(
            """
            SELECT
                link_id,
                run_id,
                source_id,
                subreddit,
                reddit_post_id,
                reddit_comment_id,
                source_type,
                url,
                domain,
                post_permalink,
                comment_permalink
            FROM extracted_links
            WHERE reddit_post_id = ?
            ORDER BY link_id ASC
            """,
            (reddit_post_id,),
        )
    )
    reference_hints = list(
        conn.execute(
            """
            SELECT
                reference_hint_id,
                run_id,
                source_id,
                subreddit,
                reddit_post_id,
                reddit_comment_id,
                source_type,
                hint_kind,
                hint_value,
                evidence,
                post_permalink,
                comment_permalink
            FROM reference_hints
            WHERE reddit_post_id = ?
            ORDER BY reference_hint_id ASC
            """,
            (reddit_post_id,),
        )
    )
    return {
        "post": post,
        "comments": comments,
        "links": links,
        "reference_hints": reference_hints,
    }


def normalize_selected_sources(source_ids: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for source_id in source_ids:
        cleaned = source_id.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        normalized.append(cleaned)
    return normalized
