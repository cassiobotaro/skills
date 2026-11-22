#!/usr/bin/env python3
"""Run the executors of iteration-17: one headless session (claude -p) per run.

Three cells: `no_skill` (the brief without the skill step), `skill_150` (adr 1.5.0,
../skill-snapshot-1.5.0) and `skill_160` (the working tree as edited). Each run starts
from the eval's fixture in a project of its own outside this repository (--scratch), in
a fresh git repository, so that no AGENTS.md, no neighbouring skill and no earlier
output is in reach of any cell. Project directories are numbered and the skills are
copied to neutral names (s1, s2), so no path names the cell.

An eval with a `followup` (eval 12) is two turns: a session that wrote no file is
resumed once with that fixed answer. The project is copied after each turn.

Usage: run.py --scratch DIR --cells no_skill,skill_150 [--evals 1,3] [--runs 3] [--workers 6]
"""
import argparse, concurrent.futures as cf, datetime, json, os, shutil, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
REPO = os.path.dirname(WS)
MODEL = "claude-sonnet-5-5"
SKILLS = {"no_skill": None,
          "skill_150": ("s1", os.path.join(WS, "skill-snapshot-1.5.0")),
          "skill_160": ("s2", os.path.join(REPO, "adr", "skills", "adr"))}
EVALS = {str(e["id"]): e for e in json.load(open(os.path.join(WS, "evals", "evals.json")))["evals"]}
DEFAULT = "1,2,3,4,5,6,7,11,12"

SKILL_STEP = ("Read the skill at {skill}/SKILL.md and follow it, including reading any reference "
              "file it tells you to read (they sit next to it under references/).")
ROOT_STEP = ("The user's repository is this directory, which is your project root and working "
             "directory: {root}\n   Work only inside it. Treat it as the top of the repository: do not "
             "read, search or write anything above it{apart}.")
MESSAGE_STEP = "The user's message is:\n\n<user_message>\n{prompt}\n</user_message>\n"
ASK_STEP = ("If you need something from the user before you can proceed, ask in your reply and stop "
            "there; the user will answer.")
REPLY_STEP = ("When you are done, end with the reply you would send to the user, exactly as you would "
              "send it. Your final message is taken as that reply.")
ANSWER = ("The user's answer is:\n\n<user_message>\n{text}\n</user_message>\n\n"
          "Continue, and end with the reply you would send to the user.")

ALLOWED = ["Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)",
           "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(diff:*)"]
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false"]


def brief(skill, root, prompt):
    steps = [SKILL_STEP.format(skill=skill)] if skill else []
    steps += [ROOT_STEP.format(root=root, apart=", apart from the skill files in step 1" if skill else ""),
              MESSAGE_STEP.format(prompt=prompt), ASK_STEP, REPLY_STEP]
    head = "You are handling a user's request" + (" with the help of a skill.\n\n" if skill else ".\n\n")
    return head + "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1)) + "\n"


def files(root):
    out = {}
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x != ".git"]
        for f in fs:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = open(p, "rb").read()
    return out


def fixture(ev, dst):
    """files/<fixture name>/<path> of the eval becomes <path> in the project."""
    os.makedirs(dst)
    for rel in EVALS[ev]["files"]:
        out = os.path.join(dst, *rel.split("/")[2:])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(os.path.join(WS, "evals", rel), out)


def call(text, skill, root, log, resume=None):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"   # zsh aliases ls to eza here, which lists nothing without a terminal
    cmd = ["claude", "-p", text, "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--setting-sources", "project,local",
           "--allowedTools", *ALLOWED]
    if skill:
        cmd += ["--add-dir", skill]   # the skill sits outside the project root
    if resume:
        cmd += ["--resume", resume]
    try:
        p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=900,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"error": "timeout after 900 s"}
    open(log, "w").write(p.stdout)
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
        return {"error": (p.stderr or p.stdout)[-400:]}
    u = final.get("usage") or {}
    return {"reply": (final.get("result") or "").strip(), "session": final.get("session_id"),
            "tokens": sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                                  "cache_read_input_tokens", "output_tokens")),
            "usd": final.get("total_cost_usd") or 0.0, "turns": final.get("num_turns") or 0,
            "models": sorted((final.get("modelUsage") or {}).keys()),
            "skills": init.get("skills"), "denials": final.get("permission_denials") or [], "tools": tools}


def run(job, scratch):
    idx, ev, cell, n = job
    rundir = os.path.join(HERE, f"eval-{ev}-{EVALS[ev]['name']}", cell, f"run-{n}")
    if os.path.exists(os.path.join(rundir, "timing.json")):
        return {"eval": ev, "cell": cell, "run": n, "skipped": True}
    skill = SKILLS[cell] and os.path.join(scratch, "skills", SKILLS[cell][0])
    project = os.path.join(scratch, "projects", f"p{idx:03d}", "project")
    shutil.rmtree(os.path.dirname(project), ignore_errors=True)
    fixture(ev, project)
    subprocess.run([*GIT, "init", "-q"], cwd=project, check=True)
    subprocess.run([*GIT, "add", "-A"], cwd=project, check=True)
    subprocess.run([*GIT, "commit", "-q", "--allow-empty", "-m", "start"], cwd=project, check=True)
    before = files(project)
    logs = os.path.join(scratch, "transcripts")
    os.makedirs(logs, exist_ok=True)
    t0, day0 = time.time(), datetime.date.today().isoformat()
    calls = [call(brief(skill, project, EVALS[ev]["prompt"]), skill, project, os.path.join(logs, f"p{idx:03d}-a.jsonl"))]
    if "error" in calls[0]:
        return {"eval": ev, "cell": cell, "run": n, "error": calls[0]["error"]}
    shutil.rmtree(rundir, ignore_errors=True)
    os.makedirs(rundir)
    answer = EVALS[ev].get("followup")
    if answer and files(project) == before:
        shutil.copytree(project, os.path.join(rundir, "outputs-before-answer"), ignore=shutil.ignore_patterns(".git"))
        more = call(ANSWER.format(text=answer), skill, project, os.path.join(logs, f"p{idx:03d}-b.jsonl"),
                    resume=calls[0]["session"])
        if "error" in more:
            return {"eval": ev, "cell": cell, "run": n, "error": "answer: " + more["error"]}
        calls.append(more)
    shutil.copytree(project, os.path.join(rundir, "outputs"), ignore=shutil.ignore_patterns(".git"))
    if answer:   # one reply file holding both turns, labelled, for the judge packet
        parts = ["FIRST REPLY (before any answer from the user):\n\n" + calls[0]["reply"]]
        if len(calls) > 1:
            parts += ["THE USER'S ANSWER:\n\n" + answer, "FINAL REPLY:\n\n" + calls[1]["reply"]]
        else:
            parts += ["(The first turn already wrote a file, so the user's answer was never sent. "
                      "The first reply is also the final reply.)"]
        open(os.path.join(rundir, "response.md"), "w").write("\n\n-----\n\n".join(parts) + "\n")
    else:
        open(os.path.join(rundir, "response.md"), "w").write(calls[0]["reply"] + "\n")
    tools = [t for c in calls for t in c["tools"]]
    timing = {"project": f"p{idx:03d}", "total_tokens": sum(c["tokens"] for c in calls),
              "cost_usd": round(sum(c["usd"] for c in calls), 4), "num_turns": sum(c["turns"] for c in calls),
              "first_turn_tokens": calls[0]["tokens"], "first_turn_turns": calls[0]["turns"],
              "total_duration_seconds": round(time.time() - t0, 1),
              "dates": sorted({day0, datetime.date.today().isoformat()}),
              "answered": len(calls) > 1, "models": sorted({m for c in calls for m in c["models"]}),
              "skills_listed": calls[0]["skills"],
              "skill_files_read": sorted({os.path.relpath(t["target"], skill) for t in tools
                                          if skill and t["tool"] == "Read" and t["target"].startswith(skill)}),
              "permission_denials": [d for c in calls for d in c["denials"]], "tool_calls": tools}
    json.dump(timing, open(os.path.join(rundir, "timing.json"), "w"), indent=2)
    return {"eval": ev, "cell": cell, "run": n, "tokens": timing["total_tokens"], "usd": timing["cost_usd"],
            "turns": timing["num_turns"], "answered": timing["answered"], "read": timing["skill_files_read"],
            "denials": len(timing["permission_denials"]),
            "new": sorted(p for p in files(project) if p not in before)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--cells", required=True)
    ap.add_argument("--evals", default=DEFAULT)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    cells = a.cells.split(",")
    for cell in cells:   # copy the skills before the workers start
        if SKILLS[cell]:
            dst = os.path.join(scratch, "skills", SKILLS[cell][0])
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(SKILLS[cell][1], dst)
    order = list(SKILLS)
    jobs = []
    for ev in a.evals.split(","):
        for cell in cells:
            for n in range(1, a.runs + 1):
                idx = (int(ev) * 10 + order.index(cell)) * 10 + n   # stable, and silent about the cell
                jobs.append((idx, ev, cell, n))
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j, scratch), jobs):
            print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
