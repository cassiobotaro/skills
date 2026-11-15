#!/usr/bin/env python3
"""Build one blind judge packet per run under judge-inputs/<id>.md.

The packet carries the user's message, the reply, the files the run left behind
(line-numbered) and the judge-decided checks of the frozen baseline. It does not say
which skill version produced the run; the id -> run mapping lives in judge-map.json,
which judges are not pointed at.
"""
import glob, hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASELINE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))["evals"]
FIXTURE = os.path.join(WS, "evals", "files", "session-service")

RULES = """# Judge packet {pid}

You are grading one reply against a fixed list of yes/no checks. You did not write the
reply. Decide each check on its own, from the material below only.

Rules:
1. A check is MET only if you can quote the exact words (from the reply, or `file:line`
   from the files) that satisfy it. Put that quote in `evidence`.
2. A check is UNMET only after you looked: in `search`, say what you looked for and where
   (e.g. "any sentence naming a design doc, whole reply").
3. If it is borderline, it is UNMET. Say "borderline" in `search` and why.
4. Length, extra detail or extra files never make a check MET. Judge the proposition only.
5. Do not modify anything. Do not open any file other than this packet.

Return ONLY a JSON object, no prose around it:
{{"packet": "{pid}", "checks": [{{"id": "<check id>", "passed": true|false, "evidence": "<quote, or empty>", "search": "<what you looked for, or empty>"}}]}}
with exactly one entry per check listed below, in the same order.
"""


def numbered(text):
    return "\n".join(f"{i + 1:>3}| {l}" for i, l in enumerate(text.rstrip("\n").split("\n")))


def tree(root):
    out = []
    for d, _, fs in os.walk(root):
        for f in fs:
            out.append(os.path.relpath(os.path.join(d, f), root))
    return sorted(out)


def main():
    os.makedirs(os.path.join(HERE, "judge-inputs"), exist_ok=True)
    mapping = {}
    for run in sorted(glob.glob(os.path.join(HERE, "eval-*", "*", "run-*"))):
        rel = os.path.relpath(run, HERE)
        ev = re.search(r"eval-(\d+)-", rel).group(1)
        pid = "p" + hashlib.sha256(("iteration-9:" + rel).encode()).hexdigest()[:8]
        mapping[pid] = rel
        meta = json.load(open(os.path.join(os.path.dirname(os.path.dirname(run)), "eval_metadata.json")))
        reply = open(os.path.join(run, "response.md"), encoding="utf-8").read()
        out = os.path.join(run, "outputs")
        fixture = tree(FIXTURE) if ev == "10" else []
        parts = [RULES.format(pid=pid), "## The user's message\n\n" + meta["prompt"], "## The reply\n\n" + reply.strip()]
        files = tree(out)
        if not files:
            parts.append("## Files in the project after the run\n\nNone. The project directory is empty.")
        else:
            sec = ["## Files in the project after the run"]
            for f in files:
                tag = "existed before the run" if f in fixture else "NEW, written by the run"
                sec.append(f"### {f} ({tag})\n\n```\n{numbered(open(os.path.join(out, f), encoding='utf-8').read())}\n```")
            parts.append("\n\n".join(sec))
        checks = [c for c in BASELINE[ev] if c["kind"] in ("reply", "invention")]
        parts.append("## Checks\n\n" + "\n".join(f"- **{c['id']}** — {c['check']}" for c in checks))
        open(os.path.join(HERE, "judge-inputs", pid + ".md"), "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
        print(pid, rel, len(checks))
    json.dump(mapping, open(os.path.join(HERE, "judge-map.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
