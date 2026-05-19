#!/usr/bin/env python3
"""Search the AAN Reddit reference SQLite corpus using FTS5."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="FTS5 query string")
    parser.add_argument("--db-path", default="data/reddit/reddit_reference.sqlite", help="Path to sqlite database")
    parser.add_argument("--kind", choices=["posts", "comments", "all"], default="all", help="Which corpus slice to search")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results per section")
    return parser.parse_args()


def connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def ensure_search_schema(connection: sqlite3.Connection, db_path: Path) -> None:
    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"
        )
    }
    required = {"posts_fts", "comments_fts", "reddit_posts", "reddit_comments"}
    missing = sorted(required - tables)
    if missing:
        missing_text = ", ".join(missing)
        raise SystemExit(
            f"Search database is not initialized at {db_path} (missing: {missing_text}). "
            "Run scripts/collect_reddit_reference.py first."
        )


def search_posts(connection: sqlite3.Connection, query: str, limit: int):
    return connection.execute(
        """
        SELECT
            p.reddit_post_id,
            p.subreddit,
            p.title,
            p.author,
            p.permalink,
            p.last_seen_at,
            snippet(posts_fts, 1, '[', ']', ' … ', 18) AS title_snippet,
            snippet(posts_fts, 2, '[', ']', ' … ', 24) AS body_snippet,
            bm25(posts_fts) AS rank
        FROM posts_fts
        JOIN reddit_posts AS p ON p.reddit_post_id = posts_fts.reddit_post_id
        WHERE posts_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (query, limit),
    ).fetchall()


def search_comments(connection: sqlite3.Connection, query: str, limit: int):
    return connection.execute(
        """
        SELECT
            c.reddit_comment_id,
            c.reddit_post_id,
            c.subreddit,
            c.author,
            c.permalink,
            c.last_seen_at,
            p.title AS post_title,
            snippet(comments_fts, 1, '[', ']', ' … ', 28) AS body_snippet,
            bm25(comments_fts) AS rank
        FROM comments_fts
        JOIN reddit_comments AS c ON c.reddit_comment_id = comments_fts.reddit_comment_id
        LEFT JOIN reddit_posts AS p ON p.reddit_post_id = c.reddit_post_id
        WHERE comments_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (query, limit),
    ).fetchall()


def main() -> int:
    args = parse_args()
    db_path = Path(args.db_path)
    if not db_path.exists():
        raise SystemExit(
            f"Search database not found at {db_path}. Run scripts/collect_reddit_reference.py first."
        )

    connection = connect(db_path)
    ensure_search_schema(connection, db_path)

    if args.kind in {"posts", "all"}:
        posts = search_posts(connection, args.query, args.limit)
        print("POSTS")
        print("=====")
        if not posts:
            print("(no matches)")
        for row in posts:
            title = row["title"] or "(untitled)"
            print(f"- r/{row['subreddit']} post {row['reddit_post_id']} by {row['author'] or '[deleted]'}")
            print(f"  title: {title}")
            if row["body_snippet"]:
                print(f"  body:  {row['body_snippet']}")
            print(f"  link:  {row['permalink']}")
            print(f"  seen:  {row['last_seen_at']}")
            print()

    if args.kind == "all":
        print()

    if args.kind in {"comments", "all"}:
        comments = search_comments(connection, args.query, args.limit)
        print("COMMENTS")
        print("========")
        if not comments:
            print("(no matches)")
        for row in comments:
            print(f"- r/{row['subreddit']} comment {row['reddit_comment_id']} by {row['author'] or '[deleted]'}")
            if row["post_title"]:
                print(f"  post:  {row['post_title']}")
            print(f"  body:  {row['body_snippet']}")
            print(f"  link:  {row['permalink']}")
            print(f"  seen:  {row['last_seen_at']}")
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
