---
name: Knowledge Map — Mission Control
description: Visual identity of the interactive knowledge-map page that Agent E (Visual Map Generator) renders for one area of knowledge.
status: final
updated: 2026-10-21
sources:
  - area-of-knowledge-expert/PROMPT.md
  - area-of-knowledge-expert/SUB_FIELDS_EXAMPLE.md
  - area-of-knowledge-expert/OVERVIEW_EXAMPLE.md
colors:
  background: '#000000'
  surface-lift: '#0A0D12'
  hairline: '#1F2328'
  line: '#2E343B'
  link-rest: '#545B64'
  ring-tick: '#191D22'
  text: '#F2F2F2'
  text-body: '#C9D1D9'
  muted: '#7D8590'
  primary: '#FF6B1A'
  secondary: '#3B82F6'
typography:
  display-area:
    fontFamily: Orbitron
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0.24em
  heading-page:
    fontFamily: Orbitron
    fontSize: 28px
    fontWeight: '400'
    letterSpacing: 0.2em
  heading-section:
    fontFamily: Orbitron
    fontSize: 15px
    fontWeight: '500'
    letterSpacing: 0.16em
  heading-group:
    fontFamily: Orbitron
    fontSize: 13px
    fontWeight: '500'
    letterSpacing: 0.16em
  label-subfield:
    fontFamily: Orbitron
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 15px
    letterSpacing: 0.14em
  label-topic:
    fontFamily: Orbitron
    fontSize: 10.5px
    fontWeight: '400'
    letterSpacing: 0.1em
  label-index:
    fontFamily: Orbitron
    fontSize: 10.5px
    fontWeight: '400'
    letterSpacing: 0.14em
  label-nav:
    fontFamily: Orbitron
    fontSize: 10px
    fontWeight: '400'
    letterSpacing: 0.26em
  label-meta:
    fontFamily: Orbitron
    fontSize: 10px
    fontWeight: '500'
    letterSpacing: 0.18em
  label-kicker:
    fontFamily: Orbitron
    fontSize: 10px
    fontWeight: '400'
    letterSpacing: 0.3em
  label-brand:
    fontFamily: Orbitron
    fontSize: 11px
    fontWeight: '400'
    letterSpacing: 0.28em
  label-tag:
    fontFamily: Orbitron
    fontSize: 10px
    fontWeight: '500'
    letterSpacing: 0.16em
  label-ring:
    fontFamily: Orbitron
    fontSize: 8px
    fontWeight: '400'
  body-reading:
    fontFamily: Inter
    fontSize: 17px
    fontWeight: '400'
    lineHeight: '1.75'
  body-citation:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.6'
rounded:
  none: 0px
  full: 9999px
spacing:
  bar-height: 64px
  page-margin: 40px
  container-max: 1160px
  article-max: 720px
  index-width: 220px
  index-gap: 72px
  section-top: 120px
  section-gap: 56px
  group-gap: 64px
  map-min-height: 640px
  map-rx-ratio: '0.28'
  map-rx-max: 560px
  map-rx-min: 220px
  map-ry-ratio: '0.32'
  map-ry-max: 300px
  topic-radius: 120px
  topic-step: 28deg
  glow-blur: 5px
components:
  node-root:
    radius: 72px
    outer-ring-radius: 80px
    fill: '{colors.background}'
    stroke: '{colors.text}'
    outer-stroke: '{colors.hairline}'
    label: '{typography.display-area}'
  node-subfield:
    dot-radius: 6.5px
    dot-radius-open: 8px
    fill: '{colors.primary}'
    glow: '{spacing.glow-blur}'
    open-ring-radius: 17px
    open-ring-stroke: '{colors.primary}'
    label: '{typography.label-subfield}'
    label-open-color: '{colors.primary}'
    label-hover-color: '{colors.secondary}'
    meta: '{typography.label-meta}'
    meta-color: '{colors.muted}'
    focus-ring: '{colors.secondary}'
  node-topic:
    marker-size: 6px
    fill: '{colors.secondary}'
    label: '{typography.label-topic}'
  edge-spoke:
    stroke: '{colors.hairline}'
    width: 1px
  edge-link:
    stroke: '{colors.link-rest}'
    width: 1px
    hot-stroke: '{colors.secondary}'
    hot-width: 1.5px
    hot-glow: '{spacing.glow-blur}'
  edge-topic:
    stroke: '{colors.secondary}'
    opacity: '0.7'
  faded:
    opacity: '0.12'
  telemetry-ring:
    tick: '{colors.ring-tick}'
    major-tick: '{colors.line}'
    label: '{typography.label-ring}'
    label-color: '{colors.line}'
  telemetry-readout:
    type: '{typography.label-meta}'
    color: '{colors.muted}'
  map-hint:
    type: '{typography.label-meta}'
    color: '{colors.muted}'
  scroll-cue:
    type: '{typography.label-meta}'
    color: '{colors.muted}'
    hover-color: '{colors.text}'
  top-bar:
    height: '{spacing.bar-height}'
    background: 'rgba(0,0,0,0.7)'
    blur: 8px
    border: '{colors.hairline}'
    brand: '{typography.label-brand}'
    nav: '{typography.label-nav}'
    nav-rest: '{colors.muted}'
    nav-active: '{colors.text}'
  sticky-index-item:
    type: '{typography.label-index}'
    color: '{colors.muted}'
    number-color: '{colors.muted}'
    rule: '{colors.hairline}'
    hover-color: '{colors.secondary}'
    active-color: '{colors.text}'
    active-rule: '{colors.primary}'
    active-number-color: '{colors.primary}'
  section-heading:
    type: '{typography.heading-section}'
    rule: '{colors.primary}'
    number-color: '{colors.primary}'
  topics-line:
    type: '{typography.label-meta}'
    label-color: '{colors.muted}'
    item-color: '{colors.text}'
  connects-line:
    type: '{typography.label-meta}'
    label-color: '{colors.muted}'
    link-color: '{colors.text}'
    link-hover: '{colors.secondary}'
  citation-link:
    type: '{typography.body-reading}'
    color: '{colors.secondary}'
    underline-opacity: '0.4'
  resource-group:
    heading: '{typography.heading-group}'
    rule: '{colors.primary}'
    number-color: '{colors.primary}'
  resource-entry:
    tag-column: 96px
    divider: '{colors.hairline}'
    citation: '{typography.body-citation}'
    citation-color: '{colors.text-body}'
    title-color: '{colors.text}'
    link: '{typography.label-meta}'
    link-color: '{colors.muted}'
    link-hover: '{colors.secondary}'
    flash: '{colors.secondary}'
    flash-opacity: '0.14'
  type-tag:
    type: '{typography.label-tag}'
    color: '{colors.primary}'
    border: '{colors.line}'
    rounded: '{rounded.none}'
  footer:
    type: '{typography.label-meta}'
    color: '{colors.muted}'
    border: '{colors.hairline}'
  focus-outline:
    color: '{colors.secondary}'
    width: 1px
    offset: 4px
---

## Brand & Style

**Mission Control · Telemetry.** The page should feel like a launch-control screen for a field of study: pure black, hairline strokes, wide-tracked uppercase labels and small telemetry details. Think spacex.com restraint, with a sci-fi display face. Decoration is rationed. The one ambient element is a slowly rotating tick ring behind the map, and everything else on screen carries information.

Two strong colors against black provide the "vibrant contrast". A rainbow was explicitly rejected, and so was the original six-neon set. The *Map of Mathematics* poster (`../map-of-mathematics.webp`) was a loose starting point only: its idea of an area with subfields around it survives, but none of its hand-drawn style does.

The reference implementation is **`assets/knowledge-map-template.html`**. Its CSS custom properties mirror these tokens one to one, and the JS reads colors from them, so nothing is duplicated. **These spines win on any conflict with the template.**

## Colors

- **Background (`{colors.background}`)** is the whole canvas. The map section adds a soft radial lift to `{colors.surface-lift}` at its center for depth. Never use a light surface.
- **Hairline (`{colors.hairline}`)** draws structure that should recede: `edge-spoke` (redundant, since every subfield has one), dividers, the top-bar border and inactive index rules.
- **Link-rest (`{colors.link-rest}`)** colors `edge-link` at rest. These lines are the map's main information, so they get 3:1 contrast against black.
- **Line (`{colors.line}`)** is decorative only: major ring ticks, ring labels and tag borders. Never use it for text that carries meaning.
- **Text (`{colors.text}`)** is for labels and headings. **Text-body (`{colors.text-body}`)** is for long reading text. **Muted (`{colors.muted}`)** is for metadata, inactive nav, index numbers and hints.
- **Primary, orange (`{colors.primary}`)**, *is the subfields*: their dots, open labels, section numbers and rules, the active index item, and type tags. Every subfield uses the same orange; numbers 01–06 tell them apart.
- **Secondary, blue (`{colors.secondary}`)**, *is interaction*. It marks things you can act on (citations, link hovers, focus outlines, highlighted lines) and things that appear because of your action (topics, which show only after you expand a subfield, and the reference flash). Nav hover and active states use white on purpose, so the global chrome stays neutral.
- Never introduce a third accent color, and never give subfields different colors.

**Contrast on `{colors.background}`:** text 18.8:1 · text-body 13.6:1 · primary 7.4:1 · muted 5.6:1 · secondary 5.7:1 · link-rest 3.1:1 (graphics) · line 1.7:1 (decorative only).

## Typography

- **Orbitron** is the display and label voice: the area name, headings, nav, map labels, indices, tags and telemetry. Always uppercase and tracked. The smallest informative size is **10px**, and muted text is set at weight 500. The only exception is `{typography.label-ring}` at 8px, which is decorative and hidden from assistive technology.
- **Inter** is the reading voice. Overview paragraphs use `{typography.body-reading}`, and citations and references use `{typography.body-citation}`. Inter text is never uppercase or tracked.
- Both families load from Google Fonts with `display=swap`, falling back to `system-ui`.
- On the map, any subfield name longer than 18 characters wraps onto two balanced lines at `{typography.label-subfield.lineHeight}`.

## Layout & Spacing

The page is one long column of three full-width sections: **Map** (exactly one viewport tall, min `{spacing.map-min-height}`), then **Overview**, then **Resources**. A fixed `top-bar` (`{spacing.bar-height}`) floats above all three.

- **Map:** the area is fixed at the center of the space below the bar. N subfields (1–6) sit evenly on an ellipse with horizontal radius `{spacing.map-rx-ratio}` × width, clamped between `{spacing.map-rx-min}` and `{spacing.map-rx-max}`. The radius also shrinks until the widest topic label fits within `{spacing.page-margin}` of the edge. The vertical radius is `{spacing.map-ry-ratio}` × the map height below the bar, up to `{spacing.map-ry-max}`. Subfields are offset half a step so none sits directly above the center. Topics fan out on a `{spacing.topic-radius}` arc, `{spacing.topic-step}` apart, pointing horizontally away from the center. The `telemetry-readout` sits top-left, the `map-hint` bottom-right and the `scroll-cue` bottom-left.
- **Overview:** inside a `{spacing.container-max}` container, the sticky index (`{spacing.index-width}`) and the article (max `{spacing.article-max}`) sit `{spacing.index-gap}` apart. Sections are separated by `{spacing.section-gap}` and a hairline.
- **Resources:** groups sit `{spacing.group-gap}` apart; entries are full-width list rows.
- Desktop only. No mobile breakpoints.

## Elevation & Depth

The page is flat; it has no shadows. Depth comes from three things only: (1) the radial lift behind the map, (2) the glow (`{spacing.glow-blur}`) on subfield dots and highlighted lines, and (3) the translucent, blurred top bar. Fading through opacity (`{components.faded.opacity}`) pushes everything that isn't related to the hovered or focused node into the background.

## Shapes

Sharp corners everywhere (`{rounded.none}`): tags, rules, focus outlines. Circles are reserved for graph nodes (`{rounded.full}`). Topic markers are 6px squares, so topics read as a different kind of node from subfields at a glance.

## Components

The token values are in the frontmatter. These names are used identically in `EXPERIENCE.md`.

- **`node-root`:** a black disc with a white stroke and a faint outer ring, holding the area name in up to two lines.
- **`node-subfield`:** a glowing orange dot with its meta line above (`01 · 5 TOPICS · 9 SOURCES`) and its name below. When open, the dot grows, gains an orange ring, and the name turns orange. Keyboard focus shows a blue ring on its hit area.
- **`node-topic`:** a blue 6px square joined to its subfield by `edge-topic`, with its label on the side facing away from the subfield.
- **`edge-spoke`, `edge-link`, `edge-topic`:** solid, straight, 1px lines. Never dashed or dotted, never curved.
- **`telemetry-ring`:** ticks every 4°, major ticks every 40° labeled `000`–`320`. It rotates once every 140 seconds. Decorative.
- **`telemetry-readout`, `map-hint`, `scroll-cue`:** muted `label-meta` text at the map's corners.
- **`top-bar`:** the brand on the left, MAP / OVERVIEW / RESOURCES on the right. The active item is white with an underline.
- **`sticky-index-item`:** a muted number plus name with a 2px left rule. The active item is white with an orange rule and an orange number.
- **`section-heading` / `resource-group`:** an orange number plus an uppercase name, behind a 2px orange left rule.
- **`topics-line` / `connects-line`:** a muted label (TOPICS, CONNECTS TO) followed by white items. In `connects-line` the items are links that turn blue on hover.
- **`citation-link`:** blue inline text with an underline at 40% opacity.
- **`resource-entry`:** a list row in 3 columns: `type-tag`, the ABNT citation (title in bold, in `{colors.text}`), and OPEN ↗.
- **`footer`:** the generation stamp and ↑ BACK TO MAP.
- **`focus-outline`:** a 1px blue outline with a 4px offset on every focusable element.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Use orange only for subfields and blue only for interaction or what your action revealed | Add a third accent or give subfields different colors |
| Draw solid, straight lines; keep `edge-link` at `{colors.link-rest}` | Use dashed, dotted or curved lines, or fade links into the hairline color |
| Keep the black canvas almost empty | Add background guide circles, grids or textures (both were rejected) |
| Use uppercase, tracked Orbitron at 10px or more for labels | Set reading text in Orbitron, or set informative labels below 10px |
| Wrap long subfield names onto two lines and fit topic labels inside the viewport | Let labels run off-screen or overlap the center |
| Use glow sparingly (dots, highlighted lines) | Add drop shadows or glow on text |
