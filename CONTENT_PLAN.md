# AAN Content Plan

Internal-only document. Not published to the site. Versioned with the source.

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
`split`, `merge`, `move`, `remove`, `draft`.

### Home

#### `index.md` — Welcome / landing

- **Single topic**: Welcome and orient first-time visitors; route them.
- **Goal**: Reader knows in 30 seconds what AAN is, what alexithymia is at a
  one-paragraph level, and which section to enter next.
- **Audience tier**: Mixed (navigational), with a lay-friendly opener.
- **Content shape**: Hub.
- **Approach**: One-line tagline → 2-paragraph "what is alexithymia" → 4-tile
  section grid → mission link → tiny featured-event slot (optional).
- **Maintenance**: Evergreen for the orientation copy; event-driven for the
  featured-event slot only.
- **Boundaries**: No deep content; that lives in linked pages. The featured
  conference shouldn't dominate the page.
- **Current state**: Currently leads with a CERE 2025 conference block that
  has more visual weight than the orientation. Mixes welcome + featured event
  + what-is summary + section navigation + mission summary.
- **Verdict**: `improve` — restructure to put the orientation first, demote
  the featured-event slot to a small card or remove if no current event,
  remove the duplication of mission text (link to `mission.md`).

### About Us

#### `mission.md` — Mission

- **Single topic**: AAN's mission statement.
- **Goal**: Reader understands the network's purpose in two sentences.
- **Audience tier**: Mixed.
- **Content shape**: Explainer (very short).
- **Approach**: One paragraph. Quotable. Stable.
- **Maintenance**: Evergreen.
- **Boundaries**: No history, no values list, no team — those go elsewhere.
- **Current state**: 217 bytes, well-scoped, single sentence.
- **Verdict**: `keep` — possibly expand to one short paragraph framing
  *why* the mission, but keep it tight.

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
- **Current state**: 686 bytes, cleanly scoped. Has a typo: "Policy makets".
- **Verdict**: `improve` — fix typo; consider adding one sentence on how to
  join.

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
- **Current state**: 153-byte placeholder that says "we are building an
  advisory board."
- **Verdict**: `draft` — list the actual advisors when you have them, even
  one. Add Robert Herrick as Founder & Executive Director here or on a
  separate `team.md`. (The TODO already calls for this.)

#### `contact.md` — Contact

- **Single topic**: How to reach AAN.
- **Goal**: Reader can email the team and knows what to expect.
- **Audience tier**: Mixed.
- **Content shape**: Form / Action (with no live form yet — just an email).
- **Approach**: Email + 2-3 sentence framing per audience type.
- **Maintenance**: Evergreen.
- **Boundaries**: Doesn't replicate FAQ; doesn't list resources.
- **Current state**: 1.7K, four small sections, decent.
- **Verdict**: `keep` — possibly add a contact form when the mailing-list
  service is picked.

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
- **Verdict**: `add` — create. The TODO calls for this.

### Emotion Researchers

These nine profiles are the strongest single-topic examples on the site —
each page is about one researcher. They share structural problems though.

**Cross-cutting issues** (apply to all nine):
1. Each has a "## Contents" table at the top that duplicates the H2 outline.
   MkDocs already generates a TOC; the manual contents table is maintenance
   debt.
2. Each has the literal duplicate H2 `## Biography and Career` repeated on
   consecutive lines (lines 21 and 23 of every profile). This is a
   build-output bug.
3. "## Related Resources" sections at the bottom are inconsistent across
   profiles.

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

- **`plutchik.md`** (1927–2006). 18.9K. `keep` + `improve` (fix duplicate
  H2; remove manual TOC table).
- **`ekman.md`** (1934). 12.6K. `keep` + `improve`. Same fixes. Note: page
  contains a substantial "The Six Basic Emotions" section that is also
  partially in `lexicon.md`. Decide: home the basic-emotions detail here
  *or* in `lexicon.md`, not both.
- **`sifneos.md`** (1920–2008). 12.2K. `keep` + `improve`. He coined
  "alexithymia" — make sure the term's etymology is *here* and `lexicon.md`
  links over rather than restating.
- **`taylor.md`**. 10.0K. `keep` + `improve`.
- **`bagby.md`**. 13.7K. `keep` + `improve`. Heavy overlap with `taylor.md`
  on TAS-20 development; consider one shared "TAS-20" page that both link
  to instead of duplicating the development story across both.
- **`parker.md`**. 9.6K. `keep` + `improve`. Same TAS-20 overlap.
- **`wilcox.md`**. 15.0K. `keep` + `improve`. Note: the Feeling Wheel
  details are also referenced in `lexicon.md`. Pick one canonical home.
- **`bermond.md`**. 11.0K. `keep` + `improve`. Same BVAQ-development overlap
  as `vorst.md`.
- **`vorst.md`**. 12.0K. `keep` + `improve`. BVAQ overlap.

> **Cross-page issue (RESEARCHERS-1)**: TAS-20 development is told in three
> places (Taylor, Bagby, Parker). BVAQ is told in two (Bermond, Vorst). This
> is duplicated content that will drift. *Recommended*: factor out an
> "Assessment Instruments" page (or one page per scale: `tas-20.md`,
> `bvaq.md`) that owns the development story; the researcher pages link to
> it and only describe each researcher's specific role.

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
- **Current state**: 9.9K, 226 lines, organized into 7 sections. Some
  answers are long enough to be their own pages.
- **Verdict**: `improve` — for any answer that runs >2 paragraphs, split
  the topic into a dedicated explainer page and shorten the FAQ entry to a
  paragraph + "read more →" link. Examples: "How does alexithymia affect
  decision-making?" deserves its own page; "Can alexithymia affect physical
  health?" deserves its own page.

#### `diagnosis.md` — Diagnosis & comorbidity

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
- **Current state**: 18.5K, 501 lines. Currently contains diagnosis +
  psychiatric comorbidities + medical comorbidities + neurodevelopmental
  conditions + substance use + trauma + treatment implications + future
  directions. **This is the worst single-topic violator on the site.**
- **Verdict**: `split` — see action plan §7. Keep `diagnosis.md` as the
  pure assessment-and-criteria page. Move comorbidities into one or more
  dedicated pages: at minimum a `comorbidities.md` hub plus dedicated
  pages where the depth warrants (e.g., `alexithymia-and-autism.md`).
  Move treatment implications into a new `treatment.md`.

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
- **Current state**: 32.4K, 723 lines. Currently contains: an alphabetical
  index, "Emotion Vocabularies" (Plutchik / Ekman / Spinoza / Darwin /
  Brené Brown / Wilcox / Damasio frameworks), a "Psychology Section" with
  core concepts, and a "Basic Emotions (Detailed)" section. Three things
  in one page.
- **Verdict**: `split` — see action plan §7. Keep `lexicon.md` as the
  alphabetical glossary only. The framework explainers move to:
  - Plutchik's wheel → `plutchik.md` (already exists; consolidate).
  - Ekman's basic emotions → `ekman.md` (already exists).
  - Wilcox's Feeling Wheel → `wilcox.md` (already exists).
  - Spinoza, Darwin, Brené Brown, Damasio — new historical/contemporary
    `frameworks/` pages, or a single `emotion-frameworks.md` hub that
    profiles each and links to deeper pages where warranted.

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
- **Current state**: 4.8K, 118 lines. Mostly clean hub. Has a "Quick Access
  Links" section that overlaps with the categories above it.
- **Verdict**: `improve` — collapse "Quick Access Links" into the category
  blurbs.

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
- **Current state**: 6.8K, 199 lines. Organized into Featured / General /
  Specialized / Web-Based + a community reviews section.
- **Verdict**: `improve` — clarify what counts as "Featured Alexithymia App"
  vs. "General Emotional Wellness." Decide whether to keep the community
  reviews section or move it into `support.md`.

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
- **Current state**: 7.7K, 209 lines. Currently mixes academic instruments
  (TAS-20, BVAQ) with mobile emotion-tracking apps and meditation apps
  (overlapping `apps.md`).
- **Verdict**: `split` — keep only the academic instruments here. Move
  emotion-tracking apps and mindfulness apps to `apps.md` (or remove the
  duplicates if `apps.md` already lists them). Consider renaming this
  page to `assessments.md` once it's instrument-only.

> **Cross-page issue (RESOURCES-1)**: There's content overlap between
> `apps.md` (mobile apps) and `tools.md` (which currently mixes academic
> instruments with apps). Resolve by tightening each page's scope per the
> verdicts above.

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
- **Current state**: 7.3K, 84 lines. Clean.
- **Verdict**: `keep` — possibly add reading-path "tracks" (e.g., "for the
  newly diagnosed", "for clinicians starting out").

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
- **Current state**: 11.8K, 366 lines, custom-styled table.
- **Verdict**: `keep` (and absorb `studies.md` — see below).

#### `studies.md` — Studies

- **Verdict**: `merge into papers.md` — `studies.md` (3.3K) and `papers.md`
  (11.8K) are the same kind of page. Pick one, redirect the other. The
  papers page already has a real sortable table; studies has prose lists.
  Keep papers.md, fold any unique entries from studies.md into it, replace
  studies.md content with a redirect note, remove from nav.

#### `podcasts.md` — Podcasts

- **Single topic**: Podcasts and podcast episodes relevant to alexithymia.
- **Goal**: Reader finds something to listen to.
- **Audience tier**: Lay.
- **Content shape**: Catalog.
- **Approach**: Episode block: host, episode title, brief, link.
- **Maintenance**: Community-driven.
- **Boundaries**: Doesn't catalog general mental-health podcasts unless they
  have specific alexithymia content.
- **Current state**: 5.6K, well-scoped.
- **Verdict**: `keep`.

### Research

#### `studies.md` — see above (`merge into papers.md`).

#### `labs.md` — Research labs

- **Single topic**: Research labs and institutions doing alexithymia work.
- **Goal**: Researcher / practitioner finds where active work happens.
- **Audience tier**: Researcher (primary), Practitioner (secondary).
- **Content shape**: Catalog (geographic).
- **Approach**: Region → institution → PIs, focus, notable research.
- **Maintenance**: Periodic review (yearly).
- **Boundaries**: Doesn't list every researcher (those have profile pages);
  doesn't list every paper (those are on `papers.md`).
- **Current state**: 9.9K, well-organized geographically.
- **Verdict**: `keep` — possibly add a "last verified" date per entry to
  support the periodic review cadence.

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
- **Current state**: 5.7K, decent. Currently features CERE 2025 (which has
  passed by April 2026 — needs maintenance).
- **Verdict**: `improve` — refresh the upcoming list; add a clear policy
  on when to remove past events (likely: keep recent past for ~6 months
  with a "past" header, then remove).

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
- **Current state**: 7.9K, 271 lines. Currently contains everyday support
  *and* crisis hotlines *and* emergency resources *and* "When to Seek
  Immediate Help" — mixing routine support with crisis content is a UX and
  safety issue.
- **Verdict**: `split` — extract crisis content into a new
  `crisis-help.md` (or `urgent-support.md`) with its own nav slot at the
  top of the Community & Events section, and follow safe-messaging
  guidelines (e.g., 988 lifeline, Crisis Text Line, internationally-
  appropriate options). Update `support.md` to be everyday-support only,
  with a single prominent "If you're in crisis, see [Crisis & Urgent
  Support](crisis-help.md)" callout at the top.

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
- **Current state**: 348 bytes, one entry from June 2025.
- **Verdict**: `improve` — add a publishing cadence note ("we post when
  we have something to say"); link conference / paper updates to
  `conferences.md` / `papers.md` rather than reposting.

---

## 6. Cross-cutting findings

A. **Same-topic duplication** drifts as soon as one copy is updated:
   - TAS-20 development told across `taylor.md` / `bagby.md` / `parker.md`.
   - BVAQ development told across `bermond.md` / `vorst.md`.
   - Plutchik's Wheel detailed in both `plutchik.md` and `lexicon.md`.
   - Ekman's basic emotions detailed in both `ekman.md` and `lexicon.md`.
   - Wilcox's Feeling Wheel detailed in both `wilcox.md` and `lexicon.md`.
   - Studies / papers split across `studies.md` and `papers.md`.
   - Apps / tools overlap across `apps.md` and `tools.md`.

B. **Researcher profile build bug**: every researcher page has a duplicate
   `## Biography and Career` heading on consecutive lines. Fix in a sweep.

C. **Manual TOC tables** at the top of every researcher page duplicate
   what MkDocs already generates. Remove.

D. **Crisis content mixed with everyday support** in `support.md` —
   safety / UX issue that should be addressed before anything else.

E. **Stub pages** (`advisors.md`, `news.md`) need either content or
   honest "we're working on this" framing with a date.

F. **Index page features a stale conference** (CERE 2025, by April 2026 in
   the past). Either rotate or stop featuring an event.

G. **No `team.md`** despite the Founder & ED being a known person. AAN
   feels more credible when the humans are visible.

## 7. Move / Remove / Improve / Add — consolidated action plan

### Add (new pages)

1. **`team.md`** — Founder & ED + future team members.
2. **`crisis-help.md`** — Crisis hotlines, safe-messaging, "if you're in
   immediate danger" page, prominently linked.
3. **`comorbidities.md`** — hub page listing the comorbidity areas
   (psychiatric / medical / neurodevelopmental / substance / trauma) and
   linking to dedicated pages where depth warrants.
4. **`treatment.md`** — therapeutic modalities, what works, what doesn't,
   with proper caveats. Currently buried inside `diagnosis.md`.
5. **`tas-20.md`** *(or a single `assessments/instruments.md`)* — owns the
   TAS-20 development and psychometrics narrative; researcher pages link
   to it.
6. **`bvaq.md`** *(same as above)* — owns the BVAQ narrative.
7. **`alexithymia-and-autism.md`** — currently a high-traffic FAQ topic +
   buried diagnosis section, deserves its own explainer.
8. **`emotion-frameworks.md` (or a `frameworks/` directory)** — owns
   Plutchik's wheel, Ekman's basic emotions, Wilcox's Feeling Wheel,
   Spinoza, Darwin, Brené Brown, Damasio as either a single hub +
   per-framework explainer pages OR one explainer per framework.

### Move (content)

- Comorbidity sections out of `diagnosis.md` → `comorbidities.md` and/or
  per-condition pages.
- Treatment implications out of `diagnosis.md` → `treatment.md`.
- Framework explanations out of `lexicon.md` → researcher pages or
  `emotion-frameworks.md`.
- TAS-20 development out of `taylor.md` / `bagby.md` / `parker.md` →
  `tas-20.md`. Each researcher page keeps only their specific role.
- BVAQ development out of `bermond.md` / `vorst.md` → `bvaq.md`.
- Emotion-tracking apps out of `tools.md` → `apps.md`.
- Crisis content out of `support.md` → `crisis-help.md`.

### Remove / merge

- `studies.md` → merge any unique entries into `papers.md`, then redirect.
- Manual `## Contents` tables on researcher pages — let MkDocs render the
  TOC.
- Duplicated `## Biography and Career` H2s on every researcher page.
- `resources.md` "Quick Access Links" → fold into the category blurbs.

### Improve

- `index.md` — orientation first, conference featured slot only when
  current.
- `mission.md` — light expansion if desired; keep brief.
- `network.md` — fix typo, add a "how to join" sentence.
- `advisors.md` — list the actual people; link to `team.md`.
- `contact.md` — wire a real form when mailing list is picked.
- `faq.md` — split long answers into dedicated explainers, leave one-paragraph
  summaries with "read more" links.
- `lexicon.md` — once frameworks are extracted, becomes a clean alphabetical
  glossary.
- `diagnosis.md` — once comorbidities + treatment are extracted, becomes a
  clean assessment-and-criteria reference.
- `tools.md` — rename to `assessments.md` once instrument-only.
- `support.md` — once crisis is extracted, becomes everyday-support catalog.
- `conferences.md` — refresh upcoming, add a past-event policy.
- `news.md` — add cadence note + clear scope.
- All researcher pages — sweep to fix the duplicate H2 build bug + drop the
  manual TOC tables.

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
