#!/usr/bin/env python3
"""Decide the kind=file and kind=absence checks of iteration-28 for every run in runs.json.

Eval 71 uses the rules iteration-27 wrote for eval 7 (../iteration-27/grade.py), unchanged.
Eval 7 has one script check, 7.G1: the session wrote no file. Writes script-checks.json.

Usage: grade.py [batch-dir]   (default: this directory; a batch directory holds its own
                               runs.json, with paths relative to it)
"""
import importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("grade27", os.path.join(HERE, "..", "iteration-27", "grade.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def tree(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


BATCH = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
out = {}
for run in json.load(open(os.path.join(BATCH, "runs.json")))["runs"]:
    root = os.path.join(BATCH, run["root"])
    if not os.path.exists(os.path.join(BATCH, run["reply"])):
        continue
    timing = json.load(open(os.path.join(os.path.dirname(root), "timing.json")))
    if run["eval"] == "71":
        out[run["key"]] = {k: bool(v) for k, v in g.script("7", root, timing).items()}
    else:
        out[run["key"]] = {"7.G1": tree(root) == ["docs/design/TEMPLATE.md"]}
json.dump(out, open(os.path.join(BATCH, "script-checks.json"), "w"), indent=2)
met = sum(v for r in out.values() for v in r.values())
print(f"{len(out)} runs, {met}/{sum(len(r) for r in out.values())} script checks met -> script-checks.json")
