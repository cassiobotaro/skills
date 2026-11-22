#!/usr/bin/env python3
"""Run the border probe described in README.md: eval 9 of design-doc, prompt alone, with
`technical-writing` installed (`both`) or not (`alone`). One headless session per run, in
a project outside the repository. Writes results.json and transcripts/.

--install project  copies the skills into the project's .claude/skills/ (the first
                   attempt, kept as results-in-project.json: the session finds the skill
                   files with `git ls-files` and reads them without the Skill tool)
--install plugin   loads each plugin from a copy outside the project with --plugin-dir,
                   so the project holds only the fixture (the default)

Usage: run.py --scratch DIR [--install plugin] [--runs 8] [--workers 4]
"""
import argparse, concurrent.futures as cf, json, os, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DD = os.path.join(REPO, "design-doc-workspace", "evals")
MODEL = "claude-sonnet-5-5"
SKILLS = {"alone": ("design-doc", "unslop"), "both": ("design-doc", "unslop", "technical-writing")}
EVAL = next(e for e in json.load(open(os.path.join(DD, "evals.json")))["evals"] if e["id"] == 9)
ORIGINAL = "docs/design/exportacao-de-relatorios.md"
MARK = "## Visão geral"
ALLOWED = ["Skill", "Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false"]


def body(text):
    return text[text.find(MARK):]


def short(name):
    return (name or "").split(":")[-1]


def run(job, scratch, install):
    idx, cell, n = job
    project = os.path.join(scratch, f"p{idx:02d}", "project")
    shutil.rmtree(os.path.dirname(project), ignore_errors=True)
    for rel in EVAL["files"]:
        out = os.path.join(project, *rel.split("/")[2:])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(os.path.join(DD, rel), out)
    plugins = []
    for name in SKILLS[cell]:
        if install == "project":
            shutil.copytree(os.path.join(REPO, name, "skills", name), os.path.join(project, ".claude", "skills", name))
        else:
            plugins += ["--plugin-dir", os.path.join(scratch, "plugins", name)]
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "start"]):
        subprocess.run([*GIT, *args], cwd=project, check=True)
    before = open(os.path.join(project, ORIGINAL), encoding="utf-8").read()
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"
    cmd = ["claude", "-p", EVAL["prompt"], "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--setting-sources", "project,local", "--allowedTools", *ALLOWED, *plugins]
    try:
        p = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True, timeout=1800,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"cell": cell, "run": n, "error": "timeout"}
    os.makedirs(os.path.join(HERE, "transcripts"), exist_ok=True)
    open(os.path.join(HERE, "transcripts", f"{cell}-run-{n}.jsonl"), "w").write(p.stdout)
    invoked, final, listed, read_files = [], None, None, set()
    for line in p.stdout.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "system" and o.get("subtype") == "init":
            listed = sorted(s for s in (o.get("skills") or []) if short(s) in SKILLS["both"])
        if o.get("type") == "assistant":
            read_files |= {name for b in (o.get("message") or {}).get("content") or []
                           if b.get("type") == "tool_use" and b["name"] != "Skill"
                           for name in SKILLS["both"] if f"/{name}/skills/{name}/" in json.dumps(b["input"])
                           or f".claude/skills/{name}/" in json.dumps(b["input"])}
            invoked += [short(b["input"].get("skill")) for b in (o.get("message") or {}).get("content") or []
                        if b.get("type") == "tool_use" and b["name"] == "Skill"]
        if o.get("type") == "result":
            final = o
    if final is None:
        return {"cell": cell, "run": n, "error": (p.stderr or p.stdout)[-300:]}
    after = open(os.path.join(project, ORIGINAL), encoding="utf-8").read()
    new = sorted(f for f in os.listdir(os.path.join(project, "docs", "design")) if f != os.path.basename(ORIGINAL))
    return {"cell": cell, "run": n, "project": f"p{idx:02d}", "installed": listed, "invoked": invoked,
            "D": "design-doc" in invoked, "T": "technical-writing" in invoked,
            "B": body(after) != body(before), "N": bool(new), "new_files": new,
            "skill_files_touched_outside_skill_tool": sorted(read_files),
            "denials": len(final.get("permission_denials") or []),
            "models": sorted((final.get("modelUsage") or {}).keys()), "usd": final.get("total_cost_usd"),
            "turns": final.get("num_turns"), "reply_start": (final.get("result") or "").strip()[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--install", choices=("project", "plugin"), default="plugin")
    ap.add_argument("--runs", type=int, default=8)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    if os.path.commonpath([scratch, REPO]) == REPO:
        raise SystemExit("--scratch must be outside the repository")
    if a.install == "plugin":   # copies of the plugin directories, outside the repository and the projects
        shutil.rmtree(os.path.join(scratch, "plugins"), ignore_errors=True)
        for name in SKILLS["both"]:
            shutil.copytree(os.path.join(REPO, name), os.path.join(scratch, "plugins", name))
    jobs = [(i * 2 + k + 1, cell, i + 1) for i in range(a.runs) for k, cell in enumerate(SKILLS)]
    out = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j, scratch, a.install), jobs):
            out.append(res)
            print(json.dumps({k: v for k, v in res.items() if k != "reply_start"}, ensure_ascii=False), flush=True)
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), ensure_ascii=False, indent=1)
    for cell in SKILLS:
        rs = [r for r in out if r["cell"] == cell and "error" not in r]
        print(cell, {k: f"{sum(r[k] for r in rs)}/{len(rs)}" for k in "DTBN"})


if __name__ == "__main__":
    main()
