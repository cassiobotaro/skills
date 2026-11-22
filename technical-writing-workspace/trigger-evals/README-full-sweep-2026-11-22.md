# First full sweeps of the technical-writing trigger set as it stands

2026-11-22, serial, through `eval-tools/run_trigger_eval.py --routine`, description of 1.0.1
(unchanged since 1.0.0).

**Why.** The one routine check so far (`serial-2026-11-22-routine-sonnet.json`) scored
24/30 on the positives, and its six misses were two queries whose premises did not hold
in this repository. Both were rewritten to carry their material and probed at five runs
(5/5 and 4/5). The set as it now stands has never been swept in full, and the skill has
no haiku number.

**Read before the sweeps.**

- claude-sonnet-5-5, 3 runs per query: the positives are a regression guard and should
  be at 90% or more; a negative that fires is listed and probed on its own at ten runs
  before it is called a false fire; the canary at full marks or the sweep is void.
- claude-haiku-5-5, positives at 5 runs: one number for the release, an early warning
  and not a target. The description is not to be tuned to it.

## Results

| | claude-sonnet-5-5 (`serial-2026-11-22-routine-sonnet-full-set.json`) | claude-haiku-5-5 (`serial-2026-11-22-routine-haiku-1.0.1.json`) |
|---|---|---|
| positives | 30/30 | 11/50 (22%) |
| negatives | 0/30 | 0/30 |
| canary | 3/3 | 3/3 |

**Sonnet.** Every positive at 3/3 on the set as it stands, the two rewritten queries
included, and no false fire. The guard holds.

**Haiku.** Per query, in the order of the set: 4, 0, 5, 0, 0, 0, 2, 0, 0, 0. Seven of the
ten positives never fire. The three that do are the README for a project described in
the message (4/5), the review of a runbook (5/5, which the routine took as its canary)
and the release notes (2/5). This is the lowest haiku number of the five skills that have one (`adr`,
`design-doc`, `structurizr` and `mermaid-sequence`, on the trimmed `AGENTS.md`, sit
between 42% and 80%). No transcript was captured,
so why haiku does not invoke the skill on the other seven is not known. The number is an
early warning for hosts that run a small model and not a target: the description was not
changed.

No cost is reported by the harness; at the rates of `eval-tools/README.md` the two sweeps
are about US$ 3.
