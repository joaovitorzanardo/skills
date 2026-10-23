# Writing a Lesson

Contents: 1. What a good Lesson does · 2. Visuals and interactive widgets · 3. Sources and citations · 4. Practice · 5. Remedial Lessons · 6. File formats (content.html, practice.json) · 7. Syllabus

## 1. What a good Lesson does

A Lesson is 15–25 minutes of reading plus 5–10 Practice questions, and it can be finished in one sitting. Small Lessons get finished, and a finished Lesson teaches more than a thorough one left half-read.

Teach for understanding, keeping the technical terms and making the reading pleasant. The habits below come from what learning research consistently supports. Each one has a reason, so adapt them to the Topic instead of applying them mechanically.

- **Open with the why.** Start with one short paragraph that connects the Lesson to the Learner's Goal ("to make your drone hover, the flight controller has to…"). Motivation is what gets a Lesson read.
- **One big idea per Lesson,** with 2–4 concepts that serve it. If you need more, split the Lesson.
- **Build on what they know.** Use the Diagnostic results: skip what's Solid, briefly refresh what's Shaky, and teach what's Missing from scratch. New ideas stick when they attach to old ones.
- **Concrete before abstract.** Show a specific case, a picture or a number first, and only then the general rule or formula. The formula then names something they've already seen.
- **Worked examples.** For anything procedural (a calculation, a derivation, a design step), show a fully worked example, then a second one with steps left for the reader in a `details.think` block. This is the fastest way to build skill in a novice.
- **Analogies, with their limits.** A good analogy is a scaffold. Say where it breaks ("unlike water, electrons…"), or it becomes a misconception later.
- **Name the misconceptions.** If there's a classic wrong idea, state it and show why it's wrong (`.callout.warn`). Ignoring a misconception doesn't remove it.
- **Make them predict.** Before revealing a result, ask the reader to guess (`details.think`). Committing to a guess, even a wrong one, makes the answer memorable.
- **Define terms on first use** with `<dfn>`, and use them consistently afterwards.
- **End with a short summary** of 3–5 bullets that match the Practice concepts, then a pointer to the Practice.

Write in the Learner's language, at the Profile's level. Keep the technical terms, and for a non-English Lesson give the English term in parentheses the first time, since that's what the Learner will search for.

## 2. Visuals and interactive widgets

Use visuals whenever a picture explains faster than prose. That means most Lessons need at least one diagram, and any concept with a parameter to vary should get a widget.

- **Diagrams:** inline `<svg>` inside a `<figure>` with a `<figcaption>`. Use the theme variables (`var(--accent)`, `var(--text)`, `var(--line)`, `var(--muted)`, `var(--accent-2)`) instead of fixed colours so it works in light and dark mode. Use a `viewBox` and no fixed width so it scales on a phone.
- **Mental models:** a labelled box-and-arrow sketch of how the parts relate. Mermaid is fine for flowcharts (`<pre class="mermaid">`, with `"mermaid"` added to `libraries`).
- **Interactive widgets:** a `<div class="widget">` with sliders, buttons and a live SVG or canvas, driven by a small `<script>` placed right after it. Good widgets let the Learner *change one thing and see the effect*: move the resistor slider and watch the current, drag the learning rate and watch the loss curve diverge. Pair the widget with a prompt ("set R so the LED gets 20 mA").
  - Keep each script self-contained: wrap it in an IIFE and select elements by id with a prefix unique to the widget.
  - Plain JS and SVG are usually enough. Add `"d3"` or `"chartjs"` to `libraries` only when the plot genuinely needs it.
- **Math:** write `\( … \)` inline and `\[ … \]` for display, and add `"katex"` to `libraries`.
- **Code:** `<pre><code>…</code></pre>`, short and runnable.

Available libraries (the build script pins their versions): `katex`, `mermaid`, `d3`, `chartjs`. Inline SVG and JS need no library. `d3` and `chartjs` load before the content, so widget scripts can call `d3` or `new Chart(…)` directly. KaTeX and Mermaid render automatically after the page loads, including inside Practice questions.

## 3. Sources and citations

Every Lesson cites real, findable sources, and its references list them at the end with links.

- **Research with web search in this Session,** and cite only what you found. Check that the title, authors and year match what you cite. If you can't verify a source, don't use it.
- **Use trusted sources for the kind of Topic:**
  - Established subjects: standard textbooks, seminal papers, university courses (e.g. MIT OCW), reference docs.
  - Fast-moving subjects (AI tooling, frameworks, workflows): official docs, recent posts by practitioners, conference talks, well-regarded YouTube explainers. Prefer the last 1–2 years and note the date.
  - Matters of preference (workflows, style): cite several viewpoints and say that they're viewpoints.
- **3–8 references per Lesson.** Cite each one in the text where its idea is used, the way academic work does. A reference list with nothing cited in the text doesn't count.
- **Format:** follow `abnt.md` for the reference entries and in-text citations. In `content.html`, each in-text citation is a link:
  ```html
  <a class="cite" href="#ref-cormen2022">(CORMEN et al., 2022)</a>
  ```
  The `id` must match a reference in `practice.json`. The build script rejects links that don't resolve and warns about references that are never cited.

## 4. Practice

The Practice is how both of you find out whether the Lesson worked, so design it to measure understanding.

- **5–10 questions:** mostly multiple choice, plus 1–2 written questions when explaining in their own words is the real test.
- **Every core concept gets at least one question,** because the pass rule needs one fully correct answer per core concept. Two questions per core concept, from different angles, give a fairer verdict.
- **Application over recall.** Ask them to predict, calculate, diagnose a wrong statement, or choose between approaches. "Which is the definition of X" is the weakest kind of question.
- **Distractors come from real misconceptions,** ideally the ones the Lesson named. A distractor nobody would pick is wasted.
- **3–4 options.** Don't make "all of the above" the answer, and don't give the right answer away by making it the longest.
- **The explanation** for each multiple-choice question says why the right answer is right *and* why the tempting wrong one is wrong. It's shown after they submit, and it's teaching too.
- **Written questions need a `model_answer` and a `rubric`.** The rubric says what earns 1 point, 0.5 and 0, so your later grading is consistent and fair.
- **Interactive tasks:** a question can refer to a widget in the Lesson ("Using the simulator above, what happens when…") as long as the answer is a choice or a short text.

## 5. Remedial Lessons

A Remedial Lesson (`lesson-NN-remedial-K`) teaches only the concepts the Check found missing. Repeating the same explanation louder rarely works, so change the approach:

- **Start from their actual mistake.** Quote their wrong answer pattern ("you picked B on both questions, which suggests…") and fix that mental model directly.
- **Use a different angle:** a new analogy, a different diagram, more and smaller worked examples, or a widget if the first Lesson had none.
- **Make it shorter** than a full Lesson: 8–15 minutes.
- **Write new Practice questions** that use the same concept ids but are new questions. Repeated questions test memory of the answer, not understanding.
- After a talk-it-through in the chat (second failure), the Remedial Lesson can be just a short recap section plus 3–5 questions.

## 6. File formats

### `src/<lesson-id>/content.html`

This is an HTML fragment (no `<html>`, `<head>` or `<body>`). The template supplies the header, title, objectives, table of contents, Practice and references. You write only the teaching. Structure it as `<section>` elements, each starting with an `<h2>`; the table of contents is built from the `<h2>`s. The building blocks are:

```html
<section>
  <h2>Why the current doesn't get "used up"</h2>
  <p>A <dfn>circuit</dfn> is …, as Ohm described <a class="cite" href="#ref-hayt2012">(HAYT; KEMMERLY; DURBIN, 2012)</a>.</p>

  <div class="callout key"><p><b>Key idea.</b> …</p></div>
  <div class="callout analogy"><p><b>Analogy.</b> … <em>Where it breaks:</em> …</p></div>
  <div class="callout warn"><p><b>Common mistake.</b> …</p></div>
  <div class="callout example"><p><b>Worked example.</b> …</p></div>

  <details class="think"><summary>Predict first: what happens if R doubles?</summary><p>…</p></details>

  <figure><svg viewBox="0 0 400 160" role="img" aria-label="…">…</svg><figcaption>Figure 1. …</figcaption></figure>

  <div class="widget" id="ohm-w">
    <label>R = <output id="ohm-r-out">100</output> Ω <input id="ohm-r" type="range" min="10" max="1000" value="100"></label>
    <svg id="ohm-svg" viewBox="0 0 400 120"></svg>
  </div>
  <script>(() => { const r = document.getElementById('ohm-r'); /* … */ })();</script>
</section>
```

### `src/<lesson-id>/practice.json`

```json
{
  "version": 1,
  "course": "pcb-design",
  "topic": "PCB design",
  "lesson": "lesson-01",
  "kind": "lesson",
  "title": "Circuits before boards: voltage, current and Ohm's law",
  "language": "pt-BR",
  "minutes": 20,
  "libraries": ["katex"],
  "objectives": ["Explain what voltage and current are", "Use Ohm's law to size a resistor"],
  "concepts": [
    {"id": "ohms-law", "name": "Ohm's law", "core": true},
    {"id": "series-parallel", "name": "Series and parallel resistors", "core": true},
    {"id": "units", "name": "Units and prefixes", "core": false}
  ],
  "questions": [
    {"id": "q1", "concept": "ohms-law", "type": "mc",
     "prompt": "A 5 V supply drives a 250 Ω resistor. What current flows?",
     "options": ["20 mA", "50 mA", "1.25 A", "It depends on the wire length"],
     "answer": 0,
     "explanation": "I = V/R = 5/250 = 0.02 A = 20 mA. 1.25 A comes from multiplying instead of dividing."},
    {"id": "q6", "concept": "series-parallel", "type": "written",
     "prompt": "Explain why adding a second resistor in parallel lowers the total resistance.",
     "model_answer": "Each branch gives current another path, so for the same voltage the total current rises, which means a lower equivalent resistance.",
     "rubric": "1: mentions extra path and more total current for the same voltage. 0.5: right conclusion, vague reason. 0: says resistance adds up or no reason."}
  ],
  "references": [
    {"id": "hayt2012", "citation": "HAYT, W. H.; KEMMERLY, J. E.; DURBIN, S. M. **Engineering circuit analysis**. 8. ed. New York: McGraw-Hill, 2012.", "url": "https://..."}
  ]
}
```

Field rules (the build script enforces them):
- `lesson` matches the folder name. `kind` is `lesson` or `remedial`. `course` is the Course folder's slug.
- Concept `id`s are kebab-case and unique. Keep the same concept id for the same concept across Lessons and Remedial Lessons, because it's how the history of a concept is tracked.
- Question `id`s are `q1`, `q2`, … in order. `answer` is the 0-based index of the correct option.
- `prompt`, `options` and `explanation` may contain inline HTML (`<code>`, `\( math \)`). The Learner's answers are always shown as plain text.
- `citation` uses `**bold**` for the part ABNT makes bold. `url` is optional but strongly preferred.

## 7. Syllabus

`SYLLABUS.md` at the root of the Course. Update the status column after every Check, and log every change of plan under "Changes".

```markdown
# PCB design: Syllabus

goal: build a small LED driver board for my bike
language: pt-BR
started: 2026-10-23

## Starting point

- Solid: basic algebra, units
- Shaky: series vs parallel
- Missing: Ohm's law intuition, reading datasheets, schematic symbols

## Lessons

| # | Lesson | Concepts | Status |
|---|---|---|---|
| 01 | Circuits before boards | ohms-law, series-parallel, units | passed: 2026-10-24, 90% |
| 02 | Reading a schematic | schematic-symbols, nets | current |
| 03 | Components and datasheets | … | planned |

## Optional, later

- High-speed signal integrity (not needed for this board)

## Changes

- 2026-10-26: added lesson-02-remedial-1 for nets (2 misses)
```
