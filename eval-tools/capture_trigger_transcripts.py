#!/usr/bin/env python3
"""Capture full transcripts for a single trigger-eval query.

`run_eval.py` reduces every session to one bit, and it does so at the *first* tool call:
anything that is not `Skill` or `Read` is recorded as a non-trigger immediately. So "did not
trigger" pools together at least three different behaviours — the model answered in prose, it
ran `find`/`grep` over the repo before invoking the skill, or it just did the work by hand.

This script runs the same nested `claude -p` sessions the same way (same injected candidate
command, same flags, serial), but keeps the whole stream and classifies the outcome:

    strict_trigger  the candidate is the first tool call            (what run_eval.py counts)
    late_trigger    the candidate is invoked, but after other tools (run_eval.py: miss)
    other_tool      tools, no candidate ever                        (run_eval.py: miss)
    prose_only      no tool calls at all                            (run_eval.py: miss)

Usage (from the repo root):

    ./eval-tools/capture_trigger_transcripts.py \
        --skill-path structurizr/skills/structurizr \
        --query "modela em Structurizr DSL ..." \
        --model haiku --runs 6 --outdir some-workspace/trigger-evals/transcripts
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path


SKILL_CREATOR_CANDIDATES = [
    Path.home() / ".claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator",
    Path.home() / ".claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator",
]


def read_description(skill_path: Path) -> tuple[str, str]:
    """Read (name, description) with skill-creator's own parser, so the injected candidate
    command is byte-identical to the one run_eval.py writes."""
    for candidate in SKILL_CREATOR_CANDIDATES:
        if (candidate / "scripts/utils.py").is_file():
            sys.path.insert(0, str(candidate))
            break
    else:
        sys.exit("skill-creator not found; install it with: claude plugin install skill-creator@claude-plugins-official")
    from scripts.utils import parse_skill_md
    name, description, _ = parse_skill_md(skill_path)
    return name, description


def run_once(query: str, skill_name: str, description: str, model: str, timeout: int,
             repo_root: Path, transcript_path: Path) -> dict:
    candidate = f"{skill_name}-skill-{uuid.uuid4().hex[:8]}"
    commands_dir = repo_root / ".claude" / "commands"
    command_file = commands_dir / f"{candidate}.md"
    commands_dir.mkdir(parents=True, exist_ok=True)
    indented = "\n  ".join(description.split("\n"))
    command_file.write_text(
        f"---\ndescription: |\n  {indented}\n---\n\n# {skill_name}\n\n"
        f"This skill handles: {description}\n"
    )
    tools: list[str] = []
    texts: list[str] = []
    raw: list[str] = []
    outcome_hint = None
    try:
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        process = subprocess.Popen(
            ["claude", "-p", query, "--output-format", "stream-json", "--verbose",
             "--include-partial-messages", "--setting-sources", "project,local",
             "--model", model],
            cwd=repo_root, env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True,
        )
        deadline = time.time() + timeout
        # stdout iteration blocks between events, so the deadline needs its own killer.
        watchdog = threading.Timer(timeout, process.kill)
        watchdog.start()
        try:
            for line in process.stdout:
                raw.append(line)
                if time.time() > deadline:
                    outcome_hint = "timeout"
                    break
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "result":
                    break
                if event.get("type") != "assistant":
                    continue
                for item in event.get("message", {}).get("content", []):
                    if item.get("type") == "tool_use":
                        target = (item.get("input", {}).get("skill")
                                  or item.get("input", {}).get("file_path")
                                  or item.get("input", {}).get("command")
                                  or item.get("input", {}).get("pattern") or "")
                        tools.append(f"{item.get('name')}({str(target)[:70]})")
                    elif item.get("type") == "text" and item.get("text", "").strip():
                        texts.append(item["text"].strip())
                # Stop as soon as the question is answered: the candidate was invoked, or the
                # session has taken enough tool steps to show what it did instead. Letting a
                # nested session run to completion would have it doing real work in the repo.
                if any(candidate in t for t in tools) or len(tools) >= 6:
                    break
        finally:
            watchdog.cancel()
            if process.poll() is None:
                process.kill()
            process.wait()
            process.stdout.close()
    finally:
        if command_file.exists():
            command_file.unlink()

    transcript_path.write_text("".join(raw))

    hit_indexes = [i for i, t in enumerate(tools) if candidate in t]
    if outcome_hint == "timeout":
        outcome = "timeout"
    elif not tools:
        outcome = "prose_only"
    elif hit_indexes and hit_indexes[0] == 0:
        outcome = "strict_trigger"
    elif hit_indexes:
        outcome = "late_trigger"
    else:
        outcome = "other_tool"
    return {
        "candidate": candidate,
        "outcome": outcome,
        "tools": tools,
        "first_text": (texts[0][:400] if texts else ""),
        "transcript": str(transcript_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--model", default="haiku")
    parser.add_argument("--runs", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    if Path.cwd() != repo_root:
        sys.exit(f"Run this from the repo root: cd {repo_root}")

    skill_name, description = read_description(Path(args.skill_path))
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    runs = []
    for i in range(args.runs):
        record = run_once(args.query, skill_name, description, args.model, args.timeout,
                          repo_root, outdir / f"{skill_name}-run{i:02d}.jsonl")
        runs.append(record)
        print(f"  run {i:02d}: {record['outcome']:15} {' -> '.join(record['tools'][:4])}")

    summary = {"skill": skill_name, "model": args.model, "query": args.query, "runs": runs}
    (outdir / f"{skill_name}-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False))
    counts: dict[str, int] = {}
    for r in runs:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    print(f"\n{skill_name} / {args.model}: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
