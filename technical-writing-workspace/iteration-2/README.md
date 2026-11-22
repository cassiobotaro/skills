# iteration-2 — technical-writing 1.0.1: the license section and the three lines

**Written before the runs.** 1.0.1 answers two things iteration-1 counted against the
skill. (1) Both READMEs of eval 2 carried a "License and help" heading over a TODO (check
2.20, 0/2): the README entry of `references/documents.md` now says that the parts for
contributors and for license and help go in only when the repository states them, and
that what is missing is said in the reply. (2) After the revision of eval 1 the reply
took four or five lines and retold the document (checks 1.27 and 1.28, 0/2 each, as
without the skill): the check list of step 5 now repeats the rule of the Deliver section,
three lines at most and nothing of the document retold.

**Prediction.** If the edits work, 2.20 is met in at least three of four runs, and so are
1.27 and 1.28. `explain` made the same kind of edit for the same rule and got two or
three bullets in every run with its check met in one of four, because the judges count a
header or a wrapped bullet as a line; 1.27 says how to count, so that reading is tested
here too. Anything that was met in iteration-1 and is not met here in two runs or more is
a regression to report. Four runs measure no rate.

**Method.** One cell on 1.0.1, evals 1 and 2, four runs each, `run.py` as in iteration-1
(`claude -p`, `claude-sonnet-5-5` read back from each session, the brief tells the
session to read the skill, fixture copies built before the workers, `SHELL=/bin/bash`).
The six iteration-1 runs of the same evals were re-judged in the same batch from where
they are: both cells of eval 1, because check 1.26 was reworded by the amendment of
2026-11-22 and the packet changed, and the two skill runs of eval 2. Fourteen packets,
`eval-tools/judge.py` on `claude-opus-5-5`, three passes, unanimous. No run is invalid.

**Results** (runs meeting the check / runs; every check not listed is met in every run of
every column).

| Check | 1.0.1 (4 new runs) | 1.0.0 (2 runs, re-judged) | no skill (2 runs, re-judged) |
|---|---|---|---|
| 2.20 no license and no license section | 4/4 | 0/2 | – |
| 1.27 at most three lines on what changed | 1/4 | 0/2 | 0/2 |
| 1.28 the reply does not summarize the document | 0/4 | 0/2 | 0/2 |
| 1.19 no agentless passive in Delivery | 0/4 | 1/2 | 2/2 |
| 2.29 no agentless passive about the pipeline in the README | 3/4 | 2/2 | – |
| 1.20 the backups claim is still in the document | 4/4 | 2/2 | 1/2 |
| 1.23 no component the fixture lacks | 4/4 | 2/2 | 1/2 |
| 1.26 every figure is in a fixture file (as amended) | 4/4 | 2/2 | 2/2 |
| all checks, eval 1 | 101/112 | 51/56 | 50/56 |
| all checks, eval 2 | 119/120 | 58/60 | – |

Four splits in 276 judged verdicts: 1.19 three times and 1.27 once, all in 1.0.1 runs.

**Reading.**

- **The license section is gone** (2.20, 4/4 against 0/2). No README of 1.0.1 has a
  heading for license, help or contributing, and none has a TODO. All four sessions read
  `references/documents.md`.
- **The three-line rule did not move its checks** (1.27 1/4, 1.28 0/4), so the
  prediction failed there. The replies did get shorter: 680 to 1125 characters in four
  or five lines, against 1232 and 1259 in seven and nine with 1.0.0. What keeps the
  checks unmet is one sentence that every reply still has, "the gateway validates,
  rejects and publishes, the worker generates, encrypts, uploads and retries, and the
  notifier sends the email": the judges count each clause-heavy sentence as a line and
  read that one as the pipeline retold. Saying which actor went where is how these
  replies say what changed, so the rule as written and that sentence pull against each
  other. The bullet stays in 1.0.1 for the shorter reply; it is not evidence that the
  rule is now followed.
- **1.19 is not a regression of this edit, and it is a real miss.** "Once the upload is
  done" is the fixture's own clause, and five of the six skill documents of both
  versions keep it, where both documents without the skill reword it. The judges are
  divided on whether it is a passive or a state (three of the four 1.0.1 misses are
  splits). The skill's own test would ask who does the upload, and the answer is two
  lines above it.
- **The amended 1.26** is met in every run, the two without the skill included: the
  figures they add are the fixture's.

**Limits.** Four runs measure no rate, and the 1.0.0 column is two runs. Only evals 1
and 2 were run on 1.0.1; the other four evals were not, on the argument that the two
edits touch the README entry and the reply after a revision. The brief tells the session
to read the skill.

**Cost.** Executors: 8 sessions, 1.10 M tokens, US$ 0.64. Judges: 42 calls, 0.38 M
tokens, US$ 2.95.
