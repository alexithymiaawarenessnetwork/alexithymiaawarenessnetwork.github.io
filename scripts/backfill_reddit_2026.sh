#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/collect_reddit_reference.py \
  --source-id reddit_alexithymia \
  --listing-sort new \
  --since-date 2026-01-01 \
  --max-posts-override 1000 \
  --pause-seconds-override 4 \
  --no-comments

cat <<'EOF'

Backfill complete.

Recommended next steps:
1. Inspect the latest run summary in data/reddit/runs/
2. Query the corpus with scripts/search_reddit_reference.py
3. If you want comment enrichment, run a smaller follow-up pass against targeted posts/authors with a slower pause.
EOF
