---
version: alpha
name: AAN Open Door
description: Hopeful, humane, grounded public-facing design system for the Alexithymia Awareness Network; community-nonprofit warmth and quiet editorial restraint with a light layer of civic trust.
colors:
  primary: "#1F2430"
  secondary: "#5E6670"
  tertiary: "#4E6A61"
  accent: "#9A5B45"
  neutral: "#F6F1EA"
  surface: "#FFFDFC"
  border: "#D8CEC3"
  tint-sage: "#E8EFEB"
  tint-clay: "#F2E5DE"
  on-primary: "#FFFFFF"
  on-tertiary: "#FFFFFF"
typography:
  h1:
    fontFamily: "Source Serif 4"
    fontSize: 3.5rem
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  h2:
    fontFamily: "Source Serif 4"
    fontSize: 2.5rem
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  h3:
    fontFamily: "Source Serif 4"
    fontSize: 1.75rem
    fontWeight: 600
    lineHeight: 1.2
  body-lg:
    fontFamily: "Inter"
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.65
  body-md:
    fontFamily: "Inter"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.65
  body-sm:
    fontFamily: "Inter"
    fontSize: 0.9375rem
    fontWeight: 400
    lineHeight: 1.55
  label-sm:
    fontFamily: "Inter"
    fontSize: 0.8125rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.04em"
  eyebrow:
    fontFamily: "Inter"
    fontSize: 0.75rem
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.08em"
rounded:
  sm: 8px
  md: 16px
  lg: 24px
  xl: 36px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  2xl: 64px
  3xl: 96px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.full}"
    padding: 14px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.full}"
    padding: 14px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.full}"
    padding: 14px
  featured-badge:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 8px
  section-divider:
    backgroundColor: "{colors.border}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    height: 1px
    width: 100%
  audience-path-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 24px
  support-callout:
    backgroundColor: "{colors.tint-sage}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 24px
  evidence-panel:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 20px
  quote-panel:
    backgroundColor: "{colors.tint-clay}"
    textColor: "{colors.primary}"
    typography: "{typography.body-lg}"
    rounded: "{rounded.xl}"
    padding: 24px
---

## Overview

This design direction is for the public face of the Alexithymia Awareness Network. It should feel hopeful, humane, and grounded: more like a welcoming public-interest organization with a strong resource library than a clinic, hospital, or default documentation portal.

The homepage should serve a mixed audience without making any one visitor feel misplaced. Primary visitor groups include people trying to understand themselves, loved ones seeking understanding, clinicians or helpers, researchers or students, and general readers who need a trustworthy starting point.

The most important user outcome is not "read everything" but "find support resources that fit why I came here." The site should help visitors locate the right path for their own purpose quickly and without emotional friction.

Decisions already made:
- The emotional first impression should be hopeful, humane, and grounded.
- The site should passively build bridges of relation so visitors feel welcome, accepted, understood, and appreciated.
- The public face should be human rather than clinical or doctory.
- The visual blend should be community nonprofit warmth plus quiet editorial restraint, with a small dash of civic/public-service trust.
- Photography should favor gentle portraits and diverse relational moments over medical, corporate, or stock-wellness tropes.

Recommended homepage structure:
1. Hero with one strong human image, one welcoming headline, one grounding subhead, and two clear entry CTAs.
2. "You may be here because..." pathways for self-understanding, caring for someone else, clinical/helping roles, and research/education.
3. "Start where you are" support pathways that emphasize practical help before deep library browsing.
4. Compact mission-and-trust section that signals evidence-informed, person-centered, and public-facing credibility without adopting provider branding.
5. Humanized content section that reflects lived difficulty, common experiences, and what support can look like.
6. Research/resources bridge that introduces the library editorially rather than throwing users into table-first navigation.

## Colors

The palette should feel quiet, warm, and emotionally safe, with enough structure to retain trust. Avoid hospital blues, startup gradients, monochrome austerity, and sugary wellness pastels.

- **Primary ({colors.primary}):** Deep ink for core text, major headings, footer backgrounds, and the strongest moments of seriousness.
- **Secondary ({colors.secondary}):** Supporting text, metadata, dividers, and quieter interface language.
- **Tertiary ({colors.tertiary}):** Main action color. This softened sage carries reassurance and steadiness; use it for primary CTAs and selected states.
- **Accent ({colors.accent}):** A restrained clay accent for emphasis, featured pull quotes, or sparing highlights. Never let it overpower the sage.
- **Neutral ({colors.neutral}):** Main page field; warmer than white so the site feels inhabited instead of sterile.
- **Surface ({colors.surface}):** Cards and lighter elevated panels.
- **Border ({colors.border}):** Hairlines, section separators, and low-contrast structure.
- **Tint Sage ({colors.tint-sage}):** Support callouts, gentle background bands, and low-pressure reassurance surfaces.
- **Tint Clay ({colors.tint-clay}):** Quote blocks or reflective editorial moments.

Color usage rule: one clear interaction color, one restrained emotional accent, and mostly neutral structure. The interface should never feel painted over.

## Typography

Typography should do most of the tone-setting work. Headings should feel literate, thoughtful, and human; body text should stay plainspoken, contemporary, and easy to scan.

- Use **Source Serif 4** for major headings and section titles. It introduces editorial warmth and dignity without becoming ornate.
- Use **Inter** for body copy, labels, navigation, metadata, and interface controls. It keeps the site clear and practical.
- Let hierarchy come from scale, spacing, and weight rather than from many font families or dramatic decorative styling.
- Body copy should remain readable at comfortable widths, with generous line height and strong paragraph rhythm.
- Eyebrow labels and small caps should be used sparingly to organize content, not to create a corporate brand voice.

## Layout

Layout should feel guided, open, and editorial rather than dense or app-like.

- Favor larger section spacing and fewer simultaneous choices above the fold.
- The homepage should use a strong single-column reading rhythm with selective two-column moments for hero, pathways, and mission/trust content.
- Keep text measures comfortable: roughly 60-72 characters for body copy and shorter for emotionally important statements.
- Use cards selectively. Not every chunk of content needs a box. Group primarily through spacing, headings, image anchoring, and quiet background shifts.
- Pathway sections should be visually obvious and immediately scannable on desktop and mobile.
- Research and library content can become denser deeper in the site, but the landing experience should remain calm and socially legible.
- On mobile, pathway choices must become stacked, thumb-friendly, and emotionally readable without requiring interpretation of icons alone.

## Elevation & Depth

Depth should be subtle.

- Prefer tonal contrast, borders, and whitespace over strong drop shadows.
- Surfaces should feel layered like editorial paper sections, not floating SaaS cards.
- Reserve stronger contrast panels for support callouts, mission blocks, and the occasional featured content area.
- Motion and depth cues should reinforce orientation, never create spectacle.

## Shapes

The geometry should feel gentle and stable.

- Buttons should be pill-shaped or softly rounded to feel inviting, not clinical.
- Cards can use medium to large radii, but keep them restrained enough to avoid a soft wellness cliché.
- Large image containers and quote panels may use the largest radius to feel calm and approachable.
- Avoid sharp, brittle edges for primary user-facing surfaces.

## Components

Core component guidance:

- **Hero:** One primary emotional image, one headline, one supportive subhead, and up to two CTAs. The hero should orient and welcome, not overwhelm.
- **Audience pathway cards:** These are one of the most important components on the site. Each card should answer a real visitor intent in plain language and route to support resources for that purpose.
- **Support callouts:** Use sage-tinted reassurance surfaces for practical help, "start here" guidance, and low-pressure next steps.
- **Evidence panels:** Use quieter neutral panels for research-backed facts, disclaimers, and trust framing so evidence supports the experience without becoming the whole personality.
- **Quote or reflection panels:** Use sparingly to humanize the site with emotionally intelligent framing. These should not become inspirational filler.
- **Buttons:** One primary CTA per section when possible. Secondary actions should remain visibly available without competing for emotional dominance.
- **Navigation:** Clear, plain-language labels. The top level should route by visitor purpose and support needs before exposing the entire information architecture.
- **Search/resource access:** Search should remain available, but it should not dominate the homepage experience.

Interaction and state guidance:
- Hover states should deepen confidence, not jump in brightness.
- Focus states must be obvious, accessible, and visually aligned with the palette.
- Error, empty, and loading states should sound calm, respectful, and useful.
- Reduced-motion users should lose flourish, not clarity.

## Do's and Don'ts

Do:
- Use photography that shows dignity, reflection, companionship, and ordinary human presence.
- Write as if the reader may be arriving uncertain, tired, curious, protective, or cautiously hopeful.
- Route people by intent: "for yourself," "for someone you care about," "for practice/helping work," and "for research/learning."
- Keep research credibility visible but emotionally backgrounded on the homepage.
- Make the first interaction feel like an invitation, not an intake form.
- Preserve strong accessibility: high contrast text, clear focus states, descriptive link copy, keyboard-friendly interactions, and restrained motion.

Don't:
- Drift into clinic, hospital, provider-network, or symptom-checker aesthetics.
- Use therapist-office stock scenes, lab-coat authority signals, or overly polished corporate healthcare imagery.
- Lean on vague wellness language, soft beige emptiness, or decorative affirmations with weak information scent.
- Let the homepage become a link dump or docs front page.
- Make every surface a rounded card with equal visual weight.
- Use fake testimonials or invented personal stories.
- Treat all visitors as if they are here for the same reason.
