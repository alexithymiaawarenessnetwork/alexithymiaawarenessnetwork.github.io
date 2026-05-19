import os
import tempfile
import unittest

from tests.test_dashboard_db import seed_db


class DashboardRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tempdir.name, "dashboard-routes.sqlite")
        seed_db(self.db_path)

        from dashboard.app import create_app

        app = create_app(db_path=self.db_path)
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_collections_page_returns_200_and_shows_sources(self) -> None:
        response = self.client.get("/dashboard/collections")

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("reddit_alexithymia", page)
        self.assertIn("reddit_cptsd", page)

    def test_feed_requires_explicit_selection(self) -> None:
        response = self.client.get("/dashboard/feed")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/collections", response.headers["Location"])

    def test_feed_shows_only_selected_collection_posts(self) -> None:
        response = self.client.get("/dashboard/feed?source_id=reddit_alexithymia")

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Newest alexithymia post", page)
        self.assertIn("Oldest alexithymia post", page)
        self.assertNotIn("Middle CPTSD post", page)

    def test_feed_rejects_disabled_only_selection(self) -> None:
        response = self.client.get("/dashboard/feed?source_id=reddit_cptsd")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/collections", response.headers["Location"])

    def test_post_detail_returns_matching_source_selection(self) -> None:
        response = self.client.get("/dashboard/posts/p-newest?source_id=reddit_alexithymia")

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Newest alexithymia post", page)
        self.assertIn("first comment", page)
        self.assertIn("nested comment", page)

    def test_post_detail_rejects_mismatched_selection(self) -> None:
        response = self.client.get("/dashboard/posts/p-newest?source_id=reddit_cptsd")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/collections", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
