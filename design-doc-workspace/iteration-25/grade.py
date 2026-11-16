#!/usr/bin/env python3
"""Script checks for the iteration-25 pilot (kind=file in checks.json). Writes script-checks.json."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parent / "evals/files/large-template/docs/design/TEMPLATE.md"
RUNS = sorted((HERE / "eval-12-template-many-sections/with_skill").glob("run-*"))
SPEC = json.loads((HERE / "checks.json").read_text())
ALL = SPEC["template_headings"]
EMPTY = SPEC["sections_with_no_substance_in_prompt"]
ROWS = SPEC["header_rows_with_no_substance_in_prompt"]
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def norm(t):
    t = re.sub(r"[*_`]", "", t)
    return re.sub(r"^\s*\d+(\.\d+)*\.?\s*", "", t).strip().lower()


def find(ms, name):
    for i, m in enumerate(ms):
        if norm(m.group(2)).startswith(name.lower()):
            return i
    return None


def body(text, ms, i):
    level = len(ms[i].group(1))
    for m in ms[i + 1:]:
        if len(m.group(1)) <= level:
            return text[ms[i].end():m.start()]
    return text[ms[i].end():]


out = {}
for run in RUNS:
    root = run / "outputs"
    design = root / "docs/design"
    docs = sorted(p for p in design.glob("*.md") if p.name != "TEMPLATE.md")
    reply = (root / "reply.md").read_text() if (root / "reply.md").exists() else ""
    res = {"O.0": bool(docs), "new_docs": [p.name for p in docs]}
    res["12.1"] = sha(design / "TEMPLATE.md") == sha(FIXTURE) and len(docs) <= 1
    res["reply_question_marks"] = reply.count("?")
    if len(docs) == 1:
        text = docs[0].read_text()
        ms = list(HEADING.finditer(text))
        pos = {n: find(ms, n) for n in ALL}
        present = [p for p in pos.values() if p is not None]
        res["12.2"] = {"present": len(present), "of": len(ALL), "in_order": present == sorted(present),
                       "missing": [n for n, p in pos.items() if p is None]}
        res["extra_headings"] = [m.group(0) for i, m in enumerate(ms) if i not in present][1:]
        res["O.1"] = {n: (body(text, ms, pos[n]).strip() if pos[n] is not None else None) for n in EMPTY}
        res["header_rows"] = {r: next((l.strip() for l in text.splitlines() if r.lower() in l.lower() and l.lstrip().startswith("|")), None) for r in ROWS}
        low = reply.lower()
        res["O.6"] = [n for n in EMPTY if pos[n] is None and n.lower() not in low] + \
                     [r for r in ROWS if res["header_rows"][r] is None and r.lower() not in low]
        res["doc_question_marks"] = text.count("?")
    out[run.name] = res

(HERE / "script-checks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
for run, res in out.items():
    print(run, {k: res.get(k) for k in ("O.0", "12.1", "12.2", "O.6", "reply_question_marks", "doc_question_marks")})
