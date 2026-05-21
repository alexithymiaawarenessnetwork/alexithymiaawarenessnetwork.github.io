# AAN Goals

Canonical repo-local goals for the Alexithymia Awareness Network.

This file owns the project's durable goals.
- `MILESTONES.md` owns stage boundaries.
- `TODO.md` owns active tasks and punch-list work.
- `CONTENT_PLAN.md` owns site information architecture and per-page editorial structure.
- `WORK-PLAN.md` orchestrates current focus across those artifacts.

Derivation rule for project-mgmt:
- treat the goal sections in this file as the canonical source for AAN goal summaries
- treat any commentary elsewhere as secondary unless it contradicts this file and is newer by explicit date

Last updated: 2026-05-19

## Goal 1 — Public organizational home

Make AAN a credible, public-facing organizational home with clear mission, visible stewardship, trustworthy contact paths, and a coherent public identity.

Success criteria:
- Visitors can quickly understand what AAN is, why it exists, and who it serves.
- The site shows real human stewardship, including founder visibility and any genuine team/advisor signals.
- Contact and mailing-list pathways are clear, working, and appropriate to the organization's current stage.
- Core public-facing pages feel intentional rather than like a loose content dump.

Primary artifacts:
- `aan/docs/index.md`
- `aan/docs/mission.md`
- `aan/docs/network.md`
- `aan/docs/contact.md`
- `aan/docs/news.md`
- future org-facing surfaces such as team/advisors when real

## Goal 2 — Strong attached library

Build a strong public alexithymia library as one of AAN's core services: lay-accessible, source-backed, clinician-respectful, and clear about the limits of the site's authority.

Success criteria:
- Core topic coverage exists and is navigable: definition, diagnosis, treatment, comorbidities, coping, support, research, resources.
- Important pages are source-backed and avoid overstating certainty or clinical authority.
- External resources are curated, vetted, and clearly framed for informational use.
- The library is useful both to newly curious readers and to practitioners/researchers looking for orientation.

Primary artifacts:
- `aan/docs/*.md`
- `CONTENT_PLAN.md`
- `aan/docs/citations.json`
- `TODO.md` library tasks

## Goal 3 — External supporting tooling boundary

Keep research/editorial tooling useful while clearly separating it from AAN's public organizational identity and website surface.

Success criteria:
- AAN planning artifacts treat Reddit/corpus tooling as external support infrastructure rather than repo-central work.
- The public MkDocs site can evolve independently of dashboard/corpus tooling.
- Scope boundaries for imported reference-data findings remain explicit.
- AAN consumes reviewed outputs from the separate tooling repo without inheriting its collection workflow as part of the site identity.

Primary artifacts:
- `README.md`
- `WORK-PLAN.md`
- `MILESTONES.md`
- `TODO.md`

## Operating rule

When strategy changes, update this file first, then reconcile `MILESTONES.md`, `WORK-PLAN.md`, and `TODO.md`.
