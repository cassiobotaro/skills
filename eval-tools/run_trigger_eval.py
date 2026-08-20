#!/usr/bin/env python3
"""Run a skill-creator trigger eval correctly against this repo.

The cached skill-creator `run_eval.py` needs two patches to produce a valid number here.
Both were found the expensive way — each one silently reports a healthy-looking sweep of
near-zero triggers, which reads as a description regression rather than a broken harness:

1. `--setting-sources project,local` is not passed to `claude -p`. The four skills in this
   repo are installed at *user* scope, so they mask the injected candidate command and every
   positive scores 0. Measured: adr/opus 0/30.
2. A trigger is counted only when the session picks the *calling worker's own* candidate
   (`<skill>-skill-<uuid>`). Every worker writes its own copy into the same
   `.claude/commands/`, so with `--num-workers 10` the session sees ten identical candidates
   and picks one at random: recall comes out divided by roughly `num_workers`. Measured on
   the same set and model: 2/30 with uuid matching, 14-20/30 matching the `<skill>-skill-`
   prefix.

This wrapper patches a throwaway copy of the upstream script rather than vendoring it, so it
tracks upstream. If a patch stops applying, it fails loudly — upstream probably fixed the bug
and the corresponding patch should be dropped rather than forced.

Usage (from the repo root):

    ./eval-tools/run_trigger_eval.py \
        --eval-set adr-workspace/trigger-evals/trigger_eval.json \
        --skill-path adr/skills/adr \
        --model haiku -o adr-workspace/trigger-evals/some-run.json

Any other flags are passed straight through to run_eval.py.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_CREATOR_CANDIDATES = [
    Path.home() / ".claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator",
    Path.home() / ".claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator",
]

PATCHES = [
    (
        "setting-sources",
        '            "--include-partial-messages",\n        ]',
        '            "--include-partial-messages",\n            "--setting-sources", "project,local",\n        ]',
    ),
    (
        "prefix-match: bind",
        '    command_file = project_commands_dir / f"{clean_name}.md"',
        '    command_file = project_commands_dir / f"{clean_name}.md"\n    match_prefix = f"{skill_name}-skill-"',
    ),
    (
        "prefix-match: stream delta",
        "                                if clean_name in accumulated_json:",
        "                                if match_prefix in accumulated_json:",
    ),
    (
        "prefix-match: block stop",
        "                                return clean_name in accumulated_json",
        "                                return match_prefix in accumulated_json",
    ),
    (
        "prefix-match: Skill fallback",
        '                            if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):',
        '                            if tool_name == "Skill" and match_prefix in tool_input.get("skill", ""):',
    ),
    (
        "prefix-match: Read fallback",
        '                            elif tool_name == "Read" and clean_name in tool_input.get("file_path", ""):',
        '                            elif tool_name == "Read" and match_prefix in tool_input.get("file_path", ""):',
    ),
]


def find_skill_creator() -> Path:
    for path in SKILL_CREATOR_CANDIDATES:
        if (path / "scripts/run_eval.py").is_file():
            return path
    sys.exit(
        "skill-creator not found. Looked in:\n  "
        + "\n  ".join(str(p) for p in SKILL_CREATOR_CANDIDATES)
        + "\nInstall it with: claude plugin install skill-creator@claude-plugins-official"
    )


def build_patched_copy(skill_creator: Path, workdir: Path) -> Path:
    shutil.copytree(skill_creator / "scripts", workdir / "scripts")
    target = workdir / "scripts/run_eval.py"
    source = target.read_text()
    for name, old, new in PATCHES:
        count = source.count(old)
        if count != 1:
            sys.exit(
                f"Patch '{name}' matched {count} times in the upstream run_eval.py, expected 1.\n"
                f"Upstream changed. Re-read {skill_creator / 'scripts/run_eval.py'} and either\n"
                f"update this patch or drop it if upstream fixed the bug."
            )
        source = source.replace(old, new)
    target.write_text(source)
    return target


def summarize(result: dict) -> int:
    """Print the summary and flag the degraded-sweep signature. Returns an exit code."""
    positives = [r for r in result["results"] if r["should_trigger"]]
    negatives = [r for r in result["results"] if not r["should_trigger"]]
    hits = sum(r["triggers"] for r in positives)
    runs = sum(r["runs"] for r in positives)
    false_fires = sum(r["triggers"] for r in negatives)
    distribution = sorted(r["triggers"] for r in positives)

    print(f"  positives   {hits}/{runs} ({100 * hits / runs:.0f}%)")
    print(f"  false fires {false_fires}/{sum(r['runs'] for r in negatives)}")
    print(f"  per-query   {distribution}")

    # When the nested sessions stop firing — a usage limit, a failing CLI — every query
    # collapses toward zero at once. That is a broken sweep, not a description regression, and
    # must never be pooled into a result.
    #
    # The tell is the whole distribution sitting on the floor, not any single query missing a
    # full run: at a per-query trigger probability near 0.4, no query reaching `runs_per_query`
    # is the *expected* outcome on a short set, and an earlier version of this check cried wolf
    # on healthy 30-run samples. Require both a very low aggregate and a ceiling barely off
    # zero before calling a sweep broken.
    runs_per_query = max(r["runs"] for r in positives) if positives else 0
    floored = distribution and max(distribution) <= max(1, runs_per_query // 4)
    if positives and hits / runs < 0.15 and floored:
        print(
            f"\n  WARNING: aggregate {hits}/{runs} with a per-query ceiling of "
            f"{max(distribution)}/{runs_per_query}. This is the degraded-sweep signature —\n"
            "  discard this sweep instead of pooling it, and re-run. Canary: adr/opus on its\n"
            "  own set has scored 14-20/30 across healthy sweeps.",
            file=sys.stderr,
        )
        return 9
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-o", "--output", help="Write the result JSON here as well as summarizing it")
    args, passthrough = parser.parse_known_args()

    repo_root = Path(__file__).resolve().parent.parent
    if Path.cwd() != repo_root:
        # run_eval.py finds the project root by walking up from the cwd to the first directory
        # holding a .claude/, and injects the candidate command there. Anywhere else, the
        # command lands in one project while the nested session evaluates another.
        sys.exit(f"Run this from the repo root: cd {repo_root}")

    skill_creator = find_skill_creator()
    with tempfile.TemporaryDirectory(prefix="trigger-eval-") as tmp:
        workdir = Path(tmp)
        script = build_patched_copy(skill_creator, workdir)
        print(f"Patched copy of {skill_creator.name}'s run_eval.py ({len(PATCHES)} patches applied)")

        completed = subprocess.run(
            [sys.executable, str(script), *passthrough],
            cwd=repo_root,
            env={**__import__("os").environ, "PYTHONPATH": str(workdir)},
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            sys.stderr.write(completed.stderr)
            return completed.returncode
        try:
            result = json.loads(completed.stdout)
        except json.JSONDecodeError:
            sys.stderr.write(completed.stderr)
            sys.exit("run_eval.py produced no JSON. Its stderr is above.")

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"Wrote {args.output}")
    return summarize(result)


if __name__ == "__main__":
    sys.exit(main())
