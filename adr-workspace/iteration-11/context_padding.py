#!/usr/bin/env python3
"""Score one defect over the eval-10 runs: a Context that says more than the user gave.

The user's message establishes exactly this for Context: login attempts are limited per
account, the limit is 5 per 15 minutes, the alternative place was the API gateway, and
the gateway cannot see account ids. Anything else in Context is padding.

The script flags a Context when it matches a pattern for the two kinds of filler seen in
iteration-9 (a motive; a general truth about where rate limiting belongs). It also
prints every Context, so the flags can be checked by reading all of them: the patterns
are a net, not the verdict.
"""
import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MOTIVE = re.compile(r"\bto (slow|prevent|protect|stop|deter|defend|guard|mitigate|reduce|block|limit abuse)|brute|guess|credential|attack|abuse|security|stuffing", re.I)
GENERAL = re.compile(r"\b(usual|usually|obvious|natural|typical|typically|standard|common|commonly|normally|traditional|conventional|default place|often)\b", re.I)


def context(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"## Context\n(.*?)\n## Decision", t, re.S)
    return " ".join(m.group(1).split()) if m else ""


rows = []
for run in sorted(glob.glob(os.path.join(HERE, "eval-10-*", "*", "run-*")), key=lambda p: (p.split(os.sep)[-2], int(p.rsplit("-", 1)[1]))):
    new = glob.glob(os.path.join(run, "outputs", "doc", "adr", "0004-*.md"))
    cfg, r = run.split(os.sep)[-2], run.split(os.sep)[-1]
    if len(new) != 1:
        rows.append({"config": cfg, "run": r, "context": None, "flags": ["no single 0004 file"]}); continue
    c = context(new[0])
    flags = [name for name, rx in (("motive", MOTIVE), ("general", GENERAL)) if rx.search(c)]
    rows.append({"config": cfg, "run": r, "words": len(c.split()), "flags": flags, "context": c})
    print(f"{cfg:10} {r:7} {len(c.split()):3}w {','.join(flags) or '-':15} {c}")
json.dump(rows, open(os.path.join(HERE, "context-padding.json"), "w"), ensure_ascii=False, indent=2)
for cfg in ("with_skill", "old_skill"):
    rs = [x for x in rows if x["config"] == cfg and x["context"] is not None]
    print(f"\n{cfg}: flagged {sum(bool(x['flags']) for x in rs)}/{len(rs)}, median words {sorted(x['words'] for x in rs)[len(rs)//2] if rs else 0}")
