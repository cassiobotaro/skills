#!/usr/bin/env python3
"""Blind-judge the runs of an eval iteration against a frozen check list.

The part of grading that every iteration rewrote, in one place: build one packet per run
that does not name its arm, judge each packet in its own headless session, and count a
check as met only when every pass says so. Checks decided from bytes (kind `file` and
`absence`) stay with the iteration: its own script writes `script-checks.json` and
`table` merges it.

    judge.py manifest <iteration-dir>    discover the runs -> runs.json (edit it freely)
    judge.py packets  <iteration-dir>    runs.json -> judge-inputs/pNN.md, judge-map.json
    judge.py judge    <iteration-dir>    judge-inputs -> judge-outputs/pNN-passK.json
    judge.py table    <iteration-dir>    script + judge verdicts -> results.json, table

A judge call is `claude -p` with no tools, its own system prompt and no user-scope
settings, started in an empty directory: about 2.8k tokens, against ~43k for a subagent
(adr iteration-16, in the git tag archive/evals-2026-11-23). One session per call, so no judge sees two packets.

runs.json:
    {"checks": "../evals/checks-baseline.json", "evals": "../evals/evals.json",
     "runs": [{"key": "8/with_skill/run-1", "eval": "8", "cell": "with_skill",
               "reply": "<file>", "root": "<project dir after the run>",
               "fixture": "<project dir before the run, or null>"}]}
Paths are relative to the iteration directory. A run of another iteration can be listed
to re-judge it in the same batch, which is what a changed packet requires.
"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_KINDS = ("file", "absence")
DEFAULT_MODEL = "claude-opus-5-5"

RULES = """# Judge packet {pid}

You are grading one reply against a fixed list of yes/no checks. You did not write the
reply. Decide each check on its own, from this packet alone.

Rules:
1. A check of kind `reply` is MET only if you can quote the exact words (from the reply,
   or `file:line` from the files) that satisfy it. Put the quote in `evidence`.
2. A check of kind `invention` is a negative ("nothing invented"). When it is MET there is
   nothing to quote: `evidence` records what you searched for and where. When it is UNMET,
   quote the invented words.
{negative}3. Any other UNMET check records in `evidence` what you looked for and where.
4. Borderline is UNMET. Say "borderline" in `evidence` and why.
5. More text or more files never raise a verdict. Judge the proposition only.

Return ONLY a JSON array, no prose around it, with one entry per check listed under
"Checks", in the same order:
[{{"id": "<check id>", "verdict": "met" or "unmet", "evidence": "<quote or search>"}}]
"""


# Added to rule 2 only in a packet that has a check of kind `negative`, so the packets of
# evals without one stay byte-identical to those judged before the kind existed.
NEGATIVE_RULE = """   A check of kind `negative` is a negative too ("no comment that ..."), under the same
   rule: when MET, `evidence` records the search; when UNMET, quote the offending words.
"""


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def tree(root):
    root = Path(root)
    if not root.is_dir():
        return []
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())


def numbered(text):
    return "\n".join(f"{i:>4}  {line}" for i, line in enumerate(text.splitlines(), 1))


def load(it):
    manifest = read_json(it / "runs.json")
    base = read_json(it / manifest["checks"])
    prompts = {str(e["id"]): e["prompt"] for e in read_json(it / manifest["evals"])["evals"]}
    return manifest, base, prompts


def judged_checks(base, ev):
    return [c for c in base["evals"][ev] if c["kind"] not in SCRIPT_KINDS]


# --- manifest -----------------------------------------------------------------------

def cmd_manifest(it, args):
    target = it / "runs.json"
    if target.exists() and not args.force:
        sys.exit(f"{target} exists; pass --force to rebuild it")
    runs, missing = [], []
    for evdir in sorted(it.glob("eval-*")):
        m = re.match(r"eval-(\d+)", evdir.name)
        if not m or not evdir.is_dir():
            continue
        for cell in sorted(p for p in evdir.iterdir() if p.is_dir()):
            for run in sorted(cell.glob("run-*")):
                root = run / "outputs"
                reply = next((p for p in (run / "response.md", root / "reply.md") if p.exists()), None)
                if reply is None:
                    missing.append(str(run.relative_to(it)))
                    continue
                runs.append({"key": f"{m.group(1)}/{cell.name}/{run.name}", "eval": m.group(1),
                             "cell": cell.name, "reply": str(reply.relative_to(it)),
                             "root": str(root.relative_to(it)), "fixture": None})
    write_json(target, {"checks": "../evals/checks-baseline.json", "evals": "../evals/evals.json", "runs": runs})
    print(f"{len(runs)} runs -> {target}")
    for r in missing:
        print("no response.md or outputs/reply.md, left out:", r)


# --- packets ------------------------------------------------------------------------

def packet(pid, run, it, base, prompts):
    ev = run["eval"]
    checks = judged_checks(base, ev)
    reply_path = it / run["reply"]
    reply = re.sub(r"\n+MODEL: \S+\s*$", "", reply_path.read_text(encoding="utf-8").strip())
    root = it / run["root"]
    fixture = it / run["fixture"] if run.get("fixture") else None
    negative = NEGATIVE_RULE if any(c["kind"] == "negative" for c in checks) else ""
    parts = [RULES.format(pid=pid, negative=negative), "## The user's message\n\n" + prompts[ev]]
    before = {}
    if fixture:
        sec = ["## Files in the project before the run"]
        for f in tree(fixture):
            before[f] = (fixture / f).read_bytes()
            sec.append(f"### {f}\n\n```\n{numbered(before[f].decode('utf-8', 'replace'))}\n```")
        parts.append("\n\n".join(sec))
    parts.append("## The reply given to the user\n\n```\n" + numbered(reply) + "\n```")
    after = [f for f in tree(root) if (root / f).resolve() != reply_path.resolve()]
    sec = ["## Files in the project after the run"]
    if not after:
        sec.append("(none)")
    for f in after:
        data = (root / f).read_bytes()
        if before.get(f) == data:
            sec.append(f"### {f} (unchanged by the run)")
            continue
        tag = "CHANGED by the run" if f in before else "NEW, written by the run"
        sec.append(f"### {f} ({tag})\n\n```\n{numbered(data.decode('utf-8', 'replace'))}\n```")
    gone = sorted(set(before) - set(after))
    if gone:
        sec.append("Deleted by the run: " + ", ".join(gone))
    parts.append("\n\n".join(sec))
    anchors = (base.get("anchors") or {}).get("invention")
    if anchors and any(c["kind"] == "invention" for c in checks):
        parts.append("## Anchor cases for checks of kind `invention`\n\n"
                     "Decide by analogy with these; they come from another run of the same kind of task.\n\n"
                     + "\n".join(f"- {a['verdict']}: {a['case']} Why: {a['why']}" for a in anchors))
    parts.append("## Checks\n\n" + "\n".join(f"- `{c['id']}` ({c['kind']}): {c['check']}" for c in checks))
    return "\n\n".join(parts) + "\n"


def cmd_packets(it, args):
    manifest, base, prompts = load(it)
    out, verdicts = it / "judge-inputs", it / "judge-outputs"
    if verdicts.is_dir() and any(verdicts.iterdir()) and not args.force:
        sys.exit("judge-outputs/ already holds verdicts tied to the current packet ids; "
                 "pass --force only if you mean to discard them")
    runs = list(manifest["runs"])
    random.Random(args.seed).shuffle(runs)
    out.mkdir(exist_ok=True)
    mapping = {}
    for i, run in enumerate(runs, 1):
        pid = f"p{i:02d}"
        mapping[pid] = run["key"]
        (out / f"{pid}.md").write_text(packet(pid, run, it, base, prompts), encoding="utf-8")
    write_json(it / "judge-map.json", mapping)
    print(f"{len(mapping)} packets -> {out}")


# --- judge --------------------------------------------------------------------------

def parse_verdicts(text, expected):
    start, end = text.find("["), text.rfind("]")
    data = json.loads(text[start:end + 1])
    out = [{"id": v["id"], "verdict": str(v["verdict"]).strip().lower(), "evidence": v.get("evidence", "")} for v in data]
    if [v["id"] for v in out] != expected:
        raise ValueError(f"check ids {[v['id'] for v in out]} do not match {expected}")
    if any(v["verdict"] not in ("met", "unmet") for v in out):
        raise ValueError("a verdict is neither met nor unmet")
    return out


def judge_one(it, pid, k, expected, model, scratch):
    target = it / "judge-outputs" / f"{pid}-pass{k}.json"
    if target.exists():
        return None
    env = {x: v for x, v in os.environ.items() if x != "CLAUDECODE"}
    cmd = ["claude", "-p", (it / "judge-inputs" / f"{pid}.md").read_text(encoding="utf-8"),
           "--model", model, "--output-format", "json", "--tools", "",
           "--system-prompt", "You grade a reply against a list of checks and answer with JSON only.",
           "--setting-sources", "project,local", "--disable-slash-commands", "--max-turns", "1"]
    # stdin closed: `claude -p` appends piped stdin to the prompt, and a judge must see the packet alone
    p = subprocess.run(cmd, cwd=scratch, env=env, capture_output=True, text=True, timeout=600,
                       stdin=subprocess.DEVNULL)
    line = next((l for l in p.stdout.splitlines() if l.startswith("{")), None)
    if line is None:
        raise RuntimeError((p.stderr or p.stdout)[-300:])
    res = json.loads(line)
    write_json(target, parse_verdicts(res.get("result") or "", expected))
    u = res.get("usage") or {}
    tokens = sum(u.get(x) or 0 for x in ("input_tokens", "cache_creation_input_tokens",
                                         "cache_read_input_tokens", "output_tokens"))
    return {"tokens": tokens, "usd": res.get("total_cost_usd") or 0.0, "models": sorted(res.get("modelUsage") or {})}


def cmd_judge(it, args):
    manifest, base, _ = load(it)
    mapping = read_json(it / "judge-map.json")
    ev_of = {r["key"]: r["eval"] for r in manifest["runs"]}
    (it / "judge-outputs").mkdir(exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="judge-empty-")
    os.makedirs(os.path.join(scratch, ".claude"))
    jobs = [(pid, k) for pid in sorted(mapping) for k in range(1, args.passes + 1)]
    if args.only:
        jobs = jobs[:args.only]
    cost_path = it / "judge-cost.json"
    cost = read_json(cost_path) if cost_path.exists() else {"calls": 0, "total_tokens": 0, "cost_usd": 0.0, "models": []}
    failed = 0

    def work(job):
        pid, k = job
        expected = [c["id"] for c in judged_checks(base, ev_of[mapping[pid]])]
        try:
            return pid, k, judge_one(it, pid, k, expected, args.model, scratch), None
        except Exception as e:  # one bad call must not lose the others; a re-run resumes
            return pid, k, None, f"{type(e).__name__}: {e}"

    with cf.ThreadPoolExecutor(args.workers) as ex:
        for pid, k, res, err in ex.map(work, jobs):
            if err:
                failed += 1
                print(f"{pid} pass {k}: FAILED {err}", flush=True)
            elif res is None:
                print(f"{pid} pass {k}: already judged", flush=True)
            else:
                cost["calls"] += 1
                cost["total_tokens"] += res["tokens"]
                cost["cost_usd"] = round(cost["cost_usd"] + res["usd"], 4)
                cost["models"] = sorted(set(cost["models"]) | set(res["models"]))
                print(f"{pid} pass {k}: {res['tokens']} tokens", flush=True)
    write_json(cost_path, cost)
    print(f"total so far: {cost['calls']} calls, {cost['total_tokens']} tokens, US$ {cost['cost_usd']}")
    if failed:
        sys.exit(f"{failed} call(s) failed; run the same command again to retry only those")


# --- table --------------------------------------------------------------------------

def cmd_table(it, args):
    manifest, base, _ = load(it)
    mapping = read_json(it / "judge-map.json")
    pid_of = {v: k for k, v in mapping.items()}
    script = read_json(it / "script-checks.json") if (it / "script-checks.json").exists() else {}
    results, splits = {}, []
    for run in manifest["runs"]:
        key, pid = run["key"], pid_of[run["key"]]
        votes = {}
        for f in sorted((it / "judge-outputs").glob(f"{pid}-pass*.json")):
            for v in read_json(f):
                votes.setdefault(v["id"], []).append(v["verdict"] == "met")
        mine = script.get(key, {})
        mine = mine.get("checks", mine)
        row = {}
        for c in base["evals"][run["eval"]]:
            if c["kind"] in SCRIPT_KINDS:
                row[c["id"]] = {"kind": c["kind"], "met": bool(mine.get(c["id"]))}
                if c["id"] not in mine:
                    row[c["id"]]["note"] = "not scored: no verdict in script-checks.json"
                continue
            got = votes.get(c["id"], [])
            row[c["id"]] = {"kind": c["kind"], "met": len(got) >= args.passes and all(got),
                            "votes": f"{sum(got)}/{len(got)}"}
            if len(got) < args.passes:
                row[c["id"]]["note"] = "not scored: missing judge pass"
            elif 0 < sum(got) < len(got):
                splits.append({"run": key, "packet": pid, "id": c["id"], "votes": row[c["id"]]["votes"]})
        results[key] = row
    write_json(it / "results.json", {"runs": results, "splits": splits})

    for ev in sorted({r["eval"] for r in manifest["runs"]}, key=int):
        runs = [r for r in manifest["runs"] if r["eval"] == ev]
        cells = list(dict.fromkeys(r["cell"] for r in runs))
        print(f"\neval {ev} (runs meeting the check / runs)\n")
        print("| Check | kind | " + " | ".join(cells) + " |\n|---|---|" + "---|" * len(cells))
        for c in base["evals"][ev]:
            line = []
            for cell in cells:
                rs = [results[r["key"]][c["id"]] for r in runs if r["cell"] == cell]
                line.append(f"{sum(x['met'] for x in rs)}/{len(rs)}")
            print(f"| {c['id']} | {c['kind']} | " + " | ".join(line) + " |")
        for kind in list(dict.fromkeys(c["kind"] for c in base["evals"][ev])):
            line = []
            for cell in cells:
                xs = [x for r in runs if r["cell"] == cell for x in results[r["key"]].values() if x["kind"] == kind]
                line.append(f"{sum(x['met'] for x in xs)}/{len(xs)}")
            print(f"| all | {kind} | " + " | ".join(line) + " |")
    notes = sorted({f"{k}:{i}" for k, r in results.items() for i, c in r.items() if "note" in c})
    if notes:
        print("\nnot scored:", ", ".join(notes))
    print("\nsplits:", json.dumps(splits))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["manifest", "packets", "judge", "table"])
    ap.add_argument("iteration", type=Path)
    ap.add_argument("--passes", type=int, default=3, help="judge passes per packet; a check is met only when all agree")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="judge model id, not an alias")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", type=int, default=0, help="judge: stop after this many calls (smoke test)")
    ap.add_argument("--seed", type=int, default=1, help="packets: shuffle seed for the packet ids")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    it = args.iteration.resolve()
    {"manifest": cmd_manifest, "packets": cmd_packets, "judge": cmd_judge, "table": cmd_table}[args.step](it, args)


if __name__ == "__main__":
    main()
