# AAN theme migration plan

Internal planning document. Not published to the public site.

Last updated: 2026-06-22

## 1. Decision direction

AAN should stop investing in deep Material for MkDocs customization as the long-term design foundation. Material is useful for documentation sites, but the current AAN direction is no longer a conventional docs portal. The new homepage mockup wants an editorial, humane, nonprofit/public-interest site with a stronger layout system, photography rules, and reusable page templates.

The preferred migration direction is:

- keep Markdown as the primary authoring format;
- move the site shell and page templates to a static-site framework with first-class layout control;
- preserve current content URLs where possible;
- use the current `mockups/aan-homepage-open-door-v24-beta.html` as the fidelity gate for the new theme;
- avoid a framework that forces every page to become a hand-coded component.

Default recommendation: **Astro static site, Markdown-first, MDX only when a page genuinely needs component-level composition.**

Why Astro is the leading option:

- Markdown files can remain the main content source.
- Each page can choose a layout through frontmatter or content collections.
- The homepage mockup can be decomposed into real components without fighting a documentation theme.
- Static output can still publish to GitHub Pages.
- Existing JSON/data assets such as citation data and paper metadata can be consumed directly.
- Interactive pieces can stay as small vanilla JS islands rather than becoming a full SPA.

Viable fallback: **Eleventy** if the project wants the thinnest possible Markdown + templates stack. Eleventy is excellent for low-JS editorial sites, but Astro is a better fit if the homepage and future bespoke sections need componentized layouts while most content remains plain Markdown.

Non-goal: migrate to another docs-first theme and then fight it into looking like the v24 mockup.

## 2. Support-section posture

Support must be **findable, calm, and safe**, but it is not the primary site focus.

Do not frame the whole conversion around Support. Do not promote Support as the dominant homepage path. Do not make Support visually louder than the broader AAN mission, education, research, and resource-library work.

Support pages need a special safety layout because the content can be urgent or sensitive. That is a content-safety requirement, not an information-architecture priority signal.

Practical rule:

- Support may appear as a utility/navigation item and as a relevant related link.
- Crisis or urgent-help language should appear only where it is contextually necessary.
- Homepage emphasis should remain balanced: understand alexithymia, learn about emotions, browse resources/research, learn about AAN.
- Assessment instruments remain informational and clinician-discretionary, never a primary conversion CTA.

## 3. Design north star

The migration is on the right track only if the new theme can faithfully build the current open-door mockup.

Source mockup:

- `mockups/aan-homepage-open-door-v24-beta.html`

Design posture:

- hopeful, humane, grounded;
- non-clinical;
- warm editorial/community nonprofit plus civic trust;
- quiet, credible, not brochure-clinical;
- people photography used sparingly and relationally;
- no fake stats, fake testimonials, fake logos, or inflated claims;
- clinician-deferring wherever assessment/treatment/support topics appear.

Fidelity gate:

1. Build the homepage in the new theme from reusable layout/components.
2. Compare the built page to the v24 beta at desktop and mobile widths.
3. If the framework cannot reproduce the mockup without hacks, it is the wrong foundation.

## 4. Proposed authoring model

Content authors should keep writing mostly in Markdown.

Baseline page shape:

```yaml
---
title: Frequently Asked Questions
description: Plain-language answers to common alexithymia questions.
page_type: explainer
audience: lay
status: published
nav_group: Understanding Alexithymia
related:
  - diagnosis.md
  - tools.md
  - papers.md
---
```

The Markdown body remains ordinary Markdown:

- headings;
- paragraphs;
- lists;
- tables;
- links;
- citation links;
- occasional HTML only when needed.

Template/layout code supplies:

- page chrome;
- heading rhythm;
- hero/introduction treatment;
- table wrappers;
- callout styling;
- related-page blocks;
- citation hover behavior;
- resource-card styling;
- mobile layout behavior.

Use **MDX only as an escape hatch** for pages that need component composition, such as the homepage, advanced resource hubs, or interactive research/library pages. Do not force routine explainers and profiles into MDX.

## 5. Core templates to build

### 5.1 Base site shell

Applies to every page.

Responsibilities:

- header/nav;
- footer;
- skip link;
- responsive menu;
- page width and background system;
- typography and token loading;
- focus states;
- analytics/GTM partials if retained;
- citation JS/CSS wiring;
- global accessibility and reduced-motion behavior.

### 5.2 Landing / orientation template

Primary use:

- `index.md` or an Astro/MDX homepage equivalent.

Purpose:

- explain what AAN is;
- give a humane one-screen orientation;
- route visitors by intent;
- express the full open-door art direction.

Build from:

- `HeroOpenDoor`;
- `AudiencePathGrid`;
- `EditorialSection`;
- `EvidencePanel`;
- `ResourcePreview`;
- `PhotoAtmosphere`;
- `SectionDivider`.

This is the most bespoke template and the visual proof that the migration is working.

### 5.3 Evidence-informed explainer template

Primary use:

- FAQ;
- diagnosis;
- treatment;
- therapy approaches;
- comorbidities;
- emotion frameworks;
- lexicon, with glossary-specific handling.

Purpose:

- make evidence-based prose readable and calm;
- support citations without making the page feel like a PDF;
- distinguish “what this means” from “what this does not mean.”

Template features:

- editorial intro block;
- optional key-point callout;
- citation hover support;
- table wrappers;
- related pages;
- clinician-discretion note when relevant;
- long-page table of contents only when useful.

### 5.4 Resource hub / resource listing template

Primary use:

- resources;
- apps;
- books;
- podcasts;
- assessment instruments.

Purpose:

- make lists scannable;
- group items without over-cardifying everything;
- provide clear metadata and source links;
- keep resource recommendations informational rather than prescriptive.

Template features:

- category cards;
- resource cards/list rows;
- metadata chips;
- filters/jump links when useful;
- last-reviewed field;
- contribution/correction note.

### 5.5 Research library / data-heavy template

Primary use:

- papers;
- labs;
- conferences;
- studies redirect/deferred page.

Purpose:

- handle dense research information without losing trust or mobile usability.

Template features:

- calm dense header;
- search/filter affordance where needed;
- responsive table container;
- metadata chips;
- source/date labels;
- generated-data compatibility;
- no decorative photography by default.

### 5.6 Researcher / concept profile template

Primary use:

- Plutchik;
- Ekman;
- Brené Brown;
- Sifneos;
- Taylor;
- Bagby;
- Parker;
- Wilcox;
- Bermond;
- Vorst.

Purpose:

- make profiles feel like useful intellectual context, not fan pages.

Template features:

- profile header;
- contribution summary;
- key concepts;
- relevance-to-AAN block;
- bibliography/source links;
- optional timeline or “known for” panel.

### 5.7 Organization / trust / update template

Primary use:

- mission;
- network;
- contact;
- advisors;
- media;
- news.

Purpose:

- make sparse institutional pages feel intentional rather than unfinished.

Template features:

- concise intro;
- trust/institutional framing;
- contact/action block where relevant;
- optional update list for news;
- no faux institutional bloat.

### 5.8 Support / practical-help template

Primary use:

- support;
- crisis-help.

Purpose:

- make urgent and practical information easy to use without turning Support into the site's primary identity.

Template features:

- urgent-help panel only on pages where it belongs;
- country/context labels;
- plain-language next steps;
- no dramatic distress imagery;
- no homepage-level visual dominance;
- clear external links;
- qualified-professional / local-emergency-service disclaimers.

## 6. Existing page classification

Classification is based on the current files in `aan/docs/` and the current `aan/mkdocs.yml` nav/not-in-nav state.

| Page | Current status | Page type | Proposed template |
|---|---:|---|---|
| `index.md` | nav | Landing / orientation | Landing / orientation |
| `mission.md` | nav | Organization / trust | Organization / trust / update |
| `network.md` | nav | Organization / trust | Organization / trust / update |
| `contact.md` | nav | Organization / trust / action | Organization / trust / update |
| `advisors.md` | not in nav | Organization / trust / placeholder | Organization / trust / update |
| `faq.md` | nav | Evidence-informed explainer | Evidence-informed explainer |
| `diagnosis.md` | nav | Evidence-informed explainer | Evidence-informed explainer |
| `comorbidities.md` | nav | Evidence-informed explainer | Evidence-informed explainer |
| `treatment.md` | nav | Evidence-informed explainer | Evidence-informed explainer |
| `therapy-approaches.md` | nav | Evidence-informed explainer | Evidence-informed explainer |
| `lexicon.md` | nav | Glossary/reference explainer | Evidence-informed explainer with glossary mode |
| `emotion-frameworks.md` | nav | Evidence-informed explainer / reference | Evidence-informed explainer with table support |
| `plutchik.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `ekman.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `brene-brown.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `sifneos.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `taylor.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `bagby.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `parker.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `wilcox.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `bermond.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `vorst.md` | nav | Researcher / concept profile | Researcher / concept profile |
| `resources.md` | nav | Resource hub | Resource hub / resource listing |
| `apps.md` | nav | Resource listing | Resource hub / resource listing |
| `tools.md` | nav | Assessment-instrument resource listing | Resource hub / resource listing with clinician-discretion note |
| `books.md` | nav | Resource listing | Resource hub / resource listing |
| `papers.md` | nav | Research library / data-heavy | Research library / data-heavy |
| `podcasts.md` | nav | Resource listing | Resource hub / resource listing |
| `labs.md` | nav | Research library / institution catalog | Research library / data-heavy |
| `support.md` | nav | Support / practical help | Support / practical-help |
| `crisis-help.md` | not in nav | Support / urgent redirect or utility page | Support / practical-help, minimal variant |
| `conferences.md` | nav | Research/community event catalog | Research library / data-heavy or organization/update depending on content depth |
| `news.md` | nav | News / update log | Organization / trust / update |
| `media.md` | not in nav | Media placeholder | Organization / trust / update |
| `studies.md` | not in nav | Legacy/deferred redirect stub | Redirect/deprecated-page template |

## 7. URL and content migration rules

Preserve public URLs where possible:

- MkDocs `/faq/` should remain `/faq/`.
- Redirect or keep stub pages for legacy/deferred routes such as `/studies/`.
- Keep the custom domain and GitHub Pages output boundary in mind.

Migration should be source-first:

- current source Markdown is the canonical content;
- generated `docs/` output is build artifact;
- do not hand-edit generated HTML except for emergency publishing fixes.

Initial migration can keep filenames stable and add frontmatter gradually. Page type can be inferred by a manifest during the first pass, then moved into frontmatter once the system is stable.

## 8. Component inventory

Build these once and reuse across templates:

- `SiteHeader`
- `SiteFooter`
- `SkipLink`
- `OpenDoorLogoLockup`
- `HeroOpenDoor`
- `SectionHeader`
- `AudiencePathCard`
- `ResourceCard`
- `EvidencePanel`
- `QuotePanel`
- `Callout`
- `SafetyNotice`
- `RelatedPages`
- `CitationLink` / citation hover behavior
- `ResponsiveTable`
- `MetadataChips`
- `ProfileHeader`
- `BibliographyBlock`
- `LastReviewed`

CSS should be token-driven and boringly reusable:

- colors;
- typography;
- spacing;
- radius;
- border;
- elevation;
- focus;
- motion;
- breakpoints/container queries.

## 9. Migration phases

### Phase 0 — Platform spike

Goal: prove the replacement stack can build the open-door mockup faithfully.

Tasks:

1. Create a small Astro prototype in a branch or isolated directory.
2. Port only the base shell, tokens, and homepage mockup.
3. Use real AAN content and current imagery.
4. Build static output.
5. Compare desktop and mobile against `aan-homepage-open-door-v24-beta.html`.

Exit criteria:

- homepage is visually faithful;
- static build works;
- no framework-level obstacle to GitHub Pages;
- Markdown pages can render through a layout;
- citation data strategy is plausible.

### Phase 1 — Content/template skeleton

Goal: render the whole current content set through rough templates.

Tasks:

1. Import all `aan/docs/*.md` pages.
2. Preserve slugs.
3. Assign each page a page type.
4. Implement basic layouts for every page type.
5. Wire global nav and footer.

Exit criteria:

- every current page has an equivalent generated page;
- no missing-route surprises;
- pages are readable even before visual polish.

### Phase 2 — Visual system implementation

Goal: make the new templates feel like the open-door system, not a docs theme.

Tasks:

1. Port tokens from `DESIGN.md` into CSS variables/design tokens.
2. Build responsive typography and spacing scales.
3. Implement cards, callouts, tables, profile headers, resource listings.
4. Rebuild citation hover styling without Material variable dependence.

Exit criteria:

- homepage, FAQ, resources, papers, and one researcher profile feel like the same site;
- mobile layouts have no horizontal overflow;
- focus states and contrast are acceptable.

### Phase 3 — Editorial conversion pass

Goal: adapt content enough to benefit from the new templates without rewriting the entire site.

Tasks:

1. Add frontmatter where useful.
2. Add descriptions/related-page metadata.
3. Convert obvious resource lists into structured data or consistent Markdown blocks.
4. Add clinician-discretion notes to assessment/treatment pages where needed.
5. Keep Support calm and findable but not promoted as a primary journey.

Exit criteria:

- templates are pulling meaningful metadata;
- resource pages scan better;
- explainers have clearer intros and next steps;
- no major content claims changed without review.

### Phase 4 — Build/publish parity

Goal: replace the MkDocs publishing path only after parity is real.

Tasks:

1. Confirm local build command.
2. Confirm GitHub Pages output directory.
3. Confirm sitemap/search/redirect behavior.
4. Compare generated route list against current site.
5. Update README/requirements/package docs.

Exit criteria:

- new build is reproducible;
- old routes are preserved or intentionally redirected;
- generated output is synchronized;
- deployment does not depend on Material/MkDocs.

## 10. Acceptance checks

### Visual

- Built homepage matches the v24 mockup closely enough that differences are intentional.
- Interior pages inherit the same typography, color, spacing, and warmth.
- Sparse org pages look intentional, not empty.
- Research/data pages remain credible and calm.
- Support pages are safe and usable without becoming the site's visual center.

### UX

- A first-time visitor can understand what AAN is within seconds.
- Navigation supports awareness, education, resources, research, and organization trust.
- No page dead-ends.
- Related links feel contextual, not SEO filler.

### Accessibility

- Semantic heading order.
- Visible focus states.
- Sufficient color contrast.
- Keyboard-accessible nav.
- Reduced-motion handling for non-essential motion.
- Tables usable on small screens.
- Descriptive link text.

### Content integrity

- AAN remains informational only.
- No assessment page implies diagnosis.
- No treatment page gives individualized medical advice.
- Citations remain available and usable.
- No fake testimonials, stats, institutions, or logos.

### Technical

- Static build passes.
- Route parity is checked.
- Generated output is not manually edited.
- CSS is tokenized rather than page-specific sprawl.
- The new system can render normal Markdown pages and special pages from the same codebase.

## 11. Open questions

1. Astro vs Eleventy: Astro is the current recommendation, but the platform spike should be allowed to disprove it.
2. Search: keep a generated static search index, use a lightweight client-side search, or defer search until the content library is larger?
3. Citations: keep the current hover-box behavior, redesign it, or simplify citation previews for the first migration?
4. Resource lists: keep them in Markdown first, or start moving high-structure resources into JSON/YAML data files?
5. Homepage authoring: should the homepage be MDX/component-authored, or should it use data files plus a fixed layout?
6. Nav grouping: preserve current MkDocs grouping initially, then tune labels after template migration; or revise IA during migration?

## 12. Next concrete step

Build a tiny platform spike rather than migrating the full site immediately:

- one Astro shell;
- one homepage built from the v24 mockup;
- one explainer page from `faq.md`;
- one resource page from `resources.md`;
- one research/data page from `papers.md`;
- one profile page from `plutchik.md`.

If those six pages feel coherent and the homepage is faithful, proceed with the full migration. If they do not, adjust the stack or template contract before touching the rest of the content.
