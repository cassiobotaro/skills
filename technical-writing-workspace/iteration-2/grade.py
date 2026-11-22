#!/usr/bin/env python3
"""Decide the kind=file and kind=absence checks for every run listed in runs.json.

The rules are iteration-1's (../iteration-1/grade.py), unchanged. This script only walks
runs.json instead of the eval-*/ directories, because the batch also holds runs of
iteration-1 that are re-judged from where they are. Writes script-checks.json.
"""
import importlib.util, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("grade1", os.path.join(HERE, "..", "iteration-1", "grade.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

out = {}
for run in json.load(open(os.path.join(HERE, "runs.json")))["runs"]:
    reply = g.read(HERE, run["reply"])
    if reply is None:
        continue
    timing = json.loads(g.read(os.path.dirname(os.path.join(HERE, run["reply"])), "timing.json") or "null")
    out[run["key"]] = g.grade(run["eval"], os.path.join(HERE, run["root"]), reply, timing)
json.dump(out, open(os.path.join(HERE, "script-checks.json"), "w"), indent=2)
met = sum(v for r in out.values() for v in r.values())
print(f"{len(out)} runs, {met}/{sum(len(r) for r in out.values())} script checks met -> script-checks.json")
