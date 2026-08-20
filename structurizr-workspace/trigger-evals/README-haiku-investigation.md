# Why structurizr looked broken on Haiku, and what was actually wrong (2026-08-20)

> **Superseded twice on the same day — also read `README-serial-baseline.md`.** Every rate in
> this file, including the n=10 and n=30 "large-sample" ones, was measured at `--num-workers 10`.
> Serially, the two queries this file resolves to 33% and 40% score 4/5 and 0/5, and the residual
> "21pp deficit" it hands to `README-21pp-analysis.md` is down to ~12pp and not statistically
> separable (p = 0.21 at n=50 per skill, p = 0.29 pooling two serial sweeps). The Portuguese
> query it flags as worth a second look is now measured at 10/35 (29%) against 29/35 (83%) for a
> literal English translation — see the serial baseline for what that does and does not mean.
>
> **Superseded in part by `README-21pp-analysis.md` (same day).** The sampling finding below
> holds. The conclusion that a real 21pp deficit remained does not: that gap was concurrency.
> At `--num-workers 1` the two skills measure 78% and 80%. Read the sections below on the
> *sampling* artifact; ignore the closing verdict that `structurizr` is "genuinely weaker".

The model A/B sweep reported `structurizr` at 47% on Haiku against 87-93% for the other three
skills, failing hardest on the *most explicit* requests — `create a workspace.dsl` at 0/6 while
the vaguer "document how our platform is structured using C4" fired 6/6. That paradox drove two
description rewrites, both of which failed (see `README-model-ab.md`).

**The paradox was a sampling artifact.** The queries that scored 0/6 do not have a trigger
probability near zero; they sit near 0.35, where a 6-sample draw hits zero about 7% of the time.
Two of them did, in the same set, and the pattern read as a signal.

## What was tested and ruled out

| Hypothesis | Test | Verdict |
|---|---|---|
| `run_eval.py` decides on the **first tool** — a session that explores the repo before invoking the skill scores as a non-trigger | Captured the full tool sequence instead of returning early, 3 runs on the 0/6 query | ~~**Dead.**~~ **Wrong verdict — this is real.** It was tested on `create a workspace.dsl`, a query with nothing to look up, so no exploration happens and the effect cannot appear. On the query naming an *existing* `workspace.dsl` the pattern is plain: read the file, `find`, then invoke. 7/10 strict vs 9/10 counting the skill anywhere. The hypothesis is conditional on the query referencing repo state. |
| Concurrency confuses the model — `--num-workers 10` means ten identical candidate skills coexist in `.claude/commands/` | 4 queries × 3 runs at `--num-workers 1` vs `10` | ~~**Dead.** 8/12 vs 9/12.~~ **Wrong verdict — this is the main cause.** 12 samples could not resolve it. At full set size: 60% at ten workers vs 78% serial. The mechanism is not identical candidates confusing the model; it is contention penalising sessions that touch the repo. See `README-21pp-analysis.md`. |
| Haiku writes the DSL directly, or picks a sibling skill, instead of triggering | Same full-sequence capture | **Not observed.** No `Write` without a preceding `Skill`, no sibling skill chosen. |

## What it actually is: per-query probabilities that 3 runs cannot resolve

Large-sample estimates for the two queries that started this, Haiku, 30 runs each:

| query | recorded (n=6) | measured (n=30) |
|---|---|---|
| `create a workspace.dsl for our order-management system` | 0/6 (0%) | **10/30 (33%)** |
| `modela em Structurizr DSL a arquitetura do nosso sistema de cobrança` | 0/6 (0%) | **12/30 (40%)** |

The full positive set at 10 runs per query, Haiku, against the shipped 1.3.0 description:

| n=10 | n=6 (recorded) | query |
|---|---|---|
| 1/10 | 0/6 | add a component diagram … to our existing C4 model in workspace.dsl |
| 4/10 | 1/6 | create a workspace.dsl for our order-management system |
| 4/10 | 0/6 | modela em Structurizr DSL a arquitetura do nosso sistema de cobrança |
| 5/10 | 1/6 | we use Structurizr — model the deployment … staging and prod AWS |
| 5/10 | 4/6 | i have an architecture i want to capture as proper C4 … |
| 5/10 | 5/6 | link our decision records from doc/adr into the architecture documentation |
| 7/10 | 4/6 | document our system landscape … 8 internal systems |
| 9/10 | 6/6 | diagram the static architecture of our microservices … |
| 10/10 | 6/6 | i want to document how our platform is structured using C4 … |
| 10/10 | 6/6 | set up the C4 model for our new SaaS — i want it as DSL … |

**No query sits at zero.** Six of the ten sit between 0.4 and 0.7, which is exactly where a
3-run sample carries almost no information and the pass/fail threshold at 0.5 is a coin flip.

*(All ten rates in this table are ten-worker rates. Serially the same set scores 74% overall,
with the shape changed rather than shifted: the `component diagram … workspace.dsl` query stays
low at 1/5, `create a workspace.dsl` rises to 4/5, and the Portuguese query drops to 0/5 — its
true serial rate being 29% over 35 samples. The conclusion that no query is at zero holds; the
per-query ordering here does not.)*

## ~~The gap is real, but a third the size~~ — superseded, the gap is ~2pp

**This section's conclusion is wrong; the numbers in it are correct but were all measured at
ten workers.** Re-measured serially the two skills sit at 78% and 80%. Kept for the record.

`adr` was the control — it scored 93% on Haiku in the same original sweep. Re-measured the same
way:

| skill on Haiku | n=3/query | n=10/query |
|---|---|---|
| adr | 93% | **81%** |
| structurizr | 47-55% | **60%** |

Both moved, in opposite directions, and the gap fell from 46pp to 21pp. So: `structurizr` **is**
genuinely weaker on Haiku than `adr` — 21pp over 100 samples per skill is not noise *(it is not
noise, but it is bias: both arms ran at ten workers)* — but it is
not the near-broken outlier the sweep portrayed, and there is no cliff on explicit
`workspace.dsl` phrasing to go hunting for. The two description rewrites were chasing a shape in
the noise.

## Consequences for how this repo measures triggers

- **Three runs per query cannot rank descriptions.** `CLAUDE.md` already says to score by
  aggregate rate rather than pass/fail; that is necessary but not sufficient. A per-query rate
  from 3 runs is close to meaningless, and pooling two such sweeps (n=6) is what produced the
  false 0/6 signal here. For a per-query claim, use n≥10; for a skill-level comparison, the
  10-query aggregate at n=3 (n=30) is usable but moved 12pp on `adr` when resampled.
- **"Reproducible across two sweeps" is not the safeguard it sounds like.** Two independent
  draws of 3 agreeing at zero is an ordinary outcome at p≈0.35, not confirmation.
- **The degraded-sweep warning in `eval-tools/run_trigger_eval.py` gives false positives.** It
  fires when no positive query reaches a full run — which is the *expected* state for a short
  eval set at high `--runs-per-query`. It fired on both healthy 30-run samples above. The
  heuristic needs to account for set size and run count, or be limited to the 3-run sweep shape
  it was written for.

## What was not explained *(answered in `README-21pp-analysis.md`: it was concurrency)*

~~Why `structurizr` is genuinely 21pp weaker than `adr` on Haiku.~~ This investigation only
established that the deficit is smaller and smoother than reported, and that the explicit-phrasing
paradox does not exist. The lowest query at n=10 (1/10, "add a component diagram … to our
existing C4 model in workspace.dsl") is the one worth looking at next, and it is the only one
where the recorded 0/6 was roughly accurate.

No description change came out of this work. The two that were tried failed, and the third —
shipped as 1.3.0 — rests on the description contradicting itself, not on these numbers.
