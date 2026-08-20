# The 21pp structurizr/adr gap on Haiku was concurrency, not the description (2026-08-20)

`README-haiku-investigation.md` closed with `structurizr` at 60% and `adr` at 81% on Haiku at
10 runs per query, called the 21pp gap real ("not noise") and left it unexplained. It is not
real. Re-measured with `--num-workers 1` and nothing else changed:

| Haiku, positives only | `--num-workers 10` | `--num-workers 1` |
|---|---|---|
| adr | 81% (n=10/query) | 80% (n=5/query) |
| **structurizr** | **60%** (n=10/query) | **78%** (n=5/query) |
| gap | **21pp** | **2pp** |

`adr` did not move. `structurizr` gained 18pp. The gap was an artifact of running the sweep
ten sessions at a time.

The two arms ran back to back on the same machine, so a drift-over-time explanation is ruled
out: it would have moved both skills.

## Why concurrency hits this skill and not the other

Under `--num-workers 1` the per-query changes are not uniform — they concentrate exactly where
the query makes the session touch the repository before it can act:

| concurrent | serial | query |
|---|---|---|
| 10% | 80% | add a component diagram … to our **existing C4 model in workspace.dsl** |
| 50% | 100% | **link our decision records from doc/adr** into the architecture documentation |
| 50% | 100% | i have an architecture i want to capture as proper C4 … |
| 40% | 80% | **create a workspace.dsl** for our order-management system |
| 100% | 100% | i want to document how our platform is structured using C4 … *(no repo reference)* |

`adr`'s query set asks for prose about a decision far more often than it points at a file that
must be located first. `structurizr`'s set is full of `workspace.dsl`, "our existing C4 model",
`doc/adr` — so its sessions do repo I/O before invoking anything, and that is the step
concurrency punishes.

## The three effects stacked on this one number

Everything measured over these two days on `structurizr`/Haiku was some mixture of:

1. **Sampling noise.** Per-query rates cluster mid-range; 3 runs carries almost no information.
   Documented in `README-haiku-investigation.md`.
2. **Concurrency depression.** 30pp on a single query (7/10 serial vs 4/10 at ten workers, same
   code, same description, same query), concentrated on repo-touching queries. This one.
3. **First-tool-wins detection.** `run_eval.py` returns non-trigger at the first tool that is
   not `Skill`/`Read`, and a `Read` only counts when the path contains the candidate name — so
   a session that opens `workspace.dsl`, runs `find`, then invokes the skill is recorded as a
   non-trigger. Captured directly: on the `existing C4 model in workspace.dsl` query, 7/10
   strict versus 9/10 counting the skill wherever it appears.

All three penalise the same thing — queries that require looking at the repository — and
`structurizr`'s set is the one made of those.

## The description is not a lever here, and that is measured

A ceiling probe ran each set against a deliberately over-broad description of matched form
("Use this skill for ANY request that involves … Always use this skill for such requests,
without exception"), 10 runs per query, Haiku:

| | shipped description | over-broad description |
|---|---|---|
| adr | 81% | **97%** |
| structurizr | 60% | **52%** |

`adr` responds to description text as expected. `structurizr` does not respond at all — the
maximally permissive text scored *below* the shipped one, with the same per-query shape.
Under concurrency the description is not what is deciding the outcome.

**Consequence.** Every description rewrite attempted for `structurizr` Haiku recall was chasing
a variable that was not moving the number: the reframed opening (dismissed at +4/60), the
removal of the `Do NOT` block, and the 1.3.0 trim. 1.3.0 still stands — it fixes a description
that contradicted itself, which is an argument from logic, not from these rates.

## What this changes about running evals here

- **`--num-workers` is not a speed knob, it is an experimental variable.** Two sweeps at
  different worker counts are not comparable. Prefer `--num-workers 1` for any number that will
  be quoted; use concurrency only for a rough smoke test, and never mix the two in one table.
- Every trigger number recorded in this repo before today was measured at ten workers, and the
  ones from repo-touching query sets are depressed by an unknown amount. ~~The `adr` numbers are
  roughly safe; the `structurizr` ones are not.~~ **Wrong — that generalisation came from Haiku
  alone.** The full serial baseline (`README-serial-baseline.md`, same day) found the single
  largest correction in the repo on `adr`/**Opus**: 67% → 98%, +31pp, bigger than `structurizr`'s
  own Haiku correction. No ten-worker number here is safe, on any skill.
- The "degraded sweep" phenomenon documented earlier — a sweep collapsing to near-zero with an
  empty stderr — is probably this same contention effect at its extreme, not only a usage limit.

## Still open *(both items answered — see `README-serial-baseline.md`)*

Whether `structurizr` and `adr` are genuinely equal on Haiku, or merely close. The serial
comparison is 78% vs 80% at n=5 per query, which settles that there is no large gap but not
that there is none. The one query that went the other way — `modela em Structurizr DSL …`,
40% concurrent to 0/5 serial — is worth a larger sample before anyone reads a Portuguese-language
weakness into it.

**Answered 2026-08-20, same day.**

- *Equal or merely close:* still not resolvable, and now with a measured reason. A second serial
  sweep put `adr` at 86% and `structurizr` at 74%; pooling both sweeps gives 83/100 vs 76/100,
  p = 0.29. Identical serial configurations move ±4-6pp between runs at n=50, so a 12pp gap sits
  inside the noise band. `structurizr` is the weakest of the four on Haiku, by an amount this
  harness cannot pin down without a much larger n.
- *The Portuguese query:* it never went the other way. Its true rate is 10/35 (29%) — the same
  number as the 40% measured concurrently, and the 0/5 was an ordinary draw. But a **literal
  English translation of it scores 29/35 (83%)**, separating in each of two sweeps and in a
  single sweep running both arms back to back (pooled p = 9e-6). This is not a general
  Portuguese weakness — the PT positives in the other three sets score 5/5, 5/5 and 4/5 on
  Haiku — it is this query against this description on this model.
