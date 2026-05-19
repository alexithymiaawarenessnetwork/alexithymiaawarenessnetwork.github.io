from __future__ import annotations

import os
from contextlib import closing

from flask import Flask, abort, redirect, render_template, request, url_for

from .db import DEFAULT_DB_PATH, connect_db, get_collection_summaries, get_feed_posts, get_post_detail, normalize_selected_sources
from .views import format_timestamp, selection_query, summarize_text


BASE_DIR = os.path.dirname(__file__)


def create_app(*, db_path: str | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )
    app.config["DASHBOARD_DB_PATH"] = db_path or DEFAULT_DB_PATH

    @app.context_processor
    def inject_helpers() -> dict[str, object]:
        return {
            "format_timestamp": format_timestamp,
            "summarize_text": summarize_text,
            "selection_query": selection_query,
        }

    @app.get("/dashboard")
    def dashboard_root():
        return redirect(url_for("collections"))

    @app.get("/dashboard/collections")
    def collections():
        message = request.args.get("message")
        with closing(connect_db(app.config["DASHBOARD_DB_PATH"])) as conn:
            summaries = get_collection_summaries(conn)
        return render_template("collections.html", summaries=summaries, selected_source_ids=[], message=message)

    @app.get("/dashboard/feed")
    def feed():
        requested_source_ids = normalize_selected_sources(request.args.getlist("source_id"))
        if not requested_source_ids:
            return redirect(url_for("collections", message="Select at least one collection to view a feed."))

        page = max(request.args.get("page", default=1, type=int), 1)
        per_page = 25
        offset = (page - 1) * per_page

        with closing(connect_db(app.config["DASHBOARD_DB_PATH"])) as conn:
            summaries = get_collection_summaries(conn)
            enabled_source_ids = {row["source_id"] for row in summaries if row["enabled"]}
            source_ids = [source_id for source_id in requested_source_ids if source_id in enabled_source_ids]
            if not source_ids:
                return redirect(url_for("collections", message="Select at least one enabled collection to view a feed."))
            posts = get_feed_posts(conn, source_ids, limit=per_page, offset=offset)

        return render_template(
            "feed.html",
            summaries=summaries,
            posts=posts,
            selected_source_ids=source_ids,
            page=page,
            has_next=len(posts) == per_page,
            message=request.args.get("message"),
        )

    @app.get("/dashboard/posts/<reddit_post_id>")
    def post_detail(reddit_post_id: str):
        requested_source_ids = normalize_selected_sources(request.args.getlist("source_id"))
        if not requested_source_ids:
            return redirect(url_for("collections", message="Select a collection before opening a post."))

        with closing(connect_db(app.config["DASHBOARD_DB_PATH"])) as conn:
            summaries = get_collection_summaries(conn)
            enabled_source_ids = {row["source_id"] for row in summaries if row["enabled"]}
            source_ids = [source_id for source_id in requested_source_ids if source_id in enabled_source_ids]
            if not source_ids:
                return redirect(url_for("collections", message="Select an enabled collection before opening a post."))
            detail = get_post_detail(conn, reddit_post_id)

        if detail is None:
            abort(404)

        post = detail["post"]
        if post["source_id"] not in source_ids:
            query = selection_query(source_ids, message="That post is outside the current collection selection.")
            return redirect(url_for("feed") + f"?{query}")

        return render_template(
            "post_detail.html",
            detail=detail,
            post=post,
            selected_source_ids=source_ids,
            page=request.args.get("page", default=1, type=int),
        )

    return app
