# Measuring the *shipped* adr description (2026-08-07)

`result.json` records the optimization run that produced `best_description`. That is **not** the
description the skill ships: commit `f92487e` ("adr 1.2.1 + structurizr 1.1.1: sharpen trigger
descriptions") hand-edited it afterwards, adding the phrasing
*"ADR N is out of date, mark it superseded and write the replacement"*. The shipped description
had never been measured. `result-current.json` is that measurement, on the same 20-query set.

## Result — 16/20

All ten should-not-trigger queries pass at 0.00, including the near-misses the set was built
around (design doc, sequence diagram, `workspace.dsl`, PRD, postmortem, "ADR vs RFC", "help me
decide Kafka or RabbitMQ"). **The description does not over-trigger.**

Four should-trigger queries miss:

| Trigger rate | Query |
|---|---|
| 0.00 | "ADR 0007 is out of date — we moved off Redis for sessions and now use the JWT approach. mark it superseded and write the new one" |
| 0.00 | "start a decision log for the platform-team repo, we don't have one yet…" |
| 0.00 | "we changed our minds about the message broker. amend the existing record to note we're now sticking with SQS…" |
| 0.33 | "the tech lead wants every significant tech choice written up in doc/adr from now on. let's record the first one: choosing pnpm over npm…" |

The uncomfortable part: **every one of those phrases is already in the description, nearly
verbatim** — "start a decision log", "amend", and the whole superseded clause `f92487e` was
written to catch. Adding more synonyms is therefore unlikely to be the fix, and could easily be
the wrong conclusion drawn from a small sample.

## What this does and does not establish

- It **does** establish that the shipped description over-triggers on nothing.
- It **does not** establish a regression against `f92487e`. `result.json`'s headline (train 12/12,
  test 7/8) came from a 60/40 split of a *different* description, so the numbers are not
  comparable. The decisive experiment — running the recorded `best_description` against this same
  full 20-query set, same conditions, same day — **was not run**: the account hit its monthly
  spend limit first. Until it is, whether the hand-edit helped, hurt, or did nothing is unknown.
- Three runs per query is a thin sample for queries sitting near the trigger boundary.

## Rerunning

From the **repo root** (not from the skill-creator directory — see `CLAUDE.md`; the wrong cwd
silently scores every query 0/3):

```bash
export PYTHONPATH=/home/cassiobotaro/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator
python -m scripts.run_eval \
  --eval-set adr-workspace/trigger-evals/trigger_eval.json \
  --skill-path adr/skills/adr \
  --model claude-opus-5 --timeout 120 --verbose
```

To settle the open question, run the same command twice with `--description` set to the shipped
text and then to `result.json`'s `best_description`, and compare on the full set.
