# One-line changes: does a clause in the description make the skill fire?

2026-11-21, claude-sonnet-5-5, serial, through `eval-tools/run_trigger_eval.py`.

## The defect

The one-line change of the trigger set ("muda o intervalo desse poller de 10 pra 45 segundos",
with the code pasted) fired 0/13 on 2026-11-21: the session returns the changed code and never
consults the skill. `MAINTAINING.md` records it as the one query that holds.

## The idea, and where it comes from

`addyosmani/agent-skills` records the same shape in its `evals/README.md`: with the code pasted,
the model answers in one turn. What moved its numbers was a clause saying the skill applies even
when the code is pasted and the answer looks obvious, followed by what the skill does first.
Those numbers were taken on claude-opus-5-5 at 3 to 6 runs per prompt, and its own one-line
behavior change stayed at 1 of 6. So this is a hypothesis, not a result to copy.

## What is measured

`oneline-probe.json`: three one-line changes with the code pasted, and a canary.

- the query of the set (the comment next to the constant stays true after the change);
- two written for this probe, in which the change makes an existing comment false
  (JavaScript, a constant; Go, a behavior change under a doc comment);
- the canary, the test query of the set (10/10 on 2026-11-21).

The two new queries were written on the same day as the clauses and by the same hand. No clause
quotes them, but they are not a blind holdout.

Five runs per query, so a number is read for the group of three (n=15), never for one query.

## The clauses

Each is inserted after "…even when the user never mentions comments, and before handing the
change back." They are tried in this order, and at most these three:

- **A** (1022 characters in all): "It applies just as much when the code is pasted in the message
  and the change is one line that looks obvious: the comments around that line are checked first
  and the code is returned second, never the change alone."
- **B** (895): "It applies even when the code is pasted in the message and the change is a single
  line."
- **C** (969): "A small request counts ("change this value", "rename this", "make this return
  X"), even with the code pasted in the message and the edit obvious from reading it."

## The rule, written before any run

1. A probe counts only when its canary fires in at least 4 of 5 runs.
2. A clause passes when the three one-line queries reach 8/15 or more **and** at least 6 more
   than the current description scored in its own probe of the same day.
3. The first clause that passes goes to the routine check, run on the current text and on the
   candidate. It ships only with no false fire on the candidate (a fire is probed at ten runs
   before it is read) and with positives no more than 3/30 under the current text's.
4. If no clause passes, the description stays as it is, and this file records the three results.

## Results

Claude Code 2.1.330. Everything below was run after the rule above was written, in this order.

### The probe (`oneline-probe.json`, 5 runs per query)

| query | current text (1.0.0) | clause A |
|---|---|---|
| poller interval, the query of the set | 0/5 | 3/5 |
| retry limit, JavaScript | 0/5 | 3/5 |
| empty slice instead of nil, Go | 1/5 | 5/5 |
| **the three one-line changes** | **1/15** | **11/15** |
| canary (pytest tests) | 4/5 | 5/5 |

Files: `serial-2026-11-21-oneline-probe-current-sonnet-n5.json` and
`serial-2026-11-21-oneline-probe-clauseA-sonnet-n5.json`.

Both probes count (rule 1), and clause A passes rule 2: 11/15, ten more than the current text.
Clauses B and C were not run, since the rule stops at the first that passes. Nothing here says
whether the shorter B would have done the same.

### The routine check (`trigger_eval.json`, 3 runs per query)

| | current text (1.0.0) | clause A |
|---|---|---|
| positives | 20/30 | 27/30 |
| false fires | 0/30 | 0/30 |
| canary | 3/3 | 3/3 |

Files: `serial-2026-11-21-routine-sonnet-before-clause.json` and
`serial-2026-11-21-routine-sonnet-after-clause.json`.

Clause A passes rule 3 and ships as 1.1.0. The text measured is the text in `SKILL.md`,
compared as strings.

## How to read it

- The probe is the evidence for the clause: 1/15 against 11/15 on the group. Five runs say
  nothing about one query, so "the Go query fires every time" is not a finding.
- The routine pair shows no false fire and no loss. Its 20/30 against 27/30 is one sweep each
  at three runs per query; by the rules in `eval-tools/README.md` that is not a measured gain.
  Two queries that scored 0/3 with the current text in this sweep (the refactor, "limpa os
  comentários") had scored 2/3 and 3/3 earlier the same day.
- The query of the set is still the weakest. Pooling the probe and the sweep it is 0/8 without
  the clause and 4/8 with it.
- The description is 1022 characters, two under the limit. The next clause has to replace
  something.
- A trigger is not adherence. None of these runs looked at whether a session that invoked the
  skill then left the comment right.
