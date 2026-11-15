# iteration-10 — Context padding A/B (adr 1.4.1 vs 1.4.0)

**Change under test.** iteration-9 found ADRs whose Context opened with facts the user
never gave (a motive for the requirement, a general truth framing the choice). 1.4.1
rewrites the Context bullet of step 4 to name that failure and say that two sentences of
real context are a complete Context, and sharpens the matching self-review item to a
sentence-by-sentence reread of Context and Consequences. Body 14 240 → 14 955 bytes. The
1.4.0 working tree tested in iteration-9 is snapshotted in `../skill-snapshot-1.4.0/`
(1.4.0 was never committed or shipped).

**Method.** Eval 10 (where the defect appeared) and the new eval 11
(`thin-context-no-padding`: one stated force, one stated trade-off, a domain that invites
filler), two runs per arm, eight executors in two batches of four. `with_skill` = working
tree (1.4.1); `old_skill` = the 1.4.0 snapshot. Executor `claude-sonnet-5-5`, judge
`claude-opus-5-5`. Grading as in iteration-9 (frozen check list, script pre-pass, blind
packets, evidence or search, three passes with unanimity), with one cost change: **one
judge agent per pass grades all eight packets** in a shuffled order, instead of one agent
per packet per pass (3 calls, 0.20 M tokens, against 24 calls and ~1.0 M). The checks for
eval 11 were added to `../evals/checks-baseline.json` before its first run.

**Results** (checks met / total, both runs of each arm).

| Eval | 1.4.1 (with_skill) | 1.4.0 (old_skill) | What happened |
|---|---|---|---|
| 10 write ADR, route linking | 23/24 | 22/24 | Every Context in both arms is two or three sentences built from the user's words; the motive and the "usual place" sentence of iteration-9 appear in no run. Check 10.9 is split 2/3 in three runs, on a different sentence: Consequences says keeping the counters in Redis "adds load" |
| 11 thin context | 24/24 | 23/24 | Both 1.4.1 runs: Context is the two stated facts, nothing else. Both 1.4.0 runs add one sentence to Context ("files kept on local disk would be lost whenever an instance is replaced"), which every pass read as a restatement. One 1.4.0 run adds to Consequences that a network read "is slower than reading from local disk" (11.10 unmet, 0/3) |
| **Total** | **47/48** | **45/48** | |

**Did the fix work?** Not shown. The defect it targets did not reproduce in the 1.4.0 arm
this time, so there was nothing for 1.4.1 to beat. Pooling eval 10 across the two
iterations, the padded Context appears in 2 of 4 runs of 1.4.0 and 0 of 2 runs of 1.4.1
(0 of 4 counting eval 11). That is the direction the change intends and it is not a
measured effect: at these sample sizes a behaviour that shows up half the time is absent
from two runs one time in four.

**What the grading showed.**

- The three split verdicts all come from the same pass (pass 1), the only one to read
  "adds load" as an inference rather than a restatement. With one agent grading every
  packet of a pass, a strict reading of one check becomes a per-pass bias; in iteration-9,
  with one agent per packet, the same check split only once. The cheaper layout trades
  independence between packets for cost, and the unanimity rule turns that into three
  unmet cells.
- Check 10.9 says a "direct logical restatement" is not an invention and leaves "adds
  load" on either side of that line. The wording needs an anchor case before it is used
  again (e.g. "more state in Redis" restates the trade-off; "adds write load" is counted
  as a restatement / as an inference — pick one).
- The script decided 16 of 24 checks per eval, all met in both arms.

**Reading.** 1.4.1 costs 715 bytes per invocation and produced the specified Context in
four runs of four; 1.4.0 produced it in two of four here and none of two in iteration-9.
Keep the change on the strength of the direction, not of a rate. A rate needs ten or more
runs per arm on eval 10, which a script can score for this one defect without a judge.

**Files.** `benchmark.md` / `benchmark.json` from skill-creator's aggregator (its "3 runs
each" header is a template default; there are two). `review.html` is the static viewer.
