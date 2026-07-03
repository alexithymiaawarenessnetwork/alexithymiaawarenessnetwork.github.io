# Alexithymia expertise map for AAN

Last updated: 2026-06-29

Internal working artifact. Not published to the site.

Purpose: give the Alex profile a durable, source-disciplined map for becoming and staying expert-level on alexithymia while keeping AAN public content safe, useful, and clinician-deferring.

## 1. Expert stance

AAN should describe alexithymia as a dimensional psychological construct, not as a self-diagnosed disorder or identity label that explains everything.

Public-facing default:

- Short answer first.
- Plain-language explanation.
- Evidence and caveats separated.
- No diagnosis, treatment instruction, or medication advice.
- Qualified-professional escalation for diagnosis/treatment; crisis routing for imminent danger.

Evidence labels used in this repo:

- well-supported — repeated primary/review support and appropriate for stable public explanation.
- review-backed — supported by review/meta-analysis, but details may vary by population/instrument.
- emerging — plausible and studied, but not settled enough for strong claims.
- community/lived-experience — useful language from communities; do not present as clinical fact without evidence.
- speculative — theoretical or early-stage; explain as hypothesis.
- needs source — useful claim shape but not yet safe to publish strongly.

## 2. Current canonical AAN content base

Core planning/source artifacts:

- `CONTENT_PLAN.md` — page schema, page audit, information architecture.
- `WORK-PLAN.md`, `GOALS.md`, `MILESTONES.md`, `TODO.md` — project state and priorities.
- `THEME_MIGRATION_PLAN.md` — Astro migration model and template taxonomy.
- `aan/docs/citations.json` — current managed citation records.
- `aan/docs/*.md` — current public content source.

Current source inventory observed on 2026-06-29:

- 36 Markdown source pages in `aan/docs/`.
- 33 managed citation records in `aan/docs/citations.json`.
- Citation record types: papers, books, one tool, one book excerpt, one chapter.
- Current Astro sibling prototype renders six routes and is not yet the production knowledge-base home.

## 3. Construct backbone

### Definition and core facets

Working public definition:

Alexithymia is commonly described as difficulty identifying feelings, difficulty describing feelings, and an externally oriented thinking style. It is usually measured dimensionally rather than diagnosed categorically.

Current AAN support:

- `aan/docs/faq.md` cites Luminet, Nielson, and Ridout (2021), Sifneos (1973), Taylor/Bagby/Parker (1997), and the Cambridge Handbook excerpt.
- `aan/docs/tools.md` separates the major measurement instruments.

Stewardship caveats:

- Avoid saying alexithymia means a person has no emotions.
- Avoid saying a person “has alexithymia” as a clinical conclusion from an online score.
- Be careful with “personality trait”; explain that this is research-construct language, not blame.

Evidence status: well-supported for the broad construct/facet framing; needs source-locking for any stronger claims about causes, stability, or prognosis.

### History and origin

Current support:

- `sifneos_1973` in `aan/docs/citations.json`.
- `aan/docs/sifneos.md` owns the Sifneos profile and etymology narrative.

Stewardship caveats:

- Keep term-origin claims narrow unless the exact historical wording/source has been checked.
- Distinguish Sifneos's psychosomatic-medicine context from current broader dimensional research.

Evidence status: well-supported for term origin; deeper history needs source-specific care.

## 4. Assessment and measurement

Core instruments currently represented:

- TAS-20 — Bagby, Parker, Taylor; DIF/DDF/EOT; common research cutoffs.
- BVAQ — Bermond/Vorst; cognitive and affective dimensions.
- PAQ — positive/negative emotion structure.
- TSIA — structured interview.
- OAS — observer-rated.
- LEAS — performance-based emotional-awareness measure.

Current AAN pages:

- `aan/docs/tools.md` is the cleanest current assessment-instrument page.
- `aan/docs/diagnosis.md` covers broader clinical assessment but needs more source-locking.

Public-answer rules:

- Call online instruments “screens” or “questionnaires,” not diagnoses.
- Explain cutoffs as research conventions, not clinical thresholds.
- Recommend qualified interpretation when results matter for care.
- Mention self-report limits, especially because alexithymia itself may affect self-awareness.

Evidence status: well-supported for instrument existence and general use; needs source-locking for every scoring/cutoff/psychometric-detail claim.

## 5. Prevalence and population claims

Current AAN support:

- `mattila_salminen_nummi_joukamaa_2006` supports a Finnish general-population estimate near 10% with age/gender associations.
- `kinnaird_stewart_tchanturia_2019` supports elevated alexithymia in autistic groups in the studies reviewed.

Rules:

- Do not generalize a single country/sample/instrument cutoff as a universal prevalence fact.
- State that estimates vary by population, instrument, cutoff, age, and clinical context.
- Avoid “1 in 10” as a floating homepage claim without adjacent citation and caveat.

Evidence status: review-backed/well-supported for “not rare” and elevated rates in some groups; exact percentages need source-specific qualifiers.

## 6. Autism and neurodevelopment

Current state:

- `aan/docs/faq.md` has a short autism answer.
- `aan/docs/comorbidities.md` has an autism block and explicitly plans `alexithymia-and-autism.md`.
- `CONTENT_PLAN.md` identifies autism/alexithymia as a high-value split-out topic.

Public-answer rules:

- Do not collapse autism and alexithymia.
- Say they are distinct constructs that can co-occur.
- Be cautious with claims that emotional/social differences “are really alexithymia”; phrase as “some studies suggest alexithymia may account for some variance in emotion-processing findings historically attributed to autism.”
- Avoid treating either construct as a defect in empathy without nuance.

Evidence status: review-backed for elevated co-occurrence; mechanistic and attribution claims need careful source language.

Next artifact needed: source-locked outline for `alexithymia-and-autism.md`.

## 7. Comorbidities and adjacent clinical contexts

Current state:

- `aan/docs/comorbidities.md` is broad and useful as an outline but contains many unsourced prevalence/mechanism/treatment-implication bullets.

Priority claim families to source-lock before strengthening:

- depression/anxiety associations;
- eating disorders;
- substance use;
- trauma/PTSD/dissociation;
- pain/IBS/psychosomatic medicine;
- neurological disease;
- autism/ADHD;
- personality-disorder overlap.

Public-answer rules:

- Say “co-occurs with” rather than “causes” unless a source supports directionality.
- Avoid implying alexithymia explains a reader's symptoms.
- For trauma, severe symptoms, or safety issues, defer to qualified support.

Evidence status: topic-level co-occurrence is review-backed in broad terms; many current page details need source-locking.

## 8. Treatment and support

Current pages:

- `aan/docs/treatment.md` — overview.
- `aan/docs/therapy-approaches.md` — modality-specific page.
- `aan/docs/support.md` and `aan/docs/crisis-help.md` — support/safety surfaces.

Public-answer rules:

- Do not present any modality as a guaranteed alexithymia treatment.
- Say clinicians may adapt therapy to be more concrete, paced, body-aware, and behavior-linked.
- Medication should be framed as relevant to co-occurring conditions, not as primary alexithymia treatment.
- For therapy questions, suggest questions to ask a licensed clinician rather than instructions.

Evidence status: needs more source grading by modality. Treat current page as provisional orientation, not final evidence review.

Next artifact needed: modality evidence table with source IDs and public wording rules.

## 9. Neurobiology, interoception, and subtypes

Local library items now available:

- Goerlich-Dobre, Votinov, Habel, Pripfl, and Lamm (2015), `Neuroanatomical Profiles of Alexithymia Dimensions and Subtypes` — work ID `neuroanatomical-profiles-of-alexithymia-dimensions-and-subtypes`.
- Taylor, Bagby, and Parker, `Disorders of Affect Regulation` — public Cambridge excerpt only, work ID `disorders-of-affect-regulation-excerpt`.
- Pinna, Manchia, Paribello, and Carpiniello (2020), treatment-response systematic review — work ID `impact-of-alexithymia-on-treatment-response-systematic-review`.
- Samur et al. (2013), clinical-applications orientation/editorial — work ID `four-decades-of-research-on-alexithymia-clinical-applications`.
- Kinnaird, Stewart, and Tchanturia (2019), autism systematic review/meta-analysis — work ID `investigating-alexithymia-in-autism-systematic-review-meta-analysis`.
- Gaggero et al. (2021), subjective interoception study — work ID `clarifying-relationship-alexithymia-subjective-interoception`.
- Brewer, Cook, and Bird (2016), `Alexithymia: a general deficit of interoception` — work ID `alexithymia-general-deficit-of-interoception`.
- Schroeders, Kubera, and Gnambs (2022), TAS-20 meta-analytic confirmatory factor analysis — work ID `structure-of-toronto-alexithymia-scale-tas20-meta-analytic-cfa`.
- Bjorngard (2018), `An Embodiment Constraint on Theories of Affect` — work ID `an-embodiment-constraint-on-theories-of-affect`; adjacent philosophy-of-emotion background, not clinical/alexithymia evidence.
- Acquisition status and blocked/needed sources are tracked in `/Users/div/Repositories/source-library/docs/ALEXITHYMIA_ACQUISITION_STATUS.md`.
- Durable acquisition want-list is tracked in `/Users/div/Repositories/source-library/docs/ALEXITHYMIA_TO_BE_ACQUIRED.md`.
- Source-library status: support sources, notes_status unreviewed; none are public-page canon until reviewed.

Safe summary from inspected abstract/introduction only:

- The paper studies cognitive and affective dimensions/subtypes of alexithymia using voxel-based morphometry.
- It reports different gray/white matter volume associations across proposed subtypes/dimensions.
- It should be treated as one neuroanatomy study, not as settled proof of biologically discrete alexithymia types.

Public-answer rules:

- Use neurobiology to explain research directions, not to imply a reader's brain is known or fixed.
- Keep “subtypes” clearly tied to Bermond/BVAQ-style dimensional theory unless broader consensus is source-backed.
- Distinguish interoception, emotional awareness, bodily arousal, and self-report confidence.

Evidence status: emerging/supporting for neurobiology and interoception; needs full review before public-page promotion.

## 10. Emotion frameworks and adjacent educational content

Current AAN pages include researchers/frameworks beyond alexithymia:

- Plutchik, Ekman, Wilcox, Brené Brown, Damasio, Spinoza, Darwin, emotion frameworks, lexicon.

Stewardship rule:

- These pages help readers build emotional vocabulary and context, but they are not alexithymia evidence by default.
- Avoid letting popular frameworks substitute for clinical/research claims about alexithymia.
- Label them as educational vocabulary/framework material unless a source explicitly links them to alexithymia outcomes.

Evidence status: mixed; useful as educational context, variable as alexithymia evidence.

## 11. Source discipline workflow

Before strengthening or adding a factual public claim:

1. Find the page and nearby pages in `aan/docs/`.
2. Check `aan/docs/citations.json` for an existing source ID.
3. Check `/Users/div/Repositories/source-library/data/collections/alexithymia-research.yaml` for local source-library works.
4. If using source-library material, inspect `WORK.yaml`, `SOURCE.md`, and the working text/PDF.
5. Assign evidence label.
6. Add or update citation data only with real bibliographic details.
7. Use precise wording: population, instrument, cutoff, method, and uncertainty.
8. Avoid copying broad copyrighted text; use short quotations only when needed and verify against the PDF.

## 12. Highest-value next source-gathering requests for Rob

If Rob can source IRL or digital material, the most valuable additions are:

1. Cambridge Handbook of Alexithymia full chapters or table of contents/indices relevant to definition, assessment, autism, treatment, and clinical contexts.
2. Taylor, Bagby, and Parker, `Disorders of Affect Regulation`, especially chapters on assessment and clinical implications.
3. Primary TAS-20, BVAQ, PAQ, TSIA, OAS papers if not already locally available.
4. Recent systematic reviews/meta-analyses on treatment/intervention outcomes.
5. Reviews on alexithymia + autism, interoception, trauma/PTSD, eating disorders, pain/IBS, and substance use.
6. Clinician-authored resources suitable for public-facing referral, especially autism/interoception/somatic/DBT/EMDR-adjacent material.

## 13. Page-development priorities

1. `alexithymia-and-autism.md` — high public usefulness, already repeatedly identified.
2. Assessment instrument split pages: `tas-20.md`, `bvaq.md`, possibly PAQ/TSIA/OAS later.
3. Treatment evidence table feeding `treatment.md` and `therapy-approaches.md`.
4. Comorbidities source-lock pass with citations per prevalence/mechanism claim.
5. Etiology/development page with careful uncertainty.
6. Coping/support page focused on clinician-safe practical navigation rather than treatment instructions.
7. Papers/library data normalization across MkDocs and Astro.

## 14. Future chatbot answer pattern

For community-facing Q&A, use this shape:

1. Short answer.
2. What is well-supported.
3. Caveats / what this does not mean.
4. What to explore next: AAN pages, questions for a clinician, or source links.
5. When to seek professional help or urgent support.

Never diagnose the user. Never prescribe treatment. Validate difficulty without confirming a condition.
