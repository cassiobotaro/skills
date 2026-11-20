#!/usr/bin/env python3
"""iteration-15 grader: every check of checks.json, from bytes.

Usage (repo root):
  python3 adr-workspace/iteration-15/grade.py script [YYYY-MM-DD]   # writes script-checks.json
  python3 adr-workspace/iteration-15/grade.py table                 # prints the per-cell table
The optional date is the day the runs were made (default: today). Read-only over the run outputs.
"""
import datetime, glob, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = "eval-13-rambling-request-portuguese"
CELLS = ["a-sonnet", "a-haiku"]
HEADINGS = ["## Status", "## Context", "## Decision", "## Consequences"]
SENTENCE_TOKENS = re.compile(r"\b(decidimos|vamos|iremos|será|serão|foi|foram|é|são|deve|devemos|ficou)\b", re.I)
FIRST_PLURAL = re.compile(r"\b(?:vamos|iremos|\w+(?:aremos|eremos|iremos))\b", re.I)
PART = r"(?:\w+(?:ad|id)[oa]s?|feit[oa]s?|escrit[oa]s?|post[oa]s?|abert[oa]s?|vist[oa]s?|entregues?|aceit[oa]s?)"
PASSIVE = re.compile(r"\b(?:é|são|foi|foram|será|serão|seja|sejam|sendo|ficou|ficaram|fica|ficam|vai ser|vão ser)\s+(?:\w+mente\s+)?"
                     + PART + r"\b", re.I)
PT_WORDS = ["que", "não", "de", "em", "uma", "para"]


def tree(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


def slugify(title):
    """adr-tools' pipeline on Linux: lowercase, every run of anything but ASCII letters and digits -> one hyphen."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def h1_title(path):
    first = open(path, encoding="utf-8").read().split("\n", 1)[0]
    return re.sub(r"^#\s*(?:\d+\.\s*)?", "", first).strip()


def section(text, name):
    m = re.search(rf"^## {name}\s*\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
    return m.group(1).strip() if m else ""


def words(text):
    return len(re.findall(r"\w+", text))


def grade(run, day):
    out = os.path.join(run, "outputs")
    r = {}
    files = tree(out)
    adrs = [f for f in files if f.startswith("doc/adr/")]
    seed = [f for f in adrs if os.path.basename(f).startswith("0001-") and f.endswith(".md")]
    dec = [f for f in adrs if os.path.basename(f).startswith("0002-") and f.endswith(".md")]
    r["F.1"] = {"passed": len(adrs) == 2 and len(seed) == 1 and len(dec) == 1, "evidence": adrs}
    r["O.5"] = {"count": len(files) - len(adrs), "evidence": [f for f in files if f not in adrs]}
    r["S.3"] = {"passed": all(re.fullmatch(r"\d{4}-[a-z0-9]+(-[a-z0-9]+)*\.md", os.path.basename(f)) for f in adrs),
                "evidence": [os.path.basename(f) for f in adrs]}
    if len(seed) == 1:
        st = h1_title(os.path.join(out, seed[0]))
        sslug = re.sub(r"^\d{4}-|\.md$", "", os.path.basename(seed[0]))
        r["S.1"] = {"passed": sslug == slugify(st), "title": st, "file": sslug, "expected": slugify(st),
                    "exercised": bool(re.search(r"[^\x00-\x7f]", st))}
    # the decision record: 0002 when there is one, else the highest-numbered ADR that is not the seed
    cand = dec or [f for f in files if re.fullmatch(r"doc/adr/\d{4}-.*\.md", f) and f not in seed][-1:]
    if len(cand) != 1:
        return r
    text = open(os.path.join(out, cand[0]), encoding="utf-8").read()
    lines = text.rstrip("\n").split("\n")
    h1 = re.match(r"# 2\. (.+)$", lines[0])
    title = h1.group(1).strip() if h1 else re.sub(r"^#\s*(?:\d+\.\s*)?", "", lines[0]).strip()
    date = re.search(r"^Date: (\S+)$", text, flags=re.M)
    h2 = [l.strip() for l in lines if l.startswith("## ")]
    status = section(text, "Status").split("\n")[0].strip()
    r["F.2"] = {"passed": bool(h1 and date and date.group(1) == day and h2 == HEADINGS and status == "Accepted"),
                "evidence": {"h1": lines[0], "date": date.group(1) if date else None, "h2": h2, "status": status}}
    slug = re.sub(r"^\d{4}-|\.md$", "", os.path.basename(cand[0]))
    r["S.2"] = {"passed": slug == slugify(title), "file": slug, "expected": slugify(title),
                "exercised": bool(re.search(r"[^\x00-\x7f]", title))}
    ctx, decision, cons = section(text, "Context"), section(text, "Decision"), section(text, "Consequences")
    found = [w for w in PT_WORDS if re.search(rf"\b{w}\b", ctx, flags=re.I)]
    r["F.4"] = {"passed": len(found) >= 3, "evidence": found}

    n_title = len(title.split())
    sent = SENTENCE_TOKENS.findall(title)
    r["T.1"] = {"passed": n_title <= 10 and not sent and not re.search(r"[.!?:]$", title),
                "title": title, "words": n_title, "sentence_tokens": sent}
    fp = FIRST_PLURAL.findall(decision)
    r["T.2"] = {"passed": bool(fp) and "sidekiq" in decision.lower(),
                "evidence": {"first_person_plural": fp[:4], "names_sidekiq": "sidekiq" in decision.lower(),
                             "opens": decision[:70]}}
    r["T.3"] = {"passed": len(lines) <= 40, "count": len(lines)}
    r["O.1"] = {"count": words(text), "context": words(ctx), "decision": words(decision), "consequences": words(cons)}
    r["O.2"] = {"count": len(PASSIVE.findall(decision)), "evidence": PASSIVE.findall(decision)[:6],
                "ficou_decidido": len(re.findall(r"ficou decidido|foi decidido|ficou acordado", text, flags=re.I))}
    r["O.3"] = {"count": len(re.findall(r"\brenom", text, flags=re.I))}
    r["O.4"] = {"count": len(re.findall(r"\b(?:Marta|Rafael)\b", text))}
    r["seed"] = {"file": seed[0] if seed else None}
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
    for cid in ["F.1", "F.2", "F.4", "S.1", "S.2", "S.3", "T.1", "T.2", "T.3"]:
        print(f"| {cid} | " + " | ".join(
            f"{sum(1 for k in cell_runs[c] if res[k].get(cid, {}).get('passed'))}/{len(cell_runs[c])}" for c in CELLS) + " |")
    for cid, field, label in [("T.1", "words", "title words"), ("T.3", "count", "lines"), ("O.1", "count", "words"),
                              ("O.1", "context", "Context words"), ("O.1", "decision", "Decision words"),
                              ("O.1", "consequences", "Consequences words"), ("O.2", "count", "passives in Decision"),
                              ("O.2", "ficou_decidido", "'ficou decidido' kept"),
                              ("O.3", "count", "mentions of the rename tangent"), ("O.4", "count", "people named"),
                              ("O.5", "count", "files outside doc/adr"), ("S.1", "exercised", "seed title has an accent"),
                              ("S.2", "exercised", "0002 title has an accent")]:
        print(f"| {cid} {label} per run | " + " | ".join(
            ", ".join(str(res[k].get(cid, {}).get(field, "-")) for k in cell_runs[c]) for c in CELLS) + " |")
    print()
    for c in CELLS:
        for k in cell_runs[c]:
            print(f"{k}: {res[k].get('S.1', {}).get('title', '-')} -> {res[k].get('S.1', {}).get('file', '-')} || "
                  f"{res[k].get('T.1', {}).get('title', '-')} -> {res[k].get('S.2', {}).get('file', '-')}")


if __name__ == "__main__":
    {"script": script, "table": table}[sys.argv[1] if len(sys.argv) > 1 else "script"]()
