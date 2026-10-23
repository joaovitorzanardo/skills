## Memory retrieval and organization

All learning memory lives in `~/.study-memory/` as markdown files. You have no vector database. You retrieve memory with your file tools: Glob to find files by name, Grep to search contents, and Read to open them. Follow these rules so retrieval stays fast and accurate as the number of topics and sessions grows.

Memory has two layers:

- **Consolidated layer** (`progress.md`, `areas/`, `topics/`): the current state of what the learner knows. It's small, kept up to date, and read first.
- **Session journal** (`sessions/`): one dated file per study session, recording what happened that day. It's append-only and read only when the raw details are needed.

### Layout

```
~/.study-memory/
├── profile.md                      # learner profile, always read (keep under ~40 lines)
├── progress.md                     # top-level index, always read
├── areas/<area>.md                 # topic tables per area (only once the index is split)
├── topics/<slug>.md                # consolidated notes per topic, read on demand
├── sessions/YYYY-MM-DD-<slug>.md   # one journal entry per session, read only when needed
└── archive.md                      # mastered, inactive topics, read only when needed
```

Slugs and area names are lowercase-kebab-case. A session file is named after the main topic's slug, e.g. `sessions/2026-10-22-neural-networks.md`. If there is a second session on the same topic and day, add a suffix: `2026-10-22-neural-networks-2.md`.

### Index format

While there are fewer than 100 active topics, `progress.md` is one flat table:

```markdown
| Topic | Slug | Area | Keywords | Mastery (1-5) | Last studied | Next step |
| ----- | ---- | ---- | -------- | ------------- | ------------ | --------- |
```

Once the table passes 100 rows, split it. Rewrite `progress.md` as a short list of areas, with one line each: name, file, topic count and a one-line description. Move each area's rows into `areas/<area>.md`, keeping the same table format. Tell the learner in one line that you reorganized the index. From then on, add new topics to the matching area file, and create a new area only when no existing one fits.

### Topic file format

```markdown
# Neural networks

keywords: neural networks, deep learning, backpropagation, gradient descent, learning rate, training
course: /absolute/path/to/neural-networks
goal: <why the learner is studying this, in their words>
Related: linear-algebra, python-numpy

## What the learner knows

- <concept> — <one-line takeaway in the learner's terms>

## Weak spots

- <concept they still struggle with, and why>

## Next steps

- <what to study next>

## Sessions

- 2026-10-22: trained a first network, backprop still unclear — 2/3 correct
```

This file holds the current truth. When a later session shows a weak spot has been overcome, move it to "What the learner knows" instead of keeping both versions.

### Session file format

```markdown
# 2026-10-22 — Neural networks

topic: neural-networks
keywords: backpropagation, learning rate, loss function, overfitting
check: 2/3 correct

## Covered

- <what was explained or practiced, in a few bullets>

## Struggled with

- <specific difficulties and mistakes>

## Learner's questions

- <questions they asked, especially ones left open>
```

Session keywords list the specific subtopics covered that day, so Grep can find them even though the filename only names the main topic. Never edit a session file after the session ends.

### Keywords

Every topic has a keywords line in its index row and at the top of its topic file, and every session file has one too. Include 4-8 keywords: the topic's own terms, common synonyms, the parent concept and the terms a learner might use to ask about it. Update topic keywords whenever a session reveals new subtopics or new ways the learner refers to the topic. Keywords are what make keyword search work, so never skip them.

### Retrieval procedure

When the learner asks about a topic:

1. Read `profile.md` and `progress.md`.
2. If the index is split, pick the most relevant area and read only that area file. Read a second area only if the topic plausibly spans both.
3. Look for a match in the index, judging by meaning, not just exact text. Check the Topic and Keywords columns.
4. If nothing matches, search before concluding the topic is new. Grep `topics/` (case-insensitive) for the topic name plus 2-3 synonyms or related terms, then grep `archive.md` the same way.
5. If a semantic search tool over `~/.study-memory/` is available, use it only when steps 3-4 find nothing.
6. Read at most 2 topic files: the best match and, if useful, one item from its `Related:` line. Don't open files speculatively.
7. Open session files only when the topic file isn't enough, for example when the learner asks what happened in a specific session ("what did we do last Tuesday?") or you need the exact details of a past difficulty. Find them with Glob (`sessions/*<slug>*` for a topic, `sessions/YYYY-MM-*` for a period) or Grep for a subtopic. Read the fewest needed, newest first.
8. If nothing is found after these steps, treat it as a new topic and create its files and index row at the end of the session.

For questions about time ("what did I study this month?"), list `sessions/` with Glob and use the filenames; open files only if the learner wants details.

### End-of-session update

Write memory in this order, so the journal is saved even if the rest fails:

1. **Create the session file** in `sessions/`.
2. **Update the topic file**: merge what was learned, resolve weak spots that are now overcome, update next steps and keywords, and add a one-line entry under "Sessions".
3. **Update the index row**: mastery (based on check results, not on how much was covered), last studied, next step and keywords.
4. **Update `profile.md`** only if the learner stated a preference or a clear pattern emerged. Ask before saving anything you inferred.

Tell the learner in one line what you saved.

### Archiving

A topic is moved to `archive.md` when it reaches mastery 5 and hasn't been studied for 90 days. Move its index row there (same table format) and keep its topic file and session files where they are. If an archived topic comes up again, move its row back into the active index. Archive topics only during the end-of-session update, and mention it in one line.

### Keeping memory clean

- Never create a duplicate topic. If a near-match exists, update it, or add the new topic and link both through `Related:`.
- The topic file is a summary, not a log. Keep detail in session files. When a topic file's "Sessions" list passes ~20 entries, condense the oldest into one line (e.g. "2026-01 to 2026-03: 12 sessions on fundamentals"); the session files themselves remain.
- If the index row and the topic file disagree, the topic file wins: fix the row. If the topic file and an old session file disagree, the topic file wins: it reflects later sessions.
