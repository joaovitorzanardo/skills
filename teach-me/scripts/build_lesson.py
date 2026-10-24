#!/usr/bin/env python3
"""Build one teach-me Lesson page.

Reads  <course>/src/<lesson-id>/practice.json and content.html,
checks them, fills assets/lesson-template.html, and writes <course>/<lesson-id>.html.

The page is an Artifact fragment (no <html>/<head>/<body>): publish it with the Artifact tool
and capabilities {"sample": {}} so the Learner can ask Claude about it from inside the page.
--standalone wraps it in a full document instead, for opening in a plain browser when the
Artifact tool isn't available (the Ask Claude panel then stays hidden). --open implies it.

  python3 build_lesson.py <course-dir> <lesson-id> [--standalone] [--open] [--check]

Exit code 0 = built (warnings may be printed), 1 = errors (nothing written).
"""
import argparse
import base64
import html
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "lesson-template.html"
# Page title words, matching the UI languages in the template.
TITLE_WORDS = {"en": ("Lesson", "review"), "pt": ("Lição", "revisão")}

# The same skeleton the Artifact tool adds at publish time, for --standalone pages.
STANDALONE = ('<!doctype html><html><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
              '</head><body>\n{page}\n</body></html>\n')

HANDS_ON_LEVELS = ("guided", "scaffolded", "independent")
LESSON_ID = re.compile(r"^lesson-(\d{2})(?:-remedial-(\d+))?$")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Pinned versions. d3 and chartjs load synchronously because widget scripts in the
# content run while the page parses; katex only runs after the page loads.
# Mermaid loads nothing: the Artifact viewer renders <pre class="mermaid"> blocks natively.
LIBRARIES = {
    "katex": [
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">',
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>',
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>',
    ],
    "mermaid": [],
    "d3": ['<script src="https://cdn.jsdelivr.net/npm/d3@7.8.5/dist/d3.min.js"></script>'],
    "chartjs": ['<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>'],
}


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def nonempty_str(v):
    return isinstance(v, str) and v.strip() != ""


def citation_html(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(text, quote=False))


def validate_hands_on(ho, questions, rep):
    """The optional hands-on exercise, done in a real tool or on paper outside the page."""
    flagged = [q.get("id") for q in questions if isinstance(q, dict) and q.get("hands_on")]
    if ho is None:
        if flagged:
            rep.err(f"questions {flagged} are marked hands_on but the Lesson has no hands_on exercise")
        return
    if not isinstance(ho, dict):
        rep.err("practice.json: hands_on must be an object")
        return
    for f in ("title", "tool", "goal", "deliverable"):
        if not nonempty_str(ho.get(f)):
            rep.err(f"hands_on: '{f}' is missing or empty")
    level = ho.get("level")
    if level not in HANDS_ON_LEVELS:
        rep.err(f"hands_on: level must be one of {list(HANDS_ON_LEVELS)}")
    minutes = ho.get("minutes")
    if not isinstance(minutes, int) or isinstance(minutes, bool) or minutes <= 0:
        rep.err("hands_on: minutes must be a positive integer")
    elif minutes > 60:
        rep.warn(f"hands_on: {minutes} minutes is long; split it, or move part of it to the next Lesson")
    for f in ("setup", "acceptance"):
        v = ho.get(f, [])
        if not isinstance(v, list) or not all(nonempty_str(x) for x in v):
            rep.err(f"hands_on: {f} must be a list of strings")
    steps = ho.get("steps", [])
    if not isinstance(steps, list):
        rep.err("hands_on: steps must be a list")
        steps = []
    for i, st in enumerate(steps, 1):
        if not isinstance(st, dict) or not nonempty_str(st.get("do")):
            rep.err(f"hands_on step {i}: 'do' is missing or empty")
            continue
        if level in ("guided", "scaffolded") and not nonempty_str(st.get("check")):
            rep.err(f"hands_on step {i}: {level} steps need a 'check' (what the Learner should see when it worked)")
        for f in ("check", "hint"):
            if f in st and not nonempty_str(st[f]):
                rep.err(f"hands_on step {i}: '{f}' is empty")
    if level == "guided" and len(steps) < 5:
        rep.warn(f"hands_on: a guided exercise with {len(steps)} step(s) is probably skipping clicks; aim for 5-20")
    if level == "scaffolded" and not 3 <= len(steps) <= 10:
        rep.warn(f"hands_on: {len(steps)} scaffolded steps; aim for 3-10")
    if level == "independent" and len(ho.get("acceptance") or []) < 2:
        rep.err("hands_on: an independent exercise needs at least 2 acceptance criteria")
    if level in ("guided", "scaffolded") and not steps:
        rep.err(f"hands_on: a {level} exercise needs steps")
    if not flagged:
        rep.err("hands_on: mark at least one question \"hands_on\": true, answerable only by doing the exercise")


def validate(course_dir, lesson_id, data, content, rep):
    m = LESSON_ID.match(lesson_id)
    if not m:
        rep.err(f"lesson id '{lesson_id}' must look like lesson-02 or lesson-02-remedial-1")
        return
    is_remedial = m.group(2) is not None

    if data.get("version") != 1:
        rep.err("practice.json: version must be 1")
    if data.get("lesson") != lesson_id:
        rep.err(f"practice.json: lesson is '{data.get('lesson')}', expected '{lesson_id}' (the folder name)")
    if data.get("course") != course_dir.name:
        rep.err(f"practice.json: course is '{data.get('course')}', expected '{course_dir.name}' (the Course folder name)")
    kind = data.get("kind")
    if kind not in ("lesson", "remedial"):
        rep.err("practice.json: kind must be 'lesson' or 'remedial'")
    elif (kind == "remedial") != is_remedial:
        rep.err(f"practice.json: kind '{kind}' doesn't match lesson id '{lesson_id}'")
    for f in ("title", "topic", "language"):
        if not nonempty_str(data.get(f)):
            rep.err(f"practice.json: '{f}' is missing or empty")
    minutes = data.get("minutes")
    if not isinstance(minutes, int) or minutes <= 0:
        rep.err("practice.json: minutes must be a positive integer")
    elif not (8 if is_remedial else 12) <= minutes <= 25:
        rep.warn(f"minutes = {minutes}: aim for 15-25 (Lesson) or 8-15 (Remedial Lesson)")
    objectives = data.get("objectives")
    if not isinstance(objectives, list) or not objectives or not all(nonempty_str(o) for o in objectives):
        rep.err("practice.json: objectives must be a non-empty list of strings")

    libs = data.get("libraries", [])
    if not isinstance(libs, list) or any(l not in LIBRARIES for l in libs):
        rep.err(f"practice.json: libraries must be a list drawn from {sorted(LIBRARIES)}")
        libs = []
    if ("\\(" in content or "\\[" in content) and "katex" not in libs:
        rep.warn("content uses \\( or \\[ math but 'katex' is not in libraries")
    if re.search(r"\bd3\.", content) and "d3" not in libs:
        rep.warn("content uses d3 but 'd3' is not in libraries")
    if re.search(r"\bnew Chart\(", content) and "chartjs" not in libs:
        rep.warn("content uses Chart.js but 'chartjs' is not in libraries")

    # concepts
    concepts = data.get("concepts")
    cids = set()
    if not isinstance(concepts, list) or not concepts:
        rep.err("practice.json: concepts must be a non-empty list")
        concepts = []
    for c in concepts:
        cid = c.get("id") if isinstance(c, dict) else None
        if not isinstance(cid, str) or not KEBAB.match(cid):
            rep.err(f"concept id {cid!r} must be kebab-case")
            continue
        if cid in cids:
            rep.err(f"concept id '{cid}' is duplicated")
        cids.add(cid)
        if not nonempty_str(c.get("name")):
            rep.err(f"concept '{cid}' has no name")
        if not isinstance(c.get("core"), bool):
            rep.err(f"concept '{cid}': core must be true or false")
    core = {c["id"] for c in concepts if isinstance(c, dict) and c.get("core") is True}
    if concepts and not core:
        rep.err("at least one concept must be core: the pass rule is built on core concepts")

    # questions
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        rep.err("practice.json: questions must be a non-empty list")
        questions = []
    lo, hi = (3, 10) if is_remedial else (5, 10)
    if questions and not lo <= len(questions) <= hi:
        rep.warn(f"{len(questions)} questions: aim for {lo}-{hi}")
    practised = {}
    for i, q in enumerate(questions, 1):
        if not isinstance(q, dict):
            rep.err(f"question #{i} is not an object")
            continue
        qid = q.get("id")
        where = f"question {qid or '#' + str(i)}"
        if qid != f"q{i}":
            rep.err(f"{where}: ids must be q1, q2, ... in order (expected q{i})")
        if q.get("concept") not in cids:
            rep.err(f"{where}: concept {q.get('concept')!r} is not in concepts")
        if not nonempty_str(q.get("prompt")):
            rep.err(f"{where}: prompt is empty")
        t = q.get("type")
        if t == "mc":
            opts = q.get("options")
            if not isinstance(opts, list) or not 2 <= len(opts) <= 5 or not all(nonempty_str(o) for o in opts):
                rep.err(f"{where}: options must be 2-5 non-empty strings")
            elif not isinstance(q.get("answer"), int) or isinstance(q.get("answer"), bool) or not 0 <= q["answer"] < len(opts):
                rep.err(f"{where}: answer must be the 0-based index of an option")
            if not nonempty_str(q.get("explanation")):
                rep.err(f"{where}: explanation is empty (it is shown after submitting, and it teaches)")
            full = 1
        elif t == "written":
            for f in ("model_answer", "rubric"):
                if not nonempty_str(q.get(f)):
                    rep.err(f"{where}: written questions need a {f}")
            full = 1
        else:
            rep.err(f"{where}: type must be 'mc' or 'written'")
            full = 0
        if full and q.get("concept") in cids:
            practised[q["concept"]] = practised.get(q["concept"], 0) + 1
    validate_hands_on(data.get("hands_on"), questions, rep)
    for cid in sorted(core - practised.keys()):
        rep.err(f"core concept '{cid}' has no question: the pass rule needs at least one per core concept")
    for cid in sorted(cids - core - practised.keys()):
        rep.warn(f"concept '{cid}' has no question")

    # references and citations
    refs = data.get("references")
    rids = set()
    if not isinstance(refs, list):
        rep.err("practice.json: references must be a list")
        refs = []
    for r in refs:
        rid = r.get("id") if isinstance(r, dict) else None
        if not isinstance(rid, str) or not re.match(r"^[a-z0-9]+$", rid):
            rep.err(f"reference id {rid!r} must be lowercase letters and digits, e.g. cormen2022")
            continue
        if rid in rids:
            rep.err(f"reference id '{rid}' is duplicated")
        rids.add(rid)
        if not nonempty_str(r.get("citation")):
            rep.err(f"reference '{rid}' has no citation")
        url = r.get("url")
        if url is not None and not (isinstance(url, str) and re.match(r"^https?://", url)):
            rep.err(f"reference '{rid}': url must start with http:// or https://")
        elif not url:
            rep.warn(f"reference '{rid}' has no url")
    if len(refs) < 3 and not is_remedial:
        rep.warn(f"{len(refs)} reference(s): a Lesson should cite 3-8 real sources")
    cited = set(re.findall(r'href="#ref-([^"]+)"', content))
    for rid in sorted(cited - rids):
        rep.err(f"content cites #ref-{rid} but there is no reference with id '{rid}'")
    for rid in sorted(rids - cited):
        rep.warn(f"reference '{rid}' is never cited in the content")

    # content shape
    if re.search(r"<\s*(html|head|body)\b", content, re.I):
        rep.err("content.html must be a fragment: no <html>, <head> or <body>")
    if "__TM_" in content:
        rep.err("content.html must not contain __TM_ markers")
    if not re.search(r"<section\b[^>]*>\s*<h2\b", content):
        rep.warn("content has no <section><h2>…: the table of contents is built from section headings")


def build(course_dir, lesson_id, data, content):
    m = LESSON_ID.match(lesson_id)
    meta = {
        "title": data["title"],
        "topic": data["topic"],
        "lesson": lesson_id,
        "number": m.group(1),
        "kind": data["kind"],
        "minutes": data["minutes"],
        "language": data["language"],
        "objectives": data["objectives"],
        "references": [
            {"id": r["id"], "citation_html": citation_html(r["citation"]), "url": r.get("url")}
            for r in data.get("references", [])
        ],
    }
    practice = {"course": data["course"], "lesson": lesson_id, "questions": data["questions"],
                "hands_on": data.get("hands_on")}
    encoded = base64.b64encode(json.dumps(practice, ensure_ascii=False).encode("utf-8")).decode("ascii")
    libs = "\n".join(tag for name in data.get("libraries", []) for tag in LIBRARIES[name])
    lesson_w, review_w = TITLE_WORDS.get(data["language"][:2].lower(), TITLE_WORDS["en"])
    number = f"{lesson_w} {m.group(1)}" + (f" {review_w} {m.group(2)}" if m.group(2) else "")
    values = {
        "TITLE": html.escape(f"{data['topic']} · {number}"),
        "LIBS": libs,
        "META": json.dumps(meta, ensure_ascii=False).replace("</", "<\\/"),
        "PRACTICE": encoded,
        "CONTENT": content,
    }
    template = TEMPLATE.read_text(encoding="utf-8")
    seen = []

    def sub(mt):
        key = mt.group(1) or mt.group(2)
        seen.append(key)
        return values[key]

    # One pass, so text inserted for one marker is never scanned for another.
    out = re.sub(r"<!--__TM_(LIBS|CONTENT)__-->|__TM_(TITLE|META|PRACTICE)__", sub, template)
    missing = set(values) - set(seen)
    if missing:
        raise RuntimeError(f"template is missing markers: {sorted(missing)}")
    return out


def open_in_browser(path):
    path = path.resolve()
    try:
        if "microsoft" in platform.uname().release.lower() and shutil.which("wslpath"):
            win = subprocess.run(["wslpath", "-w", str(path)], capture_output=True, text=True).stdout.strip()
            subprocess.run(["explorer.exe", win], check=False)  # explorer.exe exits 1 even on success
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=True)
        elif os.name == "nt":
            os.startfile(str(path))  # noqa: B606
        elif shutil.which("xdg-open"):
            subprocess.run(["xdg-open", str(path)], check=True)
        elif not webbrowser.open(path.as_uri()):
            return False
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("course_dir", type=Path)
    ap.add_argument("lesson_id")
    ap.add_argument("--standalone", action="store_true", help="write a full HTML document for a plain browser, not an Artifact")
    ap.add_argument("--open", action="store_true", help="write a standalone page and open it in the default browser")
    ap.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = ap.parse_args()

    course_dir = args.course_dir.resolve()
    src = course_dir / "src" / args.lesson_id
    rep = Report()
    data, content = {}, ""
    try:
        data = json.loads((src / "practice.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        rep.err(f"missing {src / 'practice.json'}")
    except json.JSONDecodeError as e:
        rep.err(f"practice.json is not valid JSON: {e}")
    try:
        content = (src / "content.html").read_text(encoding="utf-8")
    except FileNotFoundError:
        rep.err(f"missing {src / 'content.html'}")
    if isinstance(data, dict) and data and content:
        validate(course_dir, args.lesson_id, data, content, rep)
    elif data and not isinstance(data, dict):
        rep.err("practice.json must be a JSON object")

    for w in rep.warnings:
        print(f"WARNING: {w}")
    for e in rep.errors:
        print(f"ERROR: {e}")
    if rep.errors:
        print(f"FAILED: {len(rep.errors)} error(s); nothing written. Fix them and run again.")
        return 1

    qs = data["questions"]
    summary = (f"{args.lesson_id}: '{data['title']}' · {len(qs)} questions "
               f"({sum(q['type'] == 'mc' for q in qs)} mc, {sum(q['type'] == 'written' for q in qs)} written) · "
               f"{len(data['concepts'])} concepts · {len(data.get('references', []))} references")
    if data.get("hands_on"):
        ho = data["hands_on"]
        summary += f" · hands-on ({ho['level']}, {len(ho.get('steps', []))} steps, ~{ho['minutes']} min)"
    if args.check:
        print(f"CHECK OK: {summary}")
        return 0
    out = course_dir / f"{args.lesson_id}.html"
    page = build(course_dir, args.lesson_id, data, content)
    standalone = args.standalone or args.open
    out.write_text(STANDALONE.format(page=page) if standalone else page, encoding="utf-8")
    print(f"WROTE: {out}" + (" (standalone)" if standalone else ""))
    print(summary)
    if not standalone:
        print(f"NEXT: publish {out} with the Artifact tool, capabilities {{\"sample\": {{}}}}")
    if args.open:
        print("OPENED in the browser" if open_in_browser(out) else f"Could not open a browser; open {out} yourself")
    return 0


if __name__ == "__main__":
    sys.exit(main())
