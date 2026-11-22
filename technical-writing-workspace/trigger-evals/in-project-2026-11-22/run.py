#!/usr/bin/env python3
"""Run the probe described in README.md. Writes results.json and transcripts/.

Usage: run.py --scratch DIR [--runs 4] [--workers 4]
"""
import argparse, concurrent.futures as cf, json, os, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
REPO = os.path.dirname(WS)
MODEL = "claude-sonnet-5-5"
PLUGINS = ("technical-writing", "unslop")
EVALS = {str(e["id"]): e for e in json.load(open(os.path.join(WS, "evals", "evals.json")))["evals"]}
CANARY = "Use the technical-writing skill. "
ALLOWED = ["Skill", "Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false"]


def run(job, scratch):
    idx, ev, n, canary = job
    project = os.path.join(scratch, f"p{idx:02d}", "project")
    shutil.rmtree(os.path.dirname(project), ignore_errors=True)
    os.makedirs(project)
    for rel in EVALS[ev]["files"]:
        out = os.path.join(project, *rel.split("/")[2:])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(os.path.join(WS, "evals", rel), out)
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-q", "--allow-empty", "-m", "start"]):
        subprocess.run([*GIT, *args], cwd=project, check=True)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"
    prompt = (CANARY if canary else "") + EVALS[ev]["prompt"]
    cmd = ["claude", "-p", prompt, "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--setting-sources", "project,local", "--allowedTools", *ALLOWED]
    for name in PLUGINS:
        cmd += ["--plugin-dir", os.path.join(scratch, "plugins", name)]
    tag = f"{'canary' if canary else 'eval-' + ev}-run-{n}"
    try:
        p = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True, timeout=1500,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"eval": ev, "run": n, "canary": canary, "error": "timeout"}
    os.makedirs(os.path.join(HERE, "transcripts"), exist_ok=True)
    open(os.path.join(HERE, "transcripts", tag + ".jsonl"), "w").write(p.stdout)
    calls, final, listed = [], None, None
    for line in p.stdout.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "system" and o.get("subtype") == "init":
            listed = sorted(s for s in (o.get("skills") or []) if s.split(":")[-1] in PLUGINS)
        if o.get("type") == "assistant":
            for b in (o.get("message") or {}).get("content") or []:
                if b.get("type") == "tool_use":
                    calls.append((b["name"], (b["input"].get("skill") or "").split(":")[-1], json.dumps(b["input"])))
        if o.get("type") == "result":
            final = o
    if final is None:
        return {"eval": ev, "run": n, "canary": canary, "error": (p.stderr or p.stdout)[-300:]}
    invoked = [s for name, s, _ in calls if name == "Skill"]
    return {"eval": ev, "run": n, "canary": canary, "project": f"p{idx:02d}", "installed": listed, "invoked": invoked,
            "T": "technical-writing" in invoked,
            "first_call": bool(calls) and calls[0][0] == "Skill" and calls[0][1] == "technical-writing",
            "F": any(name != "Skill" and "/technical-writing/skills/" in raw for name, _, raw in calls),
            "tool_calls": len(calls), "models": sorted((final.get("modelUsage") or {}).keys()),
            "usd": final.get("total_cost_usd"), "turns": final.get("num_turns"),
            "denials": len(final.get("permission_denials") or []),
            "reply_start": (final.get("result") or "").strip()[:240]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--runs", type=int, default=4)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    if os.path.commonpath([scratch, REPO]) == REPO:
        raise SystemExit("--scratch must be outside the repository")
    shutil.rmtree(os.path.join(scratch, "plugins"), ignore_errors=True)
    for name in PLUGINS:
        shutil.copytree(os.path.join(REPO, name), os.path.join(scratch, "plugins", name))
    jobs = [("1", 1, True), ("1", 2, True)] + [(ev, n, False) for n in range(1, a.runs + 1) for ev in EVALS]
    jobs = [(i + 1, *j) for i, j in enumerate(jobs)]
    out = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j, scratch), jobs):
            out.append(res)
            print(json.dumps({k: v for k, v in res.items() if k != "reply_start"}, ensure_ascii=False), flush=True)
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), ensure_ascii=False, indent=1)
    ok = [r for r in out if "error" not in r]
    print("canary", f"{sum(r['T'] for r in ok if r['canary'])}/{sum(1 for r in ok if r['canary'])}")
    for ev in EVALS:
        rs = [r for r in ok if r["eval"] == ev and not r["canary"]]
        print("eval", ev, "T", f"{sum(r['T'] for r in rs)}/{len(rs)}", "first", sum(r["first_call"] for r in rs),
              "F", sum(r["F"] for r in rs))


if __name__ == "__main__":
    main()
