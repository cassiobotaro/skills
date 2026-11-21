#!/usr/bin/env python3
"""Decide the kind=file and kind=absence checks of iteration-1 from the bytes each run left.

Writes script-checks.json ({"<eval>/<cell>/run-<n>": {"<check id>": true|false}}), which
`eval-tools/judge.py table` merges with the judge's verdicts. The checks are the 8 of those
two kinds in ../evals/checks-baseline.json; a check with no rule here fails the script.
Nothing is executed: every rule reads a file or the reply. A missing file is a check not
met.

"Emoji" is decided by code point: U+1F000 to U+1FAFF, U+2600 to U+27BF, U+2B50, U+2B55 and
the variation selector U+FE0F. That counts a dingbat such as U+2713 (a check mark) and does
not count arrows or box-drawing characters.

Usage: grade.py            grade every run found under eval-*/
       grade.py --self     run the rules on the untouched fixtures and on sample replies
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))
FILES = os.path.join(WS, "evals", "files")
RATELIMIT = ["ratelimit/api.py", "ratelimit/limiter.py"]
THREAD = "suporte/thread.md"
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⭐⭕️]")
HEADING = re.compile(r"^\s*#", re.M)
LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s)", re.M)


def raw(root, rel):
    try:
        return open(os.path.join(root, rel), "rb").read()
    except OSError:
        return None


def same(root, rel):
    return raw(root, rel) is not None and raw(root, rel) == raw(FILES, rel)


def files(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


# r is the project root after the run, reply the text of the reply.
RULES = {
    "1.7": lambda r, reply: not EMOJI.search(reply),
    "3.6": lambda r, reply: all(same(r, f) for f in RATELIMIT),
    "3.7": lambda r, reply: files(r) == RATELIMIT,
    "6.1": lambda r, reply: "5432" in reply,
    "6.3": lambda r, reply: not HEADING.search(reply),
    "6.4": lambda r, reply: not LIST_ITEM.search(reply),
    "9.13": lambda r, reply: same(r, THREAD),
    "10.9": lambda r, reply: not EMOJI.search(reply),
}


def grade(ev, root, reply):
    ids = [c["id"] for c in BASE["evals"][ev] if c["kind"] in ("file", "absence")]
    missing = [i for i in ids if i not in RULES]
    if missing:
        sys.exit(f"no rule for script checks {missing}")
    return {i: bool(RULES[i](root, reply)) for i in ids}


def main():
    if sys.argv[1:] == ["--self"]:
        print("3 on the fixture:", grade("3", FILES, ""), "(3.7 is false there: files/ holds every fixture)")
        print("9 on the fixture:", grade("9", FILES, ""))
        for label, reply in (("plain", "A porta padrão é 5432."),
                             ("decorated", "# Resposta\n\n- A porta é 5432 \U0001F680\n1. veja a doc"),
                             ("check mark", "Certo ✓, e a seta → não conta.")):
            print(label, "| 6:", grade("6", FILES, reply), "| emoji-free:", RULES["1.7"](FILES, reply))
        return
    out = {}
    for evdir in sorted(d for d in os.listdir(HERE) if re.match(r"eval-\d+", d)):
        ev = re.match(r"eval-(\d+)", evdir).group(1)
        for cell in sorted(os.listdir(os.path.join(HERE, evdir))):
            for run in sorted(os.listdir(os.path.join(HERE, evdir, cell))):
                rundir = os.path.join(HERE, evdir, cell, run)
                try:
                    reply = open(os.path.join(rundir, "response.md"), encoding="utf-8").read()
                except OSError:
                    continue
                out[f"{ev}/{cell}/{run}"] = grade(ev, os.path.join(rundir, "outputs"), reply)
    json.dump(out, open(os.path.join(HERE, "script-checks.json"), "w"), indent=2)
    met = sum(v for r in out.values() for v in r.values())
    print(f"{len(out)} runs, {met}/{sum(len(r) for r in out.values())} script checks met -> script-checks.json")


if __name__ == "__main__":
    main()
