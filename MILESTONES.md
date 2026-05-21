# AAN Milestones

Canonical repo-local stage definitions for the Alexithymia Awareness Network.

This file owns milestone/state boundaries.
- `GOALS.md` explains why the project exists.
- `TODO.md` tracks the active work items inside these stages.
- `WORK-PLAN.md` summarizes which milestones are currently being pushed.

Derivation rule for project-mgmt:
- use the milestone IDs, titles, statuses, and definitions here as the canonical milestone cache source
- treat `WORK-PLAN.md` as commentary/orchestration layered on top of these milestone definitions

Last updated: 2026-05-19

## M1 — Organizational presence baseline
Status: in_progress
Supports: Goal 1

Intent:
Establish AAN as a real public-facing organization, not just a useful content site.

Definition of done:
- Home/about/contact surfaces clearly explain the organization and who runs it.
- Founder visibility is handled cleanly and credibly.
- Mailing-list/contact flow is chosen and wired.
- News/contact/community pathways feel alive enough to support trust.

Primary work surface:
- `TODO.md` → Organization presence and trust signals

## M2 — Library depth and resource quality
Status: in_progress
Supports: Goal 2

Intent:
Strengthen the attached library so it becomes one of AAN's main public services.

Definition of done:
- Major topic gaps are filled or intentionally deferred with clear next pages.
- Important missing authors/frameworks/resources are added.
- External resources are curated into a vetted library with good framing.
- Link quality and source integrity are routinely checked.

Primary work surface:
- `TODO.md` → Library depth and resource curation
- `CONTENT_PLAN.md` for page-structure decisions

## M3 — Tooling boundary hardening
Status: completed
Supports: Goal 3

Intent:
Keep external research/editorial tooling productive without letting it dominate AAN's repo identity.

Definition of done:
- Reddit collection/review tooling has a separate canonical repo.
- Public-site planning artifacts no longer read as if the dashboard/collector is core AAN repo work.
- AAN stays focused on publishing, curation, and reviewed downstream use of collected findings.

Primary work surface:
- `README.md`
- `WORK-PLAN.md`
- `TODO.md`

## M4 — Theme/system maintainability
Status: in_progress
Supports: Goal 1, Goal 2

Intent:
Keep the public site maintainable and visually coherent while content and org surfaces expand.

Definition of done:
- Theme architecture is documented.
- Reusable partials/components are intentional rather than ad hoc.
- Local dev and deploy paths remain reliable.

Primary work surface:
- `TODO.md` → Theming and presentation system
- `aan/theme/README.md`
- `local_test.sh`

## Review rule

If the current center of gravity changes, update milestone status/order here before editing the cache in `project-mgmt`.
