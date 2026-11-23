# Evals

Read this before running an eval or quoting a number from one. It is not loaded automatically:
`AGENTS.md` points here.

## What is kept, and where the rest went

Each `<plugin>-workspace/` holds only the spec:

- `evals/evals.json` — the eval set (prompt, `expected_output`, optional `files/`, assertions),
  its `smoke` list and its `fixture_strip` (2 for `files/<fixture>/<path>`, 1 for
  `files/<path>`). This is the spec for what the skill must do; **read it before changing a
  skill's behavior**.
- `evals/checks-baseline.json` — the frozen yes/no checks the judges grade against, where the
  skill has one. Do not edit a check to fit an output; amend it with a dated note.
- `trigger-evals/trigger_eval.json` — the trigger set (positives and negatives).

Every run, transcript, iteration and experiment README until 2026-11-23 is in the git tag
`archive/evals-2026-11-23` (`git show archive/evals-2026-11-23:<path>`, or
`git checkout archive/evals-2026-11-23 -- <dir>` into a scratch branch). The per-skill notes in
`MAINTAINING.md` keep the decisions and the numbers that made them. New runs go to
`<plugin>-workspace/run-<date>-<label>/`, which is gitignored: write what a run decided into
the skill's note, not a new committed directory.

## Which model

The target model is **claude-opus-5-5**, the model the author runs these skills on. Every
helper defaults to it. Quote numbers by model id, never by alias.

Other models are not measured by default. Most numbers recorded until 2026-11-23 are on
claude-sonnet-5-5, and some behaviors differ: sonnet and haiku skip an `unslop` call from
another skill that opus makes in every session (`unslop` note in `MAINTAINING.md`). Do not
change a skill to fix a behavior seen only on a model the author does not use.

## The routine for a skill change

1. **Smoke set, one run, read it yourself.**

   ```bash
   eval-tools/run_evals.py <plugin>                       # smoke ids, 1 run each, opus
   eval-tools/run_evals.py <plugin> --skill-dir <copy>    # a candidate text
   ```

   Read every `response.md` and the files under `outputs/` against the eval's
   `expected_output`. A few dollars at most. This is enough for most changes.
2. **Full set with judges, only for a large change** (a new rule, a rewritten step, a
   description change that moves what the skill claims):

   ```bash
   eval-tools/run_evals.py <plugin> --evals all --runs 2 --label full
   eval-tools/judge.py packets <plugin>-workspace/run-<date>-full
   eval-tools/judge.py judge   <plugin>-workspace/run-<date>-full
   eval-tools/judge.py table   <plugin>-workspace/run-<date>-full
   ```

   Checks of kind `file` and `absence` need a `script-checks.json` in the run directory
   (`{"<run key>": {"<check id>": true}}`); without it they are reported as not scored.
3. **Trigger check, only when the description changes**: `run_trigger_eval.py --routine` on
   the current text and on the candidate, the same day.

Write the rule for reading a result before the runs, in the commit message or the note:
what count would make you adopt the change, and what count would make you drop it.

## Rules for reading a number

- **Four runs measure no rate.** They separate a defect that shows every time from one that
  never shows. Do not rank two texts on fewer than ten runs each.
- **Three runs per trigger query cannot rank descriptions, and pooling two such sweeps does
  not fix it.** Per-query trigger probabilities cluster between 0.4 and 0.7. For a per-query
  claim use ten runs or more; compare skills by the aggregate over a group of queries, never
  by a sweep's pass/fail count.
- **Two identical serial sweeps move ±4-6 pp at n=50**; a difference under ~12 pp there is not
  a finding.
- **False fires are near zero, not zero** (one adjacent-artifact query at ~17% for
  `design-doc` on opus, "write a PRD"). A negatives-only sweep cannot tell a clean zero from a
  broken harness: run a canary, the skill's strongest positive, and believe the zeros only
  when it fires.
- **Do not fold checks into a weighted score.** Report checks met over total, by kind.
- **Adding or rewording a check changes what the judges see.** Re-judge old runs in the same
  batch instead of quoting their earlier figure.
- **Read the reply of a run that did nothing before counting it**, and report an invalid run
  next to the totals instead of dropping it.

## Harness lessons

They cost real runs; each one produced a healthy-looking wrong number.

- **`--num-workers` is an experimental variable.** Concurrency depresses the trigger rate of
  queries that make the session read the repository first (7/10 serial against 4/10 at ten
  workers, a 21 pp gap between two skills that vanished serially). Quote serial numbers only.
- **Use `run_trigger_eval.py`, not skill-creator's `run_eval.py` directly.** The cached script
  does not pass `--setting-sources project,local` (installed plugins mask the candidate) and
  miscounts with several workers. The wrapper patches a throwaway copy, prints the per-query
  distribution and warns on a degraded sweep (positives collapsing to near zero); never pool a
  degraded sweep. Run it from the repo root.
- **The trigger harness cannot measure a request about a file that is in the project.** It runs
  here, with no fixture, so the session has nothing to edit and consults the skill; in a real
  project it may edit the file directly (`design-doc` update requests: 3/3 there, 0/16 in a
  project). Use `probe_in_project.py`, which gives each session its own project with the
  fixture and loads the plugins with `--plugin-dir` from outside it, plus a canary.
- **Skills inside the project are read without the Skill tool.** A session finds committed
  `.claude/skills/` files with `git ls-files` and follows them, so an invocation count reads 0
  for a reason unrelated to the description. Load plugins from outside the project.
- **With `--plugin-dir`, a plugin's `references/` are outside the project** and their Read is
  refused without `--add-dir`: such a probe counts invocations and does not grade documents.
- **`AGENTS.md` is in the context of every run started in the repository, in every arm.** Keep
  skill behavior and eval lore out of it. A session keeps the `AGENTS.md` it started with, and
  so do its subagents.
- **No project instructions load under `/tmp`.** A session in a git repository under `/tmp`
  loads neither `AGENTS.md` nor `CLAUDE.md`; under `$HOME` it does. Confirm with a codeword
  probe when a cell depends on it.
- **Close stdin on every nested `claude -p`** (`stdin=subprocess.DEVNULL`): the CLI appends
  piped stdin to the prompt. The helpers do this.
- **Start headless sessions with `SHELL=/bin/bash`.** The author's zsh aliases `ls` to `eza`,
  which lists nothing without a terminal, and one executor concluded the project was empty.
- **Build fixture copies before the workers start**: two threads copying the same fixture on
  first use left one run in an empty project.
- **Wrap long runs in `systemd-inhibit --what=idle:sleep --mode=block`**: a suspend expires the
  in-flight session and records it as a non-trigger.
- **A sweep is visible to other sessions in the checkout**: the candidate it injects under
  `.claude/commands/` shows in an interactive session's skill list. Do not run two at once.
- **Background subagents cannot write in the main checkout**; executors here are headless
  `claude -p` sessions, which can.

## The routine trigger check

```bash
./eval-tools/run_trigger_eval.py --routine \
    --eval-set adr-workspace/trigger-evals/trigger_eval.json \
    --skill-path adr/skills/adr \
    -o adr-workspace/run-<date>-trigger.json
```

- One model, the target (`claude-opus-5-5`) by default; pass an id, not an alias.
- Positives at 3 runs per query, a regression guard: large models sit at 98-100%, and a warning
  prints under 90%. Negatives at 3 runs per query, with the best positive of the first pass as
  the canary; a canary that never fires exits non-zero.
- Serial only, 120 s timeout, under `systemd-inhibit` when it works (`--no-inhibit` to skip).
- About 63 sessions per skill. Take the reference the same day as the candidate; a stored
  baseline from weeks and CLI versions earlier is a worse comparison.

## Grading with `judge.py`

`judge.py` builds blind packets, runs the judge calls and counts the verdicts. `run_evals.py`
writes the `runs.json` it reads; for runs laid out by hand, `judge.py manifest <dir>` builds one
from `eval-<id>-*/<cell>/run-*/`.

- **Checks come from the frozen `checks-baseline.json`.** Kinds `file` and `absence` come from
  `script-checks.json`; every other kind goes to the judge, with the anchor cases when the eval
  has a check of kind `invention`. Kind `negative` (a negative that is not an invention) is
  judged like `invention`, without anchors.
- **Three passes on every check by default**, met only when all agree; a split is listed, never
  averaged. `--passes 1` for a whole batch when cost matters more.
- **One judge per packet, never one judge per pass**: a single agent grading every packet of a
  pass turned one strict reading into a per-pass bias.
- **`judge` resumes**: a call whose output exists is skipped. `--only 2` is the smoke test.
- **Name the judge by id** (`--model`, default `claude-opus-5-5`); `judge-cost.json` records
  calls, tokens and cost. A judge is a `claude -p` call with no tools, about 2.8 k tokens.
