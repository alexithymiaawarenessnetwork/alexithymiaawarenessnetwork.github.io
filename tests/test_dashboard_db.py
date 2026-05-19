import os
import sqlite3
import tempfile
import unittest


SCHEMA_SQL = """
CREATE TABLE sources (
    source_id TEXT PRIMARY KEY,
    enabled INTEGER,
    subreddit TEXT,
    notes TEXT,
    updated_at TEXT
);

CREATE TABLE reddit_posts (
    reddit_post_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    selftext TEXT,
    permalink TEXT NOT NULL,
    domain TEXT,
    outbound_url TEXT,
    created_utc REAL,
    last_seen_at TEXT,
    current_score INTEGER,
    current_num_comments INTEGER
);

CREATE TABLE reddit_comments (
    reddit_comment_id TEXT PRIMARY KEY,
    reddit_post_id TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    source_id TEXT NOT NULL,
    author TEXT,
    body TEXT,
    permalink TEXT NOT NULL,
    depth INTEGER,
    created_utc REAL,
    last_seen_at TEXT,
    current_score INTEGER
);

CREATE TABLE run_sources (
    run_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    status TEXT,
    posts_count INTEGER,
    comments_count INTEGER,
    links_count INTEGER,
    reference_hints_count INTEGER,
    error_type TEXT,
    started_at TEXT,
    finished_at TEXT
);

CREATE TABLE extracted_links (
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
    comment_permalink TEXT
);

CREATE TABLE reference_hints (
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
    comment_permalink TEXT
);
"""


def seed_db(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.executemany(
        "INSERT INTO sources(source_id, enabled, subreddit, notes, updated_at) VALUES (?, ?, ?, ?, ?)",
        [
            ("reddit_alexithymia", 1, "alexithymia", "primary", "2026-05-19T00:00:00+00:00"),
            ("reddit_cptsd", 0, "CPTSD", "disabled candidate", "2026-05-19T00:00:00+00:00"),
        ],
    )
    conn.executemany(
        "INSERT INTO reddit_posts(reddit_post_id, source_id, subreddit, title, author, selftext, permalink, domain, outbound_url, created_utc, last_seen_at, current_score, current_num_comments) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("p-newest", "reddit_alexithymia", "alexithymia", "Newest alexithymia post", "alice", "body newest", "/r/alexithymia/comments/p-newest", "self.alexithymia", None, 200.0, "2026-05-19T12:00:00+00:00", 12, 2),
            ("p-middle", "reddit_cptsd", "CPTSD", "Middle CPTSD post", "bob", "body middle", "/r/CPTSD/comments/p-middle", "self.CPTSD", None, 150.0, "2026-05-19T11:00:00+00:00", 8, 1),
            ("p-oldest", "reddit_alexithymia", "alexithymia", "Oldest alexithymia post", "carol", "body oldest", "/r/alexithymia/comments/p-oldest", "example.com", "https://example.com/old", 100.0, "2026-05-18T10:00:00+00:00", 5, 3),
        ],
    )
    conn.executemany(
        "INSERT INTO reddit_comments(reddit_comment_id, reddit_post_id, subreddit, source_id, author, body, permalink, depth, created_utc, last_seen_at, current_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("c-1", "p-newest", "alexithymia", "reddit_alexithymia", "dave", "first comment", "/r/alexithymia/comments/p-newest/c-1", 0, 201.0, "2026-05-19T12:05:00+00:00", 3),
            ("c-2", "p-newest", "alexithymia", "reddit_alexithymia", "erin", "nested comment", "/r/alexithymia/comments/p-newest/c-2", 1, 202.0, "2026-05-19T12:06:00+00:00", 2),
            ("c-3", "p-middle", "CPTSD", "reddit_cptsd", "frank", "other source comment", "/r/CPTSD/comments/p-middle/c-3", 0, 151.0, "2026-05-19T11:05:00+00:00", 1),
        ],
    )
    conn.executemany(
        "INSERT INTO run_sources(run_id, source_id, status, posts_count, comments_count, links_count, reference_hints_count, error_type, started_at, finished_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("run-1", "reddit_alexithymia", "completed", 2, 2, 1, 0, None, "2026-05-19T12:00:00+00:00", "2026-05-19T12:10:00+00:00"),
            ("run-2", "reddit_cptsd", "completed", 1, 1, 0, 0, None, "2026-05-19T11:00:00+00:00", "2026-05-19T11:05:00+00:00"),
        ],
    )
    conn.executemany(
        "INSERT INTO extracted_links(run_id, source_id, subreddit, reddit_post_id, reddit_comment_id, source_type, url, domain, post_permalink, comment_permalink) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("run-1", "reddit_alexithymia", "alexithymia", "p-oldest", None, "post", "https://example.com/old", "example.com", "/r/alexithymia/comments/p-oldest", None),
        ],
    )
    conn.executemany(
        "INSERT INTO reference_hints(run_id, source_id, subreddit, reddit_post_id, reddit_comment_id, source_type, hint_kind, hint_value, evidence, post_permalink, comment_permalink) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("run-1", "reddit_alexithymia", "alexithymia", "p-oldest", None, "post", "doi", "10.1000/test", "doi:10.1000/test", "/r/alexithymia/comments/p-oldest", None),
        ],
    )
    conn.commit()
    conn.close()


class DashboardDbTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tempdir.name, "dashboard-test.sqlite")
        seed_db(self.db_path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_collection_summaries_return_independent_rows(self) -> None:
        from dashboard.db import connect_db, get_collection_summaries

        with connect_db(self.db_path) as conn:
            rows = get_collection_summaries(conn)

        self.assertEqual([row["source_id"] for row in rows], ["reddit_alexithymia", "reddit_cptsd"])
        self.assertEqual(rows[0]["post_count"], 2)
        self.assertEqual(rows[0]["comment_count"], 2)
        self.assertEqual(rows[1]["enabled"], 0)
        self.assertEqual(rows[1]["latest_status"], "completed")

    def test_feed_posts_filter_to_selected_sources_and_sort_newest_first(self) -> None:
        from dashboard.db import connect_db, get_feed_posts

        with connect_db(self.db_path) as conn:
            rows = get_feed_posts(conn, ["reddit_alexithymia", "reddit_cptsd"], limit=10, offset=0)

        self.assertEqual([row["reddit_post_id"] for row in rows], ["p-newest", "p-middle", "p-oldest"])

        with connect_db(self.db_path) as conn:
            alex_rows = get_feed_posts(conn, ["reddit_alexithymia"], limit=10, offset=0)

        self.assertEqual([row["reddit_post_id"] for row in alex_rows], ["p-newest", "p-oldest"])

    def test_feed_posts_reject_empty_source_selection(self) -> None:
        from dashboard.db import connect_db, get_feed_posts

        with connect_db(self.db_path) as conn:
            with self.assertRaises(ValueError):
                get_feed_posts(conn, [], limit=10, offset=0)

    def test_post_detail_includes_only_matching_post_comments_links_and_hints(self) -> None:
        from dashboard.db import connect_db, get_post_detail

        with connect_db(self.db_path) as conn:
            detail = get_post_detail(conn, "p-oldest")

        self.assertEqual(detail["post"]["reddit_post_id"], "p-oldest")
        self.assertEqual(detail["comments"], [])
        self.assertEqual(detail["links"][0]["domain"], "example.com")
        self.assertEqual(detail["reference_hints"][0]["hint_value"], "10.1000/test")

        with connect_db(self.db_path) as conn:
            newest_detail = get_post_detail(conn, "p-newest")

        self.assertEqual([row["reddit_comment_id"] for row in newest_detail["comments"]], ["c-1", "c-2"])


if __name__ == "__main__":
    unittest.main()
