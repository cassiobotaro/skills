#!/usr/bin/env python3
"""iteration-26 grader: file, style and observation checks of checks.json, from bytes.

Usage (repo root):
  python3 design-doc-workspace/iteration-26/grade.py script   # writes script-checks.json and
                                                               # judge-inputs/candidates.json (blind)
  python3 design-doc-workspace/iteration-26/grade.py table    # prints the per-cell table; adds R.1
                                                               # when judge-outputs/reading.json exists
Read-only over the run outputs.
"""
import glob, json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = "eval-6-no-renderer-keeps-placeholder-no-disclaimer"
CELLS = ["a-sonnet", "b-sonnet", "a-haiku", "b-haiku"]

PART = r"(?:\w+(?:ad|id)[oa]s?|feit[oa]s?|escrit[oa]s?|post[oa]s?|abert[oa]s?|vist[oa]s?|entregues?|aceit[oa]s?|pag[oa]s?)"
PASSIVE = re.compile(r"\b(?:é|são|foi|foram|será|serão|seja|sejam|sendo|era|eram)\s+(?:\w+mente\s+)?" + PART + r"\b", re.I)
AGENT = re.compile(r"\b(?:por|pelo|pela|pelos|pelas)\b", re.I)
ANNOUNCE = re.compile(r"\b(?:este|neste|esse|nesse|o presente|this)\s+(?:documento|doc|design doc|document)\b", re.I)
DISCLAIMER = re.compile(r"não (?:foi |foram )?validad|not (?:machine-)?validated|apenas ilustra", re.I)
BOLD1 = re.compile(r"\*\*([^*\s]+)\*\*")
LABEL_START = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|>\s*)?\*\*")
COLON = re.compile(r"(?<![:/\d])[:](?=\s+\S)")


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


def words(text):
    return len(re.findall(r"\w+", text))


def sentences(line):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if s.strip()]


def prose_lines(text):
    """Lines of running prose: no headings, table rows, html, or blank lines."""
    for line in text.split("\n"):
        s = line.strip()
        if not s or s.startswith(("#", "|", "<", "![", "---")):
            continue
        yield line


def doc_of(run):
    root = os.path.join(run, "outputs", "docs", "design")
    return sorted(glob.glob(os.path.join(root, "*.md")))


def grade(run):
    r = {}
    docs = doc_of(run)
    r["F.1"] = {"passed": len(docs) == 1, "evidence": [os.path.relpath(d, run) for d in docs] or "no .md under outputs/docs/design/"}
    if len(docs) != 1:
        return r, []
    raw = open(docs[0], encoding="utf-8").read()
    body = strip_blocks(raw)
    has_dsl = any("workspace" in m for m in re.findall(r"<details>.*?</details>", raw, flags=re.S | re.I))
    r["F.2"] = {"passed": "```mermaid" in raw and "![" in raw and has_dsl,
                "evidence": {"mermaid": "```mermaid" in raw, "image": "![" in raw, "details_with_dsl": has_dsl}}
    m = DISCLAIMER.search(body)
    r["F.3"] = {"passed": m is None, "evidence": m.group(0) if m else "regex DISCLAIMER over the prose: no hit"}

    n_em = body.count("—")
    r["T.1"] = {"passed": n_em <= 2, "count": n_em}

    bold = []
    for line in prose_lines(body):
        for m in BOLD1.finditer(line):
            inner, after = m.group(1), line[m.end():m.end() + 1]
            if inner.endswith(":") or after == ":":
                continue
            if LABEL_START.match(line) and line.index("**") == m.start():
                continue
            bold.append(m.group(0))
    r["T.2"] = {"passed": not bold, "count": len(bold), "evidence": bold[:12]}

    heads = [m.start() for m in re.finditer(r"^## ", body, flags=re.M)]
    top = body[:heads[1]] if len(heads) > 1 else body
    hits = [s for line in prose_lines(top) for s in sentences(line) if ANNOUNCE.search(s)]
    r["T.3"] = {"passed": not hits, "evidence": hits[:3] or "regex ANNOUNCE before the second '## ': no hit"}

    r["O.1"] = {"count": len(re.findall(r"\s–\s", body))}
    n_words = words(body)
    passive, cands = [], []
    for line in prose_lines(body):
        for s in sentences(line):
            for m in PASSIVE.finditer(s):
                if not AGENT.search(s[m.end():]):
                    passive.append(m.group(0))
            # colon-reveal candidates: a colon mid-sentence, text after it, not a list lead-in or label
            plain = re.sub(r"`[^`]*`", "", s)
            if LABEL_START.match(plain) or plain.rstrip().endswith(":"):
                continue
            if COLON.search(re.sub(r"\*\*[^*]*:\*\*|\*\*[^*]*\*\*:", "", plain)):
                cands.append(s)
    r["O.2"] = {"count": len(passive), "per_1000_words": round(1000 * len(passive) / max(n_words, 1), 1), "evidence": passive[:8]}
    r["O.3"] = {"count": n_words}
    return r, cands


def all_runs():
    for cell in CELLS:
        for run in sorted(glob.glob(os.path.join(HERE, EVAL, cell, "run-*"))):
            yield cell, run


def script():
    results, packets = {}, []
    for cell, run in all_runs():
        key = f"{cell}/{os.path.basename(run)}"
        results[key], cands = grade(run)
        packets += [(key, c) for c in cands]
    json.dump(results, open(os.path.join(HERE, "script-checks.json"), "w"), ensure_ascii=False, indent=1)
    random.Random(26).shuffle(packets)
    os.makedirs(os.path.join(HERE, "judge-inputs"), exist_ok=True)
    blind = [{"id": f"c{i:03d}", "sentence": s} for i, (_, s) in enumerate(packets, 1)]
    json.dump(blind, open(os.path.join(HERE, "judge-inputs", "candidates.json"), "w"), ensure_ascii=False, indent=1)
    json.dump({f"c{i:03d}": k for i, (k, _) in enumerate(packets, 1)}, open(os.path.join(HERE, "judge-map.json"), "w"), indent=1)
    print(f"{len(results)} runs graded, {len(blind)} colon candidates written blind")


def table():
    res = json.load(open(os.path.join(HERE, "script-checks.json")))
    reading = {}
    p = os.path.join(HERE, "judge-outputs", "reading.json")
    if os.path.exists(p):
        jmap = json.load(open(os.path.join(HERE, "judge-map.json")))
        for cid, v in json.load(open(p)).items():
            if v.get("reveal"):
                reading[jmap[cid]] = reading.get(jmap[cid], 0) + 1
    rows = ["F.1", "F.2", "F.3", "T.1", "T.2", "T.3"]
    print("| Check | " + " | ".join(CELLS) + " |\n|---|" + "---|" * len(CELLS))
    cell_runs = {c: [k for k in sorted(res) if k.startswith(c + "/")] for c in CELLS}
    for cid in rows:
        print(f"| {cid} | " + " | ".join(
            f"{sum(1 for k in cell_runs[c] if res[k].get(cid, {}).get('passed'))}/{len(cell_runs[c])}" for c in CELLS) + " |")
    for cid, label in [("T.1", "em dashes per run"), ("T.2", "one-word bold per run"), ("O.1", "spaced en dashes per run"),
                       ("O.2", "agentless passives per run"), ("O.3", "words per run")]:
        print(f"| {cid} {label} | " + " | ".join(
            ", ".join(str(res[k].get(cid, {}).get("count", "-")) for k in cell_runs[c]) for c in CELLS) + " |")
    print("| O.2 per 1000 words | " + " | ".join(
        ", ".join(str(res[k].get("O.2", {}).get("per_1000_words", "-")) for k in cell_runs[c]) for c in CELLS) + " |")
    if os.path.exists(p):
        print("| R.1 colon reveals per run | " + " | ".join(
            ", ".join(str(reading.get(k, 0)) for k in cell_runs[c]) for c in CELLS) + " |")
        print("| R.1 met (0 reveals) | " + " | ".join(
            f"{sum(1 for k in cell_runs[c] if reading.get(k, 0) == 0)}/{len(cell_runs[c])}" for c in CELLS) + " |")


if __name__ == "__main__":
    {"script": script, "table": table}[sys.argv[1] if len(sys.argv) > 1 else "script"]()
