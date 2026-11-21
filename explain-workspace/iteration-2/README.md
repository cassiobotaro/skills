# iteration-2 — explain 1.0.1 on eval 9, and three amended checks re-judged

Two things, judged in one batch on 2026-11-21.

**1. Does 1.0.1 shorten the notes on a revised draft?** 1.0.1 (commit 6d9e4de) adds one
sentence to the "Before sending" list: for a revision of the user's draft, three lines at
most on what changed. The rule was already in section 5, and both runs of 1.0.0 in
iteration-1 gave four bullets. Eval 9 was run four times with 1.0.1, same harness and
brief as iteration-1 (`run.py` differs from it only in the fix described below).

**2. What do the amended checks say about the runs of iteration-1?** After iteration-1 the
rule text of checks 1.9, 3.1 and 4.5 was amended and check 7.9 retired
(`../evals/checks-baseline.json`, amendments of 2026-11-21, commit 46bce6c). A changed
check changes the packet, so the twelve iteration-1 runs of evals 1, 3 and 4 are judged
again here: cell `1.0.0` is iteration-1's `with_skill`, `no-skill` its `without_skill`.

Judge `claude-opus-5-5`, three passes per packet, met only when the three agree. Three
splits in the batch, each counted as not met.

## Eval 9 with 1.0.1

Four runs, 47 of 52 checks met. The three checks not met in every run:

| Check | 1.0.1 | 1.0.0 (iteration-1) | What was found |
|---|---|---|---|
| 9.12 at most three lines on what changed | 1/4 | 0/2 | two or three bullets in every run, against four in both runs of 1.0.0 |
| 9.9 no template closer | 3/4 | 2/2 | one run ends on "Qualquer dúvida, estou à disposição." |
| 9.10 no fact absent from the thread and the prompt | 3/4 | 1/2 | one run writes "Já levei sua pergunta para eles" |

On 9.12 the notes did get shorter, and the verdict barely moved. The one run that met it
has a header and two bullets. The other three: a header and three bullets, read as four
lines (judged borderline); two long bullets followed by further remarks about the change
lower down (split 2/3); three bullets and one more sentence on what was removed in the
paragraph about the recipient. The check counts lines and the judges count a header, a
wrapped bullet and a stray remark as lines, so "three lines" and "three bullets" are not
the same test.

## Evals 1, 3 and 4 on the amended text

| Check | 1.0.0 | no-skill | iteration-1, earlier text |
|---|---|---|---|
| 1.9 no concurrency term left undefined (`goroutine` exempt) | 1/2 | 0/2 | 0/2 and 0/2, three splits |
| 3.1 the contrast answered in the first three sentences | 1/2 | 0/2 | 0/2 and 0/2 |
| 4.5 no relied-on term left undefined | 0/2 | 0/2 | 0/2 and 0/2, all four borderline |

- 1.9: with `goroutine` exempt, what is left is `GOMAXPROCS` in one run with the skill
  and `seção crítica` in one run without it; the other run without the skill split 2/3.
- 3.1: the run that opens with "Because it makes the timer unnecessary" now meets the
  check; the one that opens by describing the computation does not, and neither does a
  preamble about what the repository records.
- 4.5: unanimous and no longer borderline. All four replies recommend `asyncio` as a tool
  and never say what it is. With or without the skill, this one is a miss.

The checks of these evals whose text did not change came out as in iteration-1, except
1.10 (an analogy says what corresponds to what), which went from 2/2 to 1/2 in the
`no-skill` cell on a 1/3 split: the same packet content for that check, a different
verdict. A one-run difference between two judge batches is that small.

**Limits.** Four runs of one cell and two of the others: no rate is measured. The 1.0.0
cell of eval 9 was not re-judged, since no check of eval 9 changed; its numbers are
iteration-1's. The brief tells the executor to read the skill.

**Harness.** One run of eval 9 (`run-2`) started in an empty project and said so: "suporte/
thread.md não existe. O diretório de trabalho está vazio". Cause: `fixture()` in `run.py`
created the fixture copy on first use, and with four workers starting on the same eval one
of them copied the directory before the file was in it. `run.py` now builds the fixture
copies before the workers start. The run was repeated and replaced; the empty one, its
transcript and its three verdicts are kept under `invalid/`. The same code is in the
`run.py` of the three iteration-1 directories. No run there was affected: the fixture
copies already existed when their workers started, or, in `code-comments`, every run met
the script checks that need the files.

**Cost.** Executors: five sessions, US$ 0.26 (the discarded one included). Judges: 51
calls, 0.20 M tokens, US$ 1.74 (the three discarded ones included).
