#!/usr/bin/env python3
"""iteration-12 grader: every check of checks.json, from bytes.

Usage (repo root):
  python3 adr-workspace/iteration-12/grade.py script [YYYY-MM-DD]   # writes script-checks.json
  python3 adr-workspace/iteration-12/grade.py table                 # prints the per-cell table
The optional date is the day the runs were made (default: today). Read-only over the run outputs.
"""
import datetime, glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
FIXTURE = os.path.join(WS, "evals", "files", "english-log")
EVAL = "eval-11-thin-context-no-padding"
CELLS = ["a-sonnet", "b-sonnet", "a-haiku", "b-haiku"]
HEADINGS = ["## Status", "## Context", "## Decision", "## Consequences"]
SENTENCE_TOKENS = re.compile(r"\b(we|will|decided|is|are|was|should)\b", re.I)
PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en)\b", re.I)


def tree(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def section(text, name):
    m = re.search(rf"^## {name}\s*\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
    return m.group(1).strip() if m else ""


def words(text):
    return len(re.findall(r"\w+", text))


def grade(run, day):
    out = os.path.join(run, "outputs")
    r = {}
    files, fixture = tree(out), tree(FIXTURE)
    new = [f for f in files if f not in fixture]
    untouched = all(f in files and sha(os.path.join(out, f)) == sha(os.path.join(FIXTURE, f)) for f in fixture)
    ok = len(new) == 1 and re.fullmatch(r"doc/adr/0003-[a-z0-9]+(-[a-z0-9]+)*\.md", new[0]) is not None
    r["F.1"] = {"passed": bool(ok and untouched), "evidence": {"new": new, "fixture_untouched": untouched}}
    adr = [f for f in new if f.startswith("doc/adr/") and f.endswith(".md")]
    if len(adr) != 1:
        return r
    path = os.path.join(out, adr[0])
    text = open(path, encoding="utf-8").read()
    lines = text.rstrip("\n").split("\n")
    h1 = re.match(r"# 3\. (.+)$", lines[0])
    title = h1.group(1).strip() if h1 else lines[0].lstrip("# ").strip()
    date = re.search(r"^Date: (\S+)$", text, flags=re.M)
    h2 = [l.strip() for l in lines if l.startswith("## ")]
    status = section(text, "Status").split("\n")[0].strip()
    r["F.2"] = {"passed": bool(h1 and date and date.group(1) == day and h2 == HEADINGS and status == "Accepted"),
                "evidence": {"h1": lines[0], "date": date.group(1) if date else None, "h2": h2, "status": status}}
    slug = re.sub(r"^0003-|\.md$", "", os.path.basename(adr[0]))
    r["F.3"] = {"passed": slug == slugify(title), "evidence": {"file": slug, "from_title": slugify(title)}}

    n_title = len(title.split())
    sent = SENTENCE_TOKENS.findall(title)
    r["T.1"] = {"passed": n_title <= 10 and not sent and not re.search(r"[.!?:]$", title),
                "title": title, "words": n_title, "sentence_tokens": sent}
    dec = section(text, "Decision")
    r["T.2"] = {"passed": "we will" in dec.lower() and "S3" in dec,
                "evidence": {"we_will": "we will" in dec.lower(), "names_s3": "S3" in dec}}
    r["T.3"] = {"passed": len(lines) <= 40, "count": len(lines)}
    r["O.1"] = {"count": words(text), "context": words(section(text, "Context")),
                "decision": words(dec), "consequences": words(section(text, "Consequences"))}
    r["O.2"] = {"count": len(PASSIVE.findall(dec)), "evidence": PASSIVE.findall(dec)[:6]}
    return r


def script():
    day = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()
    res = {}
    for cell in CELLS:
        for run in sorted(glob.glob(os.path.join(HERE, EVAL, cell, "run-*"))):
            res[f"{cell}/{os.path.basename(run)}"] = grade(run, day)
    json.dump(res, open(os.path.join(HERE, "script-checks.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{len(res)} runs graded against date {day}")


def table():
    res = json.load(open(os.path.join(HERE, "script-checks.json")))
    cell_runs = {c: [k for k in sorted(res) if k.startswith(c + "/")] for c in CELLS}
    print("| Check | " + " | ".join(CELLS) + " |\n|---|" + "---|" * len(CELLS))
    for cid in ["F.1", "F.2", "F.3", "T.1", "T.2", "T.3"]:
        print(f"| {cid} | " + " | ".join(
            f"{sum(1 for k in cell_runs[c] if res[k].get(cid, {}).get('passed'))}/{len(cell_runs[c])}" for c in CELLS) + " |")
    for cid, field, label in [("T.1", "words", "title words"), ("T.3", "count", "lines"), ("O.1", "count", "words"),
                              ("O.1", "context", "Context words"), ("O.1", "decision", "Decision words"),
                              ("O.1", "consequences", "Consequences words"), ("O.2", "count", "passives in Decision")]:
        print(f"| {cid} {label} per run | " + " | ".join(
            ", ".join(str(res[k].get(cid, {}).get(field, "-")) for k in cell_runs[c]) for c in CELLS) + " |")
    print()
    for c in CELLS:
        for k in cell_runs[c]:
            print(f"{k}: {res[k].get('T.1', {}).get('title', '-')}")


if __name__ == "__main__":
    {"script": script, "table": table}[sys.argv[1] if len(sys.argv) > 1 else "script"]()
