#!/usr/bin/env python3
"""Run the executors of iteration-28: one headless session (claude -p) per run.

Two cells, `a` and `b`. Both get the same brief, which tells the session to read a copy of
the design-doc skill and follow it: `skill-a` is 1.9.0 as shipped, `skill-b` the same with
one paragraph added to step 2 (diff skill-a/SKILL.md skill-b/SKILL.md). The path is the
only thing that differs, and it does not say which is which. Evals are the two of
./evals.json: eval 7 of the skill as it is, and eval 71, the same request with a sentence
in which the user says they cannot answer now. The brief has no line about nobody being
available: in eval 71 the user's own message says it, and in eval 7 nothing does.

Each run starts in its own copy of the fixture, built before the workers start, with
`--setting-sources project,local` (no user-scope skill loads, so `unslop` is not installed
in either cell) and SHELL=/bin/bash. The repository's AGENTS.md loads in both cells.

Usage: run.py <eval>:<cell>:<run> [...] [--workers N]
       run.py all [--workers N]
"""
import argparse, concurrent.futures as cf, datetime, json, os, shutil, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
REPO = os.path.dirname(WS)
SKILLS = {"a": os.path.join(HERE, "skill-a"), "b": os.path.join(HERE, "skill-b")}
RUNS = {"71": 4, "7": 2}
MODEL = "claude-sonnet-5-5"
CELLS = ("a", "b")
EVALS = {str(e["id"]): e for e in json.load(open(os.path.join(HERE, "evals.json")))["evals"]}

SKILL_STEP = ("Read the skill at {skill}/SKILL.md and follow it, including reading any reference "
              "file it tells you to read (they sit next to it under references/).")
ROOT_STEP = ("The user's repository is this directory, which is your project root and working "
             "directory: {root}\n   Work only inside it. Treat it as the top of the repository: do not "
             "read, search or write anything above it (the surrounding checkout is unrelated tooling){apart}.")
MESSAGE_STEP = 'The user\'s message is:\n\n"{prompt}"\n'
REPLY_STEP = ("When you are done, end with the reply you would send to the user, exactly as you would "
              "send it. Your final message is taken as that reply.")

ALLOWED = ["Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]


def brief(cell, root, prompt):
    steps = [SKILL_STEP.format(skill=SKILLS[cell]),
             ROOT_STEP.format(root=root, apart=", apart from the skill files in step 1"),
             MESSAGE_STEP.format(prompt=prompt), REPLY_STEP]
    head = "You are handling a user's request with the help of a skill.\n\n"
    return head + "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1)) + "\n"


def evdir(ev):
    return os.path.join(HERE, f"eval-{ev}-{EVALS[ev]['eval_name']}")


def fixture(ev):
    """Per-eval copy of the fixture, kept beside the runs so runs.json can point at it.

    files/<fixture dir>/<path> becomes <path>: the fixture directory is the project root."""
    dst = os.path.join(HERE, "fixtures", "eval-7")   # both evals share the fixture of eval 7
    if not os.path.isdir(dst):
        os.makedirs(dst)
        for rel in EVALS[ev]["files"]:
            out = os.path.join(dst, *rel.split("/")[2:])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copyfile(os.path.join(WS, "evals", rel), out)
    return dst


def run(ev, cell, n):
    rundir = os.path.join(evdir(ev), cell, f"run-{n}")
    root = os.path.join(rundir, "outputs")
    shutil.rmtree(rundir, ignore_errors=True)   # a rerun starts from the fixture again
    shutil.copytree(fixture(ev), root)
    text = brief(cell, root, EVALS[ev]["prompt"])
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"   # see the module docstring: zsh's `ls` alias lists nothing here
    cmd = ["claude", "-p", text, "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--setting-sources", "project,local",
           "--allowedTools", *ALLOWED]
    SKILL = SKILLS[cell]
    cmd += ["--add-dir", SKILL]   # the skill sits outside the project root
    t0, day0 = time.time(), datetime.date.today().isoformat()
    try:
        p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=900,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"eval": ev, "cell": cell, "run": n, "error": "timeout after 900 s"}
    tdir = os.path.join(HERE, "transcripts")
    os.makedirs(tdir, exist_ok=True)
    open(os.path.join(tdir, f"eval-{ev}-{cell}-run-{n}.jsonl"), "w").write(p.stdout)
    tools, final, init = [], None, {}
    for line in p.stdout.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "system" and o.get("subtype") == "init":
            init = o
        if o.get("type") == "assistant":
            for b in (o.get("message") or {}).get("content") or []:
                if b.get("type") == "tool_use":
                    i = b.get("input") or {}
                    tools.append({"tool": b["name"], "target": i.get("file_path") or i.get("command")
                                  or i.get("pattern") or i.get("skill") or ""})
        if o.get("type") == "result":
            final = o
    if final is None:
        return {"eval": ev, "cell": cell, "run": n, "error": (p.stderr or p.stdout)[-400:]}
    open(os.path.join(rundir, "response.md"), "w").write((final.get("result") or "").strip() + "\n")
    u = final.get("usage") or {}
    total = sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                        "cache_read_input_tokens", "output_tokens"))
    skill_files = sorted({os.path.relpath(t["target"], SKILL) for t in tools
                          if t["tool"] == "Read" and t["target"].startswith(SKILL)})
    timing = {"total_tokens": total, "duration_ms": final.get("duration_ms"),
              "total_duration_seconds": round(time.time() - t0, 1),
              "cost_usd": final.get("total_cost_usd"), "num_turns": final.get("num_turns"),
              "dates": sorted({day0, datetime.date.today().isoformat()}),
              "models": sorted((final.get("modelUsage") or {}).keys()),
              "skills_listed": init.get("skills"), "plugins_listed": init.get("plugins"),
              "skill_files_read": skill_files,
              "permission_denials": final.get("permission_denials") or [], "tool_calls": tools}
    json.dump(timing, open(os.path.join(rundir, "timing.json"), "w"), indent=2)
    return {"eval": ev, "cell": cell, "run": n, "tokens": total, "usd": final.get("total_cost_usd"),
            "turns": final.get("num_turns"), "denials": len(timing["permission_denials"]),
            "skill_files_read": skill_files,
            "skill_tool": [t["target"] for t in tools if t["tool"] == "Skill"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.runs == ["all"]:
        jobs = [(ev, cell, n) for ev in RUNS for cell in CELLS for n in range(1, RUNS[ev] + 1)]
    else:
        jobs = [(r.split(":")[0], r.split(":")[1], int(r.split(":")[2])) for r in a.runs]
    # Build every fixture copy before the workers start. fixture() is not safe to call for
    # the first time from two threads: one creates the directory, the other sees it exist
    # and copies it before the files are in, and its run starts in an empty project.
    for ev in sorted({j[0] for j in jobs}):
        fixture(ev)
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(*j), jobs):
            print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
