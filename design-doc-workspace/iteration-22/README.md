# iteration-22 — invention by consequence (design-doc 1.5.2), eval 9 against the iteration-21 baseline

**Change under test.** iteration-21 found that every run of eval 9, in both arms, stated
as fact how the download works after the move to S3 while listing the same thing as an
open question. 1.5.2 adds three things to `SKILL.md`: a paragraph in contract 2 naming
inference by *consequence* (with the test "a fact cannot be both asserted in one section
and asked in Open questions"), a matching line in the self-review list, and one sentence
in the lifecycle section. The example in the contract is about sessions and a shared
cache, not the eval's scenario. Body 19 309 → 20 113 bytes (+4.2%). The previous version
is snapshotted in `../skill-snapshot-1.5.1/`.

**Method.** Four runs of eval 9 with the working tree (1.5.2), executor
`claude-sonnet-5-5`, judge `claude-opus-5-5`, graded with the same frozen check list and
the same `grade.py` as iteration-21 (only the eval and arm lists differ). The baseline arm
was not re-run: it is the two 1.5.1 runs of iteration-21, same prompt, same executor
model, same day, same packet format. Consequences: the four packets of this iteration are
all the same arm, so the judges were blind only in the sense that a packet never names a
version, and the comparison is across two judging sessions. One pass for the `reply`
checks, three for 9.10. The third pass on run-4 was not run, because two unmet votes had
already settled it; `grade.py` reports that cell as not scored, which counts as unmet.

**Results** (checks met / total).

| | 1.5.2 (this iteration, 4 runs) | 1.5.1 (iteration-21, 2 runs) |
|---|---|---|
| file (9.1–9.5) | 20/20 | 10/10 |
| reply (9.6–9.9) | 16/16 | 8/8 |
| invention (9.10) | 2/4 | 0/2 |

Votes on 9.10, per run: run-1 3/3, run-3 3/3, run-2 2/3 (split, counted unmet), run-4 0/2.

- **What changed.** All four documents send the date of the change and "who serves the
  download now" to Open questions, and none records the run date as the date of the
  change. In iteration-21 the download path was asserted in all four runs of both arms.
- **What did not.** run-4 still writes "qualquer worker pode atender o download" three
  lines above the open question that asks it. That is exactly the pattern the new
  paragraph names, so the rule is not followed every time.
- **The split.** One of three judges failed run-2 for listing "Não fazer nada" under
  Alternativas consideradas with the user's 404 as the reason it was discarded. The other
  two read it as the status quo the user described. The skill asks for a "do nothing"
  alternative in every document, so this is the skill's own instruction meeting the
  invention check, not a slip of this run.
- **A phrase the judges disagree on.** "elimina o 404" appears in run-1 and run-4. Five
  judges accepted it as following from the user's stated cause; one called it an outcome
  the user only implied. It is the same kind of consequence the new paragraph warns
  about, and it survived.

**Reading.** Six runs cannot measure a rate (AGENTS.md): 2/4 against 0/2 is a direction,
not a number, and with the four 1.4.4 and 1.5.1 runs of iteration-21 all failing it is
2/4 against 0/4 on the same check. No file or reply check moved, so the added text cost
nothing measurable on this eval. The residual is real: one run in four still asserts the
download path. Whether "do nothing" may be written without the user having said the team
considered it is an open question about the check and the skill, not about this change.

**Cost.** Executors 4 × ~52 k = 0.21 M tokens; judges 11 × ~44 k = 0.48 M tokens.
