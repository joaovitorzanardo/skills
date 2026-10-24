#!/usr/bin/env python3
"""Score a pasted Practice results block and record it in PRACTICE_RESULTS.md.

  python3 record_results.py <course-dir> <block-file|-> [--written "q6=1,q7=0.5"] [--notes "..."] [--dry-run]

Multiple choice is re-scored from src/<lesson-id>/practice.json, never trusted from the page.
Written answers are graded by Claude and passed with --written (1, 0.5 or 0 each).

Pass rule: score >= 80% AND every core concept has at least one question with full credit.

Exit codes: 0 = recorded (or dry run), 1 = error, 2 = written answers need grading (nothing written).
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

PASS_SCORE = 0.8
HEADER = "TEACH-ME RESULTS v"


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def parse_block(text):
    i = text.find(HEADER)
    if i < 0:
        fail("no 'TEACH-ME RESULTS' header found. Ask the Learner to click 'Copy results' again and paste the whole block.")
    rest = text[i + len(HEADER):]
    version = re.match(r"(\d+)", rest)
    if not version or version.group(1) != "1":
        fail(f"unsupported results format version {version.group(1) if version else '?'}; this script reads v1")
    start, end = rest.find("{"), rest.rfind("}")
    if start < 0 or end < start:
        fail("the results block has no JSON. It was probably cut off when pasting.")
    try:
        block = json.loads(rest[start:end + 1])
    except json.JSONDecodeError as e:
        fail(f"the results JSON doesn't parse ({e}). Ask the Learner to copy it again.")
    for f in ("course", "lesson", "answers"):
        if f not in block:
            fail(f"the results block has no '{f}'")
    if not isinstance(block["answers"], dict):
        fail("'answers' must be an object")
    return block


def parse_written(arg, written_ids):
    grades = {}
    for part in filter(None, (p.strip() for p in (arg or "").split(","))):
        m = re.match(r"^(q\d+)\s*=\s*(1|1\.0|0\.5|\.5|0|0\.0)$", part)
        if not m:
            fail(f"--written entry '{part}' must look like q6=1, q6=0.5 or q6=0")
        grades[m.group(1)] = float(m.group(2))
    unknown = set(grades) - set(written_ids)
    if unknown:
        fail(f"--written grades questions that aren't written questions: {sorted(unknown)}")
    missing = [q for q in written_ids if q not in grades]
    if missing:
        fail(f"--written is missing grades for: {missing}")
    return grades


def plain(s, limit=70):
    s = re.sub(r"<[^>]+>", "", str(s))
    s = re.sub(r"\s+", " ", s).strip().replace("|", "\\|")
    return s if len(s) <= limit else s[: limit - 1] + "…"


def pct(x):
    return f"{round(x * 100)}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("course_dir", type=Path)
    ap.add_argument("block_file", help="file holding the pasted block, or - for stdin")
    ap.add_argument("--written", help='grades for written questions, e.g. "q6=1,q7=0.5"')
    ap.add_argument("--notes", default="", help="short grading notes, kept in PRACTICE_RESULTS.md")
    ap.add_argument("--dry-run", action="store_true", help="score and print, but write nothing")
    args = ap.parse_args()

    course_dir = args.course_dir.resolve()
    text = sys.stdin.read() if args.block_file == "-" else Path(args.block_file).read_text(encoding="utf-8")
    block = parse_block(text)
    if block["course"] != course_dir.name:
        fail(f"the block is for course '{block['course']}', but the Course folder is '{course_dir.name}'")
    lesson = block["lesson"]
    src = course_dir / "src" / lesson / "practice.json"
    if not src.exists():
        fail(f"no {src}: is this the right Course folder?")
    data = json.loads(src.read_text(encoding="utf-8"))
    questions = data["questions"]
    answers = block["answers"]
    written_ids = [q["id"] for q in questions if q["type"] == "written"]

    results_path = course_dir / "PRACTICE_RESULTS.md"
    existing = results_path.read_text(encoding="utf-8") if results_path.exists() else ""
    submitted = block.get("submitted") or ""
    if submitted and f"submitted: {submitted}" in existing and re.search(
            rf"^## {re.escape(lesson)} · attempt \d+.*\n\nsubmitted: {re.escape(submitted)}$", existing, re.M):
        fail(f"this exact submission ({lesson}, {submitted}) is already recorded. Nothing to do.")

    if written_ids and args.written is None:
        print(f"GRADE THESE {len(written_ids)} WRITTEN ANSWER(S), then rerun with --written \"{','.join(q + '=?' for q in written_ids)}\"\n")
        for q in questions:
            if q["type"] != "written":
                continue
            print(f"--- {q['id']} · concept: {q['concept']}")
            print(f"Prompt: {plain(q['prompt'], 400)}")
            print(f"Model answer: {q['model_answer']}")
            print(f"Rubric: {q['rubric']}")
            print(f"Learner's answer: {answers.get(q['id']) or '(blank)'}\n")
        sys.exit(2)
    grades = parse_written(args.written, written_ids) if written_ids else {}

    rows, points, by_concept = [], 0.0, {}
    for q in questions:
        a = answers.get(q["id"])
        if q["type"] == "mc":
            got = 1.0 if a == q["answer"] else 0.0
            if isinstance(a, int) and 0 <= a < len(q["options"]):
                shown = f"{chr(65 + a)}: {plain(q['options'][a], 50)}"
            else:
                shown = "(blank)"
            result = "✓" if got else f"✗ (correct: {chr(65 + q['answer'])})"
        else:
            got = grades[q["id"]]
            shown = "see below" if a else "(blank)"
            result = {1.0: "1", 0.5: "0.5", 0.0: "0"}[got]
        points += got
        c = by_concept.setdefault(q["concept"], {"points": 0.0, "n": 0, "full": False})
        c["points"] += got
        c["n"] += 1
        c["full"] = c["full"] or got == 1.0
        rows.append(f"| {q['id']} | {q['concept']} | {q['type']} | {shown} | {result} |")

    score = points / len(questions)
    core = [c["id"] for c in data["concepts"] if c.get("core")]
    missed = [cid for cid in core if not by_concept.get(cid, {}).get("full")]
    passed = score >= PASS_SCORE - 1e-9 and not missed
    verdict = "PASS" if passed else "FAIL"
    attempt = len(re.findall(rf"^## {re.escape(lesson)} · attempt \d+", existing, re.M)) + 1
    day = submitted[:10] if re.match(r"\d{4}-\d{2}-\d{2}", submitted) else datetime.date.today().isoformat()

    section = [
        f"## {lesson} · attempt {attempt} · {day}",
        "",
        f"submitted: {submitted or 'unknown'}",
        f"score: {points:g} / {len(questions)} ({pct(score)})",
        f"verdict: {verdict}",
        f"missed core concepts: {', '.join(missed) if missed else 'none'}",
        "",
        "| Q | Concept | Type | Answer | Result |",
        "|---|---|---|---|---|",
        *rows,
    ]
    written_answers = [(q, answers.get(q["id"])) for q in questions if q["type"] == "written" and answers.get(q["id"])]
    if written_answers:
        section += ["", "Written answers:", ""]
        for q, a in written_answers:
            section.append(f"- {q['id']}: " + " ".join(str(a).split()))
    if args.notes.strip():
        section += ["", f"notes: {args.notes.strip()}"]
    ho = block.get("hands_on")
    ho_line = None
    if data.get("hands_on") and isinstance(ho, dict) and isinstance(ho.get("ticked"), list):
        ho_line = f"hands-on: {len(ho['ticked'])} / {ho.get('of', '?')} ticked (self-reported, not scored)"
        section.insert(6, ho_line)
    section_text = "\n".join(section) + "\n"

    print(f"{lesson} attempt {attempt}: {pct(score)}, {verdict}")
    print(f"missed core concepts: {', '.join(missed) if missed else 'none'}")
    if ho_line:
        print(ho_line)
    elif data.get("hands_on"):
        print("hands-on: not reported in the block")
    print("by concept:")
    names = {c["id"]: c["name"] for c in data["concepts"]}
    for cid, c in by_concept.items():
        flag = "core" if cid in core else "    "
        print(f"  {flag} {cid} ({names.get(cid, '?')}): {c['points']:g}/{c['n']}{'' if c['full'] else '  <- never fully correct'}")
    wrong = [q for q in questions if q["type"] == "mc" and answers.get(q["id"]) != q["answer"]]
    if wrong:
        print("wrong multiple choice:")
        for q in wrong:
            a = answers.get(q["id"])
            picked = plain(q["options"][a], 60) if isinstance(a, int) and 0 <= a < len(q["options"]) else "(blank)"
            print(f"  {q['id']} [{q['concept']}] picked: {picked} | correct: {plain(q['options'][q['answer']], 60)}")

    if args.dry_run:
        print("DRY RUN: nothing written")
        return 0
    if not existing:
        existing = (f"# {data['topic']}: Practice Results\n\n"
                    "Written by record_results.py. Don't edit by hand: the attempt count and verdicts depend on it.\n")
    results_path.write_text(existing.rstrip("\n") + "\n\n" + section_text, encoding="utf-8")
    print(f"RECORDED in {results_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
