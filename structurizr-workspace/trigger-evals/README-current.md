# Measuring the *shipped* structurizr description (2026-08-07)

`result.json` records the optimization run that produced `best_description`. That is **not** the
description the skill ships: commit `f92487e` hand-edited it afterwards, adding the exclusion
block — *"Do NOT use it for cloud-infrastructure pictures drawn from real vendor service icons
(e.g. an AWS diagram with EC2/RDS/S3 boxes), for sequence or behavior-over-time diagrams …, or
for writing the ADR decision content itself."* That addition had never been measured.
`result-current.json` is that measurement, on the same 20-query set.

## Result — 18/20

**Every one of the ten should-not-trigger queries passes at 0.00**, and that is the headline,
because three of them are precisely what the hand-edited exclusions target:

- "generate an AWS architecture diagram with the actual service icons (boxes for EC2, RDS, S3)"
- "draw a sequence diagram showing how the checkout request flows through the gateway, order
  service and payment service over time"
- "we decided to adopt the C4 model as our documentation standard — record that decision"

Also silent on the harder near-misses: "write a design doc … including an architecture overview",
"explain what the C4 model is and how it differs from UML", "convert our existing PlantUML
diagrams to Mermaid", "review our microservices for tight coupling". **The exclusion block does
the job it was hand-written to do.**

Two should-trigger queries miss:

| Trigger rate | Query |
|---|---|
| 0.00 | "add a component diagram for the new payments service to our existing C4 model in workspace.dsl" |
| 0.00 | "link our decision records from doc/adr into the architecture documentation so the C4 views show the related ADRs" |

> **Corrected 2026-08-20 — neither query is a zero.** These 0.00s come from 3 runs each at
> `--num-workers 10`, the configuration `README-21pp-analysis.md` later showed punishes exactly
> this kind of query (both name a file the session must find first). Measured serially
> (`README-serial-baseline.md`): the component-diagram query scores 1/5 on Haiku and 5/5 on Opus,
> the ADR-linking query 5/5 on Haiku and 4/5 on Opus. The paragraph below still reaches the right
> conclusion — more synonyms are not the fix — but for the wrong reason: the boundary was not
> being drawn conservatively, the harness was reporting a miss whenever the session opened the
> named file before invoking the skill.

Both are covered by the description's own text ("component diagrams", "create or edit a .dsl
workspace"; "Also use it when linking existing ADRs … into the architecture documentation or C4
views"), so more synonyms are unlikely to be the fix. The second is the more interesting one: the
same query is a should-**not**-trigger case in the `adr` set, where it correctly stays silent —
so the boundary between the two skills is being drawn, just conservatively on both sides.

## What this does and does not establish

- It **does** establish that the exclusions added in `f92487e` hold, with no over-triggering.
- It **does not** establish whether the hand-edit changed the should-trigger side. The recorded
  run's 8/8 test score came from a 40% holdout of a *different* description, so it is not
  comparable to 18/20 on the full set. The A/B that would settle it — shipped description vs.
  `result.json`'s `best_description`, same set, same day — **was not run**: the account hit its
  monthly spend limit first.
- Three runs per query is thin for queries near the boundary.

## Rerunning

From the **repo root** (not from the skill-creator directory — see `CLAUDE.md`):

```bash
export PYTHONPATH=/home/cassiobotaro/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator
python -m scripts.run_eval \
  --eval-set structurizr-workspace/trigger-evals/trigger_eval.json \
  --skill-path structurizr/skills/structurizr \
  --model claude-opus-5 --timeout 120 --verbose
```
