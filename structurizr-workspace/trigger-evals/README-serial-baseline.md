# Serial baseline: all four skills, both models (2026-08-20)

Every trigger number recorded in this repo before today was measured at `--num-workers 10`.
`README-21pp-analysis.md` established that concurrency depresses the rate unevenly and told
anyone quoting a number to re-measure serially. This is that re-measurement, for all four
skills on both models, and it is the baseline other numbers should be compared against from
here on.

Method: `./eval-tools/run_trigger_eval.py` from the repo root, `--num-workers 1` (its default),
`--timeout 120`. Positives at `--runs-per-query 5` (n=50 per skill/model), negatives at
`--runs-per-query 3` (n=30). Shipped descriptions: `adr` 1.3.2, `design-doc` 1.3.6,
`structurizr` 1.3.0, `mermaid-sequence` 1.1.5. Files are the `serial-baseline-*.json` in each
`<skill>-workspace/trigger-evals/`.

## The baseline

Positives, aggregate trigger rate:

| skill | Haiku serial (n=50) | Haiku @10 workers (n=30-60) | Opus serial (n=50) | Opus @10 workers (n=30-60) |
|---|---|---|---|---|
| adr | 43/50 (86%) | 28/30 (93%) | **49/50 (98%)** | **20/30 (67%)** |
| design-doc | 48/50 (96%) | 28/30 (93%) | 50/50 (100%) | 25/30 (83%) |
| mermaid-sequence | 45/50 (90%) | 26/30 (87%) | 50/50 (100%) | 30/30 (100%) |
| **structurizr** | **37/50 (74%)** | **28/60 (47%)** | **49/50 (98%)** | 46/60 (77%) |
| all four | 173/200 (86.5%) | | 198/200 (99%) | |

Negatives: **1 false fire in 240 samples**, all of it on one query — see below.

## What moved, and what that says about the old numbers

**The concurrency penalty is not a `structurizr` problem.** The largest single correction in the
table is `adr` on Opus: **67% → 98%, +31pp**, larger than `structurizr`'s own Haiku correction
(+27pp). `README-21pp-analysis.md` said "the `adr` numbers are roughly safe; the `structurizr`
ones are not" — that generalisation was drawn from Haiku alone and does not hold. Every
ten-worker number in this repo is depressed by an unknown amount, `adr`'s included.

**On Opus the differences between skills are gone.** 98, 98, 100, 100 — the old ten-worker
ordering (mermaid 100% > design-doc 83% > structurizr 80% > adr 67%) was almost entirely
contention. Any Opus comparison between these four descriptions is now measuring nothing.

**The model ordering reverses.** The ten-worker sweeps had `adr` scoring *worse* on Opus than on
Haiku (67% vs 93%) and `structurizr` likewise ambiguous. Serially, Opus is at or above Haiku for
all four skills, 99% against 86.5% aggregate (Fisher p = 7e-7). Opus sessions do more work before
answering, which is exactly the behaviour contention punished hardest.

**On Haiku the skill ordering survives, but only the extremes are real.** design-doc (96%) >
mermaid-sequence (90%) > adr (86%) > structurizr (74%). structurizr vs design-doc separates
(p = 0.004); structurizr vs adr does **not** (p = 0.21), and pooling both serial sweeps ever run
(structurizr 76/100, adr 83/100) still gives p = 0.29. The honest statement is that `structurizr`
is the weakest of the four on Haiku by a margin this harness cannot pin down at n=50.

## How much does an identical sweep move?

The same serial configuration has now been run twice on two skills, hours apart:

| Haiku, positives | earlier serial (n=50) | this baseline (n=50) |
|---|---|---|
| adr | 40/50 (80%) | 43/50 (86%) |
| structurizr | 39/50 (78%) | 37/50 (74%) |

±4-6pp between identical runs, in both directions — right at the binomial standard error (~6pp
at n=50). **A 12pp skill-level difference at n=50 is inside this band.** That is the resolution
limit of a 10-query, 5-run serial sweep, and it is why the structurizr/adr question above stays
open rather than being answered by this table.

## Task 1: the Portuguese structurizr query

`README-21pp-analysis.md` left one query unexplained — index 7 of the structurizr set, *"modela em
Structurizr DSL a arquitetura do nosso sistema de cobrança, com containers e componentes"*, the
only positive that appeared to go **down** when concurrency was removed (40% at ten workers, 0/5
serial), and it warned against reading a Portuguese-language weakness into it before a larger
sample existed. Measured, Haiku, serial:

| arm | sweep 1 | sweep 2 | pooled |
|---|---|---|---|
| PT (shipped query) | 7/20 | 3/15 | **10/35 (29%)**, 95% CI [16, 45] |
| EN (literal translation, not shipped) | 16/20 | 13/15 | **29/35 (83%)**, 95% CI [67, 92] |

Two findings, and they pull in different directions:

1. **The "wrong direction" anomaly does not exist.** The query's true rate is ~29%; 40% at ten
   workers and 29% serially are the same number. The 0/5 that made it look like a reversal is an
   ordinary draw at p=0.29 (18% of five-run samples). One more instance of the rule this repo
   keeps re-learning: n=5 cannot rank anything.
2. **For this query, language is the lever.** The EN arm is a literal translation — same request,
   same vagueness, same length — and it triggers 83% against 29%. Both sweeps separate on their
   own (p = 0.0095 and p = 0.0007; pooled p = 9e-6), and the second sweep ran both arms
   back-to-back inside a single sweep, so drift cannot explain it.

**But there is no general Portuguese weakness in this repo**, and that is the part that keeps
this from being a language finding: the other three sets each carry a Portuguese positive, and on
Haiku they score `design-doc` 5/5, `mermaid-sequence` 5/5, `adr` 4/5 (14/20 at n=20). Only this
query collapses, and only on Haiku — Opus fires it 5/5.

**Verdict: neither of the plan's two options alone.** It is not the documented sampling variance
(the PT/EN separation is far outside it), and it is not "Portuguese depresses triggering" (three
other PT queries are healthy). It is an interaction between this one query and the `structurizr`
description on Haiku, where the Portuguese phrasing loses a match the English phrasing wins.

### What the misses actually are

`run_eval.py` collapses a session to one bit at the first tool call, so "did not trigger" hides
several behaviours. `eval-tools/capture_trigger_transcripts.py` (added today) keeps the whole
stream and classifies it. Eight PT runs and four EN runs:

| outcome | PT | EN |
|---|---|---|
| `strict_trigger` — candidate is the first tool | 5 | 2 |
| `late_trigger` — candidate invoked after `find`/`Read` | 1 | 0 |
| `prose_only` — no tool call at all | 2 | 2 |
| `other_tool` — tools, candidate never invoked | 0 | 0 |

**No miss is the model doing the wrong job.** Every non-trigger is the session answering in prose
with 2-4 scoping questions — the repo's own "record, don't invent" contract, which the nested
session picks up from `CLAUDE.md` and performs *without* invoking the skill (one PT transcript
quotes the phrase verbatim). The skill is never displaced by a sibling skill, and nothing is
fabricated. The one `late_trigger` is the documented first-tool-wins artifact: `find` over the
repo, two `Read`s, then the skill.

This also caps how much a description rewrite could buy here: a session that decides to ask
questions instead of acting is not choosing a different skill, it is choosing not to act yet.

## Negatives: the zero-false-fire claim now has one exception

240 negative samples across four skills and both models produced exactly one false fire:
**`design-doc` on Opus, "write a PRD for the new referral program — target users, success
metrics, scope"**, 1/3. Re-measured at n=15 it fires **2/15**; pooled **3/18 (17%)**, 95% CI
[6, 39].

It stays far below the 0.5 pass threshold, so the query still passes, and a PRD is the nearest
neighbour a design-doc description has. But the repo's strongest claim — *"0 false fires in 300
samples, the one assertion that never wavered"* — is now false as stated. The accurate version:
**1 in 240 serial samples, concentrated on a single adjacent-artifact query at ~17%.**

Sweeps of a negatives-only set have a nasty property: a degraded sweep and a perfect result are
the same output. Every negatives sweep here therefore carried a **canary** — the skill's
strongest positive query, spliced into the set. All eight canaries scored 3/3, so all eight
zeros are real zeros. The canary sets are in the scratchpad, built by the snippet in "Rerunning".

## Where Haiku actually loses

Per-query, Haiku ≤3/5 (Opus scores 5/5 on all of these except `ADR 0007` at 4/5 and the ADR-linking
query at 4/5):

| Haiku | skill | query |
|---|---|---|
| 0/5 | structurizr | modela em Structurizr DSL … *(above)* |
| 1/5 | structurizr | add a component diagram … to our **existing C4 model in workspace.dsl** |
| 1/5 | mermaid-sequence | diagram the **retry/backoff interaction** between our worker and the third-party API |
| 3/5 | structurizr | we use Structurizr — model the **deployment** … staging and prod AWS |
| 3/5 | design-doc | **review my design doc** … it's in `docs/designs/rate-limiter.md` |
| 3/5 | adr | **ADR 0007** is out of date … mark it superseded |

Three of the six name a file or record the session must locate first (`workspace.dsl`,
`docs/designs/rate-limiter.md`, `ADR 0007`) — the same class `README-21pp-analysis.md` identified
as concurrency-sensitive, still the weak class after concurrency is removed. That is consistent
with the first-tool-wins detection artifact rather than with a trigger failure: a session that
reads the named file before invoking is recorded as a miss. Anyone who wants a true number for
these queries has to count the skill wherever it appears in the transcript, not only first.

The other three are genuine boundary cases: an AWS deployment query sitting next to structurizr's
AWS-icons exclusion, a retry/backoff query that reads as flow-control rather than interaction, and
a *review* request against a description whose review half is its weaker half.

## Claims elsewhere in this repo that this baseline invalidates

All of these were corrected in place rather than deleted; the error history is part of the record.

- **`README-model-ab.md`, Part 1 table** — the four-skill model comparison. Every cell is a
  ten-worker number; the Opus column is wrong by up to 31pp and its ordering is an artifact.
- **`README-model-ab.md` and `README-haiku-investigation.md`, "zero false fires"** — held across
  those sweeps, but not universally: see the PRD query above.
- **`README-21pp-analysis.md`, "the `adr` numbers are roughly safe"** — false on Opus.
- **`README-21pp-analysis.md`, "Still open"** — the PT query question is answered above.
- **`README-haiku-investigation.md`, the n=10 per-query table** — ten-worker numbers; the two
  queries it reports at 4/10 score 4/5 and 0/5 serially, and its claim that `structurizr` is
  "genuinely weaker by 21pp" is already superseded, now further to ~12pp and not significant.
- **`structurizr-workspace/.../README-current.md`, the two queries "missing at 0.00"** — the
  `workspace.dsl` component-diagram query and the ADR-linking query. Serially they score 1/5 and
  5/5 on Haiku, 5/5 and 4/5 on Opus. Neither is a zero.
- **`adr-workspace/.../README-current.md`, "the 3 hard queries"** — reported at 5/18 (28%) under
  the shipped text, with the conclusion that they "still fall below the trigger threshold more
  often than not". Serially they score **26/30 (87%)**, 95% CI [70, 95]: 12/15 on Haiku, 14/15 on
  Opus. There are no hard queries in the `adr` set any more, and the lever that document
  recommends pursuing is aimed at a problem that was mostly contention.

## Operational notes from this session

- **A laptop suspend ruins a sweep silently.** The machine suspended 14:11 and resumed 17:02,
  mid-sweep. `run_single_query`'s timeout is wall-clock, so the in-flight session's 120s expired
  during suspend and was recorded as a non-trigger. The sweep looked healthy (70%, no degraded
  signature) and is kept as
  `serial-baseline-positives-haiku-n5-SUSPENDED-DISCARDED.json`; the clean re-run scored 74%.
  **Wrap long sweeps in `systemd-inhibit --what=idle:sleep --mode=block`** — every sweep in this
  baseline after the incident was.
- **Splice a canary positive into any negatives-only sweep** (see above).
- `eval-tools/capture_trigger_transcripts.py` answers "what did the misses actually do". It stops
  each session as soon as the question is answered, so nested sessions do not run loose in the
  working tree.
- Cost: a 50-session serial sweep runs 5-6 min on either model. The full baseline — 8 positive
  sweeps, 8 negative sweeps, the Task 1 probes — is about 900 sessions and a little over two
  hours of wall clock.

## Rerunning

```bash
# positives / negatives split, plus the canary used for negatives sweeps
python3 - <<'PY'
import json, pathlib
S = pathlib.Path("/tmp/eval-sets"); S.mkdir(exist_ok=True)
for name, ws in {"adr":"adr-workspace", "design-doc":"design-doc-workspace",
                 "structurizr":"structurizr-workspace",
                 "mermaid-sequence":"mermaid-sequence-workspace"}.items():
    full = json.load(open(f"{ws}/trigger-evals/trigger_eval.json"))
    base = json.load(open(f"{ws}/trigger-evals/serial-baseline-positives-haiku-n5.json"))
    canary = max(base["results"], key=lambda r: r["triggers"])["query"]
    pos = [q for q in full if q["should_trigger"]]
    negs = [q for q in full if not q["should_trigger"]]
    (S/f"{name}-positives.json").write_text(json.dumps(pos, indent=2, ensure_ascii=False))
    (S/f"{name}-negatives-canary.json").write_text(json.dumps(
        [next(q for q in pos if q["query"] == canary), *negs], indent=2, ensure_ascii=False))
PY

# one skill/model combination, from the repo root, never more than one at a time
systemd-inhibit --what=idle:sleep --why="trigger eval sweep" --mode=block \
  ./eval-tools/run_trigger_eval.py \
    --eval-set /tmp/eval-sets/structurizr-positives.json \
    --skill-path structurizr/skills/structurizr \
    --model haiku --runs-per-query 5 --timeout 120 \
    -o structurizr-workspace/trigger-evals/serial-baseline-positives-haiku-n5.json
```

Do not pass `--num-workers`. Do not run two sweeps at once — concurrency between *your own*
sweeps is the same variable, and it is what this baseline exists to keep out of the numbers.
