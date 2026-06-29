# Emotion theory paper cache

This directory caches the core emotion-theory sources used for the AAN emotion-theory page.

Cache policy:
- Always save structured metadata locally (`openalex.json` and `crossref.json` when available).
- Save landing-page HTML when a publisher page is fetchable.
- Save a PDF only when an open-access PDF is directly retrievable.
- For closed or blocked items, the cache still preserves citation metadata and any abstract available through metadata APIs.

Each paper directory contains a small local bundle, typically including:
- `README.txt` — quick status summary
- `abstract.txt` — normalized abstract/metadata text for offline reading
- `openalex.json` — OpenAlex metadata
- `crossref.json` — Crossref metadata
- `landing.html` / `landing_meta.json` — landing page cache when fetchable
- `paper.pdf` / `pdf_meta.json` — open-access PDF when fetchable

Summary status:

| Paper | DOI | Cached metadata | Landing page | PDF | Notes |
|---|---|---:|---:|---:|---|
| The theory of constructed emotion: an active inference account of interoception and categorization | 10.1093/scan/nsw154 | yes | no | no | OA status: bronze; landing/pdf requests blocked |
| The Theory of Constructed Emotion: More Than a Feeling | 10.1177/17456916251319045 | yes | no | no | OA status: green; landing request blocked/reset |
| An argument for basic emotions | 10.1080/02699939208411068 | yes | yes | no | closed access |
| Basic Emotions, Natural Kinds, Emotion Schemas, and a New Paradigm | 10.1111/j.1745-6916.2007.00044.x | yes | no | no | closed access; landing blocked |
| The brain basis of emotion: A meta-analytic review | 10.1017/S0140525X11000446 | yes | yes | yes | OA PDF cached |
| Core affect and the psychological construction of emotion | 10.1037/0033-295X.110.1.145 | yes | yes | no | closed access |
| Emotion, core affect, and psychological construction | 10.1080/02699930902809375 | yes | no | no | closed access; landing blocked |
| Appraisal Considered as a Process of Multilevel Sequential Checking | 10.1093/oso/9780195130072.003.0005 | yes | no | no | metadata cached; landing blocked |
| The Emotion Process: Event Appraisal and Component Differentiation | 10.1146/annurev-psych-122216-011854 | yes | yes | yes | OA PDF cached |
| Selected Principles of Pankseppian Affective Neuroscience | 10.3389/fnins.2018.01025 | yes | yes | yes | OA PDF cached |
| The Biology of Fear | 10.1016/j.cub.2012.11.055 | yes | yes | no | landing cached; OA PDF redirect loop from publisher |
