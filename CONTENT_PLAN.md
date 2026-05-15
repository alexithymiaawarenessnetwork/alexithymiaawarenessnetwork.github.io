# AAN Content Plan

Internal-only document. Not published to the site. Versioned with the source.

**Last reconciled:** 2026-05-14 — §5 audit, §6 findings, and §7 action plan refreshed against current source state. §1–§4 (framework) and §8 (process) unchanged.

The headline rule for the AAN site:

> **Each page covers a single topic.** Lists and assorted content are split into
> their own pages, not crammed together. If a page tries to be the home for two
> different things, it stops being the canonical home for either.

This file defines the framework for what a page is, applies it to every
existing page, and lays out the move/remove/improve/add plan to align the
site with that rule.

---

## 1. The per-page schema

Every page in `aan/docs/` should be able to fill in the following fields. They
live here in `CONTENT_PLAN.md` rather than in front-matter, so the public
markdown stays clean.

| Field | Meaning |
|---|---|
| **Single topic** | One sentence: the one thing this page is. If you can't say it in one sentence, the page is doing too much. |
| **Goal** | What the reader should take away or be able to do after reading. |
| **Audience tier** | Primary: who is the writing voice aimed at. Secondary tiers can read the page but the prose is tuned for the primary. |
| **Content shape** | The structural pattern the page follows (see catalog below). |
| **Approach** | How the content is presented — narrative prose, profile, alphabetical glossary, structured table, etc. |
| **Maintenance** | How / when this page gets updated (see catalog below). |
| **Boundaries** | What does *not* belong on this page. Each boundary points at where that content lives instead. |
| **Related** | Sibling pages a reader might want next. |

When a new page is proposed, fill in the schema *before* writing prose. If two
draft pages end up with the same single-topic sentence, merge them. If one
page's schema lists a half-dozen boundaries pointing at "should be on its own
page," split it.

## 2. Audience tiers

Each page picks one **primary** tier — the voice the writing serves. Secondary
tiers can still read it; they just aren't the design target.

- **Lay** — curious general public, including people newly discovering they
  may have alexithymia. Plain language, define-as-you-go, avoid jargon.
- **Practitioner** — clinicians, therapists, counselors. Comfortable with
  diagnostic language, looking for clinical relevance and references.
- **Researcher** — academics, students, fellow scientists. Expects citations,
  methodology, scale details, theoretical grounding.
- **Mixed (navigational)** — the page is a hub or list; tier-tuning happens
  on the linked-to pages.

Pages flag their tier in their schema entry below. When a topic genuinely
needs all three tiers (e.g., what is alexithymia), prefer a tier-stratified
page (lay first, then practitioner deep-dive, then researcher references) over
a single uniform voice.

## 3. Content shape catalog

Each page picks one shape:

- **Hub** — short page that orients and links to deeper pages. Few words, lots
  of routes. Example today: `resources.md`.
- **Explainer** — a focused narrative that teaches one concept end-to-end.
  Example: a tight `faq.md` answer expanded into its own page.
- **Profile** — bio + contributions + impact, one subject per page. Example:
  `plutchik.md`.
- **Glossary** — alphabetized definitions with citations. Should not contain
  framework explanations (those go on their own explainer pages).
- **Catalog / List** — curated entries of a single thing (books, podcasts,
  apps, conferences, papers, labs). Each entry is short and uniform.
- **Reference** — long, structured, lookup-oriented (e.g., diagnostic
  criteria). Heavy use of headings + tables. Reads like documentation.
- **Form / Action** — exists for the reader to *do* something (contact,
  newsletter signup). Minimal prose; the form is the page.
- **News / Log** — chronological entries. Append-mostly.

Shapes can be subdivided into sections, but a page should not switch shapes.
A glossary page should not contain a profile; a profile should not contain a
glossary.

## 4. Maintenance strategy catalog

- **Evergreen** — content does not drift. Touch only when something is wrong.
  Example: `mission.md`.
- **Periodic review (cadence)** — schedule a review (quarterly, yearly).
  Example: `labs.md` — labs come and go; review yearly.
- **Event-driven** — updates when an external event happens (new paper, new
  conference, new release). Example: `conferences.md`, `papers.md`,
  `news.md`.
- **Community-driven** — readers contribute via a documented submission path.
  Example: `apps.md`, `podcasts.md`, `books.md`.
- **AI-assisted** — refreshable via a structured prompt that reads canonical
  sources (e.g., update a researcher's recent publications by reading their
  Google Scholar). Should be paired with one of the above; AI fills, human
  curates.

Every page entry below names its maintenance strategy. Pages that don't have
one are pages that quietly rot.

## 5. Page audit

Pages are grouped by the current `mkdocs.yml` nav structure. Each entry
follows the schema. The **Verdict** field is one of: `keep`, `improve`,
`split`, `merge`, `move`, `remove`, `draft`, `defer` (intentionally
shelved — gated on a condition like "more than one person to list"),
or `done` (action shipped; entry retained for one quarterly review pass
so we can see what changed).

### Home

#### `index.md` — Welcome / landing

- **Single topic**: Welcome and orient first-time visitors; route them.
- **Goal**: Reader knows in 30 seconds what AAN is, what alexithymia is at a
  one-paragraph level, and which section to enter next.
- **Audience tier**: Mixed (navigational), with a lay-friendly opener.
- **Content shape**: Hub.
- **Approach**: One-line tagline → 2-paragraph "what is alexithymia" → 4-tile
  section grid → mission link → tiny featured-event slot (optional).
- **Maintenance**: Evergreen for the orientation copy; event-driven for any
  future featured-event slot.
- **Boundaries**: No deep content; that lives in linked pages. Any featured
  event should not dominate the page.
- **Current state** (2.8K, 62 lines): Restructured. Opens with tagline +
  one-paragraph "what is alexithymia" → four themed entry tiles
  (Understanding / Resources / Research / Community) → prominent crisis
  link → mission summary → about/contact links. The CERE 2025 block is
  gone. There is currently no featured-event slot, which is fine.
- **Verdict**: `keep` — re-evaluate if and when AAN runs or co-hosts an
  event worth featuring; until then the slot stays absent rather than
  empty.

### About Us

#### `mission.md` — Mission

- **Single topic**: AAN's mission statement.
- **Goal**: Reader understands the network's purpose in two sentences.
- **Audience tier**: Mixed.
- **Content shape**: Explainer (very short).
- **Approach**: One paragraph. Quotable. Stable.
- **Maintenance**: Evergreen.
- **Boundaries**: No history, no values list, no team — those go elsewhere.
- **Current state** (217 bytes, 4 lines): Unchanged. Single-sentence mission
  statement. Well-scoped.
- **Verdict**: `keep` — optional light expansion to a short paragraph framing
  *why* the mission, but only if the addition stays quotable.

#### `network.md` — Who AAN is for

- **Single topic**: The composition and purpose of the AAN community.
- **Goal**: Reader sees themselves (or doesn't) as the audience and
  understands what kind of network this is.
- **Audience tier**: Mixed.
- **Content shape**: Explainer.
- **Approach**: Short list of audience types + a sentence about the directory.
- **Maintenance**: Evergreen.
- **Boundaries**: Does not list specific advisors (that's `advisors.md`); does
  not list specific organizations (that's `labs.md`).
- **Current state** (754 bytes, 13 lines): Cleanly scoped. "Policy makers"
  typo fixed. Closes with "If you'd like to be part of the network,
  contact us" → contact.md, which serves as the join path.
- **Verdict**: `keep`.

#### `advisors.md` — Advisory board

- **Single topic**: Who is on the AAN advisory board, and how to apply.
- **Goal**: Reader can see current advisors and / or volunteer to be one.
- **Audience tier**: Mixed.
- **Content shape**: Profile-list.
- **Approach**: When advisors exist, short profile blocks (name, affiliation,
  one-line bio, link). Until then, a recruiting note.
- **Maintenance**: Event-driven — update when advisors join.
- **Boundaries**: Not the place for the broader network description (that's
  `network.md`).
- **Current state** (153 bytes, 3 lines): Placeholder — "we are building
  an advisory board" + a contact link. As of 2026-05-05 the page has
  been **removed from nav and from the index.md About section** because
  no advisors exist yet; the file remains in the repo as an orphan to
  preserve the URL and to make re-enabling cheap when there is an actual
  advisor to list.
- **Verdict**: `defer` (shelved) — restore to nav and populate when at
  least one advisor signs on. Until then the page is intentionally not
  surfaced; pretending an advisory board exists would be worse than
  saying nothing.

#### `contact.md` — Contact

- **Single topic**: How to reach AAN.
- **Goal**: Reader can email the team and knows what to expect.
- **Audience tier**: Mixed.
- **Content shape**: Form / Action (with no live form yet — just an email).
- **Approach**: Email + 2-3 sentence framing per audience type.
- **Maintenance**: Evergreen.
- **Boundaries**: Doesn't replicate FAQ; doesn't list resources.
- **Current state** (891 bytes, 20 lines): Recently trimmed — "Ways to
  Connect" and "Contributing" sections dropped. Now: email + audience-list
  framing (newly diagnosed / researcher / clinician / experiencer /
  contributor) + a closing community statement.
- **Verdict**: `keep` — replace the email-only path with a real form when
  a mailing-list service is picked (TODO item).

#### `team.md` — *(missing)*

- **Single topic**: People who run AAN day-to-day.
- **Goal**: Reader sees the humans behind the project.
- **Audience tier**: Mixed.
- **Content shape**: Profile-list.
- **Approach**: Robert Herrick + future team members; one short bio each.
- **Maintenance**: Event-driven.
- **Boundaries**: Distinct from `advisors.md` (advisors are external; team
  runs the project).
- **Current state**: Does not exist.
- **Verdict**: `defer` (shelved) — explicitly parked until there is more
  than one person to list. A team page with one entry would feel
  half-built; better to surface humans on existing pages (founder
  attribution in mission.md or contact.md if desired) than to ship an
  empty roster. Revisit when AAN brings on additional staff or
  long-term volunteers.

### Emotion Researchers

These nine profiles are the strongest single-topic examples on the site —
each page is about one researcher. They share structural problems though.

**Cross-cutting issues** (status as of 2026-05-14):
1. ~~Each has a "## Contents" table at the top that duplicates the H2 outline.~~
   **Resolved** — manual TOC tables removed from all 9 profiles.
2. ~~Each has the literal duplicate H2 `## Biography and Career` repeated on
   consecutive lines.~~ **Resolved.** The later consecutive-duplicate-H2
   bugs on `plutchik.md` (`## The Eight Primary Emotions` × 2) and
   `ekman.md` (`## The Six Basic Emotions` × 2) are also resolved.
3. "## Related Resources" sections at the bottom — now present on all 9
   profiles. Content varies but the section itself is consistent.

**Common schema** (overrides per page only when noted):

- **Single topic**: Life and contributions of one named researcher.
- **Goal**: Reader can place this researcher in the field, identify their
  signature contribution, and find further reading.
- **Audience tier**: Practitioner (primary), Researcher (secondary). Bios
  are accessible to a curious lay reader but the contribution sections
  assume some clinical/research vocabulary.
- **Content shape**: Profile.
- **Approach**: Header card (institution, links) → bio → signature
  contribution → applications → publications → related.
- **Maintenance**: AI-assisted + event-driven (new paper / Wikipedia
  update). Quarterly review for living researchers; evergreen for deceased.
- **Boundaries**: Does not include vocabulary/glossary entries (those are in
  `lexicon.md`); does not catalog every paper (that's `papers.md`); does
  not summarize the broader field (that's `diagnosis.md` / `faq.md`).

Per-page notes:

- **`plutchik.md`** (1927–2006). 18.0K, 390 lines. `keep`. Duplicate-H2
  cleanup is complete. Wheel detail is now home here; `lexicon.md` links
  over rather than restating. ✓
- **`ekman.md`** (1934). 11.8K, 330 lines. `keep`. Duplicate-H2 cleanup is
  complete. Basic-emotions detail is now home here; `lexicon.md` links over
  rather than restating. ✓
- **`sifneos.md`** (1920–2008). 11.3K, 222 lines. `keep`. Manual TOC + bio-H2
  duplicate fixed. Etymology of "alexithymia" lives here; `lexicon.md`
  links over. ✓
- **`taylor.md`**. 9.1K, 172 lines. `keep`. TAS-20 development still told
  here; see RESEARCHERS-1 below.
- **`bagby.md`**. 12.5K, 266 lines. `keep`. Same TAS-20 overlap with
  Taylor / Parker.
- **`parker.md`**. 8.6K, 178 lines. `keep`. Same TAS-20 overlap.
- **`wilcox.md`**. 14.0K, 308 lines. `keep`. Feeling Wheel detail is now
  home here; `lexicon.md` links over. ✓
- **`bermond.md`**. 10.0K, 203 lines. `keep`. Same BVAQ-development overlap
  with `vorst.md`.
- **`vorst.md`**. 11.0K, 242 lines. `keep`. BVAQ overlap.

> **Cross-page issue (RESEARCHERS-1) — still open**: TAS-20 development
> story is still told across `taylor.md` / `bagby.md` / `parker.md`. BVAQ
> development across `bermond.md` / `vorst.md`. `tools.md` already lists
> the TAS-20 and BVAQ as instruments and links to the developers, but it
> does *not* yet own the development narrative. The proposed factoring
> (a `tas-20.md` and a `bvaq.md`, each owning the development story; each
> researcher page describing only their specific role) is still
> recommended and would unblock the duplication. Lower priority than the
> remaining `add` items but worth scheduling.

### Understanding Alexithymia

#### `faq.md` — Frequently asked questions

- **Single topic**: Common questions about alexithymia, answered.
- **Goal**: Reader gets a concise answer to a specific question and a link
  to the deeper page.
- **Audience tier**: Lay.
- **Content shape**: Catalog (Q&A pairs) — accept this as a hybrid; FAQ is a
  recognizable format and one-question-per-page would be silly.
- **Approach**: Question → 1-3 paragraph answer → "see also" link.
- **Maintenance**: Community-driven; review whenever a question recurs in
  contact email.
- **Boundaries**: Each answer is short. Long explanations live on dedicated
  pages and are *linked to* from the FAQ.
- **Current state** (9.9K, 226 lines): Unchanged. 8 sections — Understanding
  / Common Experiences / Assessment / Treatment / Relationships / Daily
  Life / Resources / Research. Several answers still run long enough to
  deserve dedicated pages.
- **Verdict**: `improve` (still open) — split the long answers into
  dedicated explainer pages, leave one-paragraph summaries with "read
  more →" links. Top candidates: "How does alexithymia affect
  decision-making?", "Can alexithymia affect physical health?", "How do I
  handle overwhelming emotions?" Some questions ("Is alexithymia the same
  as autism?") will be served once `alexithymia-and-autism.md` exists.

#### `diagnosis.md` — Diagnosis & assessment

- **Single topic**: How alexithymia is assessed and diagnosed.
- **Goal**: Practitioner reader can understand the assessment landscape
  (instruments, criteria, differential diagnosis) and refer further.
- **Audience tier**: Practitioner (primary), Researcher (secondary).
- **Content shape**: Reference.
- **Approach**: Assessment instruments overview → core characteristics →
  clinical evaluation → differential diagnosis. *That's it.*
- **Maintenance**: Periodic review (yearly).
- **Boundaries**: Does not catalog every comorbidity (those go on dedicated
  pages); does not catalog every instrument's psychometrics (those go on
  per-instrument pages); does not give treatment advice (that's a
  treatment page).
- **Current state** (7.0K, 199 lines): Split landed. Page now covers only
  assessment instruments (TAS-20, BVAQ, OAS, LEAS, EI tools), core
  characteristics (DIF/DDF/EOT and secondaries), differential diagnosis,
  and assessment-in-clinical-practice. Forward-links explicitly defer
  comorbidities to `comorbidities.md` and treatment to `treatment.md`.
- **Verdict**: `keep`. The split that was the headline action item from
  the previous audit shipped cleanly.

#### `comorbidities.md` — Conditions co-occurring with alexithymia

- **Single topic**: The conditions alexithymia commonly co-occurs with,
  and what each association implies clinically.
- **Goal**: Practitioner / informed lay reader can see the comorbidity
  landscape (psychiatric / medical / neurodevelopmental / substance /
  trauma) at a glance, with prevalence figures and treatment hints.
- **Audience tier**: Practitioner (primary), Researcher (secondary), Lay
  (tertiary — readable but the language gets clinical).
- **Content shape**: Hub-with-content. Categories with brief blocks per
  condition; deeper writeups link out to dedicated pages where they
  exist.
- **Approach**: Five top-level categories (Psychiatric / Medical /
  Neurodevelopmental / Substance Use / Trauma & Stress) → conditions →
  short 3–4-bullet block per condition (prevalence, mechanism, treatment
  implication).
- **Maintenance**: Periodic review (yearly) — comorbidity prevalence
  figures drift; AI-assisted refresh against current literature is fine
  if a human curates citations.
- **Boundaries**: Does not cover *how* alexithymia is identified (that's
  `diagnosis.md`); does not give treatment-modality detail beyond
  one-liners (that's `treatment.md`); does not subsume autism-specific
  depth (that should be its own `alexithymia-and-autism.md`).
- **Current state** (8.2K, 218 lines): Hub-with-content, freshly added.
  Reasonable depth across all five categories. Already flags a future
  `alexithymia-and-autism.md` page in an inline note.
- **Verdict**: `keep`. Next iteration: split out
  `alexithymia-and-autism.md` (the Autism block is the best candidate
  for own-page treatment given the literature volume). Replace prevalence
  ranges with citations to the underlying meta-analyses where possible.

#### `treatment.md` — Therapeutic approaches

- **Single topic**: How alexithymia affects therapeutic approaches and
  what kinds of intervention have evidence behind them.
- **Goal**: Practitioner reader understands modifications to standard
  protocols; informed-lay reader sees the modality landscape and can
  ask the right questions of a therapist.
- **Audience tier**: Practitioner (primary), Lay (secondary).
- **Content shape**: Reference-with-narrative. Short paragraphs, then
  modality blocks.
- **Approach**: Therapeutic modifications (CBT / Psychodynamic /
  Mindfulness / EFT / Somatic / DBT) → Medication considerations →
  Family/relationship interventions → Research and future directions.
- **Maintenance**: Periodic review (yearly) — modality evidence shifts
  as new RCTs publish; AI-assisted refresh against the
  research literature is fine if a human curates.
- **Boundaries**: Does not duplicate `tools.md`'s instrument detail; does
  not catalog every comorbidity treatment (links to `comorbidities.md`);
  does not give crisis intervention guidance (that's `crisis-help.md`).
- **Current state** (5.0K, 108 lines): Freshly added. Covers all the
  major modalities and a brief medication section, links forward to
  comorbidities, tools, support, and FAQ.
- **Verdict**: `keep`. Next iteration: thicken the evidence base for each
  modality with named studies; add a "what to ask a prospective
  therapist" practical block aimed at lay readers; consider linking each
  modality to the relevant FAQ entry once those split-out pages exist.

#### `lexicon.md` — Glossary of feeling words

- **Single topic**: A glossary of emotional and feeling-related terms.
- **Goal**: Lay reader can look up a feeling word and find a precise
  definition with citation.
- **Audience tier**: Lay (primary), Practitioner (secondary).
- **Content shape**: Glossary.
- **Approach**: Alphabetized entries. Each entry: term, definition,
  etymology if useful, citation, optional notable quote.
- **Maintenance**: Community-driven for new term suggestions; AI-assisted
  for citations.
- **Boundaries**: Does **not** explain frameworks (Plutchik's Wheel, Ekman's
  basic emotions, the Feeling Wheel) — those are explainers and live on
  their own pages or on the relevant researcher's profile.
- **Current state** (16.1K, 423 lines): Split landed. Page now contains an
  alphabetical index, core psychological concepts (alexithymia, affect,
  empathy, interoception, etc.), basic-emotion entries, cultural /
  untranslatable terms (hygge, saudade, nostalgia), and a vocabulary
  reference (intensity / valence descriptors). Framework explainers are
  gone — there's a one-line forward to `emotion-frameworks.md` near the
  top. Internal cross-references to `emotion-frameworks.md` and
  researcher pages where needed.
- **Verdict**: `keep`. Next iteration: continue accepting community-
  suggested terms (per the page's footer); periodic AI-assisted refresh
  for citations.

#### `emotion-frameworks.md` — Hub for emotion frameworks

- **Single topic**: A brief framing of each major emotion framework, with
  pointers to where the work is described in full.
- **Goal**: Reader can scan the landscape of emotion theories, place each
  in its lineage (classical / historical / contemporary), and find the
  deeper page for the one they want to read.
- **Audience tier**: Mixed — lay-friendly summaries that practitioners
  and researchers can also use as a navigational map.
- **Content shape**: Hub-with-content. Each framework gets a
  one-paragraph framing; if a deeper page exists (Plutchik, Ekman,
  Wilcox researcher profiles), link to it; if not, the entry on this
  page is the canonical home (Spinoza, Darwin, Brown, Damasio).
- **Approach**: Three groupings — Classical (Plutchik, Ekman) /
  Historical (Spinoza, Darwin) / Contemporary (Wilcox, Brown, Damasio).
  Closes with a "How these frameworks relate" paragraph that orients
  alexithymia readers to the practical entry points.
- **Maintenance**: Evergreen; AI-assisted top-up if a major contemporary
  framework gains traction.
- **Boundaries**: Not a glossary (`lexicon.md`); not a researcher
  profile (link out for those); not a clinical handbook.
- **Current state** (6.1K, 110 lines): Freshly added. Covers Plutchik
  (link), Ekman (link), Spinoza, Darwin, Wilcox (link), Brown, Damasio.
  "How these frameworks relate" closer is a particularly strong
  navigational paragraph for alexithymia readers.
- **Verdict**: `keep`. Optional improvements: add Lisa Feldman Barrett's
  theory of constructed emotion (referenced in lexicon); add Panksepp's
  affective neuroscience (TODO calls for this); add Plutchik's
  psychosocial developmental model (also TODO).

### Resources

#### `resources.md` — Resources hub

- **Single topic**: Navigational entry to all the resource pages.
- **Goal**: Reader picks the right sub-resource (apps, tools, books, papers,
  podcasts, support).
- **Audience tier**: Mixed.
- **Content shape**: Hub.
- **Approach**: Short blurb per sub-resource + link.
- **Maintenance**: Evergreen — only changes when a new sub-resource page is
  added or removed.
- **Boundaries**: Doesn't itself catalog any resources.
- **Current state** (2.9K, 61 lines): Trimmed. Six themed category cards
  (Books / Apps / Assessment Instruments / Podcasts / Papers / Support)
  → Getting Started paths (new to alexithymia / looking for professional
  help / in crisis / interested in research) → Contributing → footer.
  Quick-access duplication is gone.
- **Verdict**: `keep`.

#### `apps.md` — Mobile apps

- **Single topic**: Mobile and digital apps relevant to emotional awareness.
- **Goal**: Reader finds an app worth trying.
- **Audience tier**: Lay.
- **Content shape**: Catalog.
- **Approach**: One block per app: name, platform, price, focus, features,
  pros/cons.
- **Maintenance**: Community-driven (review submissions); periodic check
  for app discontinuations.
- **Boundaries**: Does not include academic assessment instruments (those
  belong on per-instrument pages or `tools.md` if narrowly scoped).
- **Current state** (6.8K, 199 lines): Unchanged. Same Featured /
  General / Specialized / Web-Based structure plus a "Community Reviews
  & Ratings" section.
- **Verdict**: `improve` (still open) — clarify what counts as "Featured
  Alexithymia App" vs. "General Emotional Wellness." Decide whether to
  keep the community reviews section here or move it into `support.md`.
  Lower priority.

#### `tools.md` — Assessment tools

- **Single topic**: Academic assessment instruments for alexithymia.
- **Goal**: Practitioner / researcher reader finds the right scale and how
  to use it.
- **Audience tier**: Practitioner (primary), Researcher (secondary).
- **Content shape**: Catalog.
- **Approach**: One block per instrument: name, authors, what it measures,
  format, scoring, validation, where to obtain.
- **Maintenance**: Periodic (yearly) — update validation citations.
- **Boundaries**: Does **not** include emotion-tracking apps (those are
  `apps.md`); does **not** include the historical development story of
  each scale (that lives on the related researcher page or a dedicated
  scale page).
- **Current state** (7.8K, 178 lines): Split landed. Page is now
  instrument-only — TAS-20, BVAQ, OAS, LEAS, the community Online
  Alexithymia Questionnaire, EI assessments. Mobile/meditation apps
  removed; explicit forward-link to `apps.md` for those. Includes
  practical "using online assessments" and "professional assessment"
  sections plus interpretation guidance.
- **Verdict**: `keep`. Optional: rename file to `assessments.md` to match
  its content (the nav already shows "Assessment Instruments"); requires
  redirect handling for the existing `/tools/` URL.

> **Cross-page issue (RESOURCES-1) — resolved**: The `apps.md` /
> `tools.md` overlap is gone. `tools.md` is instrument-only with an
> explicit forward-link to `apps.md`. Note retained for one more
> review pass so we can see the resolution, then drop.

#### `books.md` — Books

- **Single topic**: Recommended books on alexithymia and emotion theory.
- **Goal**: Reader picks a book to read next.
- **Audience tier**: Mixed.
- **Content shape**: Catalog.
- **Approach**: Bibliographic block + one-line description + buy link.
- **Maintenance**: Community-driven; periodic review for affiliate-link
  validity (already has automation).
- **Boundaries**: Does not summarize the books' arguments (that's a review,
  not a catalog).
- **Current state** (7.3K, 84 lines): Unchanged. Clean catalog.
- **Verdict**: `keep`. Optional next iteration: add reading-path
  "tracks" (e.g., "for the newly diagnosed", "for clinicians starting
  out") so readers can pick a starting point.

#### `papers.md` — Research papers

- **Single topic**: Academic papers on alexithymia.
- **Goal**: Researcher / practitioner finds the paper they want.
- **Audience tier**: Researcher (primary), Practitioner (secondary).
- **Content shape**: Catalog (sortable table).
- **Approach**: Table with year / authors / title / journal / DOI / link.
- **Maintenance**: Event-driven (new publications); AI-assisted to keep
  current.
- **Boundaries**: Does not duplicate `studies.md`. There should be one
  papers page, not two.
- **Current state** (11.8K, 366 lines): Unchanged. Custom-styled sortable
  table.
- **Verdict**: `keep`. The `studies.md` absorption shipped — `studies.md`
  is now a redirect stub. Optional next iteration: add the missing
  papers TODO calls out; AI-assisted refresh against PubMed for new
  alexithymia papers each quarter, human-curated.

#### `studies.md` — Studies (now a redirect stub)

- **Current state** (196 bytes, 5 lines): Reduced to a redirect stub
  pointing at `papers.md`. Removed from nav (per `mkdocs.yml`,
  `studies.md` is excluded from nav and the file kept in the build only
  so the existing `/studies/` URL keeps working).
- **Verdict**: `done` — the merge shipped. Leave the redirect stub in
  place indefinitely to preserve any external links.

#### `podcasts.md` — Podcasts

- **Single topic**: Podcasts and podcast episodes relevant to alexithymia.
- **Goal**: Reader finds something to listen to.
- **Audience tier**: Lay.
- **Content shape**: Catalog.
- **Approach**: Episode block: host, episode title, brief, link.
- **Maintenance**: Community-driven.
- **Boundaries**: Doesn't catalog general mental-health podcasts unless they
  have specific alexithymia content.
- **Current state** (5.6K, 124 lines): Unchanged. Well-scoped catalog.
- **Verdict**: `keep`.

### Research

#### `labs.md` — Research labs

- **Single topic**: Research labs and institutions doing alexithymia work.
- **Goal**: Researcher / practitioner finds where active work happens.
- **Audience tier**: Researcher (primary), Practitioner (secondary).
- **Content shape**: Catalog (geographic).
- **Approach**: Region → institution → PIs, focus, notable research.
- **Maintenance**: Periodic review (yearly).
- **Boundaries**: Doesn't list every researcher (those have profile pages);
  doesn't list every paper (those are on `papers.md`).
- **Current state** (9.9K, 212 lines): Unchanged. Geographic
  organization (North America / Europe / Asia-Pacific / Emerging
  Research Centers) plus Research Networks (ISRE, CERE, EERN),
  Collaborative Projects, and Funding Bodies sections.
- **Verdict**: `keep`. Optional next iteration: add a "last verified"
  date per entry to make the yearly review cadence trackable; verify
  every lab still has a working URL.

### Community & Events

#### `conferences.md` — Conferences

- **Single topic**: Upcoming and notable conferences relevant to alexithymia.
- **Goal**: Reader finds an event to attend or submit to.
- **Audience tier**: Researcher (primary), Practitioner (secondary).
- **Content shape**: Catalog.
- **Approach**: Upcoming list (chronological) + reference info on
  conference types and how to find them.
- **Maintenance**: Event-driven.
- **Boundaries**: Doesn't host the featured conference of the index page
  (link to it); doesn't list every general psychology conference.
- **Current state** (1.3K, 26 lines): The CERE 2025 feature was removed,
  but the page was over-pruned in the process — it now contains only a
  "Conference Types Relevant to Alexithymia Research" reference list
  (CERE / ISRE / Affective Science / APA / APS / SfN / INSAR / etc.).
  No upcoming events, no past-events archive, no past-event policy
  written down.
- **Verdict**: `improve` (still open) — restore an "Upcoming" section
  even if it starts empty (so readers see the page is event-driven, and
  the empty state itself is informative). Add a written past-event
  policy (e.g., "we keep past conferences listed for 6 months with a
  'past' header, then remove"). Acceptable to leave the conference-types
  reference list at the bottom as orientation.

#### `crisis-help.md` — Crisis & urgent support

- **Single topic**: Where to go *right now* if you or someone you know is
  in acute crisis or immediate danger.
- **Goal**: Reader in distress finds the right hotline / chat in under
  10 seconds. Concerned-other reader knows what to do for someone else.
- **Audience tier**: Lay (primary), with content that's also useful to
  practitioners orienting patients.
- **Content shape**: Reference (lookup-oriented). Numbers, links, very
  short prose; the fewest possible words between landing on the page
  and finding the right resource.
- **Approach**: Headline emergency callout (911) → "Right now" hotlines
  organized by region (US / International / LGBTQ+ / Veterans) →
  "When to reach out" (de-stigmatizes calling) → "Why crisis support
  can be especially relevant for alexithymia" (one paragraph specific
  to the audience) → "Building a safety plan" (practical) → "If you're
  worried about someone else."
- **Maintenance**: Periodic review (semi-annual) — numbers and URLs
  drift; safety messaging guidelines evolve.
- **Boundaries**: This is a safety page, not an everyday-support page.
  Routine therapist directories, support groups, and family resources
  belong on `support.md`. Crisis content does not duplicate elsewhere.
- **Current state** (4.9K, 103 lines): Freshly added with strong
  safe-messaging conventions. Linked prominently from `support.md`
  (admonition callout at top), `index.md` (dedicated tile), and
  `resources.md` (Getting Started block).
- **Verdict**: `keep`. Highest-stakes page on the site; revisit every 6
  months minimum. Worth a manual link-rot check on the linked services
  whenever this is reviewed.

#### `support.md` — Support & community

- **Single topic**: Support resources and community connections for people
  with alexithymia.
- **Goal**: Reader finds support that fits their situation.
- **Audience tier**: Lay.
- **Content shape**: Catalog.
- **Approach**: Online communities → professional support → family →
  workplace → peer support.
- **Maintenance**: Periodic review (yearly).
- **Boundaries**: **Crisis content does not belong here.** Crisis hotlines
  and emergency resources need their own page with safe-messaging
  conventions and high prominence.
- **Current state** (7.0K, 228 lines): Split landed. Page is everyday-
  support only. Crisis content extracted to `crisis-help.md`; a
  prominent admonition callout at the top of `support.md` redirects
  anyone in crisis to the right page. Sections: online communities /
  professional support / family & relationships / workplace &
  educational / self-help & peer / specialized populations / resource
  directories.
- **Verdict**: `keep`. Optional next iteration: thicken the
  international support section (currently US-leaning); replace the
  thin "Specialized Populations" subsections (Autism, LGBTQ+, Cultural)
  with concrete named resources or merge them into the relevant
  upstream blocks.

### News

#### `news.md` — News & announcements

- **Single topic**: Chronological news from AAN.
- **Goal**: Reader sees recent updates.
- **Audience tier**: Mixed.
- **Content shape**: News / Log.
- **Approach**: Reverse-chronological entries with dates.
- **Maintenance**: Event-driven (post when something newsworthy happens).
- **Boundaries**: Doesn't host conference announcements (those are on
  `conferences.md`); doesn't host paper announcements (those are on
  `papers.md`).
- **Current state** (597 bytes, 17 lines): Cadence note ("we post when
  there's something worth saying — site milestones, new content
  sections, partnerships, calls for contribution. We don't post for the
  sake of posting") added; cross-links to `conferences.md` and
  `papers.md` for event/paper announcements; the original "Turning the
  lights on" June 2025 entry retained.
- **Verdict**: `keep`. The next news entry is event-driven; the page
  doesn't need further structural work right now.

---

## 6. Cross-cutting findings

Status as of 2026-05-14.

A. **Same-topic duplication** drifts as soon as one copy is updated.
   - Plutchik's Wheel — **resolved**: now home on `plutchik.md`;
     `lexicon.md` links over.
   - Ekman's basic emotions — **resolved**: now home on `ekman.md`;
     `lexicon.md` links over.
   - Wilcox's Feeling Wheel — **resolved**: now home on `wilcox.md`;
     `lexicon.md` links over.
   - Studies / papers — **resolved**: `studies.md` is now a redirect
     stub pointing at `papers.md`.
   - Apps / tools overlap — **resolved**: `tools.md` is instrument-only;
     mobile/meditation apps live on `apps.md`.
   - TAS-20 development across `taylor.md` / `bagby.md` / `parker.md` —
     **still open**. Awaiting `tas-20.md`.
   - BVAQ development across `bermond.md` / `vorst.md` — **still open**.
     Awaiting `bvaq.md`.

B. **Researcher profile duplicate-H2 bug** — **resolved**. Manual TOC tables,
   repeated `## Biography and Career` headings, and the later duplicate
   Plutchik/Ekman emotion-section headings are cleared.

C. **Manual TOC tables** on researcher pages — **resolved**. All 9 pages
   now rely on MkDocs' generated TOC.

D. **Crisis content mixed with everyday support** — **resolved**. Crisis
   content extracted to `crisis-help.md`; `support.md` now opens with an
   admonition callout that redirects anyone in crisis. Safe-messaging
   conventions in place.

E. **Stub pages** — **partially resolved / partially shelved**. `news.md`
   gained a cadence note and is now a usable News/Log page (still small
   but no longer a stub). `advisors.md` is intentionally shelved: as of
   2026-05-05 it's removed from nav and from `index.md` because no
   advisors exist yet — the file remains as an orphan to preserve the
   URL when an advisor is on board.

F. **Index page CERE 2025 feature** — **resolved**. The CERE block was
   removed and `index.md` was restructured to lead with orientation
   (tagline → "what is alexithymia" → four themed entry tiles → crisis
   callout → mission summary).

G. **No `team.md`** — **shelved**. Per 2026-05-05 decision, deferred
   until there is more than one person to list. A team page with one
   entry would feel half-built.

H. **Newly-shipped pages and their carry-on work** (added 2026-05-05).
   Four pages from the prior action plan now exist —
   `comorbidities.md`, `treatment.md`, `emotion-frameworks.md`,
   `crisis-help.md` — and each has follow-on work captured in its §5
   verdict (e.g., split out `alexithymia-and-autism.md` from
   `comorbidities.md`; thicken citations on `treatment.md`; add
   Panksepp / Barrett / Plutchik-developmental to `emotion-frameworks.md`).
   `conferences.md` was over-pruned during the CERE removal and now
   needs an upcoming-events section restored even if empty, plus a
   written past-event policy.

## 7. Move / Remove / Improve / Add — consolidated action plan

Status as of 2026-05-14. Items marked **done** stay listed (with a strikethrough)
for one quarterly review pass so we can see what shipped, then drop off.
Items marked **open** are still active. Items marked **deferred** are
intentionally parked and will only re-enter the active list when the
gating condition is met.

### Add (new pages)

1. ~~**`crisis-help.md`** — crisis hotlines, safe-messaging, "if you're
   in immediate danger" page.~~ **Done** (4.9K, 103 lines).
2. ~~**`comorbidities.md`** — hub page covering psychiatric / medical /
   neurodevelopmental / substance / trauma comorbidities.~~ **Done**
   (8.2K, 218 lines).
3. ~~**`treatment.md`** — therapeutic modalities, modifications,
   medication considerations.~~ **Done** (5.0K, 108 lines).
4. ~~**`emotion-frameworks.md`** — hub for Plutchik / Ekman / Spinoza /
   Darwin / Wilcox / Brown / Damasio with links to dedicated researcher
   pages.~~ **Done** (6.1K, 110 lines).
5. **`tas-20.md`** — owns the TAS-20 development and psychometrics
   narrative; `taylor.md` / `bagby.md` / `parker.md` link in. **Open**;
   blocks resolution of RESEARCHERS-1 cross-page issue.
6. **`bvaq.md`** — owns the BVAQ narrative; `bermond.md` / `vorst.md`
   link in. **Open**; same RESEARCHERS-1 dependency.
7. **`alexithymia-and-autism.md`** — high-traffic FAQ topic and the
   biggest Autism block in `comorbidities.md`. **Open**; flagged in
   `comorbidities.md` as a future page.

### Add (deferred)

These are intentionally parked. Add back to the active list when the
gating condition is met.

- **`team.md`** — *gated on*: more than one person to list. Until then
  surfacing the founder happens (if at all) on existing pages.
- **`advisors.md` re-enable** — *gated on*: at least one actual advisor.
  The file remains as an orphan; restore to nav and to the `index.md`
  About section when populated.

### Move (content)

- ~~Comorbidity sections out of `diagnosis.md` → `comorbidities.md`.~~
  **Done.**
- ~~Treatment implications out of `diagnosis.md` → `treatment.md`.~~
  **Done.**
- ~~Framework explanations out of `lexicon.md` → researcher pages and
  `emotion-frameworks.md`.~~ **Done.**
- ~~Emotion-tracking apps out of `tools.md` → `apps.md`.~~ **Done.**
- ~~Crisis content out of `support.md` → `crisis-help.md`.~~ **Done.**
- TAS-20 development out of `taylor.md` / `bagby.md` / `parker.md` →
  `tas-20.md` (when it exists). **Open**; blocked on §7-Add-5.
- BVAQ development out of `bermond.md` / `vorst.md` → `bvaq.md` (when
  it exists). **Open**; blocked on §7-Add-6.
- Autism-specific depth out of `comorbidities.md` →
  `alexithymia-and-autism.md` (when it exists). **Open**; blocked on
  §7-Add-7.

### Remove / merge

- ~~`studies.md` → merge into `papers.md`, leave a redirect stub.~~
  **Done.**
- ~~Manual `## Contents` tables on researcher pages.~~ **Done.**
- ~~Duplicated H2s on researcher pages.~~ **Done.** Includes the original
  repeated `## Biography and Career` headings and the later Plutchik/Ekman
  consecutive-duplicate emotion-section headings.
- ~~`resources.md` "Quick Access Links" → folded into category blurbs.~~
  **Done.**

### Improve

- ~~`index.md` — orientation first, no stale featured event.~~ **Done.**
- ~~`network.md` — fix typo, contact link as join path.~~ **Done.**
- ~~`lexicon.md` — clean alphabetical glossary post-split.~~ **Done.**
- ~~`diagnosis.md` — clean assessment-and-criteria reference post-split.~~
  **Done.**
- ~~`tools.md` — instrument-only post-split.~~ **Done.** (Optional
  rename to `assessments.md` still possible if redirect handling for
  `/tools/` is acceptable.)
- ~~`support.md` — everyday-support catalog post-split.~~ **Done.**
- ~~`news.md` — cadence note + scope.~~ **Done.**
- `mission.md` — optional light expansion to a quotable paragraph.
  **Open** (low priority).
- `contact.md` — wire a real form when a mailing-list service is picked.
  **Open** (TODO item).
- `faq.md` — split long answers into dedicated explainer pages; leave
  one-paragraph summaries with "read more →" links. **Open** (top
  candidates: decision-making, physical health, overwhelming emotions).
- `apps.md` — clarify Featured vs. General categorization; decide
  whether the community-reviews section stays here or moves to
  `support.md`. **Open** (low priority).
- ~~`conferences.md` — restore an Upcoming section (even if empty) and
  add a written past-event policy.~~ **Done.**
- `books.md` — optional reading-path tracks ("for newly diagnosed",
  "for clinicians starting out"). **Open** (low priority).
- `labs.md` — add "last verified" date per entry; URL link-rot check.
  **Open** (low priority).
- `crisis-help.md` — semi-annual link-rot check on crisis services.
  **Open** (recurring, not one-shot).
- `papers.md` — fill in missing papers from TODO; AI-assisted quarterly
  refresh against PubMed with human curation. **Open** (recurring).
- ~~Researcher pages — final sweep to clear the remaining
  consecutive-duplicate H2 on `plutchik.md` and `ekman.md`.~~ **Done.**

## 8. Process — keeping `CONTENT_PLAN.md` alive

This document is the source of truth for site IA decisions. To keep it
useful:

- When a new page is added, add an entry here in the same shape.
- When the schema changes (new field), update §1 and add the field to all
  existing entries.
- Quarterly: re-read the audit, update verdicts, retire `add` items that
  shipped, re-prioritize.
- AI-assisted refresh: run a Claude session with the prompt "Read
  CONTENT_PLAN.md, then read every file under aan/docs/, and tell me
  where the actual page diverges from its declared schema." Use the
  output to drive the next quarterly review.

The TODO.md continues to track granular tasks. This file owns the
*structure*; TODO owns the *work*. When work in TODO touches site IA,
note it here so the schema stays current.
