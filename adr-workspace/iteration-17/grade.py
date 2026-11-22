#!/usr/bin/env python3
"""Grade iteration-17 from the bytes on disk.

  grade.py script    mech.json (the checks of checks.json, every eval), script-checks.json
                     (the file/absence checks of evals 11 and 12 in ../evals/checks-baseline.json,
                     for judge.py table) and runs.json (evals 11 and 12, for judge.py)
  grade.py summary   one table per eval from mech.json, and the cost per cell

"The decision ADR" is the new Markdown file with the highest number in its name (or the
only new one), wherever the run put it, so a wrong directory fails `loc` and not every
check after it.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
EVALS = {str(e["id"]): e for e in json.load(open(os.path.join(WS, "evals", "evals.json")))["evals"]}
CELLS = ("no_skill", "skill_150", "skill_160")
HEADINGS = ["## Status", "## Context", "## Decision", "## Consequences"]
# eval -> (directory, number, language) expected of the decision ADR
WANT = {"1": ("doc/adr", 2, "pt"), "5": ("doc/adr", 2, "pt"), "7": ("doc/adr", 2, "en"),
        "3": ("doc/adr", 4, "en"), "4": ("docs/architecture/decisions", 3, "en"),
        "6": ("doc/adr", 3, "en"), "11": ("doc/adr", 3, "en"), "12": ("doc/adr", 3, "en")}
SEEDED = ("1", "5", "7")
PT = {"que", "não", "para", "uma", "com", "os", "as", "em", "é", "são", "de", "do", "da", "já", "nos"}
EN = {"the", "and", "of", "to", "we", "is", "are", "that", "will", "for", "in", "on", "with"}


def tree(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = open(p, "rb").read()
    return out


def fixture(ev):
    return {"/".join(rel.split("/")[2:]): open(os.path.join(WS, "evals", rel), "rb").read() for rel in EVALS[ev]["files"]}


def headings(text):
    out, fenced = [], False
    for i, line in enumerate(text.split("\n")):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and re.match(r"#{1,6} ", line):
            out.append((i, line.rstrip()))
    return out


def status_span(text):
    hs = headings(text)
    for j, (i, line) in enumerate(hs):
        if line == "## Status":
            return i + 1, hs[j + 1][0] if j + 1 < len(hs) else len(text.split("\n"))
    return None


def status_lines(text):
    span = status_span(text)
    return None if span is None else [l.rstrip() for l in text.split("\n")[span[0]:span[1]] if l.strip()]


def outside_status(text):
    span = status_span(text)
    lines = text.split("\n")
    return None if span is None else (lines[:span[0]], lines[span[1]:])


def slug(title):
    """adr-tools' own derivation: ASCII letters and digits kept, every other run one hyphen."""
    return re.sub(r"[^a-z0-9]+", "-", "".join(c.lower() if c.isascii() else "-" for c in title)).strip("-")


def language(text):
    span = status_span(text)
    lines = text.split("\n")
    body = [l for i, l in enumerate(lines) if not l.startswith(("#", "Date:")) and not (span and span[0] <= i < span[1])]
    words = re.findall(r"[a-zà-ÿ]+", " ".join(body).lower())
    return "pt" if sum(w in PT for w in words) > sum(w in EN for w in words) else "en"


def blank_discipline(text):
    lines = text.rstrip("\n").split("\n")
    if any(a == "" and b == "" for a, b in zip(lines, lines[1:])):
        return False
    marks = [i for i, _ in headings(text)] + [i for i, l in enumerate(lines) if l.startswith("Date: ")]
    return all((i == 0 or lines[i - 1] == "") and (i + 1 >= len(lines) or lines[i + 1] == "") for i in marks)


def fmt(path, text, dates):
    """The format checks of one ADR file."""
    lines = text.split("\n")
    base = os.path.basename(path)
    m = re.fullmatch(r"# ([1-9][0-9]*)\. (.+)", lines[0].rstrip())
    f = re.fullmatch(r"(\d{4})-(.+)\.md", base)
    d = re.search(r"^Date: (\d{4}-\d{2}-\d{2})$", text, re.M)
    return {"h1": bool(m and f and int(m.group(1)) == int(f.group(1))),
            "slug": bool(m and f and f.group(2) == slug(m.group(2))),
            "date": bool(d and d.group(1) in dates),
            "heads": [h for _, h in headings(text)][1:] == HEADINGS,
            "blank": blank_discipline(text)}


def number(path):
    m = re.match(r"(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else -1


def grade(ev, rundir):
    timing = json.load(open(os.path.join(rundir, "timing.json")))
    before, after = fixture(ev), tree(os.path.join(rundir, "outputs"))
    new = sorted(p for p in after if p not in before)
    if ev == "2":
        reply = open(os.path.join(rundir, "response.md"), encoding="utf-8").read()
        return {"nofile": not new and after == before, "asks": reply.count("?") >= 2}, timing
    c = {}
    mds = [p for p in new if p.endswith(".md")]
    adr = max(mds, key=number) if mds else None
    text = after[adr].decode("utf-8", "replace") if adr else ""
    want_dir, want_n, want_lang = WANT[ev]
    c["loc"] = bool(adr) and os.path.dirname(adr) == want_dir and bool(re.match(rf"{want_n:04d}-", os.path.basename(adr)))
    if adr:
        c.update(fmt(adr, text, timing["dates"]))
    else:
        c.update({k: False for k in ("h1", "slug", "date", "heads", "blank")})
    expected = ["Accepted"]
    if ev == "3":
        expected.append("Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)")
    c["status"] = bool(adr) and status_lines(text) == expected
    c["lang"] = bool(adr) and language(text) == want_lang
    seed = None
    if ev in SEEDED:
        seeds = [p for p in mds if p != adr and os.path.dirname(p) == "doc/adr" and os.path.basename(p).startswith("0001-")]
        seed = seeds[0] if seeds else None
        stext = after[seed].decode("utf-8", "replace") if seed else ""
        c["seed"] = bool(seed) and "documenting-architecture-decisions" in stext and "adr-tools" in stext
        sf = fmt(seed, stext, timing["dates"]) if seed else {}
        c["seed_format"] = bool(seed) and all(sf[k] for k in ("h1", "slug", "date", "heads")) and status_lines(stext) == ["Accepted"]
        if ev == "7":
            canon = open(os.path.join(WS, "skill-snapshot-1.5.0", "references", "examples.md"), encoding="utf-8").read()
            canon = canon.split("```markdown\n")[1].split("```")[0]
            c["seed_verbatim"] = bool(seed) and re.sub(r"Date: \S+", "Date: X", stext).strip() == re.sub(r"Date: \S+", "Date: X", canon).strip()
        else:
            c["seed_pt"] = bool(seed) and language(stext) == "pt"
    kept = lambda skip=(): all(after.get(p) == data for p, data in before.items() if p not in skip)
    if ev == "3":
        old = "doc/adr/0002-store-sessions-in-redis.md"
        was, now = before[old].decode(), after.get(old, b"").decode("utf-8", "replace")
        link = f"Superseded by [{text.split(chr(10))[0][2:]}]({os.path.basename(adr)})" if adr else None
        c["old_status"] = status_lines(now) == [link]
        c["old_body"] = kept((old,)) and outside_status(now) is not None and outside_status(now) == outside_status(was)
    elif before:
        c["old"] = kept()
    c["only"] = set(new) == {p for p in (adr, seed) if p} and bool(adr)
    return c, timing


def runs():
    for evdir in sorted(os.listdir(HERE)):
        m = re.match(r"eval-(\d+)-", evdir)
        if not m:
            continue
        for cell in CELLS:
            d = os.path.join(HERE, evdir, cell)
            for run in sorted(os.listdir(d)) if os.path.isdir(d) else []:
                if os.path.exists(os.path.join(d, run, "timing.json")):
                    yield m.group(1), cell, run, os.path.join(d, run)


def script():
    mech, frozen, manifest, cost = {}, {}, [], {}
    for ev, cell, run, d in runs():
        key = f"{ev}/{cell}/{run}"
        c, t = grade(ev, d)
        mech[key] = c
        cost[key] = {"tokens": t["total_tokens"], "first_turn_tokens": t["first_turn_tokens"], "usd": t["cost_usd"],
                     "turns": t["num_turns"], "read": t["skill_files_read"], "answered": t["answered"],
                     "denials": len(t["permission_denials"]), "models": t["models"],
                     "adr_listed": any("adr" == s or s.endswith(":adr") for s in t["skills_listed"] or [])}
        if ev == "11":
            frozen[key] = {"11.1": c["loc"] and c["only"], "11.2": c["h1"] and c["slug"], "11.3": c["date"], "11.4": c["heads"],
                           "11.5": c["status"], "11.6": c["blank"], "11.11": c["old"], "11.12": c["only"]}
        if ev == "12":
            frozen[key] = {"12.1": os.path.isdir(os.path.join(d, "outputs-before-answer")),
                           "12.3": c["loc"] and c["slug"] and c["h1"] and c["only"],
                           "12.4": c["date"] and c["heads"] and c["status"] and c["blank"],
                           "12.7": c["old"] and c["only"]}
        if ev in ("11", "12"):
            manifest.append({"key": key, "eval": ev, "cell": cell, "reply": os.path.relpath(os.path.join(d, "response.md"), HERE),
                             "root": os.path.relpath(os.path.join(d, "outputs"), HERE), "fixture": "../evals/files/english-log"})
    dump = lambda name, data: json.dump(data, open(os.path.join(HERE, name), "w"), indent=1, ensure_ascii=False)
    dump("mech.json", mech)
    dump("cost.json", cost)
    dump("script-checks.json", frozen)
    dump("runs.json", {"checks": "../evals/checks-baseline.json", "evals": "../evals/evals.json", "runs": manifest})
    print(len(mech), "runs graded")


def summary():
    mech = json.load(open(os.path.join(HERE, "mech.json")))
    cost = json.load(open(os.path.join(HERE, "cost.json")))
    cells = [c for c in CELLS if any(k.split("/")[1] == c for k in mech)]
    for ev in sorted({k.split("/")[0] for k in mech}, key=int):
        print(f"\neval {ev} {EVALS[ev]['name']} (runs meeting the check / runs)\n\n| Check | " + " | ".join(cells) + " |\n|---|" + "---|" * len(cells))
        rows = {c: [v for k, v in mech.items() if k.startswith(f"{ev}/{c}/")] for c in cells}
        for check in next(iter(rows[cells[0]]), {}):
            print(f"| {check} | " + " | ".join(f"{sum(r.get(check, False) for r in rows[c])}/{len(rows[c])}" for c in cells) + " |")
    print("\ncost per run (mean over the runs of the cell; eval 12 counted by its first turn only)\n\n| | " + " | ".join(cells) + " |\n|---|" + "---|" * len(cells))
    rows = {c: [v for k, v in cost.items() if k.split("/")[1] == c] for c in cells}
    line = lambda label, f: print(f"| {label} | " + " | ".join(f(rows[c]) for c in cells) + " |")
    line("runs", lambda r: str(len(r)))
    line("tokens, thousands", lambda r: f"{sum(x['first_turn_tokens'] for x in r) / len(r) / 1000:.0f}")
    line("US$ total", lambda r: f"{sum(x['usd'] for x in r):.2f}")
    line("runs that read references/examples.md", lambda r: f"{sum('references/examples.md' in x['read'] for x in r)}/{len(r)}")
    line("runs with a denied tool call", lambda r: f"{sum(x['denials'] > 0 for x in r)}/{len(r)}")
    line("runs that listed an adr skill", lambda r: f"{sum(x['adr_listed'] for x in r)}/{len(r)}")
    print("models:", sorted({m for v in cost.values() for m in v["models"]}))


if __name__ == "__main__":
    {"script": script, "summary": summary}[sys.argv[1]]()
