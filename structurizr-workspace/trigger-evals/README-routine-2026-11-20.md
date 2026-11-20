# Routine check on Haiku 5.5 after the AGENTS.md split (2026-11-20)

The first trigger numbers taken with the trimmed `AGENTS.md` in context. Until this date
the file named in every session what each of the four skills does; see
`eval-tools/README.md` and `adr-workspace/iteration-16/README.md`. No description changed.

**Method.** `./eval-tools/run_trigger_eval.py --routine` from the repo root, once per
skill, one after another: `claude-haiku-5-5` (the id passed to `--model`, not read back
from the transcripts), positives at 5 runs per query, negatives at 1, the best positive of
the first pass spliced in three times as canary, serial, 120 s timeout, under
`systemd-inhibit`. Claude Code 2.1.329. An interactive session was open in the checkout
and idle while the sweeps ran. Files: `<skill>-workspace/trigger-evals/serial-2026-11-20-routine-haiku.json`.

| Skill | before (old AGENTS.md) | 2026-11-20 (trimmed) | per-query, sorted | negatives | canary | Fisher p |
|---|---|---|---|---|---|---|
| adr | 28/50 (56%), 2026-11-15 | 21/50 (42%) | `[0, 0, 0, 0, 1, 1, 4, 5, 5, 5]` | 0/10 | 3/3 | 0.23 |
| design-doc | 37/50 (74%), 2026-10-31 | 31/50 (62%) | `[0, 0, 1, 2, 3, 5, 5, 5, 5, 5]` | 0/10 | 3/3 | 0.28 |
| structurizr | 31/50 (62%), 2026-10-31 | 36/50 (72%) | `[0, 1, 2, 3, 5, 5, 5, 5, 5, 5]` | 0/10 | 3/3 | 0.40 |
| mermaid-sequence | 46/50 (92%), 2026-10-31 | 38/50 (76%) | `[0, 0, 4, 4, 5, 5, 5, 5, 5, 5]` | 0/10 | 3/3 | 0.054 |
| pooled | 142/200 (71%) | 126/200 (63%) | 12 queries down, 6 up, 22 equal | 0/40 | 12/12 | 0.11 |

The "before" column is recomputed from the result files, on the same ten queries per
skill. For `structurizr` the file holds 31/50; the 69% quoted elsewhere is 31/45, with the
ADR-linking query (0/5 then, 3/5 now) left out of the count.

- **No skill separates from its earlier number.** Three go down by 12 to 16 points and
  one goes up by 10. Two identical serial sweeps have moved 4 to 6 points at this size and
  a 12-point gap between skills did not separate; the closest here is `mermaid-sequence`
  at p = 0.054, uncorrected, one of four comparisons.
- **Where the moves are.** In `adr` and `mermaid-sequence` the queries that name the
  artifact stay at 5/5 and the whole drop sits in the ones that describe the need without
  naming it: the six indirect `adr` queries go from 8/30 to 2/30, and two
  `mermaid-sequence` queries ("diagram the retry/backoff interaction…", "show the message
  flow for our async order processing…") go from 4/5 to 0/5 each. `structurizr` does not
  follow that pattern: the Portuguese query goes 2/5 to 5/5 and the ADR-linking one 0/5 to
  3/5, while "diagram the static architecture of our microservices…" goes 4/5 to 0/5.
- **Harness healthy.** Every canary 3/3, four to six queries at 5/5 in each skill, no
  false fire in 40 negative samples.

**Reading.** These are the reference numbers for Haiku 5.5 from here on, because they are
the only ones measured with the `AGENTS.md` a session now loads. They do not show that
trimming the file changed the trigger rate: the pooled drop of 8 points has p = 0.11, the
runs of one query are not independent, and the two sides differ by 5 to 20 days and by
CLI version as well as by the file. The one pattern worth a test is the indirect queries
of `adr` and `mermaid-sequence`; five runs per query do not rank queries, so that test is
those queries at ten runs or more, with the old and the trimmed file side by side as in
iteration-16.

**Limits.** One sweep per skill. Negatives at one run are a smoke test. Cost not
recorded: `run_eval.py` does not report it (252 sessions).
