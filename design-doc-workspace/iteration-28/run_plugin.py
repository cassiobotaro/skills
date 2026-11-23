#!/usr/bin/env python3
"""Run the cells that the amendment of 2026-11-22 adds: the skill installed and invoked.

`pa` is skill-a (design-doc 1.9.0) and `pc` is skill-c (the revised paragraph). Each run
is a headless session in a project of its own outside the repository, a fresh git
repository with the fixture of eval 7, given the eval's prompt and nothing else.
`design-doc` (the plugin directory of the repository with the cell's copy of the skill in
it) and `unslop` are loaded with --plugin-dir from copies outside the project, and
--add-dir lets the session read their reference files. Outputs land where run.py puts
them: eval-<id>-<name>/<cell>/run-<n>/.

`pn`, added on 2026-11-23, is `pa` without `unslop`: only `design-doc` is loaded. Each run
records the skills the session listed at start (`skills_listed` in timing.json), so that
the absence of `unslop` is read from the session and not assumed.

`pg`, added on 2026-11-23, is `pn` with a copy of the repository's AGENTS.md at the root
of the project, committed with the fixture, so that it loads as project instructions.
It is left out of the copied outputs, so the judge packets match those of `pn`.
Under /tmp no project instructions file loads, so `pg` did not test that; `pg2` is the
same cell and must be run with --scratch under $HOME (see eval-tools/README.md).

`pd`, added on 2026-11-23, is `pn` with skill-d: 1.9.0 plus one self-review bullet
(diff skill-a/SKILL.md skill-d/SKILL.md).

`pe`, added on 2026-11-23, is `pn` with skill-e: 1.9.0 plus one paragraph in contract 2
(diff skill-a/SKILL.md skill-e/SKILL.md).

`pn-opus` and `pe-opus`, added on 2026-11-23, are `pn` and `pe` with the executor on
claude-opus-5-5 (MODEL_OF); every other cell runs on MODEL.

Usage: run_plugin.py --scratch DIR <eval>:<cell>:<run> [...] [--workers N]
"""
import argparse, concurrent.futures as cf, datetime, json, os, shutil, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
REPO = os.path.dirname(WS)
MODEL = "claude-sonnet-5-5"
CELLS = {"pa": "skill-a", "pc": "skill-c", "pn": "skill-a", "pg": "skill-a", "pg2": "skill-a", "pd": "skill-d", "pe": "skill-e",
         "pn-opus": "skill-a", "pe-opus": "skill-e"}
NO_UNSLOP = {"pn", "pg", "pg2", "pd", "pe", "pn-opus", "pe-opus"}
MODEL_OF = {"pn-opus": "claude-opus-5-5", "pe-opus": "claude-opus-5-5"}
WITH_AGENTS = {"pg", "pg2"}
EVALS = {str(e["id"]): e for e in json.load(open(os.path.join(HERE, "evals.json")))["evals"]}
ALLOWED = ["Skill", "Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false"]


def stage(scratch):
    base = os.path.join(scratch, "plugins")
    shutil.rmtree(base, ignore_errors=True)
    for cell, copy in CELLS.items():
        dst = os.path.join(base, cell, "design-doc")
        shutil.copytree(os.path.join(REPO, "design-doc"), dst)
        shutil.rmtree(os.path.join(dst, "skills", "design-doc"))
        shutil.copytree(os.path.join(HERE, copy), os.path.join(dst, "skills", "design-doc"))
    shutil.copytree(os.path.join(REPO, "unslop"), os.path.join(base, "unslop"))


def run(job, scratch):
    idx, ev, cell, n = job
    rundir = os.path.join(HERE, f"eval-{ev}-{EVALS[ev]['eval_name']}", cell, f"run-{n}")
    project = os.path.join(scratch, f"p{idx:02d}", "project")
    shutil.rmtree(os.path.dirname(project), ignore_errors=True)
    for rel in EVALS[ev]["files"]:
        out = os.path.join(project, *rel.split("/")[2:])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(os.path.join(WS, "evals", rel), out)
    if cell in WITH_AGENTS:
        shutil.copyfile(os.path.join(REPO, "AGENTS.md"), os.path.join(project, "AGENTS.md"))
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "start"]):
        subprocess.run([*GIT, *args], cwd=project, check=True)
    dd, un = os.path.join(scratch, "plugins", cell, "design-doc"), os.path.join(scratch, "plugins", "unslop")
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"
    cmd = ["claude", "-p", EVALS[ev]["prompt"], "--model", MODEL_OF.get(cell, MODEL), "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--setting-sources", "project,local", "--allowedTools", *ALLOWED,
           "--plugin-dir", dd]
    cmd += ["--add-dir", dd] if cell in NO_UNSLOP else ["--plugin-dir", un, "--add-dir", dd, un]
    t0, day0 = time.time(), datetime.date.today().isoformat()
    try:
        p = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True, timeout=1800,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"eval": ev, "cell": cell, "run": n, "error": "timeout"}
    os.makedirs(os.path.join(HERE, "transcripts"), exist_ok=True)
    open(os.path.join(HERE, "transcripts", f"eval-{ev}-{cell}-run-{n}.jsonl"), "w").write(p.stdout)
    tools, final, listed = [], None, []
    for line in p.stdout.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "system" and o.get("subtype") == "init":
            listed = sorted(o.get("skills") or [])
        if o.get("type") == "assistant":
            for b in (o.get("message") or {}).get("content") or []:
                if b.get("type") == "tool_use":
                    i = b.get("input") or {}
                    tools.append({"tool": b["name"], "target": i.get("file_path") or i.get("command")
                                  or i.get("pattern") or i.get("skill") or ""})
        if o.get("type") == "result":
            final = o
    if final is None:
        return {"eval": ev, "cell": cell, "run": n, "error": (p.stderr or p.stdout)[-300:]}
    shutil.rmtree(rundir, ignore_errors=True)
    os.makedirs(rundir)
    shutil.copytree(project, os.path.join(rundir, "outputs"), ignore=shutil.ignore_patterns(".git", *(["AGENTS.md"] if cell in WITH_AGENTS else [])))
    open(os.path.join(rundir, "response.md"), "w").write((final.get("result") or "").strip() + "\n")
    u = final.get("usage") or {}
    invoked = [t["target"].split(":")[-1] for t in tools if t["tool"] == "Skill"]
    timing = {"project": f"p{idx:02d}", "cost_usd": final.get("total_cost_usd"), "num_turns": final.get("num_turns"),
              "total_tokens": sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                                          "cache_read_input_tokens", "output_tokens")),
              "total_duration_seconds": round(time.time() - t0, 1),
              "dates": sorted({day0, datetime.date.today().isoformat()}),
              "models": sorted((final.get("modelUsage") or {}).keys()), "skills_invoked": invoked,
              "skills_listed": listed,
              "permission_denials": final.get("permission_denials") or [], "tool_calls": tools}
    json.dump(timing, open(os.path.join(rundir, "timing.json"), "w"), indent=2)
    new = sorted(f for d, _, fs in os.walk(os.path.join(project, "docs")) for f in fs if f != "TEMPLATE.md")
    return {"eval": ev, "cell": cell, "run": n, "usd": timing["cost_usd"], "turns": timing["num_turns"],
            "invoked": invoked, "unslop_listed": any("unslop" in x for x in listed), "denials": len(timing["permission_denials"]), "new": new}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    if os.path.commonpath([scratch, REPO]) == REPO:
        raise SystemExit("--scratch must be outside the repository")
    stage(scratch)
    jobs = [(i + 1, *r.split(":")[:2], int(r.split(":")[2])) for i, r in enumerate(a.runs)]
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j, scratch), jobs):
            print(json.dumps(res, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
