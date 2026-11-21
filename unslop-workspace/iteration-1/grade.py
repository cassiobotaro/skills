#!/usr/bin/env python3
"""Decide the kind=file and kind=absence checks of iteration-1 from the bytes each run left.

Writes script-checks.json ({"<eval>/<cell>/run-<n>": {"<check id>": true|false}}), which
`eval-tools/judge.py table` merges with the judge's verdicts. The checks are the 18 of
those two kinds in ../evals/checks-baseline.json; a check with no rule here fails the
script. Nothing is executed: every rule reads a file or the reply. A missing file is a
check not met.

Usage: grade.py            grade every run found under eval-*/
       grade.py --self     grade the untouched fixtures, to see the checks discriminate
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))
README_FX = os.path.join(WS, "evals", "files", "readme-en")
LOG_FX = os.path.join(WS, "evals", "files", "decision-log")
ADR = "doc/adr/0002-use-redis-for-sessions.md"
QUOTE = '"the sync is a crucial, robust safety net — not just a script"'


def read(root, rel):
    try:
        return open(os.path.join(root, rel), encoding="utf-8", newline="").read()
    except OSError:
        return None


def raw(root, rel):
    try:
        return open(os.path.join(root, rel), "rb").read()
    except OSError:
        return None


def files(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


def bash_block():
    lines = read(README_FX, "README.md").split("\n")
    a = lines.index("```bash")
    return "\n".join(lines[a:lines.index("```", a + 1) + 1])


def prose(text):
    """README text with fenced blocks and double-quoted passages removed, lowercased."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r'"[^"\n]*"|“[^”\n]*”', " ", text)
    return text.replace("’", "'").lower()


def lacks(root, rel, phrase, strip=False):
    t = read(root, rel)
    return t is not None and phrase.lower() not in (prose(t) if strip else t.lower())


def has(root, rel, needle):
    t = read(root, rel)
    return t is not None and needle in t


# r is the project root after the run, reply the text of the reply.
RULES = {
    "1.2": lambda r, reply: "`cache.flush_all()`" in reply,
    "2.1": lambda r, reply: raw(r, "README.md") is not None and raw(r, "README.md") != raw(README_FX, "README.md"),
    "2.2": lambda r, reply: files(r) == ["README.md"],
    "2.3": lambda r, reply: (read(r, "README.md") is not None
                             and "\n" + bash_block() + "\n" in "\n" + read(r, "README.md") + "\n"),
    "2.4": lambda r, reply: has(r, "README.md", QUOTE),
    "2.5": lambda r, reply: (read(r, "README.md") or "").split("\n")[0] == "# Ledger sync",
    "2.6": lambda r, reply: has(r, "README.md", "`ledger_snapshots`"),
    "2.7": lambda r, reply: lacks(r, "README.md", "In today's fast-paced world", strip=True),
    "2.8": lambda r, reply: lacks(r, "README.md", "serves as", strip=True),
    "2.9": lambda r, reply: lacks(r, "README.md", "not just", strip=True),
    "2.10": lambda r, reply: lacks(r, "README.md", "In conclusion", strip=True),
    "2.11": lambda r, reply: lacks(r, "README.md", "Let me know if", strip=True),
    "2.14": lambda r, reply: "README.md" in reply,
    "3.1": lambda r, reply: raw(r, ADR) is not None and raw(r, ADR) == raw(LOG_FX, ADR),
    "3.2": lambda r, reply: lacks(r, "notes.md", "In order to"),
    "3.3": lambda r, reply: lacks(r, "notes.md", "it is worth noting that"),
    "3.4": lambda r, reply: lacks(r, "notes.md", "serves as"),
    "3.6": lambda r, reply: has(r, "notes.md", ADR),
}


def grade(ev, root, reply):
    ids = [c["id"] for c in BASE["evals"][ev] if c["kind"] in ("file", "absence")]
    missing = [i for i in ids if i not in RULES]
    if missing:
        sys.exit(f"no rule for script checks {missing}")
    return {i: bool(RULES[i](root, reply)) for i in ids}


def main():
    if sys.argv[1:] == ["--self"]:
        print("2", grade("2", README_FX, ""))
        print("3", grade("3", LOG_FX, ""))
        return
    out = {}
    for evdir in sorted(d for d in os.listdir(HERE) if re.match(r"eval-\d+", d)):
        ev = re.match(r"eval-(\d+)", evdir).group(1)
        for cell in sorted(os.listdir(os.path.join(HERE, evdir))):
            for run in sorted(os.listdir(os.path.join(HERE, evdir, cell))):
                rundir = os.path.join(HERE, evdir, cell, run)
                reply = read(rundir, "response.md")
                if reply is not None:
                    out[f"{ev}/{cell}/{run}"] = grade(ev, os.path.join(rundir, "outputs"), reply)
    json.dump(out, open(os.path.join(HERE, "script-checks.json"), "w"), indent=2)
    met = sum(v for r in out.values() for v in r.values())
    print(f"{len(out)} runs, {met}/{sum(len(r) for r in out.values())} script checks met -> script-checks.json")


if __name__ == "__main__":
    main()
