#!/usr/bin/env python3
"""Merge the script pre-pass and the three judge passes into <run>/grading.json.

Script checks are taken as decided. Judge checks take the majority of the three passes;
a check on which the passes disagree is flagged `borderline` and counted as not met,
whatever the majority says. A judge verdict with neither a quote nor a recorded search
is `not scored` and also counted as not met.
"""
import collections, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASELINE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))["evals"]
MAP = json.load(open(os.path.join(HERE, "judge-map.json")))
PID = {v: k for k, v in MAP.items()}
PASSES = (1, 2, 3)


def load_pass(pid, k):
    p = os.path.join(HERE, "judge-outputs", f"{pid}-pass{k}.json")
    raw = open(p, encoding="utf-8").read().strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
    return {c["id"]: c for c in json.loads(raw)["checks"]}


def main():
    table = collections.defaultdict(lambda: collections.Counter())
    flips = []
    for run in sorted(glob.glob(os.path.join(HERE, "eval-*", "*", "run-*"))):
        rel = os.path.relpath(run, HERE)
        ev = re.search(r"eval-(\d+)-", rel).group(1)
        cfg = rel.split(os.sep)[1]
        script = {c["id"]: c for c in json.load(open(os.path.join(run, "checks-script.json")))["checks"]}
        passes = [load_pass(PID[rel], k) for k in PASSES]
        rows = []
        for c in BASELINE[ev]:
            row = {"id": c["id"], "text": c["check"], "kind": c["kind"], "assertion": c["assertion"]}
            if c["id"] in script:
                s = script[c["id"]]
                row.update(passed=s["passed"], evidence=s["evidence"], decided_by="script")
                row.update({k: s[k] for k in ("ref", "search") if k in s})
            else:
                votes = [p[c["id"]] for p in passes]
                # A met kind=invention check is a negative ("nothing invented"): there is no
                # sentence to quote, so its evidence is the recorded search.
                neg = c["kind"] == "invention"
                scored = [bool((v.get("evidence") or (neg and v.get("search"))) if v["passed"] else v.get("search")) for v in votes]
                yes = sum(1 for v in votes if v["passed"])
                unanimous = yes in (0, len(votes))
                passed = yes == len(votes) and all(scored)
                pick = next((v for v in votes if v["passed"] == (yes * 2 > len(votes))), votes[0])
                row.update(passed=passed, decided_by="judge", votes=f"{yes}/{len(votes)}",
                           borderline=not unanimous, not_scored=not all(scored),
                           evidence=pick.get("evidence") or pick.get("search") or "",
                           passes=[{"passed": v["passed"], "evidence": v.get("evidence", ""), "search": v.get("search", "")} for v in votes])
                if not unanimous:
                    flips.append((rel, c["id"], f"{yes}/{len(votes)}"))
            rows.append(row)
            table[(ev, cfg, c["kind"])]["total"] += 1
            table[(ev, cfg, c["kind"])]["met"] += row["passed"]
        met = sum(r["passed"] for r in rows)
        json.dump({"eval_name": rel.split(os.sep)[0], "skill": "adr", "config": cfg, "run": rel.split(os.sep)[2],
                   "baseline": "evals/checks-baseline.json",
                   "summary": {"passed": met, "failed": len(rows) - met, "total": len(rows), "pass_rate": round(met / len(rows), 4)},
                   "expectations": rows},
                  open(os.path.join(run, "grading.json"), "w"), ensure_ascii=False, indent=2)
        fails = [r["id"] + ("~" if r.get("borderline") else "") for r in rows if not r["passed"]]
        print(f"{rel:75} {met}/{len(rows)}  unmet: {' '.join(fails) or '-'}")
    print("\nby eval / arm / kind (met/total over both runs)")
    for (ev, cfg, kind), c in sorted(table.items(), key=lambda x: (int(x[0][0]), x[0][1], x[0][2])):
        print(f"  eval {ev:>2}  {cfg:10}  {kind:9}  {c['met']}/{c['total']}")
    print(f"\njudge checks with split passes: {len(flips)}")
    for f in flips:
        print("  ", *f)
    json.dump({"split_checks": flips}, open(os.path.join(HERE, "judge-splits.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
