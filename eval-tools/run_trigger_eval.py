#!/usr/bin/env python3
"""Run a skill-creator trigger eval correctly against this repo.

The cached skill-creator `run_eval.py` needs two patches to produce a valid number here.
Both were found the expensive way — each one silently reports a healthy-looking sweep of
near-zero triggers, which reads as a description regression rather than a broken harness:

1. `--setting-sources project,local` is not passed to `claude -p`. The skills in this
   repo are installed at *user* scope, so they mask the injected candidate command and every
   positive scores 0. Measured: 0/30 on opus.
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
        --eval-set design-doc-workspace/trigger-evals/trigger_eval.json \
        --skill-path design-doc/skills/design-doc \
        --model claude-sonnet-5-5 -o design-doc-workspace/trigger-evals/some-run.json

It also defaults `--num-workers` to 1, against upstream's 10. Concurrency is an experimental
variable here, not a speed knob: it depresses the trigger rate specifically for queries that
make the session read the repository first, which manufactured a 21pp gap between two skills
that vanished once both were re-measured serially. See
`structurizr-workspace/trigger-evals/README-21pp-analysis.md`.

Any other flags are passed straight through to run_eval.py.

Routine check (the default thing to run after a description change):

    ./eval-tools/run_trigger_eval.py --routine \\
        --eval-set adr-workspace/trigger-evals/trigger_eval.json \\
        --skill-path adr/skills/adr -o adr-workspace/trigger-evals/some-run.json

`--routine` is the whole protocol in one command, on one model: the positives at 3 runs per
query, then the negatives at 3 runs per query with the best-scoring positive as a canary,
serially, with a 120 s timeout, under `systemd-inhibit` when it exists. About 63 sessions
per skill.

It defaults to the target model, claude-sonnet-5-5: the model that reads the user's request
is the one that decides to invoke a skill, and for this repository's skills that is a large
model. There the positives sit at 98-100%, so they are a regression guard (a warning prints
under 90%), and the runs go to the negatives, where the only trigger defect ever found on a
large model was (a false fire at ~17%). Haiku is opt-in (`--model claude-haiku-5-5
--runs-per-query 5`): take one number per release as an early warning, and do not tune a
description to it.
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

ROUTINE_MODEL = "claude-sonnet-5-5"  # the target model; see eval-tools/README.md
ROUTINE_POSITIVE_RUNS = 3
ROUTINE_NEGATIVE_RUNS = 3
ROUTINE_CEILING = 0.90  # the target model has held 98-100% on every skill's positives
ROUTINE_TIMEOUT = 120
INHIBIT = ["systemd-inhibit", "--what=idle:sleep", "--mode=block", "--why=trigger eval sweep"]

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
    if negatives:
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
            "  discard this sweep instead of pooling it, and re-run. Canary: on opus every skill\n"
            "  scores 98-100% on its own positives in a healthy serial sweep.",
            file=sys.stderr,
        )
        return 9
    return 0


def inhibit_prefix() -> list[str]:
    """systemd-inhibit when it works here: a suspend mid-sweep records non-triggers."""
    if not shutil.which(INHIBIT[0]):
        return []
    if subprocess.run([*INHIBIT, "true"], capture_output=True).returncode != 0:
        print("  note: systemd-inhibit is installed but refused; running without it.", file=sys.stderr)
        return []
    return INHIBIT


def run_sweep(script: Path, workdir: Path, repo_root: Path, flags: list[str], prefix: list[str]) -> dict:
    completed = subprocess.run(
        [*prefix, sys.executable, str(script), *flags],
        cwd=repo_root,
        env={**__import__("os").environ, "PYTHONPATH": str(workdir)},
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        sys.exit(completed.returncode)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        sys.stderr.write(completed.stderr)
        sys.exit("run_eval.py produced no JSON. Its stderr is above.")


def routine(args, passthrough: list[str], script: Path, workdir: Path, repo_root: Path) -> int:
    """Positives, then negatives with a canary, on one model. See the module docstring."""
    model = args.model or ROUTINE_MODEL
    timeout = args.timeout or ROUTINE_TIMEOUT
    positive_runs = args.runs_per_query or ROUTINE_POSITIVE_RUNS
    items = json.loads(Path(args.eval_set).read_text())
    positives = [i for i in items if i["should_trigger"]]
    negatives = [i for i in items if not i["should_trigger"]]
    if not positives or not negatives:
        sys.exit("--routine needs an eval set with both should_trigger true and false queries.")
    copies = max(1, -(-args.canary_runs // args.negative_runs))
    canary_total = copies * args.negative_runs
    sessions = len(positives) * positive_runs + len(negatives) * args.negative_runs + canary_total
    print(
        f"Routine check on {model}: {len(positives)} positives x {positive_runs}, "
        f"{len(negatives)} negatives x {args.negative_runs}, canary x {canary_total} "
        f"= {sessions} sessions, serial, timeout {timeout}s"
    )
    if not model.startswith("claude-"):
        print(f"  note: '{model}' is an alias. Record the id it resolved to next to the number.", file=sys.stderr)
    prefix = [] if args.no_inhibit else inhibit_prefix()
    common = [*passthrough, "--model", model, "--timeout", str(timeout), "--num-workers", "1"]

    def sweep(queries: list[dict], runs: int, name: str) -> dict:
        path = workdir / f"{name}.json"
        path.write_text(json.dumps(queries, ensure_ascii=False))
        return run_sweep(script, workdir, repo_root, [*common, "--eval-set", str(path), "--runs-per-query", str(runs)], prefix)

    protocol = {"model": model, "timeout": timeout, "num_workers": 1, "positive_runs": positive_runs,
                "negative_runs": args.negative_runs, "canary_runs": canary_total}
    pos = sweep(positives, positive_runs, "positives")
    out = {"skill_name": pos["skill_name"], "description": pos["description"], "protocol": protocol,
           "results": pos["results"], "canary": None}
    code = summarize(pos)
    if code:
        if args.output:
            Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print("  Negatives not run: the positives look degraded.", file=sys.stderr)
        return code

    hits = sum(r["triggers"] for r in pos["results"])
    runs = sum(r["runs"] for r in pos["results"])
    if model == ROUTINE_MODEL and hits / runs < ROUTINE_CEILING:
        print(
            f"\n  WARNING: {hits}/{runs} on {model}, which has held 98-100% on every skill's\n"
            "  positives. A regression candidate, not yet a regression: two identical sweeps\n"
            "  move 4-6 points at n=50, more at this size. Re-run before reading it.\n",
            file=sys.stderr,
        )

    best = max(pos["results"], key=lambda r: r["triggers"])
    if best["triggers"] < best["runs"]:
        print(f"  note: no positive reached a full run; the canary is the best one, at {best['triggers']}/{best['runs']}.")
    canary_item = {"query": best["query"], "should_trigger": True}
    neg = sweep([*negatives, *[canary_item] * copies], args.negative_runs, "negatives")
    canary = next(r for r in neg["results"] if r["should_trigger"])
    neg_results = [r for r in neg["results"] if not r["should_trigger"]]
    fired = [r for r in neg_results if r["triggers"]]
    out["results"] = [*pos["results"], *neg_results]
    out["canary"] = {**canary, "positive_score": f"{best['triggers']}/{best['runs']}"}
    if args.output:
        Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print(f"Wrote {args.output}")

    print(f"  false fires {sum(r['triggers'] for r in neg_results)}/{sum(r['runs'] for r in neg_results)}")
    for r in fired:
        print(f"    fired {r['triggers']}/{r['runs']}: {r['query'][:90]}")
    print(f"  canary      {canary['triggers']}/{canary['runs']}")
    if canary["triggers"] == 0:
        print(
            "\n  WARNING: the canary never fired, so the negatives pass cannot tell a clean zero\n"
            "  from a broken harness. Do not quote the false-fire count; re-run.",
            file=sys.stderr,
        )
        return 9
    if canary["triggers"] < canary["runs"]:
        print("  note: the canary missed some runs. The harness was alive; the zeros stand, loosely.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False
    )
    parser.add_argument("-o", "--output", help="Write the result JSON here as well as summarizing it")
    parser.add_argument(
        "--num-workers", type=int, default=1,
        help="Concurrent sessions (default 1). An experimental variable, not a speed knob — "
             "see the warning this prints above 1.",
    )
    parser.add_argument(
        "--routine", action="store_true",
        help="The routine check: positives, then negatives with a canary, on one model "
             f"(default {ROUTINE_MODEL}). See the top of this file.",
    )
    parser.add_argument("--eval-set", help="Eval set JSON (passed to run_eval.py; --routine splits it)")
    parser.add_argument("--model", help=f"Model id (passed to run_eval.py; --routine defaults to {ROUTINE_MODEL})")
    parser.add_argument("--runs-per-query", type=int, help=f"Runs per query (--routine: positives, default {ROUTINE_POSITIVE_RUNS})")
    parser.add_argument("--timeout", type=int, help=f"Seconds per session (--routine defaults to {ROUTINE_TIMEOUT})")
    parser.add_argument("--negative-runs", type=int, default=ROUTINE_NEGATIVE_RUNS,
                        help=f"--routine: runs per negative query (default {ROUTINE_NEGATIVE_RUNS})")
    parser.add_argument("--canary-runs", type=int, default=3, help="--routine: canary runs in the negatives pass (default 3)")
    parser.add_argument("--no-inhibit", action="store_true", help="--routine: do not wrap the sweeps in systemd-inhibit")
    args, passthrough = parser.parse_known_args()

    if args.routine:
        if args.num_workers != 1:
            sys.exit("--routine produces the number you quote, so it runs serially. Drop --num-workers.")
        if not args.eval_set:
            sys.exit("--routine needs --eval-set.")
    else:
        # Single sweep, as before: hand the flags this wrapper parsed back to run_eval.py.
        for flag, value in (("--eval-set", args.eval_set), ("--model", args.model),
                            ("--runs-per-query", args.runs_per_query), ("--timeout", args.timeout)):
            if value is not None:
                passthrough = [*passthrough, flag, str(value)]

    # Upstream defaults this to 10, which is why the wrapper owns the flag instead of passing
    # it through: a rate measured at ten workers is not comparable with a serial one.
    if args.num_workers > 1:
        print(
            f"\n  WARNING: --num-workers {args.num_workers}. Concurrency depresses the trigger\n"
            "  rate, and not evenly — the penalty lands on queries that make the session read\n"
            "  the repository before it can act. Measured on the structurizr set: 60% at ten\n"
            "  workers against 78% serially, manufacturing a 21pp gap against another skill that\n"
            "  does not exist. Treat this run as a smoke test: do\n"
            "  not quote it, and do not table it beside a serial number.\n",
            file=sys.stderr,
        )

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
        if args.routine:
            return routine(args, passthrough, script, workdir, repo_root)
        result = run_sweep(script, workdir, repo_root, [*passthrough, "--num-workers", str(args.num_workers)], [])

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"Wrote {args.output}")
    return summarize(result)


if __name__ == "__main__":
    sys.exit(main())
