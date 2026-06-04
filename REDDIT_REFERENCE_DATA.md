# Reddit reference-data note for AAN

The canonical home for Reddit collection, enrichment, dashboard review, and governance is now:
- `/Users/div/Repositories/reddit-scraper`

AAN is no longer the source-of-truth repo for that tooling.

Use the separate repo for:
- subreddit source configuration
- collection and enrichment runs
- search and dashboard review
- Reddit corpus governance and provenance
- preparation of reviewed findings for downstream use

AAN should only consume reviewed outputs from that project.

Rules that still apply on the AAN side:
- do not auto-publish Reddit content
- do not treat Reddit content as authoritative on its own
- independently review any FAQ/resource/citation candidate before using it in site content
