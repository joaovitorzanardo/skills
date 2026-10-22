#!/usr/bin/env python3
"""Build MAP.html for one area of knowledge (Agent E, the Visual Map Generator).

Reads <area-dir>/SUB_FIELDS.md, <area-dir>/OVERVIEW.md and <area-dir>/<sub-field-slug>/RESOURCES.md,
turns them into the km-data JSON described in references/design/EXPERIENCE.md § Data Contract,
runs the "Validation before write" rules, and writes <area-dir>/MAP.html from the frozen template.

Usage:
    python build_map.py <area-dir>            build MAP.html and print a report
    python build_map.py <area-dir> --check    only parse and report problems, write nothing
    python build_map.py <area-dir> --open     build, then open MAP.html in the default browser

Exit codes: 0 = ok (fixes and gaps are listed in the report), 1 = fatal (no page written).
Standard library only.
"""

import argparse
import datetime
import html
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import unicodedata
import webbrowser
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "knowledge-map-template.html"
DATA_BLOCK = re.compile(r'(<script type="application/json" id="km-data">)(.*?)(</script>)', re.S)

MAX_SUBFIELDS, MAX_TOPICS = 6, 5
TYPES = {"BOOK", "PAPER", "COURSE", "ARTICLE", "VIDEO"}
TYPE_ALIASES = {
    "TEXTBOOK": "BOOK", "MONOGRAPH": "BOOK", "HANDBOOK": "BOOK",
    "JOURNAL": "PAPER", "CONFERENCE": "PAPER", "SURVEY": "PAPER", "PREPRINT": "PAPER", "THESIS": "PAPER",
    "LECTURE": "COURSE", "LECTURES": "COURSE", "MOOC": "COURSE", "LECTURE NOTES": "COURSE",
    "BLOG": "ARTICLE", "WEB": "ARTICLE", "WEBSITE": "ARTICLE", "DOCS": "ARTICLE", "DOCUMENTATION": "ARTICLE",
    "TUTORIAL": "ARTICLE", "REPORT": "ARTICLE",
    "TALK": "VIDEO", "PODCAST": "VIDEO",
}
SKIP_H2 = {"resources", "references", "bibliography", "further-reading", "sources"}


class Report:
    def __init__(self):
        self.fixes, self.gaps = [], []

    def fix(self, msg):
        self.fixes.append(msg)

    def gap(self, msg):
        self.gaps.append(msg)


class Fatal(Exception):
    pass


# ---------- text helpers ----------

def slug(s):
    """Same slug as the template: ASCII, lowercase, hyphen-separated."""
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def ref_id(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9-]", "", s)


def plain(s):
    """Strip markdown emphasis/code/link syntax, leaving text."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`]+", "", s)
    return s.strip()


def inline_html(s, resolve_cite):
    """Markdown inline → the HTML the template allows: <b>, <i> and citation links only."""
    s = html.escape(s.strip(), quote=False)

    def cite(m):
        text, rid = m.group(1), m.group(2)
        target = resolve_cite(rid, text)
        return f'<a class="cite" href="#ref-{target}">{text}</a>' if target else text

    s = re.sub(r"\[([^\]]+)\]\(#ref-([^)\s]+)\)", cite, s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)  # any other link keeps only its text
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return s


def paragraphs(lines):
    """Group lines into paragraphs separated by blank lines. List items are folded into prose."""
    out, cur = [], []
    for line in lines + [""]:
        t = line.strip()
        if not t:
            if cur:
                out.append(" ".join(cur))
                cur = []
            continue
        cur.append(re.sub(r"^([-*+]|\d+\.)\s+", "", t))
    return out


def read(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


# ---------- SUB_FIELDS.md ----------

def parse_subfields(area_dir, rep):
    path = area_dir / "SUB_FIELDS.md"
    if not path.exists():
        raise Fatal(f"{path} not found; there is nothing to map.")
    area, subs, cur = None, [], None
    for line in read(path):
        m = re.match(r"^(#{1,3})\s+(.*?)\s*#*\s*$", line)
        if m and len(m.group(1)) <= 2 and area is None:
            area = plain(m.group(2))
        elif m and len(m.group(1)) == 3:
            cur = {"name": plain(m.group(2)), "topics": [], "desc": []}
            subs.append(cur)
        elif cur is not None:
            b = re.match(r"^\s*[-*+]\s+(.*)", line)
            if b:
                cur["topics"].append(plain(b.group(1)))
            elif line.strip():
                cur["desc"].append(line.strip())
    if not area:
        raise Fatal("SUB_FIELDS.md has no '## <Area name>' heading.")
    if not subs:
        raise Fatal("SUB_FIELDS.md lists no '### <Sub-field>' sections.")

    # rule 1: 1–6 sub-fields
    if len(subs) > MAX_SUBFIELDS:
        rest = ", ".join(s["name"] for s in subs[MAX_SUBFIELDS:])
        rep.fix(f"{len(subs)} sub-fields; kept the first {MAX_SUBFIELDS}, dropped: {rest}")
        subs = subs[:MAX_SUBFIELDS]

    seen = set()
    for s in subs:
        # rule 2: ≤ 5 topics
        if len(s["topics"]) > MAX_TOPICS:
            rep.fix(f"{s['name']}: {len(s['topics'])} topics, kept the first {MAX_TOPICS}")
            s["topics"] = s["topics"][:MAX_TOPICS]
        if not s["topics"]:
            rep.gap(f"{s['name']}: no topics in SUB_FIELDS.md")
        # rule 3: unique slugs (the folder name is the un-suffixed slug)
        s["dir"] = slug(s["name"])
        sid = s["dir"] or "subfield"
        while sid in seen:
            sid += "-2"
        if sid != s["dir"]:
            rep.fix(f"{s['name']}: id collision, re-slugged to '{sid}'")
        seen.add(sid)
        s["id"] = sid
        s["desc"] = " ".join(s["desc"])
    return area, subs


# ---------- RESOURCES.md ----------

def parse_resources(path, rep, label):
    entries, cur = [], None
    for line in read(path):
        h = re.match(r"^###\s+(.*?)\s*$", line)
        if h:
            cur = {"id": ref_id(plain(h.group(1))), "type": "", "citation": "", "url": ""}
            entries.append(cur)
            continue
        f = re.match(r"^\s*[-*+]?\s*\**\s*(type|citation|url|link|doi|why)\s*:?\**\s*:?\s*(.*)$", line, re.I)
        if cur is not None and f:
            key, val = f.group(1).lower(), f.group(2).strip()
            if key in ("url", "link", "doi"):
                key = "url"
            if key != "why":
                cur[key] = val

    out = []
    for e in entries:
        if not e["id"]:
            rep.fix(f"{label}: entry with an empty id dropped")
            continue
        if not e["citation"]:
            rep.fix(f"{label}: '{e['id']}' has no Citation line, dropped")
            continue
        t = plain(e["type"]).upper()
        t = TYPE_ALIASES.get(t, t)
        if t not in TYPES:
            rep.fix(f"{label}: '{e['id']}' type '{e['type'] or '(none)'}' → ARTICLE")
            t = "ARTICLE"
        url = plain(e["url"].strip("<>"))
        if re.match(r"^(doi:\s*)?10\.\d{4,}/", url, re.I):
            url = "https://doi.org/" + re.sub(r"^doi:\s*", "", url, flags=re.I)
        if url and not re.match(r"^https?://", url):
            if url.lower() not in ("", "none", "-", "n/a", "na"):
                rep.fix(f"{label}: '{e['id']}' URL '{url}' is not http(s), removed")
            url = ""
        out.append({"id": e["id"], "type": t, "citation_md": e["citation"], "url": url})
    return out


# ---------- OVERVIEW.md ----------

def parse_overview(area_dir, subs, rep):
    path = area_dir / "OVERVIEW.md"
    if not path.exists():
        rep.gap("OVERVIEW.md not found; intro and sub-field texts fall back to SUB_FIELDS.md")
        return [], {}, {}
    by_key = {}
    for s in subs:
        by_key[slug(s["name"])] = s["id"]
        by_key[s["id"]] = s["id"]
    intro, bodies, connects = [], {}, {}
    h2_count, target, skipping = 0, None, False
    for line in read(path):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            level, title = len(m.group(1)), plain(m.group(2))
            if level <= 2:
                h2_count += 1
                skipping = slug(title) in SKIP_H2
                target = "intro" if h2_count == 1 else None
            elif level == 3 and not skipping:
                target = by_key.get(slug(title))
                if target is None:
                    rep.gap(f"OVERVIEW.md: section '{title}' matches no sub-field, ignored")
                    target = "ignored"
            continue
        if skipping or target in (None, "ignored"):
            continue
        c = re.match(r"^\s*[-*+]?\s*\**\s*connects\s+to\s*:?\**\s*:?\s*(.*)$", line, re.I)
        if c and target != "intro":
            connects[target] = c.group(1)
            continue
        if target == "intro":
            intro.append(line)
        else:
            bodies.setdefault(target, []).append(line)
    return intro, bodies, connects


def resolve_connects(raw, s, subs, rep):
    if raw is None:
        return []
    names = {slug(x["name"]): x["id"] for x in subs}
    ids = {x["id"] for x in subs}
    items = [i for i in re.split(r"[;,]", raw) if i.strip()] if ";" not in raw else raw.split(";")
    out = []
    for item in items:
        key = slug(re.sub(r"^\s*\d+\s+", "", plain(item)))
        if not key:
            continue
        cid = names.get(key) or (key if key in ids else None)
        # rule 4: connects must exist and not point to itself
        if cid is None:
            rep.fix(f"{s['name']}: 'Connects to' item '{plain(item)}' matches no sub-field, dropped")
        elif cid == s["id"]:
            rep.fix(f"{s['name']}: 'Connects to' points to itself, dropped")
        elif cid not in out:
            out.append(cid)
    return out


# ---------- assemble + validate ----------

def build_data(area_dir, date, rep):
    area, subs = parse_subfields(area_dir, rep)
    sub_dirs = {s["dir"] for s in subs}

    # rule 5: resources are keyed by sub-field; folders that match none are reported
    for p in sorted(area_dir.glob("*/RESOURCES.md")):
        if p.parent.name not in sub_dirs:
            rep.gap(f"{p.parent.name}/RESOURCES.md matches no sub-field in SUB_FIELDS.md, ignored")

    resources, all_ids, renamed = {}, {}, {}
    for s in subs:
        p = area_dir / s["dir"] / "RESOURCES.md"
        if not p.exists():
            rep.gap(f"{s['name']}: {s['dir']}/RESOURCES.md missing, shown as 'No sources found'")
            resources[s["id"]] = []
            continue
        entries = parse_resources(p, rep, f"{s['dir']}/RESOURCES.md")
        if not entries:
            rep.gap(f"{s['name']}: RESOURCES.md has no usable entries")
        # rule 6: resource ids unique across the page
        for e in entries:
            orig = e["id"]
            if orig in all_ids:
                n, new = 1, orig
                while new in all_ids:
                    new = orig + "bcdefghijklmnopqrstuvwxyz"[n - 1]
                    n += 1
                renamed[(s["id"], orig)] = new
                rep.fix(f"{s['name']}: duplicate resource id '{orig}' renamed to '{new}'")
                e["id"] = new
            all_ids[e["id"]] = s["id"]
        resources[s["id"]] = entries

    # rule 7: every citation link points at a real resource id
    def resolver(owner):
        def resolve(rid, text):
            rid = ref_id(rid)
            if (owner, rid) in renamed:
                return renamed[(owner, rid)]
            if rid in all_ids:
                return rid
            m = re.match(r"\(?\s*([A-Za-zÀ-ÿ'-]+).*?(\d{4}[a-z]?)", plain(text))
            guess = ref_id(m.group(1) + m.group(2)) if m else ""
            if guess in all_ids:
                rep.fix(f"citation '#ref-{rid}' → '#ref-{guess}' (matched by author and year)")
                return guess
            rep.fix(f"citation '{plain(text)}' (#ref-{rid}) has no matching resource, link removed")
            return None
        return resolve

    intro_md, bodies, connects = parse_overview(area_dir, subs, rep)

    intro = [inline_html(p, resolver(None)) for p in paragraphs(intro_md)]
    # rule 8: intro and every overview non-empty
    if not intro:
        names = ", ".join(s["name"] for s in subs)
        intro = [html.escape(f"{area} is organized here into {len(subs)} sub-fields: {names}.", quote=False)]
        rep.gap("OVERVIEW.md: no area introduction; used a one-line placeholder")

    out_subs = []
    for s in subs:
        ov = [inline_html(p, resolver(s["id"])) for p in paragraphs(bodies.get(s["id"], []))]
        if not ov:
            fallback = s["desc"] or f"{s['name']} is a sub-field of {area}."
            ov = [inline_html(fallback, resolver(s["id"]))]
            rep.gap(f"OVERVIEW.md: no section for '{s['name']}'; used the SUB_FIELDS.md description")
        if s["id"] not in connects and (area_dir / "OVERVIEW.md").exists():
            rep.gap(f"OVERVIEW.md: '{s['name']}' has no 'Connects to' line, so it has no map links")
        out_subs.append({
            "id": s["id"], "name": s["name"], "topics": s["topics"], "overview": ov,
            "connects": resolve_connects(connects.get(s["id"]), s, subs, rep),
        })

    res_out = {
        sid: [{"id": e["id"], "type": e["type"],
               "citation": inline_html(e["citation_md"], lambda *_: None), "url": e["url"]} for e in lst]
        for sid, lst in resources.items()
    }
    return {"area": area, "generated": date, "intro": intro, "subfields": out_subs, "resources": res_out}


# ---------- write + verify ----------

def encode(data):
    # rule 9: a real encoder, and "</" can never close the script tag
    return json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")


def write_map(area_dir, data):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    m = DATA_BLOCK.search(tpl)
    if not m:
        raise Fatal(f"km-data block not found in {TEMPLATE}")
    page = tpl[: m.start(2)] + "\n" + encode(data) + "\n" + tpl[m.end(2):]
    out = area_dir / "MAP.html"
    out.write_text(page, encoding="utf-8")

    # verify: frozen parts untouched, JSON parses back to the same object
    back = out.read_text(encoding="utf-8")
    m2 = DATA_BLOCK.search(back)
    if not m2 or back[: m2.start(2)] != tpl[: m.start(2)] or back[m2.end(2):] != tpl[m.end(2):]:
        raise Fatal("MAP.html verification failed: the frozen template code changed")
    if json.loads(m2.group(2)) != data:
        raise Fatal("MAP.html verification failed: km-data does not parse back to the same data")
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
    ap.add_argument("area_dir", type=Path)
    ap.add_argument("--check", action="store_true", help="parse and report only; write nothing")
    ap.add_argument("--open", action="store_true", help="open MAP.html in the default browser")
    ap.add_argument("--date", default=datetime.date.today().isoformat(), help="generation date, YYYY-MM-DD")
    args = ap.parse_args()

    rep = Report()
    try:
        data = build_data(args.area_dir, args.date, rep)
        out = None if args.check else write_map(args.area_dir, data)
    except Fatal as e:
        print(f"FATAL: {e}")
        return 1

    subs = data["subfields"]
    links = {tuple(sorted((s["id"], c))) for s in subs for c in s["connects"]}
    print(f"{'CHECK' if args.check else 'WROTE'}: {out or args.area_dir}")
    print(f"area: {data['area']} · sub-fields {len(subs)} · topics {sum(len(s['topics']) for s in subs)}"
          f" · links {len(links)} · sources {sum(len(v) for v in data['resources'].values())}")
    for s in subs:
        print(f"  - {s['id']}: {len(s['topics'])} topics, {len(data['resources'].get(s['id'], []))} sources,"
              f" connects {s['connects'] or '—'}")
    for title, items in (("FIXES", rep.fixes), ("GAPS", rep.gaps)):
        print(f"{title} ({len(items)}):" + ("" if items else " none"))
        for i in items:
            print(f"  - {i}")
    if out and args.open:
        print("opened in browser" if open_in_browser(out) else f"could not open a browser; open {out} manually")
    return 0


if __name__ == "__main__":
    sys.exit(main())
