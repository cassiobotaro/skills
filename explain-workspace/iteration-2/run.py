#!/usr/bin/env python3
"""Run the executors of iteration-2: one headless session (claude -p) per run.

Same harness as iteration-1, word for word in the brief. The skill on disk is explain
1.0.1, so `with_skill` here is 1.0.1; the 1.0.0 cells are the runs of iteration-1, which
runs.json lists for re-judging. Only eval 9 is run again: 1.0.1 changes one line, about
the notes on a revised draft. SHELL=/bin/bash, as in iteration-1.

Usage: run.py <eval>:<cell>:<run> [...] [--workers N]
       run.py all [--runs N] [--workers N]
"""
import argparse, concurrent.futures as cf, json, os, shutil, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
REPO = os.path.dirname(WS)
SKILL = os.path.join(REPO, "explain", "skills", "explain")
MODEL = "claude-sonnet-5-5"
CELLS = ("with_skill", "without_skill")
EVALS = {str(e["id"]): e for e in json.load(open(os.path.join(WS, "evals", "evals.json")))["evals"]}

SKILL_STEP = ("Read the skill at {skill}/SKILL.md and follow it, including reading any reference "
              "file it tells you to read (they sit next to it under references/).")
ROOT_STEP = ("The user's repository is this directory, which is your project root and working "
             "directory: {root}\n   Work only inside it. Treat it as the top of the repository: do not "
             "read, search or write anything above it (the surrounding checkout is unrelated tooling){apart}.")
MESSAGE_STEP = 'The user\'s message is:\n\n"{prompt}"\n'
ALONE_STEP = ("Nobody is available to answer follow-up questions in this session. If you would ask "
              "the user something, put the question in your reply and stop there.")
REPLY_STEP = ("When you are done, end with the reply you would send to the user, exactly as you would "
              "send it. Your final message is taken as that reply.")

ALLOWED = ["Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]


def brief(cell, root, prompt):
    with_skill = cell == "with_skill"
    steps = [SKILL_STEP.format(skill=SKILL)] if with_skill else []
    steps += [ROOT_STEP.format(root=root, apart=", apart from the skill files in step 1" if with_skill else ""),
              MESSAGE_STEP.format(prompt=prompt), ALONE_STEP, REPLY_STEP]
    head = "You are handling a user's request" + (" with the help of a skill.\n\n" if with_skill else ".\n\n")
    return head + "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1)) + "\n"


def evdir(ev):
    return os.path.join(HERE, f"eval-{ev}-{EVALS[ev]['name']}")


def fixture(ev):
    """Per-eval copy of the fixture, kept beside the runs so runs.json can point at it.

    files/<path> becomes <path> (files/ratelimit/limiter.py becomes ratelimit/limiter.py)."""
    dst = os.path.join(HERE, "fixtures", f"eval-{ev}")
    if not os.path.isdir(dst):
        os.makedirs(dst)
        for rel in EVALS[ev]["files"]:
            out = os.path.join(dst, os.path.relpath(rel, "files"))
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
    if cell == "with_skill":
        # The skill sits outside the project root; without this its Read is denied.
        cmd += ["--add-dir", SKILL]
    t0 = time.time()
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
    read_skill = any(t["tool"] == "Read" and t["target"].startswith(SKILL) for t in tools)
    timing = {"total_tokens": total, "duration_ms": final.get("duration_ms"),
              "total_duration_seconds": round(time.time() - t0, 1),
              "cost_usd": final.get("total_cost_usd"), "num_turns": final.get("num_turns"),
              "models": sorted((final.get("modelUsage") or {}).keys()),
              "skills_listed": init.get("skills"), "plugins_listed": init.get("plugins"),
              "read_skill_file": read_skill,
              "permission_denials": final.get("permission_denials") or [], "tool_calls": tools}
    json.dump(timing, open(os.path.join(rundir, "timing.json"), "w"), indent=2)
    return {"eval": ev, "cell": cell, "run": n, "tokens": total, "usd": final.get("total_cost_usd"),
            "turns": final.get("num_turns"), "denials": len(timing["permission_denials"]),
            "read_skill_file": read_skill,
            "skill_tool": [t["target"] for t in tools if t["tool"] == "Skill"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--runs", type=int, default=2, dest="n")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.runs == ["all"]:
        jobs = [(ev, cell, n) for ev in EVALS for cell in CELLS for n in range(1, a.n + 1)]
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
