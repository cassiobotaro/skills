# structurizr trigger text across models, and what 1.3.0 changed (2026-08-19/20)

Started as a Haiku-vs-Opus comparison of all four skills. Three of them were healthy on both
models; `structurizr` was not, and that turned into a description change. Both halves are
recorded here because the harness lesson cost more than the result did.

## Part 1 — the four skills across models (shipped descriptions)

Aggregate trigger rate, 20 queries per skill (10 positive / 10 negative), 3 runs per query.

| skill | Haiku | Opus | false fires |
|---|---|---|---|
| adr | 28/30 (93%) | 20/30 (67%) | 0/60 |
| design-doc | 28/30 (93%) | 25/30 (83%) | 0/60 |
| mermaid-sequence | 26/30 (87%) | 30/30 (100%) | 0/60 |
| **structurizr** | **28/60 (47%)** | 24/30 (80%) | 0/60 |

Zero false fires anywhere, both models — the descriptions do not leak into neighboring work.
`adr` is *better* on Haiku than on Opus. Only `structurizr` fails, and it fails hardest on the
most explicit requests: `create a workspace.dsl` 0/6 and `modela em Structurizr DSL` 0/6 on
Haiku, while the vaguer "document how our platform is structured using C4" fires 6/6.

## Part 2 — the arms, pooled over healthy sweeps

| arm | Haiku | Opus | false fires (Opus) |
|---|---|---|---|
| 1.2.3, full `Do NOT` block | 28/60 (47%) | 46/60 (77%) | 0/60 |
| reframed opening, block kept | 32/60 (53%) | 22/30 (73%) | 0/30 |
| block removed entirely | 74/120 (62%) | 39/60 (65%) | **5/60** |
| **1.3.0 — ADR clause dropped, AWS + sequence kept** | **33/60 (55%)** | **42/60 (70%)** | **0/60** |

Two things the numbers settled:

- **Reframing the opening did nothing.** The `adr` H1 lever (say what the work *is*, don't add
  synonyms) moved this skill by +4 samples in 60 — noise. Recorded so nobody pays for it twice.
- **The AWS-icons clause is load-bearing.** Remove the whole block and the negative "generate an
  AWS architecture diagram with the actual service icons" fires 3/3 then 2/3 on Opus,
  deterministically. It is the only negative that ever fired in this whole exercise.

## What 1.3.0 actually fixes

The 1.2.3 description contradicted itself: it says to trigger when *linking existing ADRs from
`doc/adr` into the C4 views*, then two clauses later forbids "writing the ADR decision content
itself" — and Haiku obeyed the prohibition, killing the linking positive. That query scores
**2/6 at 1.2.3, 5/6 at 1.3.0**. This is a logical defect, not a statistical one, which is why it
was worth shipping while the recall deltas below are not.

The recall differences between 1.2.3 and 1.3.0 (+8pp Haiku, -7pp Opus) sit inside this harness's
drift band and should **not** be claimed as improvements. The three exclusions still exist — they
moved into the SKILL.md body as a "Check the scope first" table, where they guide behavior after
triggering instead of competing for the trigger decision.

## Harness — read this before running anything here

The cached skill-creator `run_eval.py` needs two patches to produce a valid number in this repo,
and produced two entirely discarded sweeps before they were found:

1. **`--setting-sources project,local`** on the `claude -p` argv. Without it the user-scope
   installed plugins mask the injected candidate: adr/opus scores **0/30**.
2. **Prefix-match `<skill>-skill-`**, not the worker's exact uuid. Every worker writes its own
   candidate into the same `.claude/commands/`, so with `--num-workers 10` the session sees ten
   identical candidates and picks one — exact-uuid matching divides recall by ~`num_workers`.
   Same set, same model: **2/30** with uuid match, **18-20/30** with prefix match.

**Sweeps degrade intermittently.** A baseline Opus sweep scored 22/30, and the very next sweep of
the same text scored 2/30 with distribution `[0,0,0,0,0,0,0,0,1,1]` against the healthy
`[0,0,2,2,3,3,3,3,3,3]`. Print the per-query distribution, discard any sweep whose positives never
reach 3/3, and never pool a degraded sweep into a result. Canary: adr/opus has scored 14-20/30 across healthy sweeps — a wide band, which is itself the point.
