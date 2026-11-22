#!/usr/bin/env python3
"""Run the executors of iteration-27: one headless session (claude -p) per run.

Two cells, `v160` (design-doc 1.6.0, commit 53c2dae) and `v170` (design-doc 1.7.0, commit
cb8c72e). What 1.7.0 adds only happens "when the technical-writing skill is installed" and
through the Skill tool, so a brief that says "read this SKILL.md" cannot exercise it. Each
run therefore starts in a project of its own outside this repository (--scratch), a fresh
git repository holding the eval's fixture and three installed skills under
`.claude/skills/`: `design-doc` at the cell's version, and `technical-writing` and
`unslop` as they are at cb8c72e, the same in both cells. The session gets the eval's
prompt word for word and nothing else. No AGENTS.md is in reach, project directories are
numbered, and the skill directory has the same name in both cells, so no path names the
cell.

`--setting-sources project,local` keeps user-scope plugins out. SHELL=/bin/bash because
the user's zsh aliases `ls` to `eza`, which lists nothing without a terminal. Fixture
copies are built before the workers start. `.git` and `.claude` are left out of the copy
kept as `outputs/`, so the judge packet shows only the project's own files.

Usage: run.py --scratch DIR <eval>:<cell>:<run> [...] [--workers N]
       run.py --scratch DIR all [--runs N] [--workers N]
"""
import argparse, concurrent.futures as cf, datetime, json, os, shutil, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
REPO = os.path.dirname(WS)
MODEL = "claude-sonnet-5-5"
CELLS = {"v160": "53c2dae", "v170": "cb8c72e", "v160w": "53c2dae", "v170w": "cb8c72e"}
BASE_CELLS = ("v160", "v170")
# The `w` cells were added by the amendment of 2026-11-22 in checks.json, after the first
# 20 runs: on evals 7 and 9 a session given the prompt alone asks first and writes nothing,
# so the write step that 1.7.0 changes never runs. They append one sentence to the user's
# message, and on eval 9, where design-doc was invoked in 0 of 8 sessions, name the skill.
WRITE_NOW = (" Não vou conseguir responder perguntas agora: escreve o documento com o que eu já disse "
             "e deixa as perguntas no final.")
NAMED = {"9": " Usa a skill design-doc."}
SHARED = "cb8c72e"   # technical-writing 1.0.0 and unslop as they are next to design-doc 1.7.0
EVAL_IDS = ("1", "4", "6", "7", "9")
EVALS = {str(e["id"]): e for e in json.load(open(os.path.join(WS, "evals", "evals.json")))["evals"]}
ALLOWED = ["Skill", "Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false"]


def export(commit, plugin, dst):
    """<plugin>/skills/<plugin>/ as it is at a commit, written to dst."""
    os.makedirs(dst)
    tar = subprocess.run(["git", "-C", REPO, "archive", commit, f"{plugin}/skills/{plugin}"],
                         check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "--strip-components=3", "-C", dst], input=tar, check=True)


def stage(scratch):
    base = os.path.join(scratch, "skills")
    shutil.rmtree(base, ignore_errors=True)
    for cell, commit in CELLS.items():
        export(commit, "design-doc", os.path.join(base, cell, "design-doc"))
    for plugin in ("technical-writing", "unslop"):
        export(SHARED, plugin, os.path.join(base, "shared", plugin))


def evdir(ev):
    return os.path.join(HERE, f"eval-{ev}-{EVALS[ev]['eval_name']}")


def fixture(ev):
    """Per-eval copy of the fixture, kept beside the runs so runs.json can point at it."""
    dst = os.path.join(HERE, "fixtures", f"eval-{ev}")
    if not os.path.isdir(dst):
        os.makedirs(dst)
        for rel in EVALS[ev]["files"]:
            out = os.path.join(dst, *rel.split("/")[2:])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copyfile(os.path.join(WS, "evals", rel), out)
    return dst


def run(job, scratch):
    idx, ev, cell, n = job
    rundir = os.path.join(evdir(ev), cell, f"run-{n}")
    project = os.path.join(scratch, "projects", f"p{idx:03d}", "project")
    shutil.rmtree(os.path.dirname(project), ignore_errors=True)
    shutil.copytree(fixture(ev), project)
    skills = os.path.join(project, ".claude", "skills")
    shutil.copytree(os.path.join(scratch, "skills", cell, "design-doc"), os.path.join(skills, "design-doc"))
    for plugin in ("technical-writing", "unslop"):
        shutil.copytree(os.path.join(scratch, "skills", "shared", plugin), os.path.join(skills, plugin))
    subprocess.run([*GIT, "init", "-q"], cwd=project, check=True)
    subprocess.run([*GIT, "add", "-A"], cwd=project, check=True)
    subprocess.run([*GIT, "commit", "-q", "--allow-empty", "-m", "start"], cwd=project, check=True)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"
    prompt = EVALS[ev]["prompt"] + (NAMED.get(ev, "") + WRITE_NOW if cell.endswith("w") else "")
    cmd = ["claude", "-p", prompt, "--model", MODEL, "--output-format", "stream-json",
           "--verbose", "--permission-mode", "acceptEdits", "--setting-sources", "project,local",
           "--allowedTools", *ALLOWED]
    t0, day0 = time.time(), datetime.date.today().isoformat()
    try:
        p = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True, timeout=1800,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"eval": ev, "cell": cell, "run": n, "error": "timeout after 1800 s"}
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
    shutil.rmtree(rundir, ignore_errors=True)
    os.makedirs(rundir)
    shutil.copytree(project, os.path.join(rundir, "outputs"), ignore=shutil.ignore_patterns(".git", ".claude"))
    open(os.path.join(rundir, "response.md"), "w").write((final.get("result") or "").strip() + "\n")
    u = final.get("usage") or {}
    total = sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                        "cache_read_input_tokens", "output_tokens"))
    invoked = [t["target"] for t in tools if t["tool"] == "Skill"]
    read = sorted({os.path.relpath(t["target"], skills) for t in tools
                   if t["tool"] == "Read" and t["target"].startswith(skills)})
    timing = {"project": f"p{idx:03d}", "total_tokens": total, "output_tokens": u.get("output_tokens"),
              "cost_usd": final.get("total_cost_usd"), "num_turns": final.get("num_turns"),
              "total_duration_seconds": round(time.time() - t0, 1), "prompt_suffix": prompt[len(EVALS[ev]["prompt"]):],
              "dates": sorted({day0, datetime.date.today().isoformat()}),
              "models": sorted((final.get("modelUsage") or {}).keys()),
              "skills_listed": init.get("skills"), "skills_invoked": invoked, "skill_files_read": read,
              "permission_denials": final.get("permission_denials") or [], "tool_calls": tools}
    json.dump(timing, open(os.path.join(rundir, "timing.json"), "w"), indent=2)
    return {"eval": ev, "cell": cell, "run": n, "tokens": total, "usd": final.get("total_cost_usd"),
            "turns": final.get("num_turns"), "invoked": invoked, "denials": len(timing["permission_denials"]),
            "seconds": timing["total_duration_seconds"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--runs", type=int, default=2, dest="n")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    if os.path.commonpath([scratch, REPO]) == REPO:
        raise SystemExit("--scratch must be outside the repository")
    order = [(ev, cell, n) for ev in EVAL_IDS for cell in BASE_CELLS for n in range(1, a.n + 1)]
    if a.runs == ["all"]:
        wanted = order
    else:
        wanted = [(r.split(":")[0], r.split(":")[1], int(r.split(":")[2])) for r in a.runs]
    # Project numbers are shuffled by a fixed seed so that pNNN does not sort by cell.
    import random
    numbers = list(range(1, len(order) + 1))
    random.Random(27).shuffle(numbers)
    idx = dict(zip(order, numbers))
    jobs = [(idx.get(j, (40 if j[1].endswith("w") else 900) + i), *j) for i, j in enumerate(wanted)]
    stage(scratch)
    for ev in sorted({j[1] for j in jobs}):
        fixture(ev)
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j, scratch), jobs):
            print(json.dumps(res, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
