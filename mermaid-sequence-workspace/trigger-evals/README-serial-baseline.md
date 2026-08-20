# mermaid-sequence in the serial baseline (2026-08-20)

Full write-up for all four skills: `../../structurizr-workspace/trigger-evals/README-serial-baseline.md`.
Numbers here are `--num-workers 1`, shipped 1.1.5, files `serial-baseline-*.json`.

| | positives | negatives |
|---|---|---|
| Haiku | 45/50 (90%) | 0/30 |
| Opus | 50/50 (100%) | 0/30 |

Nine of the ten positives score 5/5 on Haiku, including the Portuguese one. The whole deficit is
a single query: *"diagram the retry/backoff interaction between our worker and the third-party
API"* at **1/5** (5/5 on Opus). It is the one positive in the set that does not name a
participant chain — retry/backoff reads as flow control rather than as two parties talking over
time, which is the boundary this skill shares with a flowchart. Worth a larger sample before
anyone treats it as a description defect: at n=5 the difference between 20% and 50% is invisible.

The negatives include the C4/`workspace.dsl` and design-doc near-misses, and none of them fired
on either model.
