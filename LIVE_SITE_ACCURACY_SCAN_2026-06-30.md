# Live site accuracy scan — alexithymiaawarenessnetwork.org

Date: 2026-06-30

Scope: live public site at `https://alexithymiaawarenessnetwork.org/`, compared against the current local AAN source repo where useful.

Method:

- Fetched `https://alexithymiaawarenessnetwork.org/sitemap.xml` and crawled all 32 listed live URLs.
- Extracted visible main-page text into `/tmp/aan_live_scan/` for review.
- Checked internal live links discovered during the crawl: 32 internal URLs returned HTTP 200.
- Checked citation references of the form `citations.json#id`: 19 live citation references, 0 missing IDs against local `aan/docs/citations.json`.
- Spot-checked high-risk factual areas: diagnosis, treatment, comorbidities, assessment instruments, papers, apps/tools, labs/institutions, support/crisis pages.
- Used Crossref/OpenAlex/Semantic Scholar/PubMed metadata for selected bibliographic checks.

Important boundary: this is an accuracy/provenance scan, not a full rewrite. “Acquired” or “found in a source” still does not mean ready for public claims without a source-locking pass.

## Executive summary

The live site has several strong pages, especially the FAQ and crisis/support routing, but the current public site is not yet source-disciplined enough for confident public launch.

Highest-risk findings:

1. The live site appears stale relative to the current local generated output/source for at least the Treatment page.
2. The Comorbidities page contains many specific prevalence, causal, and treatment-implication claims with no citations.
3. The Apps page appears to contain placeholder/fabricated app listings, ratings, reviews, and broken store links.
4. The Papers page has bibliographic errors and placeholder `href="#"` links.
5. BVAQ citation metadata is wrong in the public tools/FAQ/citation layer.
6. Researcher/lab profile pages contain many biographical/institutional claims without visible provenance and should be treated as unverified.
7. Treatment and support pages include some clinical-effectiveness language that needs source-locking or softening.

## Findings

### Critical: live site is stale/out of sync with current local source for Treatment

Evidence:

- Live `https://alexithymiaawarenessnetwork.org/treatment/` begins with the older wording: “This page covers therapeutic modifications, medication considerations, family/relationship interventions, and emerging research.” Extracted at `/tmp/aan_live_scan/30-treatment.txt:1-7`.
- Current source `aan/docs/treatment.md:3-16` has newer, safer framing: “There is no single standard treatment for alexithymia itself…” and positions Treatment as an overview with `therapy-approaches.md` carrying modality detail.
- Local generated output `docs/treatment/index.html:1819-1822` also contains the newer wording.

Why it matters:

- The public site may not reflect recent safety/accuracy cleanup already present locally.
- Any public-site audit needs to distinguish “live problem” from “source already fixed but not deployed.”

Recommended action:

- Before content edits, decide whether to deploy/rebuild the current MkDocs output or keep live intentionally frozen.
- Add a deployment freshness check to future audits: compare live page hash/text against local `docs/` output for all sitemap routes.

### Critical: Apps page contains apparent placeholders/fabricated community ratings and broken app-store links

Evidence:

- `aan/docs/apps.md:7-26` lists “Emotion Tracker Pro,” community rating `4.2/5 based on 47 reviews`, named testimonial, and app-store links. Both app-store URLs returned 404 in the link check.
- `aan/docs/apps.md:28-47` lists “Feeling Wheel Interactive,” rating `4.7/5 based on 23 reviews`, named testimonial; iOS and Android store links returned 404.
- `aan/docs/apps.md:49-68` lists “Mindful Emotions,” rating `4.1/5 based on 31 reviews`, named testimonial; store links returned 404.
- Additional broken or dubious links included `emotionregulationtoolkit.org`, the Google Forms review link, and `forum.alexithymiaawarenessnetwork.org` certificate mismatch.

Why it matters:

- Public readers may treat ratings/testimonials as real community evidence.
- Fake or placeholder app claims are a trust issue, especially on a mental-health-adjacent site.

Recommended action:

- Quarantine or rewrite Apps before public promotion.
- Remove all ratings/testimonials unless backed by a real AAN review dataset.
- Only list apps with verified URLs, current availability, pricing/date checked, and a clear disclaimer: not endorsed, not diagnostic, not treatment.

### Critical: Comorbidities page is claim-dense and unsourced

Evidence:

- `aan/docs/comorbidities.md` has no `citations.json`, DOI, or URL references.
- It gives specific prevalence estimates without citations:
  - depression: `40-60%` at `aan/docs/comorbidities.md:11-16`
  - IBS: `40-50%` at `aan/docs/comorbidities.md:69-73`
  - eating disorders/anorexia: `60-80%` at `aan/docs/comorbidities.md:101-107`
  - autism: `40-65%` at `aan/docs/comorbidities.md:117-123`
  - alcohol use disorder: `45-67%` at `aan/docs/comorbidities.md:153-161`
- It also makes causal/clinical claims needing qualification, e.g. “Alexithymia may predispose to depression” at `aan/docs/comorbidities.md:13-16`, “Trauma impact: May cause or worsen alexithymic traits” at `aan/docs/comorbidities.md:183-191`, and multiple treatment implications.

Why it matters:

- These claims are plausible in broad direction but too specific and too clinical without exact sources, populations, instruments, and caveats.
- The page currently reads more definitive than the evidence trail supports.

Recommended action:

- Turn Comorbidities into a source-locked claim map before public launch.
- For now, either remove exact percentages or attach citations and qualifiers for population/instrument/cutoff.
- Split out autism first, because AAN already has Kinnaird et al. 2019 in citations/source-library and the FAQ handles it cautiously.

### Major: BVAQ citation metadata is wrong or at least misleading

Evidence:

- `aan/docs/tools.md:29-42` and `aan/docs/faq.md:23-25` cite “Bermond & Vorst (2013)” for the BVAQ.
- `aan/docs/citations.json:303-318` records `bermond_vorst_2013_bvaq` as 2013, *Personality and Individual Differences*, 54(1), 30–35, DOI `10.1016/j.paid.2012.08.011`.
- Crossref lookup for “Validity and reliability of the Bermond–Vorst Alexithymia Questionnaire” returned Vorst & Bermond, 2001, *Personality and Individual Differences*, 30(3), 413–434, DOI `10.1016/S0191-8869(00)00033-7`.

Why it matters:

- The site’s BVAQ source trail points to the wrong bibliographic record for the primary BVAQ validation paper.
- This affects FAQ, Assessment Instruments, Papers, and citation hover behavior.

Recommended action:

- Replace or split the BVAQ citation after inspecting the actual 2013 paper currently referenced.
- Add the 2001 Vorst & Bermond primary validation record.
- Audit all pages using `bermond_vorst_2013_bvaq` before strengthening BVAQ claims.

### Major: Papers page has multiple bibliographic errors and placeholder links

Evidence:

- `aan/docs/papers.md:163-170` lists Rieffe/Oosterveld/Terwogt as 2018, *Personality and Individual Differences*, 45(8), 788–792. OpenAlex resolved the named paper as 2005/2006 publication metadata: DOI `10.1016/j.paid.2005.05.013`, *Personality and Individual Differences*, 40(1), 123–133.
- `aan/docs/papers.md:195-203` lists Lumley/Neely/Burger as 2020. Crossref resolved it as 2007, *Journal of Personality Assessment*, 89(3), 230–246, DOI `10.1080/00223890701629698`.
- `aan/docs/papers.md:211-219` lists Gaggero et al. scientometric review as 2021, Frontiers in Psychiatry 12, 662866; Crossref resolved it as 2020, Frontiers in Psychiatry 11, DOI `10.3389/fpsyt.2020.611489`.
- Several rows use `href="#"` rather than source URLs, e.g. `aan/docs/papers.md:167`, `aan/docs/papers.md:183`, `aan/docs/papers.md:199`, `aan/docs/papers.md:215`.

Why it matters:

- The Papers page is meant to be a research gateway; bibliographic errors undermine the whole evidence posture.

Recommended action:

- Replace the hand-coded papers table with generated rows from `citations.json` and/or source-library metadata.
- Add a validator for title/year/journal/DOI rows and forbid `href="#"` for published papers.

### Major: Researcher and lab pages contain many unsupported biographical/institutional claims

Evidence:

- Bagby profile includes detailed claims about doctoral training, grants, CAMH affiliation, research leadership, workshop development, technology applications, etc. See examples at `aan/docs/bagby.md:9-17`, `aan/docs/bagby.md:96-138`, and the live page `/bagby/`.
- Bermond profile similarly includes detailed academic biography and leadership claims at `aan/docs/bermond.md:9-17`, plus many broad research contribution claims throughout the page.
- Labs page assigns principal investigators, focus areas, “notable research,” and project statuses across many institutions, e.g. `aan/docs/labs.md:9-37`, `aan/docs/labs.md:51-75`, `aan/docs/labs.md:171-184`.
- Several lab URLs failed or returned 404/name-resolution errors in the link check, including Berkeley SI, UvA Psychology path, Tilburg Psychology path, and others.

Why it matters:

- These pages look authoritative but are not visibly sourced. Some may be outdated or wrong, and some project names/statuses look like placeholders.

Recommended action:

- Quarantine researcher/lab pages behind “draft/unverified” language or reduce each to source-backed basics.
- For each profile, require a source register: official university profile, ORCID/Google Scholar, selected publications, and explicit “last checked” date.
- Remove project statuses unless verified from current project pages.

### Major: Treatment/Support clinical-effectiveness wording needs source-locking and softening

Evidence:

- Treatment page says antidepressants “may be less effective when emotional-processing difficulty remains untreated” and “medication plus psychotherapy or emotional-skills work is generally more useful than medication alone” at `aan/docs/treatment.md:24-42`, without citations.
- Support page says EFT is “specifically designed for emotional awareness” and “effective for alexithymia-related challenges” at `aan/docs/support.md:81-85`; somatic therapies are “particularly helpful for alexithymia” at `aan/docs/support.md:99-104`.

Why it matters:

- These are treatment-effectiveness claims. AAN’s safety posture should defer to clinicians and avoid implying a specific modality works for alexithymia unless review-backed.

Recommended action:

- Source-lock Treatment and Support against Pinna et al. 2020 and Tsubaki & Shimizu 2024 before public-strength wording.
- Until then, change “effective/particularly helpful” to “some clinicians use/adapt…” or “may be relevant for some people, depending on clinical context.”

### Moderate: FAQ is comparatively strong but inherits BVAQ citation issue

Evidence:

- FAQ has good boundaries: informational only, not a diagnosis, clinician interpretation required. See `aan/docs/faq.md:1-3`, `aan/docs/faq.md:15-29`, `aan/docs/faq.md:43-45`.
- Prevalence and autism wording are appropriately qualified at `aan/docs/faq.md:31-37`.
- The BVAQ line inherits the citation problem at `aan/docs/faq.md:23-25`.

Recommended action:

- Keep FAQ as the style model for public-facing answers.
- Fix BVAQ citation and consider adding one sentence that online self-screens are not equivalent to TAS-20/PAQ/TSIA/OAS clinical/research assessment.

### Moderate: emotion-framework pages need caveats around contested models

Evidence:

- Emotion Frameworks describes Ekman’s six universal emotions as “claimed to be biologically determined and recognized across cultures” at `aan/docs/emotion-frameworks.md:12-16`, which is a decent caveat.
- The “How these frameworks relate” section says “These models are not mutually exclusive” at `aan/docs/emotion-frameworks.md:101-115`.

Why it matters:

- Modern emotion science has active disagreement, especially basic emotion theory vs constructed emotion. Saying the models are “not mutually exclusive” may over-harmonize incompatible assumptions.

Recommended action:

- Add caveat language: these frameworks can be useful educational tools, but some make conflicting scientific claims.
- Link to Barrett/Lindquist/Russell/Scherer citation records already present in `citations.json`.

### Positive findings

- Sitemap is present and listed 32 URLs.
- All discovered internal links returned HTTP 200.
- Citation JSON is publicly available at `/citations.json`.
- 19 citation hash references resolved to existing local citation IDs.
- FAQ has clear non-diagnostic and clinician-deferring framing.
- Support/crisis page has appropriate urgent-resource hierarchy and live crisis links checked successfully.

## Recommended next task graph

1. Deployment freshness check
   - Compare all live pages to local generated `docs/` output.
   - Decide whether to deploy current local site before content cleanup.

2. Quarantine obvious placeholders
   - Apps page ratings/testimonials/app links.
   - Labs/project statuses.
   - Unsupported detailed researcher biographies.

3. Bibliography cleanup
   - Fix BVAQ citation.
   - Fix Papers table metadata and remove `href="#"` placeholders.
   - Generate Papers from structured citation/source-library metadata.

4. Comorbidities source-lock pass
   - Remove or cite all exact prevalence numbers.
   - Add population/instrument/cutoff caveats.
   - Split autism page first.

5. Treatment/support safety pass
   - Source against treatment systematic reviews.
   - Soften modality-effectiveness claims.
   - Keep clinician-deferring language prominent.

6. Researcher/lab provenance pass
   - Require source register per profile/lab entry.
   - Use official profiles and publication records only.

## Verification artifacts

- Live crawl text and JSON: `/tmp/aan_live_scan/`
- Live URLs crawled: 32
- Internal live links checked: 32, all HTTP 200
- Citation refs checked: 19, missing IDs: 0
