#!/usr/bin/env python3
"""Decide the kind=file and kind=absence checks of iteration-27, and count what its
checks.json measures outside the met/unmet table.

  grade.py            -> script-checks.json ({"<eval>/<cell>/run-<n>": {"<check id>": bool}}),
                         which `eval-tools/judge.py table` merges with the judge's verdicts,
                         and observations.json (O.2 to O.4 and M.1 to M.4 per run, with tokens,
                         cost and turns)
  grade.py table      -> the observations per cell, from observations.json
  grade.py --self     -> the script checks on the untouched fixtures

Nothing is executed. 'The document' is the one new .md file under docs/design/; a check
on it is not met when there is none. The passive regex, the prose selection and the word
count are those of ../iteration-26/grade.py, copied so that O.2 and O.3 mean the same.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASE = json.load(open(os.path.join(HERE, "checks.json")))
CELLS = ("v160", "v170", "v160w", "v170w")
DESIGN = "docs/design"
ORIGINAL = "docs/design/exportacao-de-relatorios.md"
BODY_MARK = "## Visão geral"

PART = r"(?:\w+(?:ad|id)[oa]s?|feit[oa]s?|escrit[oa]s?|post[oa]s?|abert[oa]s?|vist[oa]s?|entregues?|aceit[oa]s?|pag[oa]s?)"
PASSIVE = re.compile(r"\b(?:é|são|foi|foram|será|serão|seja|sejam|sendo|era|eram)\s+(?:\w+mente\s+)?" + PART + r"\b", re.I)
AGENT = re.compile(r"\b(?:por|pelo|pela|pelos|pelas)\b", re.I)
DISCLAIMER = re.compile(r"não (?:foi |foram )?validad|not (?:machine-)?validated|apenas ilustra", re.I)
SE_FORM = re.compile(r"\b\w+-se\b", re.I)
INSTALL = re.compile(r"\b(?:apt(?:-get)?|brew|dnf|yum|pacman|snap|npm|pip3?|pipx)\s+(?:install|add|i)\b"
                     r"|\buv\s+tool\s+install\b|\bdocker\s+pull\b")
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def read(path):
    try:
        return open(path, encoding="utf-8", newline="").read()
    except OSError:
        return None


def fixture_dir(ev):
    return os.path.join(HERE, "fixtures", f"eval-{ev}")


def new_docs(ev, root):
    d = os.path.join(root, DESIGN)
    had = set(os.listdir(os.path.join(fixture_dir(ev), DESIGN))) if os.path.isdir(os.path.join(fixture_dir(ev), DESIGN)) else set()
    return sorted(os.path.join(d, f) for f in (os.listdir(d) if os.path.isdir(d) else [])
                  if f.endswith(".md") and f not in had)


def the_doc(ev, root):
    docs = new_docs(ev, root)
    return (docs[0], read(docs[0])) if len(docs) == 1 else (None, None)


def strip_blocks(text):
    """Drop fenced code and <details> blocks; what is left is what a reader sees as prose."""
    text = re.sub(r"<details>.*?</details>", "", text, flags=re.S | re.I)
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return "\n".join(out)


def sentences(line):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if s.strip()]


def prose_lines(text):
    for line in text.split("\n"):
        s = line.strip()
        if not s or s.startswith(("#", "|", "<", "![", "---")):
            continue
        yield line


def h2(text):
    return [l.rstrip()[3:].strip() for l in strip_blocks(text or "").split("\n") if l.startswith("## ")]


def in_order(want, got):
    it = iter(got)
    return all(w in it for w in want)


def has_dsl(text):
    return any("workspace" in m for m in re.findall(r"<details>.*?</details>", text or "", flags=re.S | re.I))


def mermaid_kinds(text):
    """First non-empty line of each fenced mermaid block."""
    out = []
    for m in re.finditer(r"```mermaid[^\n]*\n(.*?)```", text or "", flags=re.S):
        lines = [l.strip() for l in m.group(1).split("\n") if l.strip() and not l.strip().startswith("%%")]
        out.append(lines[0].split()[0] if lines else "")
    return out


def row(text, label):
    """The value cell of the header-table row with this bold label, or None."""
    m = re.search(r"^\|\s*\*\*" + re.escape(label) + r"\*\*\s*\|(.*)\|\s*$", text or "", flags=re.M)
    return m.group(1).strip() if m else None


def between(text, start, end, needle):
    lines = [l.rstrip() for l in strip_blocks(text or "").split("\n")]
    if start not in lines or end not in lines:
        return False
    a, b = lines.index(start), lines.index(end)
    return needle in lines[a:b]


def links_to(text, base, target):
    return any(os.path.realpath(os.path.join(base, m)) == os.path.realpath(target) for m in LINK.findall(text))


def eval9(root, timing):
    fixture = read(os.path.join(fixture_dir("9"), ORIGINAL))
    orig = os.path.join(root, ORIGINAL)
    orig_text = read(orig) or ""
    design = os.path.join(root, DESIGN)
    new = new_docs("9", root)
    one = new[0] if len(new) == 1 else None
    i = orig_text.find(BODY_MARK)
    head, body = (orig_text, "") if i < 0 else (orig_text[:i], orig_text[i:])
    changed = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(root, "docs")) for f in fs
               if not (os.path.join(d, f) == orig and orig_text == fixture)]
    dates = [x for p in changed for x in DATE.findall(read(p) or "")]
    run_dates = set(timing["dates"])
    known = set(DATE.findall(fixture)) | run_dates
    return {"9.1": len(new) == 1,
            "9.2": bool(body) and body == fixture[fixture.find(BODY_MARK):],
            "9.3": bool(one) and links_to(head, design, one),
            "9.4": bool(one) and links_to(read(one), design, orig),
            "9.5": bool(run_dates & set(dates)) and all(x in known for x in dates)}


def script(ev, root, timing):
    path, doc = the_doc(ev, root)
    n = len(new_docs(ev, root))
    prose = strip_blocks(doc) if doc else ""
    kinds = mermaid_kinds(doc)
    if ev == "1":
        return {"1.1": n == 1, "1.12": has_dsl(doc), "1.13": "![" in prose,
                "1.14": doc is not None and all(k == "sequenceDiagram" for k in kinds)}
    if ev == "4":
        name = os.path.basename(path).lower() if path else ""
        return {"4.1": n == 1,
                "4.2": in_order(["Resumo", "Contexto", "Proposta", "Riscos", "Plano de entrega"], h2(doc)),
                "4.3": between(doc, "## Proposta", "## Riscos", "### Compensações"),
                "4.4": "dd-2026-008" in name,
                "4.5": "DD-2026-008" in (row(doc, "Documento") or ""),
                "4.7": "INC-4412" in (doc or ""), "4.8": "429" in (doc or ""), "4.9": "Retry-After" in (doc or "")}
    if ev == "6":
        calls = timing.get("tool_calls") or []
        return {"6.1": n == 1, "6.3": has_dsl(doc), "6.4": "![" in prose,
                "6.5": doc is not None and all(k == "sequenceDiagram" for k in kinds),
                "6.6": "sequenceDiagram" in kinds,
                "6.7": doc is not None and DISCLAIMER.search(prose) is None,
                "6.9": not any(c["tool"] == "Bash" and INSTALL.search(c["target"]) for c in calls)}
    if ev == "7":
        heads = [re.sub(r"^#+\s*", "", l).strip().lower() for l in prose.split("\n") if re.match(r"#{1,6} ", l)]
        dates = DATE.findall(doc or "")
        return {"7.1": n == 1,
                "7.3": in_order(["Motivação", "Proposta", "Riscos", "Plano de rollout", "Métricas de sucesso",
                                 "Perguntas abertas"], h2(doc)),
                "7.4": all(row(doc, x) is not None for x in ("Documento", "Estado", "Autores", "Revisores",
                                                             "Criado em", "Última atualização")),
                "7.5": doc is not None and not any(h in ("visão geral", "escopo e contexto", "objetivos e fora de escopo")
                                                   for h in heads),
                "7.13": "Rafael Nunes" in (row(doc, "Autores") or ""),
                "7.14": "rascunho" in (row(doc, "Estado") or "").lower(),
                "7.15": bool(dates) and all(d in timing["dates"] for d in dates)}
    return eval9(root, timing)


def observe(ev, root, timing):
    _, doc = the_doc(ev, root)
    invoked = timing.get("skills_invoked") or []
    tw, un = ("technical-writing" in invoked), ("unslop" in invoked)
    out = {"M.1": "design-doc" in invoked, "M.2": tw, "M.3": un,
           "M.4": tw and un and invoked.index("technical-writing") < invoked.index("unslop"),
           "skills_invoked": invoked, "tokens": timing["total_tokens"], "output_tokens": timing.get("output_tokens"),
           "usd": timing["cost_usd"], "turns": timing["num_turns"], "seconds": timing["total_duration_seconds"]}
    if doc is None:
        return out
    body = strip_blocks(doc)
    passive, se = [], []
    for line in prose_lines(body):
        for s in sentences(line):
            passive += [m.group(0) for m in PASSIVE.finditer(s) if not AGENT.search(s[m.end():])]
            se += SE_FORM.findall(s)
    words = len(re.findall(r"\w+", body))
    out.update({"O.2": len(passive), "O.2_per_1000_words": round(1000 * len(passive) / max(words, 1), 1),
                "O.2_evidence": passive, "O.3": words, "O.4": len(se), "O.4_evidence": se})
    return out


def runs():
    for evdir in sorted(d for d in os.listdir(HERE) if re.match(r"eval-\d+", d)):
        ev = re.match(r"eval-(\d+)", evdir).group(1)
        for cell in CELLS:
            base = os.path.join(HERE, evdir, cell)
            for run in sorted(os.listdir(base)) if os.path.isdir(base) else []:
                rundir = os.path.join(base, run)
                if os.path.exists(os.path.join(rundir, "response.md")):
                    yield ev, cell, run, rundir


def table():
    obs = json.load(open(os.path.join(HERE, "observations.json")))
    evs = sorted({k.split("/")[0] for k in obs}, key=int)
    def cell(ev, c, field):
        return ", ".join(str(obs[k].get(field, "-")) for k in sorted(obs) if k.startswith(f"{ev}/{c}/"))
    for field, label in [("O.2", "agentless passives"), ("O.2_per_1000_words", "per 1000 words"), ("O.3", "words"),
                         ("O.4", "'-se' forms"), ("tokens", "tokens"), ("usd", "US$"), ("turns", "turns")]:
        print(f"\n{label} per run\n\n| Eval | " + " | ".join(CELLS) + " |\n|---|" + "---|" * len(CELLS))
        for ev in evs:
            print(f"| {ev} | " + " | ".join(cell(ev, c, field) or "-" for c in CELLS) + " |")
    print("\nmechanics (runs meeting it / runs)\n\n| | " + " | ".join(CELLS) + " |\n|---|" + "---|" * len(CELLS))
    for m in ("M.1", "M.2", "M.3", "M.4"):
        line = []
        for c in CELLS:
            rs = [v for k, v in obs.items() if k.split("/")[1] == c]
            line.append(f"{sum(bool(r[m]) for r in rs)}/{len(rs)}")
        print(f"| {m} | " + " | ".join(line) + " |")


def main():
    if sys.argv[1:] == ["table"]:
        return table()
    if sys.argv[1:] == ["--self"]:
        for ev in ("1", "4", "6", "7", "9"):
            print(ev, script(ev, fixture_dir(ev), {"dates": ["2026-11-22"], "tool_calls": []}))
        return
    checks, obs = {}, {}
    for ev, cell, run, rundir in runs():
        timing = json.load(open(os.path.join(rundir, "timing.json")))
        res = script(ev, os.path.join(rundir, "outputs"), timing)
        ids = [c["id"] for c in BASE["evals"][ev] if c["kind"] in ("file", "absence")]
        if sorted(ids) != sorted(res):
            sys.exit(f"eval {ev}: rules {sorted(res)} do not match the script checks {sorted(ids)}")
        checks[f"{ev}/{cell}/{run}"] = {i: bool(res[i]) for i in ids}
        obs[f"{ev}/{cell}/{run}"] = observe(ev, os.path.join(rundir, "outputs"), timing)
    json.dump(checks, open(os.path.join(HERE, "script-checks.json"), "w"), indent=2)
    json.dump(obs, open(os.path.join(HERE, "observations.json"), "w"), ensure_ascii=False, indent=1)
    met = sum(v for r in checks.values() for v in r.values())
    print(f"{len(checks)} runs, {met}/{sum(len(r) for r in checks.values())} script checks met -> script-checks.json")


if __name__ == "__main__":
    main()
