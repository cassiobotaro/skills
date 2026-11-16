# iteration-21 — lifecycle and "no doc needed" A/B (design-doc 1.5.1 vs 1.4.4), graded against a frozen check list

**Change under test.** design-doc 1.5.0 added a section on updating a document whose
design changed (edit in place until the system ships, then a linked amendment) and
extended contract 5 to the unambiguous change (say a doc is not needed, ask once). 1.5.1
only touched `NOTICE.md`. The last version without either behaviour, 1.4.4, is snapshotted
in `../skill-snapshot-1.4.4/`.

**Method.** Evals 9 (`amend-shipped-doc`) and 10 (`unambiguous-change-no-doc`), two runs
per arm, eight executors in two batches of four. `with_skill` = working tree (1.5.1);
`old_skill` = the snapshot. Executor `claude-sonnet-5-5`, judge `claude-opus-5-5` (each
reported its own id). Grading follows `adr-workspace/iteration-9` as amended in AGENTS.md:

1. **Frozen check list.** `../evals/checks-baseline.json` splits the 10 assertions into 18
   atomic checks (10 + 8). It was written before any run of this iteration, but after its
   author had read one with-skill run of each eval in iteration-20.
2. **Script first.** `grade.py files` decides the 6 `file` / `absence` checks from the
   bytes on disk (`script-checks.json`).
3. **Blind judge for the rest.** `grade.py packets` writes one packet per run under
   `judge-inputs/`; a packet does not name the arm (`judge-map.json` holds the mapping).
   One judge per packet per pass: one pass for the 10 `reply` checks, three for the 2
   `invention` checks, met only when unanimous. 24 judge calls, outputs in `judge-outputs/`.
4. `grade.py table` aggregates into `results.json`. No composite score.

**Results** (checks met / total, both runs of each arm).

| Eval | 1.5.1 (with_skill) | 1.4.4 (old_skill) | What happened |
|---|---|---|---|
| 9 amend shipped doc | 18/20 (file 10/10, reply 8/8, invention 0/2) | 10/20 (file 2/10, reply 8/8, invention 0/2) | Both 1.5.1 runs leave the original's body byte-identical, add one header link and write a 2.3 KB amendment that links back. Both 1.4.4 runs rewrite the original's body in place and create no second document. All four runs state the change and the user's reason, and all four fail the invention check |
| 10 unambiguous change | 15/16 (absence 2/2, reply 11/12, invention 2/2) | 8/16 (absence 2/2, reply 4/12, invention 2/2) | No run creates a file. Both 1.5.1 runs say no choice is open and a doc would restate the implementation, then ask the one question and offer a mini-doc. Both 1.4.4 runs open a discovery interview (problem, costs, alternatives, impacted teams, rollout) and promise the doc once it is answered |
| **Total** | **33/36** | **18/36** | |

**The finding that is not about the change.** Check 9.10 (nothing invented) fails in all
four runs of eval 9, in both arms. The recurring invention is the download path: every
document states as fact that any worker now serves the file from the bucket ("qualquer
worker atende", "o endpoint lê o arquivo do bucket"), while the same document lists "who
serves the download now" as an open question. The 1.4.4 runs add more, one each: run-1 records
2026-11-16, the run date, as the date the change was adopted; run-2 carries the 7-day
retention and its cron over to the bucket. Votes: 0/3 on three runs, 1/3 on 1.5.1 run-2 (the one split,
`results.json`). This is a contract 2 breach by inference, the kind the contract already
names, and the lifecycle section did not cause it. It also confirms the two phrases
flagged by hand in iteration-20.

**Other unmet checks.** 10.7 on 1.5.1 run-2: the reply closes with "me conte a decisão e as
opções que vocês pesaram", which the judge read as asking for alternatives and called
borderline, hence unmet. 10.5 and 10.6 are met on one 1.4.4 run only on the literal words
(it asks whether the phone format is defined, and says the doc would be short).

**Reading.** Four runs per eval cannot measure a rate (AGENTS.md). What they show: the two
behaviours are absent in every 1.4.4 run and present in every 1.5.1 run, and the gap sits
in script-decided checks for eval 9 (10/10 against 2/10), which no judge reading can
move. The amendment came out as a mini-doc in both runs, so the full-structure amendment
seen in iteration-20 (a different executor model, claude-fable-5-2) did not recur. The
invention in the amendment is the defect worth a follow-up, and it needs its own A/B.

**Cost.** Executors 8 × ~49 k = 0.39 M tokens; judges 24 × ~41 k = 0.98 M tokens.
