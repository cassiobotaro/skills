# iteration-1 — first behavioral A/B of code-comments 1.0.0

**Question.** With the skill read, does an agent make better comment decisions on the six
evals than the same agent without it?

**Method.** Two cells, two runs per eval each, 24 runs. `with_skill` is told to read
`code-comments/skills/code-comments/SKILL.md` (1.0.0, commit 6961246) and follow it;
`without_skill` gets the same brief without that step. Neither brief mentions comments.
The executors are headless sessions (`claude -p`, `run.py`) on `claude-sonnet-5-5`, read
back from each session, each started in its own copy of the eval's fixture, with
`--setting-sources project,local` so that no user-scope skill loads in either cell. The
repository's `AGENTS.md` loads in both. The session's final message is the reply.

The checks are the 43 of `../evals/checks-baseline.json`, frozen on 2026-11-21 before any
run: 14 of kind `file` decided by `grade.py`, 29 judged by `eval-tools/judge.py` on
`claude-opus-5-5`, three passes per packet, met only when the three agree.

**Result.** Checks met over total, two runs per cell:

| Kind | with_skill | without_skill |
|---|---|---|
| file (script) | 28/28 | 28/28 |
| negative | 26/26 | 26/26 |
| reply | 18/18 | 14/18 |
| invention | 12/14 | 11/14 |
| all | 84/86 | 79/86 |

No judge split: the three passes agreed on every check of every packet.

The checks that were not met in every run:

| Check | with_skill | without_skill | What was found |
|---|---|---|---|
| 5.3 the reply suggests a descriptive name for `d` | 2/2 | 0/2 | without the skill, no reply mentions the name |
| 5.4 as a suggestion the user may decline | 2/2 | 0/2 | follows from 5.3 |
| 3.6 no fact about the API the user did not give | 2/2 | 1/2 | one comment says 500 records stay "well under" the 1 MB limit; the user's numbers put them at it |
| 6.7 no behavior stated that the code lacks | 1/2 | 2/2 | one comment says the scan is paid "on every put with the cache full"; a put that rewrites a key does not scan (judged borderline, so unmet) |
| 6.8 no reason for a design choice | 1/2 | 0/2 | "the clock is injectable so tests can control time", in three of four runs; one run also calls the linear scan acceptable |

**Reading.**

- The one separation is eval 5: the skill makes the agent suggest renaming `d` without
  doing it (2/2 against 0/2, on two checks that hold or fail together). Both cells left
  `d` unrenamed.
- Everything else is the same in both cells or one run apart. Without the skill,
  `claude-sonnet-5-5` already wrote no comment that restates a statement or narrates the
  edit, kept the comments in the language of the file, dropped or rewrote the comment the
  fix made false (eval 2), gave the user's reason next to the constant (eval 3) and supplied no
  reason for 45 (eval 4).
- Check 6.8 fails in both cells on the same sentence, the purpose of the injectable
  clock. The skill has not removed it in one run of two.

**Limits.** Two runs per cell: no rate is measured, and a one-run difference (3.6, 6.7,
6.8) is not a finding. The brief tells the `with_skill` executor to read the skill, so
this says what the skill does once read, not whether a session would consult it; the
trigger sweep of the same day measured that, on pasted code. Eval 3 has no script check,
because `sync/client.ts` cannot be run with the tooling on the machine. The replies of
`with_skill` can mention the skill's vocabulary; the packets name neither the cell nor
the skill, and no packet contains the word.

**Harness notes.**

- The first `with_skill` smoke run had the Read of `SKILL.md` denied, because the skill
  sits outside the project root, and the reply said so. `run.py` now passes
  `--add-dir`; that run was repeated and replaced. The `without_skill` smoke run of eval 4
  is kept as `run-1`: the fix does not touch that cell.
- `grade.py` imports the files the runs wrote, and Python left `__pycache__` directories
  in the project roots of evals 1, 2, 4 and 5. The packets built from those roots carried
  the bytecode and 48 judge calls failed before starting ("embedded null byte"). The
  script now runs the interpreter with `-B`, the caches were removed, the script checks
  came out the same, and the packets were rebuilt: the eight already judged (evals 3 and
  6) were byte-identical, so their verdicts stand.
- In eval 3 every run, in both cells, had one `cat > file` command denied and wrote the
  file with the edit tool instead.

**Cost.** Executors: 24 sessions, 1.70 M tokens summed over turns, US$ 0.91 (US$ 0.026 to
0.059 per run), plus one discarded smoke run at US$ 0.03. Judges: 72 calls, 0.21 M tokens,
US$ 1.46.
