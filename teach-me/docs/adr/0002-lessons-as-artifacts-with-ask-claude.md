# Lessons are published as Claude Artifacts with an Ask Claude panel

Each Lesson page is built as an Artifact fragment and published with the Artifact tool, declaring the `sample` capability. The page has an **Ask Claude** panel: the Learner asks questions while reading, and Claude answers with the Lesson's text, objectives, references and Practice state as context. We chose this because questions come up while reading, and a local HTML file sent the Learner back to the terminal to ask them.

## Considered Options

- **Local HTML file opened in the browser** (the previous approach): no account needed, but questions about the material mean switching to the chat and describing what they were reading.
- **Artifact without `sample`**: a shareable link, but still no way to ask from the page.
- **Artifact with `sample`**: questions are answered in place, on the Learner's own Claude account, with the whole Lesson as context.

## Consequences

- Before the Practice is submitted, the panel's instructions forbid revealing Practice answers and allow only hints. After submission it may explain every question. The answer key still ships in the page, as in ADR 0001.
- Practice still returns by paste-back (ADR 0001). The Check writes files in the Course folder, which a page can't do.
- The Ask Claude conversation lives in the Learner's browser storage only. It never reaches the Check or the memory, so ask the Learner in the chat if their questions matter for the Check.
- The template must follow the Artifact page contract: no `<html>`/`<head>`/`<body>`, themed tokens with `data-theme` guards, no `confirm()`/`alert()`, no network fetches. Mermaid is rendered by the viewer.
- `build_lesson.py --open` still writes a standalone page for when the Artifact tool isn't available. There the panel stays hidden.
