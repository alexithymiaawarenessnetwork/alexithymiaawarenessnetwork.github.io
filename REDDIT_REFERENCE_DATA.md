# Reddit reference-data collection for AAN

This is an internal working note for collecting Reddit content as reference data only.

## Purpose

Use Reddit as a source of:
- community-language examples
- recurring question themes
- candidate external links
- candidate citation leads
- rough signals about what people with alexithymia talk about, ask about, or link to

This data is not authoritative and is not auto-published.

## Governance posture

- Collection purpose: internal research support only
- Distribution default: `no_distribution`
- Publication rule: nothing from this pipeline is automatically promoted into the public site
- Review rule: any FAQ, resource entry, or citation that originates from Reddit must be independently reviewed before use
- Confidence rule: Reddit content is anecdotal/community speech, not clinical guidance

## Artifacts

Configuration lives in:
- `config/reddit_reference_sources.json`

Canonical SQLite backend:
- `data/reddit/reddit_reference.sqlite`

Collected outputs also land in versioned run artifacts for audit/debugging:
- `data/reddit/runs/<run_id>.json`
- `data/reddit/snapshots/<run_id>/posts.jsonl`
- `data/reddit/snapshots/<run_id>/comments.jsonl`
- `data/reddit/snapshots/<run_id>/links.jsonl`
- `data/reddit/snapshots/<run_id>/reference_hints.jsonl`
- `data/reddit/snapshots/<run_id>/summary.json`
- `data/reddit/snapshots/<run_id>/fetch_log.json`

The database stores both current searchable records and provenance/run metadata:
- source registry and listing modes
- collection runs
- per-source run status/counts
- fetch request logs
- canonical posts/comments
- per-run post/comment observations
- extracted links
- reference hints
- FTS5 indexes for posts and comments

## Collector usage

Basic run against all enabled sources:

```bash
python3 scripts/collect_reddit_reference.py
```

Dryer/smaller validation run:

```bash
python3 scripts/collect_reddit_reference.py --max-posts-override 5 --max-comments-override 5
```

Collect a single source ID from the config:

```bash
python3 scripts/collect_reddit_reference.py --source-id reddit_alexithymia
```

Write to a custom database path:

```bash
python3 scripts/collect_reddit_reference.py --db-path data/reddit/custom.sqlite
```

Full-text search the database:

```bash
python3 scripts/search_reddit_reference.py 'recovery OR recovered'
python3 scripts/search_reddit_reference.py 'autism' --kind comments
```

Local dashboard:

```bash
python3 scripts/run_reddit_dashboard.py
# then open http://127.0.0.1:8010/dashboard/collections
```

The dashboard is intentionally browse-first:
- it starts at the collections page, not a mixed global feed
- collections remain independent unless you explicitly select more than one
- the feed view shows a chronological union only for the currently selected collection set
- post detail pages keep the current collection context in navigation

Operational note:

```bash
# if Reddit starts returning 429s, retry one source at a time
python3 scripts/collect_reddit_reference.py --source-id reddit_alexithymia --max-posts-override 25
```

The collector now retries transient 429/5xx responses with backoff, but Reddit still behaves more reliably when adjacent subreddit pulls are staggered rather than burst together.

## Polite 2026 backfill process

Goal: ensure we have at least all 2026 posts for `r/alexithymia` without doing an aggressive full-history scrape.

Recommended sequence:

1. Validate connectivity with a tiny sample:

```bash
python3 scripts/collect_reddit_reference.py \
  --source-id reddit_alexithymia \
  --listing-sort new \
  --since-date 2026-01-01 \
  --max-posts-override 5 \
  --pause-seconds-override 4 \
  --no-comments
```

2. Run the full 2026 post backfill, still comments-off:

```bash
./scripts/backfill_reddit_2026.sh
```

Equivalent explicit command:

```bash
python3 scripts/collect_reddit_reference.py \
  --source-id reddit_alexithymia \
  --listing-sort new \
  --since-date 2026-01-01 \
  --max-posts-override 1000 \
  --pause-seconds-override 4 \
  --no-comments
```

3. Only after the post corpus is stable, do smaller comment-enrichment runs. Keep them targeted and slower, for example a small validation pass with comments enabled:

```bash
python3 scripts/collect_reddit_reference.py \
  --source-id reddit_alexithymia \
  --listing-sort new \
  --since-date 2026-01-01 \
  --max-posts-override 25 \
  --max-comments-override 10 \
  --pause-seconds-override 5
```

Why this is polite:
- uses a descriptive user-agent
- pages `new` chronologically and stops once posts fall before 2026
- respects `Retry-After` on 429s
- avoids the expensive per-post comment fan-out during the initial backfill
- keeps pulls single-source and staggered rather than bursty

## What the collector extracts

Per post:
- title, body text, author, score, timestamps, permalink
- outbound URL if present
- URLs extracted from post text
- simple citation hints such as DOI / PMID / arXiv references

Per comment:
- body, author, score, timestamps, permalink
- URLs extracted from comment text
- simple citation hints such as DOI / PMID / arXiv references

Derived outputs:
- flattened links table for downstream link review
- flattened reference-hints table for downstream citation triage

## Safe use guidance

Recommended downstream workflow:
1. use the snapshot to identify recurring questions
2. draft candidate FAQ answers independently
3. support claims with primary literature or high-quality sources, not Reddit alone
4. if a Reddit post links to a useful paper/site, verify the destination directly before citing it

## Notes on related subreddits

Current active collection scope:
- `r/alexithymia` only

Related subreddits may remain listed in config as disabled candidates, but the default rule is:
- keep each subreddit dataset independent unless we explicitly decide to group them later
- do not treat adjacent communities as part of the alexithymia corpus by default
- any future expansion still remains internal/reference-only and human-reviewed downstream
