# The adr trigger description: what was measured, and what it cost to learn (2026-08-07)

Four full sweeps of the same 20-query set, three descriptions. The headline: **the trigger text
shipped in 1.3.0 was rewritten to reframe what the work *is*, and that — not adding synonyms —
is what moved the needle.** Getting there took one wrong turn worth recording.

## The descriptions

| Arm | Description | Files |
|---|---|---|
| **shipped-1.2.x** | the pre-1.3.0 frontmatter: format facts in a parenthetical, then a list of trigger phrases | `result-current.json`, `ab-shipped.json` |
| **recorded** | `result.json`'s `best_description` from the original optimization run — commit `f92487e` had hand-edited on top of it, so it was never what shipped | `ab-recorded.json` |
| **H1 maintenance** | reframes the work as maintaining a *file collection with cross-file invariants* (monotonic numbering, slug derivation, supersede touching two files and the Status section only, the English literals the importers parse), and says outright: use this **including the operations that look like a one-line edit** | `ab-h1-maintenance.json`, `ab-h1-maintenance-run2.json` — **now shipped as 1.3.0** |

All three name the same trigger phrases. "start a decision log", "amend", and the supersede
clause appear in every one. The only thing H1 changes is what it claims the job is.

## Result — aggregate trigger rate, pooled across sweeps

| Arm | the 3 hard queries | all 10 should-trigger | all 10 should-NOT-trigger |
|---|---|---|---|
| shipped-1.2.x | **0 / 18** (0%) | 33 / 60 (55%) | **0 / 60** |
| recorded | **0 / 9** (0%) | 19 / 30 (63%) | **0 / 30** |
| **H1 (shipped 1.3.0)** | **5 / 18 (28%)** | **39 / 60 (65%)** | **0 / 60** |

The three hard queries are the ones that had never fired under any earlier description:

- "ADR 0007 is out of date — … mark it superseded and write the new one"
- "start a decision log for the platform-team repo, we don't have one yet…"
- "we changed our minds about the message broker. amend the existing record…"

**0 triggers in 27 samples** across the two old descriptions; **5 in 18** under H1. H1 is the
only text that has ever fired on them. It is also better overall (65% vs 55%) and over-triggers
on nothing — zero hits across 60 negative samples, including the near-miss "link all our
existing ADRs from doc/adr into the Structurizr architecture docs" that H1's own mention of the
`!adrs` importer put at risk.

**28% is an improvement, not a fix.** Those three queries still fall below the trigger threshold
more often than not. If they matter, the next lever is the same one that worked here — what the
description says the work *is* — pushed further, not more phrasings.

## The wrong turn, and the methodology lesson

The two H1 sweeps scored **19/20 and then 15/20** — same description, same set, same day. That
4-query swing is what the sweep-level pass/fail metric does at 3 runs per query: a query whose
true trigger probability sits near the threshold flips sides between identical runs.

On the strength of the 19/20 alone, this file briefly recorded the hypothesis as "confirmed".
It wasn't — one sweep cannot establish a 2-query difference on a harness with a 4-query swing.
By the same token, the earlier "shipped 17/20 = recorded 17/20, therefore the hand-edit changed
nothing" was also over-read: a tie in a noisy metric is not evidence of equivalence.

**Score by pooled trigger rate over a group of queries, never by one sweep's headline.** 0/27
versus 5/18 survives the noise; "19 beat 17" does not. This is now recorded in `CLAUDE.md`.

## Rerunning

From the **repo root**, never from the skill-creator directory (the wrong cwd silently scores
every query 0/3 — see `CLAUDE.md`):

```bash
export PYTHONPATH=/home/cassiobotaro/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator
python -m scripts.run_eval \
  --eval-set adr-workspace/trigger-evals/trigger_eval.json \
  --skill-path adr/skills/adr \
  --model claude-opus-5 --timeout 120 --verbose
```

Add `--description "$(cat some-variant.txt)"` to test a candidate without editing `SKILL.md`.
Run any comparison **at least twice per arm** and pool the results before believing it.
