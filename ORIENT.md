# ORIENT

Last updated: 2026-06-29

## What this repo is now

This repo is the current canonical source of truth for the Alexithymia Awareness Network knowledge base and the legacy MkDocs website source.

The long-term direction is to deprecate the website shell here and move public-site rendering to the sibling Astro project, while keeping AAN's knowledge-base grounding, editorial plans, citations, and source discipline anchored here unless a future migration explicitly moves them.

## Start here

1. `README.md` — current repo identity, source/generated-site boundary, deploy notes.
2. `GOALS.md` — durable project goals.
3. `MILESTONES.md` — active stage boundaries.
4. `WORK-PLAN.md` — current orchestration layer and canonical planning artifact list.
5. `TODO.md` — active task surface.
6. `CONTENT_PLAN.md` — page-level editorial schema and coverage audit.
7. `THEME_MIGRATION_PLAN.md` — Astro migration direction, template taxonomy, and site-design constraints.
8. `AUDIT.md` — migration/audit findings and risks already accepted by Rob.
9. `ALEXITHYMIA_EXPERTISE_MAP.md` — working domain map for AAN content stewardship.
10. `SOURCE_LIBRARY_POINTER.yaml` — project pointer into Rob's local source-library collection for alexithymia.

## Source vs generated boundary

- Edit public content in `aan/docs/*.md`.
- Edit MkDocs configuration in `aan/mkdocs.yml` while MkDocs remains live.
- Treat root `docs/` as generated GitHub Pages output from MkDocs; do not hand-edit it except for emergency publishing fixes.
- `aan/docs/citations.json` is the current citation data source for the MkDocs site and must stay source-preserved during Astro migration.

## Sibling Astro project

Sibling repo: `/Users/div/Repositories/a-a-n-astro`

Current inspected state:

- It is an Astro 7 static-site prototype, not yet the full production migration.
- It renders six prototype routes: `/`, `/faq/`, `/resources/`, `/papers/`, `/plutchik/`, `/support/`.
- It has a route ledger at `src/content/data/route-ledger.json` and currently tracks the full MkDocs route count as 35 for later parity work.
- It keeps citation data in `src/content/data/citations.json` and publishes `public/citations.json` / `dist/citations.json`.
- It has validators: `npm run validate:citations`, `npm run validate:spike`, and `npm test`.

Migration posture:

- Use this repo as the content/citation baseline.
- Use the Astro sibling as the future rendering/template layer.
- Domain/reference layer: `/Users/div/Repositories/alexithymia-kb`. Its `AAN_CONTENT_POLICY.md` encodes Rob's standard that AAN publish only factual, citable, verified accurate information in kind, respectful, sensitive, clear, direct, non-alarmist, non-clinical language.
- Maintain broad alexithymia knowledge outside the website page structure in `alexithymia-kb`, with source assets in `source-library`; compose Astro HTML as the curated public sharing layer.
- Do not let the Astro project become a second unsynchronized knowledge base. Content movement needs either a sync process or an explicit cutover decision.
- Preserve routes where practical, but the site is still early enough that correctness and source discipline matter more than freezing every URL prematurely.

## Local source library

Central library repo: `/Users/div/Repositories/source-library`

Current alexithymia collection:

- `data/collections/alexithymia-research.yaml`
- Current registered works: eight support sources across neuroanatomy, foundational book excerpt, treatment response, clinical applications, autism, interoception, and TAS-20 psychometrics.
- Acquisition status artifact: `/Users/div/Repositories/source-library/docs/ALEXITHYMIA_ACQUISITION_STATUS.md`
- Acquisition want-list: `/Users/div/Repositories/source-library/docs/ALEXITHYMIA_TO_BE_ACQUIRED.md`
- Article-reading derivative rule: when reading an article, source-library now preserves extracted text, relevant/extracted images, and a derivative manifest beside the PDF where possible; HTML reader output is skipped by default when the PDF is captured.
- All registered works remain `notes_status: unreviewed`; collection membership means “available for review,” not public AAN canon.

Usage rule:

- Use the source-library collection to find local materials.
- Do not treat local possession of a PDF as permission to reproduce it.
- Use metadata, brief quotations, and line/page references; confirm publication quotes against the PDF before publishing.
- Promote source-library works into AAN citations or public prose only after an explicit review pass.

## Dedicated alexithymia knowledgebase

Domain/reference repo: `/Users/div/Repositories/alexithymia-kb`

Use it for source-locked claim maps, papers, assessment instruments, researchers/labs/resources, evidence grades, publication-candidate records, and future Astro exports. This repo should replace ad hoc website-page prose as the place where AAN domain knowledge is curated and audited.

## AAN public-answer boundary

AAN is informational and community-oriented, not a clinician, therapist, diagnostic service, or crisis service.

For public-facing answers:

- Explain concepts plainly.
- Distinguish established evidence from plausible interpretation and lived-experience framing.
- Do not diagnose a reader or imply a score/questionnaire settles their mental health.
- Defer diagnosis, treatment planning, medication, severe symptoms, and safety issues to qualified professionals or local emergency/crisis resources.
- For self-harm, abuse, medical emergency, or imminent danger signals, route to immediate human/crisis support rather than ordinary educational answering.

## Current high-risk knowledge-base areas

1. `aan/docs/comorbidities.md` contains many prevalence and mechanism statements that need stronger citation-locking before being treated as polished public authority.
2. `aan/docs/diagnosis.md` is useful but contains some unsourced assessment and clinical-protocol claims that should be tied to primary scale papers or clinician/review sources.
3. `aan/docs/treatment.md` and `aan/docs/therapy-approaches.md` need modality-by-modality evidence grading and clinician-deferring language.
4. `aan/docs/papers.md` in MkDocs still contains raw HTML/CSS/JS and placeholder `href="#"` items; the Astro prototype has already started normalizing this into data/component form.
5. `aan/docs/citations.json` is useful but incomplete relative to the page claims and the paper/library ambitions.
6. The autism/alexithymia page is still missing even though it is repeatedly identified as a high-value split-out page.

## Practical next moves

1. Keep building the local source-library collection: ingest available alexithymia PDFs/books metadata, especially reviews/meta-analyses and foundational assessment papers.
2. Create source-locked claim maps for: definition/factors, assessment instruments, prevalence, autism overlap, treatment evidence, comorbidities, interoception/neurobiology.
3. Convert the highest-risk public pages from broad prose claims into citation-backed explainers with explicit uncertainty.
4. Continue Astro migration from six-page prototype toward full route/content parity, while keeping citations and content provenance anchored here until cutover.
