#!/usr/bin/env python3
"""Run the executors of iteration-16: one headless session (claude -p) per run.

Each cell is a skill snapshot plus the directory the session starts in. The start
directory decides which AGENTS.md text reaches the context: ctx-a holds the file as
committed at 2bc0e04 (with the per-skill notes), ctx-b the file as trimmed on 2026-11-20.
The repository root's own AGENTS.md (trimmed) is loaded in both, so the cells differ by
the removed text only. The brief is iteration-9's, word for word, with the paths changed.

Usage: run.py <cell>:<run> [<cell>:<run> ...] [--workers N] [--transcripts DIR]
"""
import argparse, concurrent.futures as cf, json, os, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
EVAL = "eval-8-scope-open-design-request"
MODEL = "claude-sonnet-5-5"
CELLS = {
    "cell-a": {"skill": "skill-snapshot-1.3.2", "ctx": "ctx-a"},
    "cell-b": {"skill": "skill-snapshot-1.3.2", "ctx": "ctx-b"},
    "cell-c": {"skill": "skill-snapshot-1.4.0", "ctx": "ctx-b"},
}
PROMPT = json.load(open(os.path.join(WS, "evals", "evals.json")))["evals"]
PROMPT = next(e for e in PROMPT if e["id"] == 8)["prompt"]

BRIEF = """You are handling a user's request with the help of a skill.

1. Read the skill at {skill}/SKILL.md and follow it, including reading any reference file it tells you to read (they sit next to it under references/).
2. The user's repository is this directory, which is your project root and working directory: {root}
   Work only inside it. Treat it as the top of the repository: do not read, search or write anything above it (the surrounding checkout is unrelated tooling), apart from the skill files in step 1.
3. The user's message is:

"{prompt}"

4. Nobody is available to answer follow-up questions in this session. If you would ask the user something, put the question in your reply and stop there.
5. When you are done, save the reply you would send to the user, exactly as you would send it, to {response} (this file is the only thing you may write outside the project root). Then return that same reply verbatim as your final message, followed by one last line of the form `MODEL: <your exact model id>`."""

ALLOWED = ["Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]


def run(cell, n, transcripts):
    cfg = CELLS[cell]
    rundir = os.path.join(HERE, EVAL, cell, f"run-{n}")
    root = os.path.join(rundir, "outputs")
    os.makedirs(root, exist_ok=True)
    brief = BRIEF.format(skill=os.path.join(WS, cfg["skill"]), root=root, prompt=PROMPT,
                         response=os.path.join(rundir, "response.md"))
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = ["claude", "-p", brief, "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--allowedTools", *ALLOWED]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=os.path.join(HERE, cfg["ctx"]), env=env, capture_output=True,
                       text=True, timeout=900)
    os.makedirs(transcripts, exist_ok=True)
    open(os.path.join(transcripts, f"{cell}-run-{n}.jsonl"), "w").write(p.stdout)
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
        return {"cell": cell, "run": n, "error": (p.stderr or p.stdout)[-400:]}
    u = final.get("usage") or {}
    total = sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                        "cache_read_input_tokens", "output_tokens"))
    timing = {"total_tokens": total, "duration_ms": final.get("duration_ms"),
              "total_duration_seconds": round(time.time() - t0, 1),
              "cost_usd": final.get("total_cost_usd"), "num_turns": final.get("num_turns"),
              "models": sorted((final.get("modelUsage") or {}).keys()),
              "permission_denials": final.get("permission_denials") or [], "tool_calls": tools}
    json.dump(timing, open(os.path.join(rundir, "timing.json"), "w"), indent=2)
    if not os.path.exists(os.path.join(rundir, "response.md")):
        open(os.path.join(rundir, "response.md"), "w").write(final.get("result") or "")
        timing["response_salvaged"] = True
    return {"cell": cell, "run": n, "tokens": total, "usd": final.get("total_cost_usd"),
            "turns": final.get("num_turns"), "denials": len(timing["permission_denials"]),
            "skill_tool": [t["target"] for t in tools if t["tool"] == "Skill"],
            "salvaged": timing.get("response_salvaged", False)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--transcripts", required=True)
    a = ap.parse_args()
    jobs = [(r.split(":")[0], int(r.split(":")[1])) for r in a.runs]
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j[0], j[1], a.transcripts), jobs):
            print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
