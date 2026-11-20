#!/usr/bin/env python3
"""Grade iteration-16 against the frozen checks of eval 8.

  grade.py packets              build one blind packet per run (12 new runs + the 4 eval-8
                                runs of iteration-9) under judge-inputs/, mapping in judge-map.json
  grade.py judge --scratch DIR  three passes per packet, one headless session per call, no
                                tools, started in an empty directory; verdicts in judge-outputs/
  grade.py aggregate            8.4 from the bytes on disk, the rest from the judges (met only
                                when the three passes agree); writes results.json

The packet text and rules are iteration-9's, plus the anchor cases that
../evals/checks-baseline.json has carried since iteration-10.
"""
import argparse, concurrent.futures as cf, glob, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))
CHECKS = BASE["evals"]["8"]
EVAL = "eval-8-scope-open-design-request"
JUDGE_MODEL = "claude-opus-5-5"
PASSES = 3
CELLS = {"cell-a": "1.3.2, old AGENTS.md", "cell-b": "1.3.2, trimmed AGENTS.md",
         "cell-c": "1.4.0, trimmed AGENTS.md",
         "it9-old_skill": "1.3.2, iteration-9 (subagent, old AGENTS.md)",
         "it9-with_skill": "1.4.0, iteration-9 (subagent, old AGENTS.md)"}

RULES = """# Judge packet {pid}

You are grading one reply against a fixed list of yes/no checks. You did not write the
reply. Decide each check on its own, from the material below only.

Rules:
1. A check is MET only if you can quote the exact words (from the reply, or `file:line`
   from the files) that satisfy it. Put that quote in `evidence`.
2. A check is UNMET only after you looked: in `search`, say what you looked for and where
   (e.g. "any sentence naming a design doc, whole reply").
3. If it is borderline, it is UNMET. Say "borderline" in `search` and why.
4. Length, extra detail or extra files never make a check MET. Judge the proposition only.
5. Do not modify anything. Do not open any file other than this packet.

Return ONLY a JSON object, no prose around it:
{{"packet": "{pid}", "checks": [{{"id": "<check id>", "passed": true|false, "evidence": "<quote, or empty>", "search": "<what you looked for, or empty>"}}]}}
with exactly one entry per check listed below, in the same order.
"""


def runs():
    """(key, cell, run directory) for the new runs and the re-judged iteration-9 ones."""
    out = []
    for d in sorted(glob.glob(os.path.join(HERE, EVAL, "cell-*", "run-*"))):
        out.append((os.path.relpath(d, HERE), os.path.basename(os.path.dirname(d)), d))
    for d in sorted(glob.glob(os.path.join(WS, "iteration-9", EVAL, "*", "run-*"))):
        out.append((os.path.relpath(d, WS), "it9-" + os.path.basename(os.path.dirname(d)), d))
    return out


def tree(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


def packets():
    os.makedirs(os.path.join(HERE, "judge-inputs"), exist_ok=True)
    prompt = next(e for e in json.load(open(os.path.join(WS, "evals", "evals.json")))["evals"] if e["id"] == 8)["prompt"]
    judged = [c for c in CHECKS if c["kind"] in ("reply", "invention")]
    anchors = "\n".join(f"- {a['verdict']}: {a['case']} ({a['why']})" for a in BASE["anchors"]["invention"])
    mapping = {}
    for key, cell, d in runs():
        pid = "p" + hashlib.sha256(("iteration-16:" + key).encode()).hexdigest()[:8]
        mapping[pid] = {"run": key, "cell": cell}
        reply = open(os.path.join(d, "response.md"), encoding="utf-8").read().strip()
        reply = re.sub(r"\n+MODEL: \S+\s*$", "", reply)
        files = tree(os.path.join(d, "outputs")) if os.path.isdir(os.path.join(d, "outputs")) else []
        assert not files, (key, files)  # eval 8: a run that wrote a file needs the file in the packet
        parts = [RULES.format(pid=pid), "## The user's message\n\n" + prompt, "## The reply\n\n" + reply,
                 "## Files in the project after the run\n\nNone. The project directory is empty.",
                 "## Checks\n\n" + "\n".join(f"- **{c['id']}** — {c['check']}" for c in judged),
                 "## Anchor cases for the invention check (8.7)\n\n" + anchors]
        open(os.path.join(HERE, "judge-inputs", pid + ".md"), "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
    json.dump(mapping, open(os.path.join(HERE, "judge-map.json"), "w"), indent=2)
    print(len(mapping), "packets,", len(judged), "judged checks each")


def judge_one(pid, k, scratch):
    out = os.path.join(HERE, "judge-outputs", f"{pid}-pass{k}.json")
    if os.path.exists(out):
        return pid, k, 0, 0.0
    packet = open(os.path.join(HERE, "judge-inputs", pid + ".md"), encoding="utf-8").read()
    env = {x: v for x, v in os.environ.items() if x != "CLAUDECODE"}
    cmd = ["claude", "-p", packet, "--model", JUDGE_MODEL, "--output-format", "json", "--tools", "",
           "--system-prompt", "You grade a reply against a list of checks and answer with JSON only.",
           "--setting-sources", "project,local", "--disable-slash-commands", "--max-turns", "1"]
    p = subprocess.run(cmd, cwd=scratch, env=env, capture_output=True, text=True, timeout=300)
    res = json.loads(next(l for l in p.stdout.splitlines() if l.startswith("{")))
    text = res["result"]
    verdict = json.loads(text[text.index("{"):text.rindex("}") + 1])
    assert [c["id"] for c in verdict["checks"]] == [c["id"] for c in CHECKS if c["kind"] != "absence"], pid
    json.dump(verdict, open(out, "w"), indent=1, ensure_ascii=False)
    u = res["usage"]
    tok = sum(u.get(x) or 0 for x in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    return pid, k, tok, res.get("total_cost_usd") or 0.0


def judge(scratch, workers, only):
    os.makedirs(os.path.join(HERE, "judge-outputs"), exist_ok=True)
    os.makedirs(os.path.join(scratch, ".claude"), exist_ok=True)
    pids = sorted(json.load(open(os.path.join(HERE, "judge-map.json"))))
    jobs = [(p, k) for p in pids for k in range(1, PASSES + 1)][: only or None]
    tok = usd = 0
    with cf.ThreadPoolExecutor(workers) as ex:
        for pid, k, t, c in ex.map(lambda j: judge_one(j[0], j[1], scratch), jobs):
            tok += t; usd += c
            print(pid, k, t, flush=True)
    print(f"judge calls {len(jobs)}, tokens {tok}, usd {usd:.4f}")
    json.dump({"calls": len(jobs), "total_tokens": tok, "cost_usd": round(usd, 4), "model": JUDGE_MODEL},
              open(os.path.join(HERE, "judge-cost.json"), "w"), indent=2)


def aggregate():
    mapping = json.load(open(os.path.join(HERE, "judge-map.json")))
    dirs = {key: d for key, _, d in runs()}
    rows, splits = [], []
    for pid, m in sorted(mapping.items(), key=lambda x: x[1]["run"]):
        d = dirs[m["run"]]
        out = os.path.join(d, "outputs")
        res = {"8.4": not (os.path.isdir(out) and tree(out))}
        passes = [json.load(open(os.path.join(HERE, "judge-outputs", f"{pid}-pass{k}.json"))) for k in range(1, PASSES + 1)]
        for i, c in enumerate([c for c in CHECKS if c["kind"] != "absence"]):
            votes = [bool(p["checks"][i]["passed"]) for p in passes]
            res[c["id"]] = all(votes)
            if len(set(votes)) > 1:
                splits.append({"packet": pid, "run": m["run"], "check": c["id"], "votes": votes})
        rows.append({"packet": pid, "run": m["run"], "cell": m["cell"], "checks": dict(sorted(res.items()))})
    json.dump({"runs": rows, "splits": splits}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    ids = [c["id"] for c in CHECKS]
    print("| Check | " + " | ".join(CELLS) + " |\n|---|" + "---|" * len(CELLS))
    for cid in ids:
        cells = []
        for cell in CELLS:
            rs = [r for r in rows if r["cell"] == cell]
            cells.append(f"{sum(r['checks'][cid] for r in rs)}/{len(rs)}")
        print(f"| {cid} | " + " | ".join(cells) + " |")
    tot = []
    for cell in CELLS:
        rs = [r for r in rows if r["cell"] == cell]
        tot.append(f"{sum(sum(r['checks'].values()) for r in rs)}/{len(rs) * len(ids)}")
    print("| all | " + " | ".join(tot) + " |")
    print("splits:", json.dumps(splits))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["packets", "judge", "aggregate"])
    ap.add_argument("--scratch")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", type=int, default=0)
    a = ap.parse_args()
    {"packets": packets, "judge": lambda: judge(a.scratch, a.workers, a.only), "aggregate": aggregate}[a.step]()
