---
name: area-of-knowledge-expert
description: Maps a whole area of knowledge for someone starting to learn it. Given a field (math, robotics, economics, linguistics…), it runs a team of subagents that pick its main sub-fields and topics, research real academic sources for each one (textbooks, seminal papers, courses), write a gentle introduction to the field with ABNT citations, and produce an interactive visual map (MAP.html) opened in the browser. Use whenever I want to get oriented in a new field, ask "what is X made of", "map the field of X", "where do I start learning X", want a study map, reading list or overview of an area's sub-fields, even if I don't say "map". Don't use it for a single narrow topic or question (explaining one algorithm or concept), for a reading list on one paper or problem, or for planning study sessions.
---

# Area of Knowledge Expert

You orchestrate a small team that turns the name of a field into a study kit for a newcomer: what the field is made of, what to read, and a map to explore it. You're the only agent the user talks to. The work is done by subagents, each with its own brief in `agents/`, and a script builds the final page.

The run is fully automatic: once the area is clear, don't stop for approval between phases. The user expects to come back to a finished map.

## The pipeline

```
           ┌─ B Area Mapper ──────────► SUB_FIELDS.md
           │
A (you) ───┼─ C Resource Researcher ×N ─► <sub-field>/RESOURCES.md   (one per sub-field, in parallel)
           │
           ├─ D Overview Writer ───────► OVERVIEW.md                (reads the two above, cites the resources)
           │
           └─ E scripts/build_map.py ──► MAP.html → opened in the browser
```

The order matters. The overview cites the researchers' sources by id, so it is written after them. The map needs all three files.

Every output lives in one folder, `./<area-slug>/` in the current working directory (for example `./computer-science/`). Sub-field folders use the slug of the sub-field name (`algorithms-data-structures/`). A slug is lowercase ASCII, with accents removed and every run of other characters replaced by `-`.

`<skill-dir>` below means this skill's base directory, the absolute path you were given when the skill loaded. Subagents don't know it, so always pass absolute paths.

## Step 0 — Pin down the area

- Take the area from the request. If there is none, ask for it. That's the only question in a normal run.
- If it's a single topic rather than a field ("quicksort", "the French Revolution"), ask whether they want the field around it ("algorithms", "modern European history") or this topic mapped as if it were a field.
- Use the field's usual English name in title case ("Computer Science"). All generated content is in English, even if the user writes in another language, because the page's interface is in English.
- **If `./<area-slug>/` already exists**, ask once: *resume* (keep finished files, redo only what's missing), *start over* (delete the folder's generated files), or *use a new folder name*. If you can't ask (an unattended run), resume.

## Step 1 — Map the sub-fields (Agent B)

Spawn one `general-purpose` subagent:

```
You are the Area Mapper. Read <skill-dir>/agents/area-mapper.md and follow it.
Area: <Area Name>
Output path: <abs-area-dir>/SUB_FIELDS.md
Example to imitate: <skill-dir>/assets/examples/computer-science/SUB_FIELDS.md
```

When it returns, run `python3 <skill-dir>/scripts/build_map.py <area-dir> --check`. The sub-field list in its output is the parsed truth. Missing OVERVIEW/RESOURCES gaps are expected at this point. A FATAL here means SUB_FIELDS.md is unusable: send the mapper the error once, and if it fails again, stop and tell the user.

## Step 2 — Research resources (Agent C, one per sub-field)

Spawn **all researchers in a single message** so they run in parallel, one `general-purpose` subagent per sub-field:

```
You are a Resource Researcher. Read <skill-dir>/agents/resource-researcher.md and follow it.
Citation rules: <skill-dir>/references/abnt.md
Area: <Area Name>
Sub-field: <Sub-field Name>
Scope: <its one-line description>
Topics: <topic>; <topic>; <topic>; <topic>; <topic>
Output path: <abs-area-dir>/<sub-field-slug>/RESOURCES.md
Example to imitate: <skill-dir>/assets/examples/computer-science/algorithms-data-structures/RESOURCES.md
```

Use the slugs exactly as `--check` printed them as ids, so the folders match what the script expects. When resuming, only spawn researchers for sub-fields whose RESOURCES.md is missing.

When they're all back, run `--check` again and look at the FIXES and GAPS:
- Entries dropped for a missing citation, or a file that parsed to far fewer sources than the researcher reported, mean the format went wrong. Re-run that one researcher once and quote the script's complaint.
- A sub-field with no sources is acceptable when the researcher says nothing citable exists. The page has a state for it. Note it for the final report.

Don't read the RESOURCES.md files into your own context to check them. The script and the researchers' short replies are enough, and the files are long.

## Step 3 — Write the overview (Agent D)

Spawn one `general-purpose` subagent:

```
You are the Overview Writer. Read <skill-dir>/agents/overview-writer.md and follow it.
Citation rules: <skill-dir>/references/abnt.md
Area directory: <abs-area-dir>  (contains SUB_FIELDS.md and each <sub-field>/RESOURCES.md)
Output path: <abs-area-dir>/OVERVIEW.md
Example to imitate: <skill-dir>/assets/examples/computer-science/OVERVIEW.md
```

Run `--check` again. Fix small problems yourself with targeted edits to OVERVIEW.md: a citation pointing at the wrong id, a misspelled sub-field name in a heading or a **Connects to** line, or a missing **Connects to** line. Re-run the writer once only if whole sections are missing.

## Step 4 — Build and open the map (Agent E)

```bash
python3 <skill-dir>/scripts/build_map.py <area-dir> --open
```

The script is Agent E. It parses the three kinds of file, applies the validation rules from the page's data contract (at most 6 sub-fields and 5 topics, unique ids, valid links and citations, no empty sections), serializes the data with a real JSON encoder with `</` escaped, writes it into a copy of `assets/knowledge-map-template.html` without touching anything else, checks that the result parses back, and opens it (WSL, macOS, Windows and Linux are handled). It prints every fix it made and every gap it found.

Don't hand-edit MAP.html or the template. If the page is wrong, fix the markdown and run the script again, so the markdown stays the source of truth.

## Step 5 — Report to the user

Keep it short:

- The path to `MAP.html`, and whether it opened. If not, give the path so they can open it themselves.
- The counts: sub-fields, topics, sources, links.
- One "start here" pointer per sub-field: the first resource each researcher recommended.
- Anything worth knowing: sub-fields with no sources, branches the mapper left out, and fixes the script applied that changed content (fixes that only tidied ids aren't worth mentioning).

## If something fails

- **A subagent fails or returns nothing:** retry it once with the same prompt. If it fails again, carry on. The script turns a missing RESOURCES.md into "No sources found" and a missing overview section into the SUB_FIELDS.md description. Report the gap.
- **No web search available:** the researchers can't verify sources, so say so before starting. Unverified citations defeat the purpose, so don't let them cite from memory.
- **The script exits with FATAL:** it means SUB_FIELDS.md is missing or empty, or the template is broken. Nothing is written in that case. Fix the cause and run it again.

## Files in this skill

| Path | What it is | Who reads it |
|---|---|---|
| `agents/area-mapper.md` | Brief for Agent B | the mapper subagent |
| `agents/resource-researcher.md` | Brief for Agent C | each researcher subagent |
| `agents/overview-writer.md` | Brief for Agent D | the writer subagent |
| `references/abnt.md` | ABNT reference and in-text citation rules, resource ids | C and D |
| `scripts/build_map.py` | Agent E: validate, encode, inject, verify, open | you run it |
| `assets/knowledge-map-template.html` | The finished page design. Only its `km-data` JSON changes per area | the script |
| `assets/examples/computer-science/` | A complete example of every markdown file. It is also a test fixture: `build_map.py` on a copy of it must report no fixes or gaps | B, C, D |
| `references/design/` | `DESIGN.md` (visual identity) and `EXPERIENCE.md` (behavior and data contract) of the page | only someone changing the page itself; not needed for a run |
