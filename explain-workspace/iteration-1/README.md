# iteration-1 — first behavioral A/B of explain 1.0.0

**Question.** With the skill read, does an agent explain and write for other people better
than the same agent without it, on the ten evals?

**Method.** Two cells, two runs per eval each, 40 runs. `with_skill` is told to read
`explain/skills/explain/SKILL.md` (1.0.0, commit 9c7e5fd) and follow it; `without_skill`
gets the same brief without that step. The executors are headless sessions (`claude -p`,
`run.py`) on `claude-sonnet-5-5`, read back from each session, each started in its own
copy of the eval's fixture (an empty directory for the seven evals that have none), with
`--setting-sources project,local` so that no user-scope skill loads in either cell, and
with `SHELL=/bin/bash` so that a bare `ls` lists the files (see
`../../unslop-workspace/iteration-1/README.md`). The session's final message is the reply.

The checks are the 89 of `../evals/checks-baseline.json`, frozen on 2026-11-21 before any
run (commit ea11b0b): 8 decided by `grade.py` from the bytes, 81 judged by
`eval-tools/judge.py` on `claude-opus-5-5`, three passes per packet, met only when the
three agree. No run did nothing: the only short replies are the four of eval 6, which asks
for one line.

**Result.** Checks met over total, two runs per cell:

| Kind | with_skill | without_skill |
|---|---|---|
| file and absence (script) | 16/16 | 16/16 |
| reply | 68/70 | 65/70 |
| negative | 64/74 | 55/74 |
| invention | 17/18 | 15/18 |
| all | 165/178 | 151/178 |

Six splits in 324 judged verdicts, each counted as not met: three on 1.9, and one each on
9.9, 10.4 and 10.5.

Where the cells differ:

| Check | with_skill | without_skill | What was found |
|---|---|---|---|
| 10.2 ends with exactly one question or task | 2/2 | 0/2 | without the skill the turn closes on three or four exercises |
| 10.3 asks nothing else before it | 2/2 | 0/2 | same replies |
| 10.5 leaves out the call stack, memoization, tail calls | 2/2 | 0/2 | one reply has a section on the stack; the other only previews it (split 2/3) |
| 10.4 no more than two new ideas | 1/2 | 0/2 | with the skill, one reply adds "trust the recursive call" as a third (split 1/3) |
| 9.9 no template closer | 2/2 | 0/2 | "Qualquer dúvida, é só falar"; "Se precisar de algo até quinta, é só me chamar" (split 2/3) |
| 9.10 no fact absent from the thread and the prompt | 1/2 | 0/2 | "já encaminhei seu pedido", an action nobody reported, in three of four runs; one also dates Monday as 16/11 |
| 9.5 first answer within two sentences of the greeting | 2/2 | 1/2 | one reply gives the date in its fourth sentence |
| 7.6 asserts causation nowhere | 2/2 | 1/2 | "caminhar faz bem e está associado a menos demência" |
| 7.8 adds no fact absent from the file | 2/2 | 1/2 | same sentence |
| 1.11 an analogy says where it stops working | 1/2 | 0/2 | the lock or bathroom-key analogy carries no limit in three of four runs |

Not met in any run of either cell:

| Check | What was found |
|---|---|
| 1.9 no concurrency term left undefined | `goroutine`, `seção crítica` or `GOMAXPROCS` used before or without a definition; three of the four verdicts are splits |
| 3.1 the contrast answered in the first three sentences | with the skill the opening describes the mechanism ("Because it makes the timer unnecessary…"); without it the opening says the motive is not recorded. Judged borderline in the first case |
| 4.5 no term the reader did not use left undefined | `asyncio` is named as a tool and never defined, in all four |
| 7.9 the text is not longer than the 87-word summary | about 100 to 160 words in all four |
| 9.12 the remarks on what changed take at most three lines | four or five bullets in all four |

**Reading.**

- The clearest effect is the teaching loop (eval 10): with the skill the first turn is one
  idea, one case and one question; without it, a lecture and a list of exercises. Four
  checks move together, so this is one behavior, seen in both runs.
- In the texts for someone else (evals 7 and 9) the skill keeps the claim and the facts
  closer to the source and drops the stock closer. It does not stop "I have already
  forwarded your request" in one run of two.
- Five checks fail in both cells, with or without the skill: every borrowed term defined
  (1.9, 4.5), the answer first (3.1), a simplified text no longer than its source (7.9)
  and at most three lines on what changed (9.12). All five come from the eval spec, so
  either the skill does not get there yet or the check is stricter than intended; 1.9,
  3.1 and 4.5 were judged borderline, 7.9 and 9.12 were not.
- On the other evals (2, 5, 6, 8) both cells met every check: the wrong premise corrected
  first, the baseline risk shown with hypothetical numbers, the one-line fact left at one
  or two sentences, the email with a gap instead of an invented deadline.

**Limits.** Two runs per cell: no rate is measured, and a one-run difference is not a
finding. The brief tells the `with_skill` executor to read the skill, so this is about
what the skill does once read. Counts of words, sentences and lines were made by the judge,
which counts badly near a limit; 7.9 and 9.12 are far from theirs. The check list has no
anchor cases, and 1.9 shows it: what counts as "a concurrency term the user did not use"
split the judges on three of four packets.

**Cost.** Executors: 40 sessions, 1.64 M tokens summed over turns, US$ 1.48 (US$ 0.017 to
0.055 per run). Judges: 120 calls, 0.42 M tokens, US$ 3.49.
