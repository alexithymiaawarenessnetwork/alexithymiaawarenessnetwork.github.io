# AAN Audit Log

Internal audit coordination artifact. Not published to the public site.

## Active audit request

### 2026-06-23 11:30 EDT — Astro prototype implementation plan audit

- Primary worker/model family: OpenAI / Codex-family Hermes session
- Requested auditor/model family: Claude Code
- Scope: read-only audit of the Astro prototype implementation plan before starting the sibling Astro project
- Files to inspect:
  - `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md`
  - `THEME_MIGRATION_PLAN.md`
  - `WORK-PLAN.md`
- Questions / risks to probe:
  - Is the six-page Astro spike plan complete enough for autonomous implementation?
  - Are sequencing, verification gates, and stop conditions strong enough?
  - Are route/content/citation/search/deployment parity risks under-specified?
  - Does the plan preserve AAN’s constraints: informational-only, clinician-deferring, support findable but not primary, no fake claims/assets?
  - Does the plan avoid over-componentizing Markdown authoring?
  - What should be tightened before implementation begins?
- Constraints:
  - Read-only audit of planning artifacts; do not modify implementation files.
  - Return severity-ranked findings with exact file/line references where possible.
- Status: completed via independent Hermes subagent fallback; Claude Code read-only audit attempted but failed with `401 Invalid authentication credentials` despite `claude auth status` reporting an active first-party login.

## Findings

### 2026-06-23 11:30 EDT — Astro prototype plan audit findings

Auditor path:

- Preferred cross-model auditor: Claude Code.
- Attempted command: `HOME=$HOME claude -p ... --allowedTools Read --max-turns 8`.
- Result: failed with `API Error: 401 Invalid authentication credentials`.
- Fallback auditor: independent Hermes subagent, read-only, file/terminal tools.

Rob's disposition / plan-update notes:

1. Citations: Rob wants to manage the source for citations and ensure no citation source, ID, or link behavior is lost during the Astro transition.
2. Routes/sitemap: Track the full site map and route inventory. Breaking changes are less concerning because the site is not meaningfully publicly launched yet, but the migration should still know what exists and what changes.
3. Papers: Normalize `papers.md`; move existing search/sort/table behavior out of raw Markdown and into the research-library template/component system.
4. Testing: Yes, automate testing rather than relying on manual checks.
5. Material/provenance cleanup: Yes, but handle content/material cleanup separately, not as part of the Astro production transition. The transition should avoid introducing new unsourced claims/assets and should preserve source/provenance context for the separate cleanup lane.
6. Search: Treat search as a separately developed feature. The initial Astro spike may support generated static search; heavier search UX can come later.
7. Support hierarchy: Proceed with the recommended measurable hierarchy checks so Support remains findable without becoming the site's primary identity.

#### Major: Citation parity is a high-risk blocker and is sequenced too late

Evidence:

- Plan preserves citation links during migration: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:172-179`.
- Proposed Astro structure stores `citations.json` under `src/content/data/`: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:89-90`.
- Citation rebuild is deferred to Task 11: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:542-565`.
- Current FAQ links directly to `citations.json#...`: `aan/docs/faq.md:9`, `aan/docs/faq.md:13`, `aan/docs/faq.md:23-27`.
- Current theme behavior depends on custom includes and JS: `aan/theme/main.html:6-18`, `aan/theme/assets/js/citations.js:24-31`, `aan/theme/assets/js/citations.js:45-52`.

Why it matters:

- Putting citation data in Astro source does not automatically make `/citations.json` publicly fetchable.
- Preserved Markdown citation links could become broken links or lose the current citation affordance.
- This threatens the plan's `Content integrity = 5` gate.

Suggested fix:

- Move citation behavior before or alongside Task 5/6.
- Define a canonical public citation contract: publish `/citations.json`, generate citation pages, or rewrite Markdown links at build time.
- Add a build-time validator for every `citations.json#id` reference.
- Include no-JS fallback and keyboard-accessible preview behavior.

#### Major: Route/search/deployment parity is acknowledged but not gated early enough

Evidence:

- Spike scope is six pages: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:34-45`.
- Search and deployment cutover are out of scope for the spike: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:56-63`.
- Route/search/sitemap/redirect behavior is deferred to full migration: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:710-719`.
- Current MkDocs config has production URL/output boundary, search, hidden pages, and broader nav: `aan/mkdocs.yml:2-8`, `aan/mkdocs.yml:15-16`, `aan/mkdocs.yml:24-38`, `aan/mkdocs.yml:40-79`.

Why it matters:

- A visually successful six-page spike could still miss legacy URLs, hidden routes, search, sitemap, or custom-domain behavior.
- This could create false migration confidence.

Suggested fix:

- Add a preflight baseline inventory task before project creation.
- Inventory all source Markdown pages, generated routes, hidden built routes, redirects/stubs, `CNAME`, sitemap, and search index behavior.
- Require a route/search/deployment parity report template during the spike even if only six pages are implemented.

#### Major: Markdown authoring portability is under-specified, especially for `papers.md`

Evidence:

- Plan says ordinary pages stay Markdown and authors should not hand-code wrappers: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:143-170`.
- Markdown/MkDocs-specific syntax search happens only after copying: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:278-284`.
- `papers.md` embeds page-local CSS, raw HTML controls/table, inline `onclick`, and page-local JS: `aan/docs/papers.md:5-98`, `aan/docs/papers.md:100-112`, `aan/docs/papers.md:108-111`, `aan/docs/papers.md:295-363`.

Why it matters:

- One of the proof pages is not ordinary Markdown.
- The prototype may fail Astro Markdown constraints, preserve fragile/inaccessible behavior, or force authors into component markup.

Suggested fix:

- Move Markdown/HTML inventory before content copy.
- Create a conversion matrix for raw HTML, inline styles, inline scripts, admonitions, relative `.md` links, tables, and external links.
- Treat `papers.md` as a structured-data/component exception or define an explicit authoring contract for research-library pages.

#### Major: Accessibility verification is too manual and misses known risks

Evidence:

- Base shell verification only checks visible focus: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:318-323`.
- Homepage checks are visual/responsive, not accessibility-testable: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:348-362`.
- Accessibility scorecard is subjective: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:691-706`.
- Theme plan lists accessibility expectations without executable checks: `THEME_MIGRATION_PLAN.md:517-525`.
- Current `papers.md` search input lacks a programmatic label, sortable headers are clickable `<th onclick=...>` rather than keyboard-operable buttons with `aria-sort`, and current citation JS is click-first: `aan/docs/papers.md:100-112`, `aan/theme/assets/js/citations.js:45-68`.

Why it matters:

- AAN's support and research content must remain usable by keyboard and assistive tech.
- Accessibility regressions would affect citation access, table sorting/search, nav, and urgent-help content.

Suggested fix:

- Add Playwright + axe checks, HTML validation, keyboard smoke tests, mobile overflow checks, reduced-motion checks, and contrast checks.
- Require input labels, real buttons for sortable headers, `aria-sort`, focusable citation previews, Escape/blur behavior, and no keyboard traps.

#### Major: Asset and claim provenance is not an explicit gate

Evidence:

- Theme plan forbids fake stats/testimonials/logos/inflated claims: `THEME_MIGRATION_PLAN.md:57-65`.
- Homepage port task preserves approved copy and imagery: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:340-345`.
- Mockup says “1 in 10 people are affected by Alexithymia” without adjacent citation: `mockups/aan-homepage-open-door-v24-beta.html:1855-1857`.
- Mockup uses remote Wikimedia/Unsplash imagery: `mockups/aan-homepage-open-door-v24-beta.html:41-52`, `mockups/aan-homepage-open-door-v24-beta.html:684-744`, `mockups/aan-homepage-open-door-v24-beta.html:1870-1876`, `mockups/aan-homepage-open-door-v24-beta.html:1969-1976`.

Why it matters:

- The prototype could normalize hotlinked or insufficiently licensed imagery, imply real community/institutional presence through stock portraits, or publish uncited prevalence claims.

Suggested fix:

- Add asset/claim provenance gate before homepage acceptance.
- Verify license/source/attribution for every image.
- Decide whether to localize assets.
- Document alt-text intent.
- Avoid testimonial-like implications.
- Source, soften, or remove the “1 in 10” claim until cited.

#### Major: Search parity is an open question even though current search is a production feature

Evidence:

- Current MkDocs site enables search: `aan/mkdocs.yml:15-16`.
- Plan excludes heavy interactive search from spike scope: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:56-63`.
- Search/sitemap/redirect behavior is deferred: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:714-719`.
- Theme plan leaves search unresolved: `THEME_MIGRATION_PLAN.md:543-548`.
- Comparison acceptance criteria omit search: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:608-615`.

Why it matters:

- For a resource/library site, search is content findability, not decoration.

Suggested fix:

- Decide spike-level search explicitly: not present, static generated index, or lightweight client search.
- Add a parity note comparing MkDocs search to the Astro choice.
- Make unresolved search strategy a blocker before production cutover.

#### Major: Support hierarchy needs measurable checks

Evidence:

- Theme plan says Support must be findable but not primary: `THEME_MIGRATION_PLAN.md:34-48`.
- Plan repeats this at `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:222-228` and `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:340-345`.
- Mockup includes Support as a primary nav item and a full Support homepage band with urgent support cards: `mockups/aan-homepage-open-door-v24-beta.html:1827-1831`, `mockups/aan-homepage-open-door-v24-beta.html:2005-2049`.

Why it matters:

- Visual hierarchy can drift even when the written constraint is correct.
- The homepage could accidentally feel crisis/support-first rather than informational/library-first.

Suggested fix:

- Add a homepage hierarchy review: count/order primary CTAs, compare visual weight of Support vs understanding/research/resources/organization, and require reviewer signoff that Support is accessible but not dominant.

#### Minor: Mockup links use generated MkDocs paths that conflict with planned Astro routes

Evidence:

- Plan wants clean slugs: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:376-399`.
- Mockup links point to generated `../docs/.../index.html`: `mockups/aan-homepage-open-door-v24-beta.html:1927`, `mockups/aan-homepage-open-door-v24-beta.html:1933`, `mockups/aan-homepage-open-door-v24-beta.html:1939`, `mockups/aan-homepage-open-door-v24-beta.html:1945`, `mockups/aan-homepage-open-door-v24-beta.html:1964-1965`, `mockups/aan-homepage-open-door-v24-beta.html:2016-2034`.

Why it matters:

- Literal homepage extraction can preserve broken/environment-specific links.

Suggested fix:

- Add a homepage link-rewrite step and run a link checker against built Astro output.

#### Minor: Baseline repo hygiene checks should be Task 0, not late verification notes

Evidence:

- Task 1 immediately creates the sibling project: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:231-260`.
- Current repo git/build checks appear late under exact verification: `.hermes/plans/2026-06-22_223425-astro-prototype-plan.md:726-741`.
- Work plan says canonical task/state changes live in other planning artifacts and must stay aligned: `WORK-PLAN.md:7-15`, `WORK-PLAN.md:53-60`.

Why it matters:

- The new sibling project setup should not begin before confirming baseline repo state, MkDocs strict build, route inventory, and planning artifact alignment.

Suggested fix:

- Add Task 0: `git status`, current MkDocs strict build, baseline route inventory, and confirmation that TODO/CONTENT_PLAN/THEME_MIGRATION_PLAN remain aligned.

## History

- 2026-06-23 11:30 EDT — Created audit request for the Astro prototype implementation plan.
- 2026-06-23 11:30 EDT — Claude Code read-only audit attempted and failed with 401 authentication error.
- 2026-06-23 11:30 EDT — Independent Hermes subagent completed read-only audit; findings recorded above.
