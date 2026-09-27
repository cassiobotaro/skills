# Probe — eval 7 ownership call: does the 1.5.0 classification row change behaviour?

**Question.** Iteration-7 (1.4.0) and iteration-8 (1.5.0) each had one run of eval 7 model the
customers' Flutter app as an external system without asking who builds it. One sample per version
says nothing (CLAUDE.md: per-query claims need n ≥ 10). This probe runs the identical eval-7 prompt
five more times per version, foreground subagents, project root = each run's `outputs/`, Docker
validation available. Snapshots: `../../skill-snapshot-1.4.0`, `../../skill-snapshot-1.5.0`.

**The row under test** (`c4-classification.md`, 1.5.0): *Mobile / desktop client app — its own
container, inside the system whose team builds it. If the prompt doesn't say who builds it, ask;
don't default to an external system, and don't silently absorb it either.*

**Outcome classes.** `asked_first` — no ownership decision taken; the reply presents the clear
parts and asks (with or without a partial draft that leaves the app out). `external_then_asked` —
file delivered with the app as an external `softwareSystem`, ownership raised afterwards.
`container_no_ask` — app absorbed as a container, ownership never raised.

## Result (probe n=5 per version, plus the one iteration run each → n=6)

| Outcome | 1.4.0 | 1.5.0 |
|---|---|---|
| asked_first | 0 | **4** (runs 1, 2, 3, 5) |
| external_then_asked | 4 (runs 1, 2, 3 + iteration-7) | 2 (run 4 + iteration-8) |
| container_no_ask | 2 (runs 4, 5) | 0 |

Mean tokens, probe runs: 1.4.0 74k, 1.5.0 70k (asking first is cheaper than drafting the whole
file). Every delivered DSL validated clean.

**Reading.** 1.4.0 never asks first and splits its silent default both ways (external 4, container 2)
— the model was guessing, and guessing differently each time. 1.5.0 asks first in 4 of 6 and never
absorbs the app silently; when it does decide, it picks external and raises the question in the same
reply. 4/6 vs 0/6 asked-first is p ≈ 0.03 one-sided (Fisher) at n=6 per arm — a directional shift,
not a precise rate. The row works; it is not airtight, and n=6 cannot say whether the residual is
30% or 10%. Not worth tightening further on this evidence: the 1.5.0 misses are the mild form
(decision + question in one reply), and pushing harder risks the skill asking on prompts where
ownership is actually clear.
