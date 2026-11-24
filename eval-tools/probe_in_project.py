#!/usr/bin/env python3
"""Count which skill a session invokes when the request arrives in a real project.

The trigger harness (run_trigger_eval.py) runs in this repository, with no fixture and one
injected candidate, so it cannot measure a request about a file that is in the project:
the session there has nothing to edit and consults the skill. This probe gives each
session a project of its own outside the repository, a fresh git repository holding the
eval's fixture, loads the plugins with --plugin-dir from copies that are also outside the
project, and sends the eval's prompt and nothing else. It counts invocations. It does not
grade what the session wrote: without --add-dir a plugin's references/ cannot be read.

    eval-tools/probe_in_project.py --workspace adr-workspace --plugins adr,unslop \\
        --evals 3,6 --count adr --scratch /tmp/somewhere --out adr-workspace/run-<date>-in-project

--count names the skill whose invocations are the point; --canary-eval (default: the first
of --evals) is run twice with "Use the <skill> skill." before its prompt, because a zero
from a broken harness looks like a zero from the description. Writes <out>/results.json
and <out>/transcripts/. Skills inside the project (.claude/skills/, committed) are found
by `git ls-files` and read without the Skill tool, which is why the plugins stay outside:
see eval-tools/README.md.
"""
import argparse, concurrent.futures as cf, glob, json, os, shutil, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = ["Skill", "Bash(date:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(mkdir:*)", "Bash(cat:*)", "Bash(pwd)"]
GIT = ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false"]


def events_of(stdout, turn):
    """Tool calls of one `claude -p` stream, in order: (turn, tool, skill name or file path)."""
    ev, final, listed = [], None, None
    for line in stdout.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "system" and o.get("subtype") == "init":
            listed = o.get("skills") or []
        if o.get("type") == "assistant" and not o.get("parent_tool_use_id"):
            for b in (o.get("message") or {}).get("content") or []:
                if b.get("type") == "tool_use":
                    i = b["input"]
                    ev.append((turn, b["name"], (i.get("skill") or "").split(":")[-1] or i.get("file_path")
                               or i.get("description") or ""))
        if o.get("type") == "result":
            final = o
    return ev, final, listed


def subagents_of(session_id):
    """Each subagent of the session, read from the transcripts the CLI keeps under ~/.claude/projects."""
    out = []
    for f in sorted(glob.glob(os.path.expanduser(f"~/.claude/projects/*/{session_id}/subagents/agent-*.jsonl"))):
        skills, writes, models = [], [], set()
        for line in open(f):
            try:
                o = json.loads(line)
            except ValueError:
                continue
            m = o.get("message") or {}
            if o.get("type") == "assistant" and isinstance(m.get("content"), list):
                models.add(m.get("model"))
                for b in m["content"]:
                    if b.get("type") == "tool_use" and b["name"] == "Skill":
                        skills.append((b["input"].get("skill") or "").split(":")[-1])
                    if b.get("type") == "tool_use" and b["name"] in ("Write", "Edit"):
                        writes.append((b["name"], b["input"].get("file_path")))
        out.append({"agent": os.path.basename(f)[6:-6], "models": sorted(x for x in models if x),
                    "skills": skills, "writes": writes})
    return out


def run(job, a, evals, plugins):
    idx, ev, n, canary = job
    project = os.path.join(a.scratch, f"p{idx:02d}", "project")
    shutil.rmtree(os.path.dirname(project), ignore_errors=True)
    os.makedirs(project)
    for rel in evals[ev].get("files") or []:
        out = os.path.join(project, *rel.split("/")[a.strip:])   # files/<fixture>/<path> becomes <path>
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(os.path.join(a.spec_dir, rel), out)
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-q", "--allow-empty", "-m", "start"]):
        subprocess.run([*GIT, *args], cwd=project, check=True)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["SHELL"] = "/bin/bash"   # zsh aliases ls to eza here, which lists nothing without a terminal
    prompts = [(f"Use the {a.count} skill. " if canary else "") + evals[ev]["prompt"]]
    if not canary:
        prompts += evals[ev].get("followups") or ([evals[ev]["followup"]] if evals[ev].get("followup") else [])
    allowed = ALLOWED + (["Agent", "Task"] if a.allow_agent else [])
    os.makedirs(os.path.join(a.out, "transcripts"), exist_ok=True)
    tag = f"{'canary' if canary else 'eval-' + ev}-run-{n}"
    events, finals, listed, session = [], [], None, None
    for turn, prompt in enumerate(prompts, 1):
        cmd = ["claude", "-p", prompt, "--model", a.model, "--output-format", "stream-json", "--verbose",
               "--permission-mode", "acceptEdits", "--setting-sources", "project,local", "--allowedTools", *allowed]
        if session:
            cmd += ["--resume", session]
        for name in plugins:
            cmd += ["--plugin-dir", os.path.join(a.scratch, "plugins", name)]
        try:
            p = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True, timeout=a.timeout,
                               stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return {"eval": ev, "run": n, "canary": canary, "error": f"timeout in turn {turn}"}
        suffix = "" if turn == 1 else f"-turn-{turn}"
        open(os.path.join(a.out, "transcripts", tag + suffix + ".jsonl"), "w").write(p.stdout)
        ev_t, final, lst = events_of(p.stdout, turn)
        if final is None:
            return {"eval": ev, "run": n, "canary": canary, "error": f"turn {turn}: " + (p.stderr or p.stdout)[-300:]}
        events += ev_t
        finals.append(final)
        listed = listed or lst
        session = final.get("session_id")
    listed = sorted(s for s in (listed or []) if s.split(":")[-1] in plugins)
    invoked = [d for _, name, d in events if name == "Skill"]
    changed = subprocess.run([*GIT, "status", "--porcelain", "-uall"], cwd=project, capture_output=True, text=True).stdout
    return {"eval": ev, "run": n, "canary": canary, "project": f"p{idx:02d}", "session": session,
            "installed": listed, "invoked": invoked, "hit": a.count in invoked,
            "first_call": bool(events) and events[0][1:] == ("Skill", a.count),
            "events": events, "subagents": subagents_of(session) if session else [],
            "files_changed": sorted(l[3:] for l in changed.splitlines()),
            "models": sorted({m for f in finals for m in (f.get("modelUsage") or {})}),
            "usd": sum(f.get("total_cost_usd") or 0 for f in finals),
            "turns": [f.get("num_turns") for f in finals],
            "denials": sum(len(f.get("permission_denials") or []) for f in finals),
            "replies": [(f.get("result") or "").strip() for f in finals]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", required=True, help="<plugin>-workspace, whose evals/evals.json and fixtures are used")
    ap.add_argument("--plugins", required=True, help="comma-separated plugin directories of the repository to load")
    ap.add_argument("--evals", required=True, help="comma-separated eval ids")
    ap.add_argument("--count", required=True, help="the skill whose invocations are counted")
    ap.add_argument("--scratch", required=True, help="a directory outside the repository")
    ap.add_argument("--out", required=True)
    ap.add_argument("--strip", type=int,
                    help="leading path parts to drop from each fixture file (default: fixture_strip in "
                         "evals.json, else 2): 2 for files/<fixture>/<path>, 1 for files/<path>")
    ap.add_argument("--runs", type=int, default=4)
    ap.add_argument("--canary-eval")
    ap.add_argument("--model", default="claude-opus-5-5", help="a model id, not an alias")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=1500)
    ap.add_argument("--spec", help="an evals.json to read instead of <workspace>/evals/evals.json; its fixture "
                    "paths are relative to its own directory. An eval may carry a \"followup\" prompt, or a list "
                    "of \"followups\", sent as later turns of the same session (--resume); \"/compact\" is one")
    ap.add_argument("--allow-agent", action="store_true", help="let the session start subagents (Agent tool)")
    ap.add_argument("--plugin-src", action="append", default=[], metavar="NAME=DIR",
                    help="load plugin NAME from DIR instead of the repository (a candidate text); repeatable")
    a = ap.parse_args()
    a.scratch, a.out = os.path.abspath(a.scratch), os.path.abspath(a.out)
    if os.path.commonpath([a.scratch, REPO]) == REPO:
        raise SystemExit("--scratch must be outside the repository")
    plugins = a.plugins.split(",")
    ids = a.evals.split(",")
    spec_path = os.path.abspath(a.spec) if a.spec else os.path.join(REPO, a.workspace, "evals", "evals.json")
    a.spec_dir = os.path.dirname(spec_path)
    spec = json.load(open(spec_path))
    evals = {str(e["id"]): e for e in spec["evals"]}
    if a.strip is None:
        a.strip = spec.get("fixture_strip", 2)
    shutil.rmtree(os.path.join(a.scratch, "plugins"), ignore_errors=True)
    src = dict(x.split("=", 1) for x in a.plugin_src)
    for name in plugins:
        shutil.copytree(os.path.abspath(src.get(name, os.path.join(REPO, name))),
                        os.path.join(a.scratch, "plugins", name))
    canary = a.canary_eval or ids[0]
    jobs = [(canary, 1, True), (canary, 2, True)] + [(ev, n, False) for n in range(1, a.runs + 1) for ev in ids]
    jobs = [(i + 1, *j) for i, j in enumerate(jobs)]
    os.makedirs(a.out, exist_ok=True)
    out = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda j: run(j, a, evals, plugins), jobs):
            out.append(res)
            print(json.dumps({k: v for k, v in res.items() if k not in ("replies", "events", "subagents")},
                             ensure_ascii=False), flush=True)
    json.dump({"count": a.count, "plugins": plugins, "plugin_src": src, "model": a.model, "runs": out},
              open(os.path.join(a.out, "results.json"), "w"), ensure_ascii=False, indent=1)
    ok = [r for r in out if "error" not in r]
    print("canary", f"{sum(r['hit'] for r in ok if r['canary'])}/{sum(1 for r in ok if r['canary'])}")
    for ev in ids:
        rs = [r for r in ok if r["eval"] == ev and not r["canary"]]
        print("eval", ev, f"{sum(r['hit'] for r in rs)}/{len(rs)}", "as first call", sum(r["first_call"] for r in rs))
    print("cost US$", round(sum(r.get("usd") or 0 for r in ok), 2), "errors", len(out) - len(ok))


if __name__ == "__main__":
    main()
