#!/usr/bin/env python3
"""Script checks for the iteration-24 pilot (kind=file in checks.json).

Usage: python3 grade.py   (run from anywhere; writes script-checks.json next to itself)
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parent / "evals/files/optional-template/docs/design/TEMPLATE.md"
RUNS = sorted((HERE / "eval-11-template-optional-sections/with_skill").glob("run-*"))

REQUIRED = ["Motivação", "Proposta", "Riscos", "Perguntas abertas"]
DISPENSABLE = [
    "Histórias de usuário",
    "Critérios de aceite",
    "Estratégia de migração",
    "Plano de rollout",
]
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def find(headings, name):
    """Index of the first heading whose text starts with `name` (case-insensitive)."""
    for i, (_, text) in enumerate(headings):
        if re.sub(r"[*_`]", "", text).strip().lower().startswith(name.lower()):
            return i
    return None


def section_body(text, headings_iter, idx):
    start = headings_iter[idx].end()
    level = len(headings_iter[idx].group(1))
    for m in headings_iter[idx + 1:]:
        if len(m.group(1)) <= level:
            return text[start:m.start()]
    return text[start:]


out = {}
for run in RUNS:
    design = run / "outputs/docs/design"
    docs = sorted(p for p in design.glob("*.md") if p.name != "TEMPLATE.md")
    res = {"new_docs": [p.name for p in docs]}
    template_ok = (design / "TEMPLATE.md").exists() and sha(design / "TEMPLATE.md") == sha(FIXTURE)
    res["11.1"] = len(docs) == 1 and template_ok
    res["template_unchanged"] = template_ok
    if len(docs) == 1:
        text = docs[0].read_text()
        ms = list(HEADING.finditer(text))
        hs = [(len(m.group(1)), m.group(2)) for m in ms]
        res["headings"] = [f"{'#' * lvl} {t}" for lvl, t in hs]
        pos = [find(hs, n) for n in REQUIRED]
        res["11.2"] = all(p is not None for p in pos) and pos == sorted(pos)
        mi = find(hs, "Métricas de sucesso")
        res["11.3"] = mi is not None and "0,1" in section_body(text, ms, mi)
        res["O.1"] = {}
        res["O.1_bodies"] = {}
        for n in DISPENSABLE:
            i = find(hs, n)
            res["O.1"][n] = "present" if i is not None else "absent"
            if i is not None:
                res["O.1_bodies"][n] = section_body(text, ms, i).strip()
    out[run.name] = res

(HERE / "script-checks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
for run, res in out.items():
    print(run, {k: v for k, v in res.items() if k in ("11.1", "11.2", "11.3", "O.1")})
