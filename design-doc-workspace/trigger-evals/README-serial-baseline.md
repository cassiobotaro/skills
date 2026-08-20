# design-doc in the serial baseline (2026-08-20)

Full write-up for all four skills: `../../structurizr-workspace/trigger-evals/README-serial-baseline.md`.
Numbers here are `--num-workers 1`, shipped 1.3.6, files `serial-baseline-*.json`.

| | positives | negatives |
|---|---|---|
| Haiku | 48/50 (96%) | 0/30 |
| Opus | 50/50 (100%) | **1/30** |

Best of the four skills on both models, and the only one to score a clean 50/50.

**The one false fire in the entire baseline is here.** On Opus, *"write a PRD for the new
referral program — target users, success metrics, scope"* fired 1/3 in the sweep and 2/15 on a
follow-up probe — **3/18 (17%)**, CI [6, 39], recorded in
`serial-baseline-prd-falsefire-probe-opus-n15.json`. It stays well under the 0.5 threshold, so
the query passes and nothing needs changing; what it retires is the repo-wide claim that these
descriptions have *never* over-triggered. A PRD is the nearest neighbour this description has,
and it leaks slightly on the strongest model.

The one weak positive on Haiku is *"review my design doc … it's in `docs/designs/rate-limiter.md`"*
at 3/5 (5/5 on Opus) — a review request naming a file, which is both the description's weaker
half and the query shape this harness under-counts.
