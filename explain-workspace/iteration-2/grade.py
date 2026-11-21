#!/usr/bin/env python3
"""Decide the kind=file and kind=absence checks of iteration-2 with iteration-1's rules.

Reads runs.json, which lists the four new runs of eval 9 and the iteration-1 runs of evals
1, 3 and 4 that are re-judged here, and writes script-checks.json keyed by run key.

Usage: grade.py
"""
import importlib.util, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("it1", os.path.join(HERE, "..", "iteration-1", "grade.py"))
it1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(it1)

runs = json.load(open(os.path.join(HERE, "runs.json")))["runs"]
out = {}
for r in runs:
    reply = open(os.path.join(HERE, r["reply"]), encoding="utf-8").read()
    out[r["key"]] = it1.grade(r["eval"], os.path.join(HERE, r["root"]), reply)
json.dump(out, open(os.path.join(HERE, "script-checks.json"), "w"), indent=2)
met = sum(v for row in out.values() for v in row.values())
print(f"{len(out)} runs, {met}/{sum(len(row) for row in out.values())} script checks met -> script-checks.json")
