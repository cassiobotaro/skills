#!/usr/bin/env python3
"""Run a skill's behavioral evals: one headless session (claude -p) per run.

    eval-tools/run_evals.py technical-writing                 # the smoke set, one run each, on opus
    eval-tools/run_evals.py technical-writing --evals all --runs 2
    eval-tools/run_evals.py technical-writing --evals 3 --skill-dir /path/to/candidate
    eval-tools/run_evals.py technical-writing --cell without_skill

Reads <plugin>-workspace/evals/evals.json. `--evals smoke` (the default) runs the ids in its
`smoke` list. Each run starts in its own copy of the eval's fixture (built before the workers
start), with `--setting-sources project,local`, SHELL=/bin/bash and stdin closed; the brief
tells the session to read the skill and follow it, and the session's final message is the
reply. `fixture_strip` in evals.json says how many leading parts of each fixture path to drop
(2 for files/<fixture>/<path>, 1 for files/<path>).

Writes <plugin>-workspace/run-<date>-<label>/ (gitignored): eval-<id>-<name>/<cell>/run-<n>/
with outputs/ (the project after the run), response.md and timing.json, plus transcripts/,
fixtures/ and a runs.json that `eval-tools/judge.py packets|judge|table` reads as it is.
Read the replies before grading anything; see eval-tools/README.md.
"""
import argparse, concurrent.futures as cf, datetime, json, os, shutil, subprocess, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def brief(skill, root, prompt):
    steps = [SKILL_STEP.format(skill=skill)] if skill else []
    steps += [ROOT_STEP.format(root=root, apart=", apart from the skill files in step 1" if skill else ""),
              MESSAGE_STEP.format(prompt=prompt), ALONE_STEP, REPLY_STEP]
    head = "You are handling a user's request" + (" with the help of a skill.\n\n" if skill else ".\n\n")
    return head + "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1)) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plugin")
    ap.add_argument("--evals", default="smoke", help="'smoke' (default), 'all', or comma-separated ids")
    ap.add_argument("--runs", type=int, default=1, help="runs per eval (default 1)")
    ap.add_argument("--cell", default="with_skill", choices=["with_skill", "without_skill"])
    ap.add_argument("--skill-dir", help="the skill directory to read (default: the repository's)")
    ap.add_argument("--model", default="claude-opus-5-5", help="a model id, not an alias")
    ap.add_argument("--label", default="", help="suffix of the output directory")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()

    ws = os.path.join(REPO, f"{a.plugin}-workspace")
    spec = json.load(open(os.path.join(ws, "evals", "evals.json")))
    evals = {str(e["id"]): e for e in spec["evals"]}
    strip = spec.get("fixture_strip", 2)
    ids = (spec.get("smoke") if a.evals == "smoke" else list(evals) if a.evals == "all"
           else a.evals.split(","))
    ids = [str(i) for i in ids]
    skill = None
    if a.cell == "with_skill":
        skill = os.path.abspath(a.skill_dir or os.path.join(REPO, a.plugin, "skills", a.plugin))
    name = "run-" + datetime.date.today().isoformat() + (f"-{a.label}" if a.label else "")
    out = os.path.join(ws, name)

    def fixture(ev):
        dst = os.path.join(out, "fixtures", f"eval-{ev}")
        if not os.path.isdir(dst):
            os.makedirs(dst)
            for rel in evals[ev].get("files", []):
                f = os.path.join(dst, *rel.split("/")[strip:])
                os.makedirs(os.path.dirname(f), exist_ok=True)
                shutil.copyfile(os.path.join(ws, "evals", rel), f)
        return dst

    def run(ev, n):
        e = evals[ev]
        rundir = os.path.join(out, f"eval-{ev}-{e.get('name') or 'eval'}", a.cell, f"run-{n}")
        root = os.path.join(rundir, "outputs")
        shutil.rmtree(rundir, ignore_errors=True)
        shutil.copytree(fixture(ev), root)
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        env["SHELL"] = "/bin/bash"   # a zsh `ls` alias to eza lists nothing without a terminal
        cmd = ["claude", "-p", brief(skill, root, e["prompt"]), "--model", a.model,
               "--output-format", "stream-json", "--verbose", "--permission-mode", "acceptEdits",
               "--setting-sources", "project,local", "--allowedTools", *ALLOWED]
        if skill:
            cmd += ["--add-dir", skill]   # the skill sits outside the project root
        t0 = time.time()
        try:
            p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True,
                               timeout=a.timeout, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return {"eval": ev, "run": n, "error": f"timeout after {a.timeout} s"}
        tdir = os.path.join(out, "transcripts")
        os.makedirs(tdir, exist_ok=True)
        open(os.path.join(tdir, f"eval-{ev}-{a.cell}-run-{n}.jsonl"), "w").write(p.stdout)
        tools, final = [], None
        for line in p.stdout.splitlines():
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if o.get("type") == "assistant":
                for b in (o.get("message") or {}).get("content") or []:
                    if b.get("type") == "tool_use":
                        i = b.get("input") or {}
                        tools.append({"tool": b["name"], "target": i.get("file_path") or i.get("command")
                                      or i.get("pattern") or i.get("skill") or ""})
            if o.get("type") == "result":
                final = o
        if final is None:
            return {"eval": ev, "run": n, "error": (p.stderr or p.stdout)[-400:]}
        open(os.path.join(rundir, "response.md"), "w").write((final.get("result") or "").strip() + "\n")
        timing = {"cost_usd": final.get("total_cost_usd"), "num_turns": final.get("num_turns"),
                  "duration_s": round(time.time() - t0, 1),
                  "models": sorted((final.get("modelUsage") or {}).keys()),
                  "permission_denials": final.get("permission_denials") or [], "tool_calls": tools}
        json.dump(timing, open(os.path.join(rundir, "timing.json"), "w"), indent=2)
        return {"eval": ev, "run": n, "usd": final.get("total_cost_usd"), "models": timing["models"],
                "turns": final.get("num_turns"), "denials": len(timing["permission_denials"])}

    jobs = [(ev, n) for ev in ids for n in range(1, a.runs + 1)]
    for ev in ids:
        fixture(ev)   # before the workers: two first calls from two threads race
    results = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(*j), jobs):
            print(json.dumps(res), flush=True)
            results.append(res)

    runs = []
    for ev, n in jobs:
        d = f"eval-{ev}-{evals[ev].get('name') or 'eval'}/{a.cell}/run-{n}"
        if os.path.exists(os.path.join(out, d, "response.md")):
            runs.append({"key": f"{ev}/{a.cell}/run-{n}", "eval": ev, "cell": a.cell,
                         "reply": f"{d}/response.md", "root": f"{d}/outputs",
                         "fixture": f"fixtures/eval-{ev}"})
    json.dump({"checks": "../evals/checks-baseline.json", "evals": "../evals/evals.json",
               "model": a.model, "skill": skill, "runs": runs},
              open(os.path.join(out, "runs.json"), "w"), indent=2)
    usd = sum(r.get("usd") or 0 for r in results)
    errors = sum(1 for r in results if "error" in r)
    print(f"{len(runs)} runs -> {out}  cost US$ {usd:.2f}  errors {errors}")


if __name__ == "__main__":
    main()
