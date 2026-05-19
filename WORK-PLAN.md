# AAN Work Plan

Internal working artifact. Not published to the public site.

Last updated: 2026-05-19

## Current focus

Priority active internal build:
- Reddit reference dashboard for the local research corpus

Why now:
- the Reddit reference corpus is large enough that command-line inspection is no longer the best primary interface
- collection boundaries now matter explicitly at the UI level
- editorial/research review will be easier with a local browse-first tool than with ad hoc SQL and CLI queries

## Project goal

Build a local-only dashboard for the Reddit reference corpus that:
- starts at a collections view
- lets us explicitly select which collections to view
- shows a Reddit-style chronological feed across the selected union
- opens individual posts with post body and comments
- preserves collection boundaries unless the viewer intentionally unions them

## Product rules

- internal-only; not part of the public AAN site
- no auto-publishing or promotion into public content
- explicit collection selection before any unioned feed
- current active corpus scope is `r/alexithymia`
- future related subreddits may exist in the DB but remain separate unless explicitly grouped in the UI

## v1 acceptance criteria

1. Landing page shows collections, not a global mixed feed.
2. User can select one or more collections and only then view a feed.
3. Feed is chronological and readable.
4. Clicking a post opens full post content and comments.
5. Current selected collections remain visible throughout navigation.
6. Dashboard reads from the SQLite corpus only; no write path.
7. Public MkDocs site build remains unaffected.

## Delivery shape

### Phase 1 — Collections home
Goal: make the data legible at the collection level.

Deliver:
- local dashboard app scaffold
- collections landing page
- per-collection summary cards/table
- explicit collection selection flow

Primary files likely involved:
- `dashboard/app.py`
- `dashboard/db.py`
- `dashboard/templates/base.html`
- `dashboard/templates/collections.html`
- `dashboard/static/dashboard.css`
- `scripts/run_reddit_dashboard.py`
- `tests/test_dashboard_routes.py`
- `tests/test_dashboard_db.py`

### Phase 2 — Chronological feed
Goal: support browsing selected collections like a Reddit feed.

Deliver:
- feed route with repeated `source_id` query params
- newest-first post query across selected collections
- pagination
- Reddit-style feed rows with metadata/snippets

Primary files likely involved:
- `dashboard/db.py`
- `dashboard/views.py`
- `dashboard/templates/feed.html`
- `tests/test_dashboard_db.py`
- `tests/test_dashboard_routes.py`

### Phase 3 — Post detail and comments
Goal: make a post reviewable without leaving the dashboard.

Deliver:
- post detail route
- full post body
- chronological comments with indentation by `depth`
- links/reference-hints sections
- safe back-navigation preserving collection selection

Primary files likely involved:
- `dashboard/db.py`
- `dashboard/app.py`
- `dashboard/templates/post_detail.html`
- `tests/test_dashboard_db.py`
- `tests/test_dashboard_routes.py`

### Phase 4 — Boundary safeguards and polish
Goal: make the UI honest about scope and safe against accidental cross-collection confusion.

Deliver:
- visible selected-collections banner
- detail-page guard against mismatched source selection
- empty states and disabled-collection labelling
- docs for local usage and governance

Primary files likely involved:
- `dashboard/app.py`
- `dashboard/templates/*.html`
- `README.md`
- `REDDIT_REFERENCE_DATA.md`

## Immediate next slice

Build through Phase 2 first:
1. app scaffold
2. collections home
3. explicit selection flow
4. chronological feed

Then review in browser before building post detail/comments.

## Validation

Minimum checks for v1 slices:
- route tests pass
- DB query tests pass
- local app launches on `127.0.0.1:8010`
- feed only shows explicitly selected collections
- public MkDocs build still works unchanged

Expected commands:
- `python3 -m unittest tests/test_dashboard_db.py -v`
- `python3 -m unittest tests/test_dashboard_routes.py -v`
- `python3 scripts/run_reddit_dashboard.py`

## Risks / cautions

- keep this separate from the public site architecture; do not entangle with MkDocs templates unless there is a later clear reason
- do not blur collection boundaries in the name of convenience
- do not overbuild the UI before the core browse flow is proven useful
- the current corpus is still partial/backfilled, so the feed is chronological over what we have, not a complete archival mirror
