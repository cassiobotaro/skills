# iteration-9 — scope section A/B (adr 1.4.0 vs 1.3.2), graded against a frozen check list

**Change under test.** A "Check the scope first" section was added to `SKILL.md`, before
the contract, mirroring `structurizr` and `mermaid-sequence`: an open design goes to
`design-doc`, a choice not yet made is not recorded, and `!adrs` wiring is left to
`structurizr`. The hand-off drops the stale Structurizr URL and the one-row reference
table becomes a sentence. Body 13 266 → 14 240 bytes. The last shipped version, 1.3.2, is
snapshotted in `../skill-snapshot-1.3.2/`.

**Method.** Evals 8, 9 and 10, two runs per arm, twelve executors in three batches of
four. `with_skill` = working tree (1.4.0); `old_skill` = the snapshot. Executor
`claude-sonnet-5-5`, judge `claude-opus-5-5` (each executor reported its own id).

This iteration also pilots a stricter grading, adapted from the `spec-driven-eval` skill
of Tech Leads Club:

1. **Frozen check list.** `../evals/checks-baseline.json` was written before any run and
   splits the 12 assertions into 25 atomic yes/no checks (7 + 6 + 12).
2. **Script first.** `check_files.py` decides the 10 `file` / `absence` checks from the
   bytes on disk (tree diff against the fixture, sha256, H1/slug, date, headings,
   blank-line discipline).
3. **Blind judge for the rest.** `build_judge_inputs.py` writes one packet per run under
   `judge-inputs/` with the prompt, the reply, the line-numbered files and the 15
   `reply` / `invention` checks. A packet does not say which arm produced it
   (`judge-map.json` holds the mapping).
4. **Evidence or search.** A met check quotes the words that satisfy it; an unmet check
   records what was searched; borderline resolves to unmet.
5. **Three passes, unanimity required.** Each packet was judged three times
   (`judge-outputs/`, 36 calls). `aggregate_checks.py` counts a judge check as met only
   when all three passes say so; a split is flagged borderline (`judge-splits.json`).

**Results** (checks met / total, both runs of each arm).

| Eval | 1.4.0 (with_skill) | 1.3.2 (old_skill) | What happened |
|---|---|---|---|
| 8 open design | 14/14 | 12/14 | All four runs refuse to write an ADR and create no file. Both 1.4.0 runs name a design doc and say its decisions become ADRs. One 1.3.2 run does the same in a closing sentence; the other never mentions a design doc and offers a `Proposed` ADR listing the open questions (8.5, 8.6 unmet, 0/3 on both) |
| 9 undecided choice | 12/12 | 12/12 | All four runs say there is nothing to record, create no file and offer a later or `Proposed` ADR. Not discriminating: rule 1 of the old skill already covers it |
| 10 write ADR, route linking | 22/24 | 23/24 | All four runs write a well-formed `0004`, leave 0001–0003 byte-identical, create no `workspace.dsl` and say the linking is outside this skill. 1.4.0 names the `structurizr` skill; 1.3.2 says "the Structurizr tooling" and one run cites the stale docs URL. Check 10.9 (nothing invented) fails in three of four runs — see below |
| **Total** | **48/50** | **47/50** | |

**The finding that is not about scope.** In eval 10 the Context section opens with facts
the user never gave: "to slow down repeated guessing" and "the API gateway is the usual /
obvious place for rate limiting". Both 1.4.0 runs do it (0/3 on 10.9, unanimous); one
1.3.2 run does the second only (2/3, borderline) and one is clean (3/3). This is a rule 1
breach in the written ADR, present in both arms, so the scope section did not cause it.
Two runs per arm cannot say whether 1.4.0 does it more often.

**What the stricter grading changed.**

- 59 of 60 judge verdicts were unanimous across the three passes. The single split is
  10.9 on one 1.3.2 run. One pass would have produced the same table, except for that
  cell, which would have been a coin flip between met and unmet.
- The evidence rule had a hole: a met *negative* check ("nothing invented") has no
  sentence to quote, so the first aggregation marked 12 such verdicts "not scored" and
  counted them unmet. `aggregate_checks.py` now accepts the recorded search as evidence
  for `kind=invention`. The frozen baseline was not edited; its note should say this
  before the next iteration.
- Cost: executors 12 × ~48 k = 0.57 M tokens; judges 36 × ~43 k = 1.53 M tokens, almost
  all of it fixed subagent overhead, not the packet (a packet is 3–6 KB).

**Reading.** Four runs per eval cannot measure a rate (AGENTS.md). What they show: the
scope section makes the design-doc hand-off and the `structurizr` hand-off explicit in
every 1.4.0 run, where 1.3.2 got there in one run of two (eval 8) or in vaguer words
(eval 10). Eval 9 does not separate the arms and can be dropped from future A/Bs of this
section. The invention in Context is the defect worth a follow-up.

**Files.** `benchmark.md` / `benchmark.json` come from skill-creator's aggregator, which
counts checks as expectations; its header says "3 runs each", a template default — there
are two. `review.html` is the static viewer.
