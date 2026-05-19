# Reddit reference data

This directory stores internal-only Reddit collection artifacts for AAN research support.

Contents are reference material for tasks like:
- FAQ drafting support
- candidate link/citation discovery
- language-pattern review
- community-topic reconnaissance

Rules:
- Do not auto-publish or auto-quote collected Reddit content into the site.
- Treat all outputs as source material requiring human review.
- Respect the source governance posture documented in `REDDIT_REFERENCE_DATA.md`.

Expected contents:
- `reddit_reference.sqlite` — canonical SQLite backend with FTS5 search indexes and run provenance
- `runs/` — per-run metadata and counts
- `snapshots/<run_id>/` — posts/comments/links/reference hints collected in a run
