#!/usr/bin/env python3
"""Run the probe described in README.md. Writes results.json and transcripts/.

Usage: run.py --scratch DIR --candidate a|b [--update 8] [--near 4] [--first 1] [--workers 4]
Results go to results-<candidate>.json (appended) and transcripts-<candidate>/.
"""
import argparse, concurrent.futures as cf, json, os, re, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
MODEL = "claude-sonnet-5-5"
PLUGINS = ("design-doc", "unslop", "technical-writing")
DD = os.path.join(REPO, "design-doc-workspace", "evals")
TW = os.path.join(REPO, "technical-writing-workspace", "evals")
EVAL9 = next(e for e in json.load(open(os.path.join(DD, "evals.json")))["evals"] if e["id"] == 9)
EXPORTER = next(e for e in json.load(open(os.path.join(TW, "evals.json")))["evals"] if e["id"] == 1)
CELLS = {"update": (DD, EVAL9["files"], EVAL9["prompt"], 8),
         "near": (TW, EXPORTER["files"], "A gente subiu o limite do export de 100 mil pra 250 mil linhas. "
                                         "Atualiza a documentação.", 4)}
ORIGINAL = "docs/design/exportacao-de-relatorios.md"
MARK = "## Visão geral"
ALLOWED = ["Skill", "Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false"]


def stage(scratch, tag):
    """Copies of the three plugins outside the repository, design-doc with the candidate description."""
    base = os.path.join(scratch, "plugins")
    shutil.rmtree(base, ignore_errors=True)
    for name in PLUGINS:
        shutil.copytree(os.path.join(REPO, name), os.path.join(base, name))
    cand = open(os.path.join(HERE, f"candidate-{tag}.txt"), encoding="utf-8").read().strip()
    path = os.path.join(base, "design-doc", "skills", "design-doc", "SKILL.md")
    text = open(path, encoding="utf-8").read()
    new, n = re.subn(r"description: >\n.*?\n---", lambda m: "description: " + json.dumps(cand, ensure_ascii=False) + "\n---",
                     text, count=1, flags=re.S)
    assert n == 1
    open(path, "w", encoding="utf-8").write(new)


def run(job, scratch, tag):
    idx, cell, n = job
    root, files, prompt, _ = CELLS[cell]
    project = os.path.join(scratch, f"p{idx:02d}", "project")
    shutil.rmtree(os.path.dirname(project), ignore_errors=True)
    for rel in files:
        out = os.path.join(project, *rel.split("/")[2:])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(os.path.join(root, rel), out)
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "start"]):
        subprocess.run([*GIT, *args], cwd=project, check=True)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"
    cmd = ["claude", "-p", prompt, "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--setting-sources", "project,local", "--allowedTools", *ALLOWED]
    for name in PLUGINS:
        cmd += ["--plugin-dir", os.path.join(scratch, "plugins", name)]
    try:
        p = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True, timeout=1800,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"cell": cell, "run": n, "error": "timeout"}
    os.makedirs(os.path.join(HERE, f"transcripts-{tag}"), exist_ok=True)
    open(os.path.join(HERE, f"transcripts-{tag}", f"{cell}-run-{n}.jsonl"), "w").write(p.stdout)
    invoked, final, listed = [], None, None
    for line in p.stdout.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "system" and o.get("subtype") == "init":
            listed = sorted(s for s in (o.get("skills") or []) if s.split(":")[-1] in PLUGINS)
        if o.get("type") == "assistant":
            invoked += [(b["input"].get("skill") or "").split(":")[-1]
                        for b in (o.get("message") or {}).get("content") or []
                        if b.get("type") == "tool_use" and b["name"] == "Skill"]
        if o.get("type") == "result":
            final = o
    if final is None:
        return {"cell": cell, "run": n, "error": (p.stderr or p.stdout)[-300:]}
    res = {"cell": cell, "run": n, "project": f"p{idx:02d}", "installed": listed, "invoked": invoked,
           "D": "design-doc" in invoked, "T": "technical-writing" in invoked,
           "models": sorted((final.get("modelUsage") or {}).keys()), "usd": final.get("total_cost_usd"),
           "turns": final.get("num_turns"), "denials": len(final.get("permission_denials") or []),
           "reply_start": (final.get("result") or "").strip()[:300]}
    if cell == "update":
        before = open(os.path.join(DD, EVAL9["files"][0]), encoding="utf-8").read()
        after = open(os.path.join(project, ORIGINAL), encoding="utf-8").read()
        new = sorted(f for f in os.listdir(os.path.join(project, "docs", "design")) if f != os.path.basename(ORIGINAL))
        res.update({"B": after[after.find(MARK):] != before[before.find(MARK):], "N": bool(new), "new_files": new})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--candidate", required=True, choices=("a", "b"))
    ap.add_argument("--update", type=int, default=8)
    ap.add_argument("--near", type=int, default=4)
    ap.add_argument("--first", type=int, default=1, help="number of the first run, to add runs to a cell")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    if os.path.commonpath([scratch, REPO]) == REPO:
        raise SystemExit("--scratch must be outside the repository")
    stage(scratch, a.candidate)
    jobs = [(i + 1, cell, n) for i, (cell, n) in enumerate(
        [("update", n) for n in range(a.first, a.first + a.update)]
        + [("near", n) for n in range(a.first, a.first + a.near)])]
    path = os.path.join(HERE, f"results-{a.candidate}.json")
    out = json.load(open(path)) if os.path.exists(path) else []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j, scratch, a.candidate), jobs):
            out.append(res)
            print(json.dumps({k: v for k, v in res.items() if k != "reply_start"}, ensure_ascii=False), flush=True)
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    for cell in CELLS:
        rs = [r for r in out if r["cell"] == cell and "error" not in r]
        print(cell, {k: f"{sum(bool(r.get(k)) for r in rs)}/{len(rs)}" for k in ("D", "T", "B", "N")})


if __name__ == "__main__":
    main()
