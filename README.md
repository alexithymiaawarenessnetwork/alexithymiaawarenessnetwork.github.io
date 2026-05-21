# AAN: The Alexithymia Awareness Network

Public-facing organizational site for the Alexithymia Awareness Network, with a strong attached library of alexithymia resources — an MkDocs-built site deployed via GitHub Pages.

This repository contains the source code and content for the Alexithymia Awareness Network website, hosted at [alexithymiaawarenessnetwork.org](https://alexithymiaawarenessnetwork.org).

> **Status:** active · p0 · org/site bootstrap plus library build-out. Canonical planning artifacts: [`GOALS.md`](GOALS.md), [`MILESTONES.md`](MILESTONES.md), [`WORK-PLAN.md`](WORK-PLAN.md), [`CONTENT_PLAN.md`](CONTENT_PLAN.md), and [`TODO.md`](TODO.md).

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

## Internal Research Tooling Boundary

Reddit collection and review tooling now lives in the separate repo:
- `/Users/div/Repositories/reddit-scraper`

Use that repo for:
- subreddit source configuration
- collection/enrichment runs
- local dashboard/search review
- Reddit reference-data governance and downstream review prep

AAN is now a consumer of reviewed outputs from that tooling, not the canonical home of the collector itself.

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
