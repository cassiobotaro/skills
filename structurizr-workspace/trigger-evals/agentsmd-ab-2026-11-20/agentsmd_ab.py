#!/usr/bin/env python3
"""A/B of the AGENTS.md text on the trigger rate of indirect queries (see prediction.json).

Reuses eval-tools/run_trigger_eval.py for the patched copy of run_eval.py and adds one
patch of its own: the nested session starts in the directory named by TRIGGER_EVAL_CWD
instead of the project root. Run from the repo root:

    agentsmd_ab.py <dir holding the old AGENTS.md> <dir holding the trimmed one> [--smoke]
"""
import json, os, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "eval-tools"))
import run_trigger_eval as rte  # noqa: E402

PRED = json.loads((HERE / "prediction.json").read_text())
ORDER = [("adr", "a", 1), ("adr", "b", 1), ("mermaid-sequence", "a", 1), ("mermaid-sequence", "b", 1),
         ("mermaid-sequence", "b", 2), ("mermaid-sequence", "a", 2), ("adr", "b", 2), ("adr", "a", 2)]


def main():
    ctx = {"a": Path(sys.argv[1]).resolve(), "b": Path(sys.argv[2]).resolve()}
    smoke = "--smoke" in sys.argv
    if Path.cwd() != REPO:
        sys.exit(f"Run this from the repo root: cd {REPO}")
    prefix = rte.inhibit_prefix()
    with tempfile.TemporaryDirectory(prefix="trigger-ab-") as tmp:
        work = Path(tmp)
        script = rte.build_patched_copy(rte.find_skill_creator(), work)
        src = script.read_text()
        old = "            cwd=project_root,\n"
        assert src.count(old) == 1, "upstream changed the Popen call"
        script.write_text(src.replace(old, '            cwd=os.environ.get("TRIGGER_EVAL_CWD", project_root),\n'))
        order = [("adr", "a", 0), ("adr", "b", 0), ("mermaid-sequence", "a", 0), ("mermaid-sequence", "b", 0)] if smoke else ORDER
        for skill, arm, block in order:
            s = PRED["sets"][skill]
            queries = [s["canary"]] if smoke else [*s["queries"], s["canary"]]
            path = work / f"{skill}-{arm}-{block}.json"
            path.write_text(json.dumps([{"query": q, "should_trigger": True} for q in queries], ensure_ascii=False))
            os.environ["TRIGGER_EVAL_CWD"] = str(ctx[arm])
            t0 = time.time()
            res = rte.run_sweep(script, work, REPO, ["--eval-set", str(path), "--skill-path", f"{skill}/skills/{skill}",
                                                    "--model", "claude-haiku-5-5", "--timeout", "120", "--num-workers", "1",
                                                    "--runs-per-query", "1" if smoke else "5"], prefix)
            by = {r["query"]: r for r in res["results"]}
            can = by[s["canary"]]
            ind = [by[q] for q in s["queries"] if q in by]
            res["arm"], res["block"], res["canary_query"] = arm, block, s["canary"]
            if not smoke:
                (HERE / f"{skill}-{arm}-block{block}.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
            print(f"{time.strftime('%H:%M:%S')} {skill} arm {arm} block {block}: indirect "
                  f"{sum(r['triggers'] for r in ind)}/{sum(r['runs'] for r in ind)} {[r['triggers'] for r in ind]} "
                  f"| canary {can['triggers']}/{can['runs']} | {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
