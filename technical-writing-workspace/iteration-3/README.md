# iteration-3 — technical-writing 1.0.1 on evals 3 to 6

**Written before the runs.** 1.0.1 was measured only on evals 1 and 2 (iteration-2), the
two its edits were aimed at. Its two edits (the README entry of `references/documents.md`
and a bullet repeated in the check list of step 5) touch no rule that evals 3 to 6 test
directly, so this batch is a regression check on the rest of the set: the runbook (3),
the review (4), the pull request description (5) and the good guide left alone (6).

**Prediction.** Nothing moves. Every check met in both 1.0.0 skill runs of iteration-1 is
met in at least three of four runs here; a check met there in 2/2 and here in two runs of
four or fewer is a regression to report and read. The one place a change could show is
the reply after a review or a description, where the step-5 bullet asks for at most three
lines on what changed; no check of evals 3 to 6 counts those lines, so that is read from
the replies and not scored. Four runs measure no rate.

**Method.** One cell on 1.0.1, evals 3 to 6, four runs each, `run.py` as in iteration-2
(`claude -p`, `claude-sonnet-5-5` read back from each session, the brief tells the session
to read the skill, fixture copies built before the workers, `SHELL=/bin/bash`, `unslop` not
installed). Check 3.21 was reworded by the amendment of 2026-11-22, after iteration-1, so
the four iteration-1 runs of eval 3 (both cells) are re-judged in the same batch from where
they are; the packets of evals 4 to 6 did not change, and their iteration-1 verdicts are
quoted as they are. Twenty packets, `eval-tools/judge.py` on `claude-opus-5-5`, three
passes, met only when the three agree. Script checks by `grade.py`, iteration-1's rules.

## Results

No run is invalid. Every reply was read before counting: all four runbooks of eval 3 were
written after reading the fixture, all four reviews of eval 4 left `docs/webhooks.md`
untouched, and all four runs of eval 6 left the guide untouched (their replies name "the
skill", as in iteration-1). 80/80 script checks met. 60 judge calls, three passes,
unanimous except four splits, none of them on a 1.0.1 run (3.20 three times and 3.14
once, all on the re-judged iteration-1 runs).

All checks, met over total:

| Eval | 1.0.1 (4 new runs) | 1.0.0 (iteration-1, 2 runs) | no skill (iteration-1, 2 runs) |
|---|---|---|---|
| 3 runbook (re-judged with 3.21 as amended) | 82/84 | 41/42 | 28/42 |
| 4 review | 44/44 | 22/22 | 16/22 |
| 5 pull request description | 61/64 | 30/32 | 23/32 |
| 6 good guide left alone | 60/60 | 30/30 | 30/30 |

Checks not met in every 1.0.1 run:

| Check | 1.0.1 | 1.0.0 | no skill | What was found |
|---|---|---|---|---|
| 3.16 no escalation policy or time limit invented | 3/4 | 2/2 | 0/2 | run-2: "Acompanhe por 10 minutos" and "dispara de novo em menos de 1 hora" stated as criteria, neither in the fixture |
| 3.20 nothing about how incidents usually go | 3/4 | 1/2 | 0/2 | run-3: "da mais provável à menos provável", a ranking of causes the fixture does not give; borderline |
| 5.4 the stream within the first three sentences | 2/4 | 2/2 | 0/2 | in sentence 4 |
| 5.5 the reason within the first three sentences | 3/4 | 1/2 | 2/2 | in sentence 4 |

3.21 as amended is met in every skill run of both versions and in neither run without
the skill.

**Reading.**

- **No regression from 1.0.1.** Every check met in both 1.0.0 runs is met in at least
  three of four 1.0.1 runs, except 5.4. The prediction held everywhere else.
- **5.4 is not an effect of 1.0.1, and it is a real trade.** The first three sentences of
  the description have to hold three facts: the 413, the stream and the OOM kills. In
  three of the four runs one of the three fell to sentence 4, the stream twice and the
  reason once; one run got all three in. 1.0.0 had the same trade the other way (5.4 2/2,
  5.5 1/2). Pooled, the two checks are met 5 of 8 times with 1.0.1 and 3 of 4 with
  1.0.0, which separates nothing. Neither edit of 1.0.1 touches the pull request entry.
- **The runbook misses are one sentence each**, both about how to proceed and not about
  who to call: a 10-minute watch and a one-hour re-alert written as escalation criteria,
  and a "most likely first" order of causes. The contacts and the SLA are TODOs in all
  four.
- **The replies are not three lines**, and no check here asks them to be: 16 to 25 lines
  after a runbook, 9 to 13 after leaving the guide alone. The step-5 bullet is about a
  revision of the user's draft, which none of these evals is.

**Limits.** Four runs measure no rate, and the 1.0.0 column has two. The brief tells the
executor to read the skill, so this says nothing about triggering. `unslop` was not
installed, so step 5 had nothing to invoke. `AGENTS.md` loads in every run.

**Cost.** Executors US$ 1.86 (16 sessions), judges US$ 3.39 (60 calls, `judge-cost.json`),
US$ 5.25 in all.
