#!/usr/bin/env python3
"""Grade iteration-23 against ../evals/checks-baseline.json.

  grade.py files    script-decided checks (kind=file/absence) -> script-checks.json
  grade.py packets  blind judge packets -> judge-inputs/, judge-map.json
  grade.py table    script + judge verdicts -> results.json and a table on stdout

Judge outputs are expected at judge-outputs/<packet>-pass<N>.json as a list of
{"id", "verdict": "met"|"unmet", "evidence"}. Pass 1 covers every judge check;
passes 2 and 3 cover kind=invention only.
"""
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent / "evals"
_BASE = json.loads((EVALS / "checks-baseline.json").read_text(encoding="utf-8"))
BASELINE = _BASE["evals"]
ANCHORS = _BASE.get("anchors", {})
PROMPTS = {str(e["id"]): e["prompt"] for e in json.loads((EVALS / "evals.json").read_text(encoding="utf-8"))["evals"]}
FIXTURE = EVALS / "files/shipped/docs/design/exportacao-de-relatorios.md"
ORIGINAL = "docs/design/exportacao-de-relatorios.md"
RUN_DATE = "2026-11-16"
BODY_MARK = "## Visão geral"
DIRS = {"9": "eval-9-amend-shipped-doc"}
ARMS = ("with_skill", "old_skill")
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def runs():
    for ev, d in DIRS.items():
        for arm in ARMS:
            for run in sorted((HERE / d / arm).glob("run-*")):
                yield ev, arm, run.name, run / "outputs"


def tree(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())


def links_to(text, base, target):
    return any((base / m).resolve() == target.resolve() for m in LINK.findall(text))


def split(text):
    i = text.find(BODY_MARK)
    return (text, "") if i < 0 else (text[:i], text[i:])


def files_eval9(root):
    fixture = FIXTURE.read_text(encoding="utf-8")
    design = root / "docs/design"
    orig = root / ORIGINAL
    orig_text = orig.read_text(encoding="utf-8") if orig.exists() else ""
    new = [p for p in design.glob("*.md") if p.name != orig.name] if design.exists() else []
    one = new[0] if len(new) == 1 else None
    head, body = split(orig_text)
    changed = [p for p in (root / "docs").rglob("*") if p.is_file() and not (p == orig and orig_text == fixture)]
    dates = [d for p in changed for d in DATE.findall(p.read_text(encoding="utf-8", errors="replace"))]
    known = set(DATE.findall(fixture)) | {RUN_DATE}
    return {
        "9.1": len(new) == 1,
        "9.2": bool(body) and body == split(fixture)[1],
        "9.3": bool(one) and links_to(head, design, one),
        "9.4": bool(one) and links_to(one.read_text(encoding="utf-8"), design, orig),
        "9.5": RUN_DATE in dates and all(d in known for d in dates),
    }


def files_eval10(root):
    return {"10.1": [f for f in tree(root) if f != "reply.md"] == []}


def cmd_files():
    out = {}
    for ev, arm, run, root in runs():
        res = files_eval9(root) if ev == "9" else files_eval10(root)
        out[f"{ev}/{arm}/{run}"] = {"checks": res, "tree": tree(root)}
    (HERE / "script-checks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, v in out.items():
        print(k, v["checks"])


def numbered(text):
    return "\n".join(f"{i:>4}  {line}" for i, line in enumerate(text.splitlines(), 1))


def packet(ev, root, kinds):
    checks = [c for c in BASELINE[ev] if c["kind"] in kinds]
    parts = [
        "# Judge packet",
        "",
        "Decide each check below as met or unmet from this packet alone.",
        "- A met check of kind `reply` must quote the literal words that satisfy it.",
        "- An unmet check records what you searched for and where.",
        "- A met check of kind `invention` has nothing to quote: record what you searched for.",
        "- Borderline is unmet. More text or more files never raise a verdict.",
        "",
        "## The user's message",
        "",
        PROMPTS[ev],
        "",
    ]
    if ev == "9":
        parts += ["## The document as it was before the run (" + ORIGINAL + ")", "", "```", numbered(FIXTURE.read_text(encoding="utf-8")), "```", ""]
    reply = root / "reply.md"
    parts += ["## The reply given to the user", "", "```", numbered(reply.read_text(encoding="utf-8")) if reply.exists() else "(no reply.md was written)", "```", ""]
    files = [f for f in tree(root) if f != "reply.md"]
    parts += ["## Files under the project root after the run", ""]
    if not files:
        parts += ["(none)", ""]
    for f in files:
        parts += [f"### {f}", "", "```", numbered((root / f).read_text(encoding="utf-8", errors="replace")), "```", ""]
    if "invention" in kinds and ANCHORS.get("invention"):
        parts += ["## Anchor cases for checks of kind `invention`", "", "Decide by analogy with these; they come from another run of the same task.", ""]
        parts += [f"- {a['verdict']}: {a['case']} Why: {a['why']}" for a in ANCHORS["invention"]]
        parts += [""]
    parts += ["## Checks", ""]
    parts += [f"- `{c['id']}` ({c['kind']}): {c['check']}" for c in checks]
    return "\n".join(parts) + "\n"


def cmd_packets():
    items = list(runs())
    random.Random(23).shuffle(items)
    out = HERE / "judge-inputs"
    out.mkdir(exist_ok=True)
    mapping = {}
    for i, (ev, arm, run, root) in enumerate(items, 1):
        pid = f"p{i:02d}"
        mapping[pid] = f"{ev}/{arm}/{run}"
        (out / f"{pid}-full.md").write_text(packet(ev, root, ("reply", "invention")), encoding="utf-8")
        (out / f"{pid}-invention.md").write_text(packet(ev, root, ("invention",)), encoding="utf-8")
    (HERE / "judge-map.json").write_text(json.dumps(mapping, indent=1) + "\n", encoding="utf-8")
    print(len(mapping), "packets")


def cmd_table():
    script = json.loads((HERE / "script-checks.json").read_text(encoding="utf-8"))
    mapping = json.loads((HERE / "judge-map.json").read_text(encoding="utf-8"))
    by_run = {v: k for k, v in mapping.items()}
    results, splits = {}, []
    for key, s in script.items():
        ev = key.split("/")[0]
        pid = by_run[key]
        passes = {}
        for f in sorted((HERE / "judge-outputs").glob(f"{pid}-pass*.json")):
            for v in json.loads(f.read_text(encoding="utf-8")):
                passes.setdefault(v["id"], []).append(v["verdict"].strip().lower() == "met")
        row = {}
        for c in BASELINE[ev]:
            if c["kind"] in ("file", "absence"):
                row[c["id"]] = {"kind": c["kind"], "met": bool(s["checks"][c["id"]])}
                continue
            votes = passes.get(c["id"], [])
            need = 3 if c["kind"] == "invention" else 1
            row[c["id"]] = {"kind": c["kind"], "met": len(votes) >= need and all(votes), "votes": f"{sum(votes)}/{len(votes)}"}
            if len(votes) < need:
                row[c["id"]]["note"] = "not scored: missing judge pass"
            elif 0 < sum(votes) < len(votes):
                splits.append({"run": key, "packet": pid, "id": c["id"], "votes": row[c["id"]]["votes"]})
        results[key] = row
    (HERE / "results.json").write_text(json.dumps({"runs": results, "splits": splits}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for ev in DIRS:
        for arm in ARMS:
            rows = [r for k, r in results.items() if k.startswith(f"{ev}/{arm}/")]
            kinds = {}
            for r in rows:
                for c in r.values():
                    m, t = kinds.get(c["kind"], (0, 0))
                    kinds[c["kind"]] = (m + c["met"], t + 1)
            total = (sum(m for m, _ in kinds.values()), sum(t for _, t in kinds.values()))
            unmet = sorted({f"{k.split('/')[-1]}:{i}" for k, r in results.items() if k.startswith(f"{ev}/{arm}/") for i, c in r.items() if not c["met"]})
            print(f"eval {ev} {arm}: {total[0]}/{total[1]}", {k: f"{m}/{t}" for k, (m, t) in kinds.items()}, "unmet:", unmet)
    print("splits:", splits)


if __name__ == "__main__":
    {"files": cmd_files, "packets": cmd_packets, "table": cmd_table}[sys.argv[1]]()
