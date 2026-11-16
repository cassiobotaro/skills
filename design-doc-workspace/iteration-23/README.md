# iteration-23 — eval 9 with anchored judges: design-doc 1.5.3 against 1.5.2, and the residual invention

**Change under test.** 1.5.3 changed one bullet of `references/sections.md`: the "do
nothing" alternative is still always written, but its reason is the pain the user
described and nothing more, and with no pain described it becomes a question. The
iteration also does two things the previous ones left open: it puts the anchor cases of
`../evals/checks-baseline.json` in front of the judges, and it looks again at the residual
of iteration-22 (a document asserting how the download works while asking it).

**Method.** Eval 9 only. `with_skill` = four new runs of the working tree (1.5.3),
executor `claude-sonnet-5-5`. `old_skill` = the four 1.5.2 runs of iteration-22, copied
here unchanged and not re-run (1.5.2 is commit `6f03b8b`; the two versions share the whole
of `SKILL.md`). All eight were graded together: script checks first, then eight blind
packets in shuffled order (`judge-map.json`), judge `claude-opus-5-5`, one judge per
packet per pass, three passes on every invention check, 24 calls. The packets carry the
three anchor cases. Before any run, checks 9.11 (download path stated as fact) and 9.12
(reason of the "do nothing" entry) were added by dated amendment to tell apart the two
ways 9.10 had failed; 9.10 is unchanged and covers both, so the three overlap and are
reported per check. `grade.py table` prints one figure per kind (10/12 and 8/12 for
invention): that figure sums overlapping checks and should not be quoted.

**Results** (runs meeting the check / runs; a run meets an invention check only at 3/3).

| Check | 1.5.3 (4 new runs) | 1.5.2 (4 runs of iteration-22, re-judged) |
|---|---|---|
| file 9.1–9.5 | 20/20 | 20/20 |
| reply 9.6–9.9 | 16/16 | 16/16 |
| 9.10 nothing invented | 3/4 | 2/4 |
| 9.11 download path not asserted | 3/4 | 2/4 |
| 9.12 "do nothing" reason is the user's | 4/4 | 4/4 |

Every one of the 24 judge calls agreed with the other passes on the same packet: all
votes are 3/3 or 0/3, no split.

- **"Do nothing" (9.12).** Not discriminating: both arms are at the ceiling. Six of the
  eight documents carry the entry, and in all six the reason is the user's 404 and nothing
  else, in 1.5.2 as much as in 1.5.3. The new instruction neither helped nor hurt on this
  eval; the anchor is what removed the disagreement (the same 1.5.2 run-2 that split 2/3
  on this entry in iteration-22 is 3/3 on 9.12 here).
- **The residual (9.10, 9.11).** The two checks fail together in every case, on one
  sentence each: "qualquer worker pode atender o download" (1.5.2 run-4), "o que tira a
  dependência de qual worker atende o download" (1.5.2 run-2), "o download não depende
  mais de qual worker recebe a request" (1.5.3 run-3). The last two do not state the
  mechanism, they presuppose it: the sentence is about the 404 going away, and "a worker
  serves the download" rides along. Judges called both borderline, and borderline is
  unmet. Both arms carry the same contract text on this point, so pooled it is 3 runs in
  8.
- **The measurement moved under the check.** 1.5.2 run-2 was not failed for its download
  sentence in iteration-22 (its only unmet vote there was about "do nothing"); here all
  three judges fail it for that sentence. The document is byte-identical. What changed is
  the packet: a check that names the download path made the judges look for it. So the
  2/4 of iteration-22 and the 2/4 here are the same count reached for partly different
  reasons, and the iteration-22 figure understated the download-path failures by one.

**Reading.** Eight runs cannot measure a rate (AGENTS.md); 3/4 against 2/4 is not a
difference. What the iteration establishes: (1) with anchors and an atomic check the
judges stop splitting: none of the eight packets split here, against two of the eight
eval-9 packets of iterations 21 and 22 (23 calls on 9.10); (2) the "do nothing" rule
has no measurable effect here because there was no defect to fix once the check was
anchored; (3) the residual is about 3 in 8 and has changed shape, from asserting the
mechanism outright to presupposing it inside a sentence about the benefit. Writing "the
file no longer depends on the disk of one worker" without saying who serves the download
is what the clean runs do.

**Cost.** Executors 4 × ~50 k = 0.20 M tokens; judges 24 × ~44 k = 1.06 M tokens.
