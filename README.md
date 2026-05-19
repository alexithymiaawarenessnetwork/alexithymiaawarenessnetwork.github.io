# AAN: The Alexithymia Awareness Network

Public knowledgebase and organizational web presence for the Alexithymia Awareness Network — an MkDocs-built site deployed via GitHub Pages.

This repository contains the source code and content for the Alexithymia Awareness Network website, hosted at [alexithymiaawarenessnetwork.org](https://alexithymiaawarenessnetwork.org).

> **Status:** active · p0 · in content build-out. See [`CONTENT_PLAN.md`](CONTENT_PLAN.md) for the editorial roadmap and [`TODO.md`](TODO.md) for the working punch list.

## Site Structure

- **`/docs/`** - Generated site files served by GitHub Pages
- **`/aan/docs/`** - Source markdown content files
- **`/aan/mkdocs.yml`** - MkDocs configuration
- **`deploy.sh`** - Automated deployment script

## Making Content Updates

### 1. Edit Content
Edit the markdown files in `/aan/docs/`:
- `index.md` - Main landing page content
- `intro.md` - Introduction to Alexithymia
- `contact.md` - Contact information
- `mission.md` - Mission statement
- `advisors.md` - Advisory board
- `lexicon.md` - Words for feelings
- `network.md` - Network information
- `news.md` - News and updates
- `resources.md` - Articles, papers, books, and media

### 2. Deploy Changes
Use the automated deployment script:

```bash
# Deploy with default commit message
./deploy.sh

# Deploy with custom commit message
./deploy.sh "Updated contact information"
```

The script will:
1. Build the MkDocs site
2. Check for changes
3. Commit and push to GitHub
4. Trigger GitHub Pages deployment

### 3. Manual Deployment (Alternative)
If you prefer to deploy manually:

```bash
# Build the site
cd aan
mkdocs build
cd ..

# Commit and push
git add .
git commit -m "Your commit message"
git push origin main
```

## Development Setup

### Prerequisites
- Python 3.7+
- MkDocs with Material theme

### Installation
```bash
pip install mkdocs mkdocs-material
```

### Local Development
```bash
cd aan
mkdocs serve
```

This will start a local development server at `http://localhost:8000` with live reloading.

## Internal Research Tooling

This repo also contains internal-only collection utilities that support editorial and research work but are not part of the public site build.

### Reddit reference-data collector

Use `scripts/collect_reddit_reference.py` to collect reference-only snapshots from configured subreddits such as `r/alexithymia`. Subreddit datasets are kept independent by default unless explicitly grouped later.

- Config: `config/reddit_reference_sources.json`
- Governance + usage notes: `REDDIT_REFERENCE_DATA.md`
- Output directory: `data/reddit/`
- SQLite backend: `data/reddit/reddit_reference.sqlite`
- FTS search helper: `scripts/search_reddit_reference.py`
- Local dashboard launcher: `scripts/run_reddit_dashboard.py`

Example validation run:

```bash
python3 scripts/collect_reddit_reference.py --max-posts-override 5 --max-comments-override 5
```

Polite 2026 post backfill for the current `r/alexithymia` scope:

```bash
./scripts/backfill_reddit_2026.sh
```

Example search:

```bash
python3 scripts/search_reddit_reference.py 'recovery OR recovered'
```

Local dashboard:

```bash
.venv/bin/python scripts/run_reddit_dashboard.py
# open http://127.0.0.1:8010/dashboard/collections
```

Important: collected Reddit material is for internal review only. Nothing from that pipeline should be auto-published or treated as authoritative without independent review.

## Site Configuration

The site uses:
- **MkDocs** for static site generation
- **Material for MkDocs** theme for styling
- **GitHub Pages** for hosting
- Custom domain: `alexithymiaawarenessnetwork.org`

## Contributing

1. Make your changes to the markdown files in `/aan/docs/`
2. Test locally with `mkdocs serve`
3. Deploy using `./deploy.sh "Description of changes"`

The site will be automatically updated on GitHub Pages within a few minutes.

## Related Projects

Part of a larger AAN / Herrick-model body of work tracked in [`/Users/div/Repositories/project-mgmt/`](../project-mgmt/):

- **`voice-recording-analysis`** — pipeline turning interview recordings into transcripts → LSA → Neo4j graph
- **`a-good-life`** — interview source corpus (Bella, DR0000_xxxx series) likely fed into the pipeline above
- **`polarity-sim`** — the Herrick model expressed as a runnable simulation (TS + React + D3)
- **`emotion-graph`** — emotion-data visualizer
- **`herrick-coping-analysis-tool`** — Python CLI for coping analysis on emotional-content inputs
- **`metagamist`** — adjacent research/knowledge collection (AGL interviews, emotion/cognition guides)
