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

## The A/B — settled: the hand-edit changed nothing

The decisive experiment has now run. Same 20-query set, same day, same conditions, 3 runs per
query: arm **A** the shipped description, arm **B** `result.json`'s recorded `best_description`,
passed via `--description`. Files: `ab-shipped.json` / `ab-recorded.json`.

**A = 17/20. B = 17/20.** The commit `f92487e` hand-edit neither helped nor hurt.

More useful than the tie: **both arms miss the same three queries, at 0.00 in both.**

| A | B | Query |
|---|---|---|
| 0.00 | 0.00 | "ADR 0007 is out of date … mark it superseded and write the new one" |
| 0.00 | 0.00 | "start a decision log for the platform-team repo, we don't have one yet…" |
| 0.00 | 0.00 | "we changed our minds about the message broker. amend the existing record…" |

Both descriptions already contain "start a decision log", "amend", and the whole supersede
clause. Two different wordings, three independent runs (`result-current`, A, B), the same three
hard zeros. **Adding synonyms is not the lever** — that hypothesis is now tested and dead, which
is the point of having run this.

What these three share is that they read as *maintenance on a log* rather than authoring a
record — mark a status, start a directory, edit an existing file. That fits the documented
triggering behaviour (Claude skips a skill for tasks it judges it can already handle directly)
better than it fits any wording gap. Testing that would mean changing what the description
*claims the work is*, not which words it lists — and it should be tested before it is believed.

Run-to-run variance is about one query: the earlier `result-current.json` scored 16/20, with
"the tech lead wants every significant tech choice written up in doc/adr…" at 0.33; in arm A it
passed at 0.67. Treat 16 vs 17 as noise. The three zeros are not noise.

## Other notes

- The shipped description over-triggers on nothing: all ten should-not-trigger queries sit at
  0.00 in both arms, including the near-misses (design doc, sequence diagram, `workspace.dsl`,
  PRD, postmortem, "ADR vs RFC", "help me decide Kafka or RabbitMQ").
- `result.json`'s headline (train 12/12, test 7/8) came from a 60/40 split, so it was never
  comparable to a full-set score. It is superseded by the A/B above.

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
