# iteration-28 — risks nobody gave, when the user wants the document before answering

**Written before the runs.** iteration-27 gave eval 7 with one more sentence, "Não vou
conseguir responder perguntas agora: escreve o documento com o que eu já disse e deixa as
perguntas no final.", and all four documents (two with 1.6.0, two with 1.7.0) filled the
template's Riscos section with risks the user had not given: the Redis or the service
failing in the critical path, a resend after the 24-hour window. Without that sentence
the skill asks for the risks and writes no file, which is its contract. With it, the
skill has no instruction: step 2 says the questions are the deliverable, and contract 3
says that a hole where Risks should be reads as "nobody thought about risks". The model
fills the hole.

**Candidate.** One paragraph at the end of step 2 (`diff skill-a/SKILL.md
skill-b/SKILL.md`, 484 characters): when the user wants the document before they can
answer, each unfilled section is one line that says it awaits their answer and points to
the question, and what occurred to the writer and the user did not state is a question
too, never a row in the section.

**Method, checks, prediction and rule** are in `checks.json`, frozen before any run:
cells `a` (1.9.0 as shipped) and `b` (with the paragraph), four runs each on eval 71 (the
request with the sentence) and two each on eval 7 (the request alone, a guard that the
skill still asks first). Headless sessions on `claude-sonnet-5-5`, `run.py`; the brief
tells the session to read the copy of the skill. Judged by `eval-tools/judge.py` on
`claude-opus-5-5`, three passes, unanimous, one batch.

## Results

Two batches, because the first did not reproduce the defect. The second is the amendment
of 2026-11-22 in `checks.json`, written after the first was judged and before any of its
own runs.

**First batch: the brief tells the session to read the skill** (`run.py`, cells `a` and
`b`; runs meeting the check / runs).

| Check | a (1.9.0) | b (first paragraph) |
|---|---|---|
| 7.8 Riscos states no risk nobody gave | 4/4 | 4/4 |
| 7.24 no such risk anywhere outside Perguntas abertas | 4/4 | 2/4 |
| 7.23 Riscos says it awaits the answer | 4/4 | 4/4 |
| 7.19 no technology, team or stakeholder nobody named | 1/4 | 3/4 |
| all 24 checks of eval 71 | 93/96 | 93/96 |
| eval 7, 7.G1 the session wrote no file | 2/2 | 0/2 |
| eval 7, 7.6 and 7.7 asks for risks and rollout | 4/4 | 4/4 |

The shipped skill did not show the defect here: all four of its Riscos sections hold the
+5 ms the user gave and one line sending the rest to Perguntas abertas. Candidate b is
rejected on its own account. Its paragraph opens "When the user wants the document before
they can answer (they say so, or nobody is there to reply)", and a headless session reads
the second half as true: on the request without the sentence, both b runs wrote the
document instead of asking first. It also names the Redis failure in Proposta as
something pending, in two of four documents.

**Second batch: the skill installed and invoked** (`run_plugin.py`, cells `pa` and `pc`,
`plugin-batch/`). `design-doc` and `unslop` are loaded with `--plugin-dir` from copies
outside the project and the session gets the prompt alone, which is the kind of harness
in which iteration-27 saw the defect. `skill-c` is a second paragraph, written before any
`pa` output: it opens "Only when the user says they want the document before they can
answer" and bars the unstated risk from "a row in that section" and from "a clause in
another one". All twelve sessions invoked `design-doc`; the eight that wrote a document
invoked `unslop` after it.

| Check | pa (1.9.0) | pc (second paragraph) |
|---|---|---|
| 7.8 Riscos states no risk nobody gave | 2/4 | 3/4 |
| 7.24 no such risk anywhere outside Perguntas abertas | 1/4 | 1/4 |
| 7.23 Riscos says it awaits the answer | 4/4 | 4/4 |
| 7.11 the +5 ms cost under a heading of its own | 3/4 | 1/4 |
| 7.19 no technology, team or stakeholder nobody named | 1/4 | 3/4 |
| 7.6 asks the user for the risks | 3/4 | 4/4 |
| 7.22 no actor nobody established | 3/4 | 4/4 |
| all 24 checks of eval 71 | 85/96 | 88/96 |
| eval 7, 7.G1 the session wrote no file | 2/2 | 2/2 |
| eval 7, 7.6 and 7.7 asks for risks and rollout | 4/4 | 4/4 |

One split in the first batch (7.19) and two in the second (7.24, 7.19), counted as not
met.

**Third batch, 2026-11-23: the skill installed, `unslop` not installed** (`run_plugin.py`,
cell `pn`, `plugin-batch-no-unslop/`). The question and the rule are the amendment of
2026-11-23 in `checks.json`, written before the runs: is `unslop` what puts the unstated
risks in the document? Two answers, one from the transcripts of `pa` and one from four new
runs.

*From the `pa` transcripts, at no cost.* Each transcript holds the document as the session
first wrote it, before it invoked `unslop`. In the two `pa` runs that fail 7.8 (run-2,
run-3) the Riscos section is byte-identical before and after `unslop`. In run-1 the first
draft said "Mitigação: medir a latência real em cada fase do rollout" and "A análise de
falha do Redis, da perda de chaves e do próprio serviço ainda não foi feita", and `unslop`
replaced both with a pointer to Perguntas abertas; the document then met 7.8. The drafts
were not judged. `unslop` added no risk in any of the four, and in one it removed lines
of the kind that fail the check in `pn`.

*Cell `pn`*: `pa` with `design-doc` alone loaded with `--plugin-dir`. All four sessions
invoked `design-doc` through the Skill tool, none listed `unslop` (`skills_listed` in each
`timing.json`), and all four wrote one document.

| Check | pa (1.9.0, with `unslop`) | pn (1.9.0, without) |
|---|---|---|
| 7.8 Riscos states no risk nobody gave | 2/4 | 0/4 |
| 7.24 no such risk anywhere outside Perguntas abertas | 1/4 | 0/4 |
| 7.23 Riscos says it awaits the answer | 4/4 | 2/4 |
| 7.11 the +5 ms cost under a heading of its own | 3/4 | 3/4 |
| 7.19 no technology, team or stakeholder nobody named | 1/4 | 2/4 |
| 7.6 asks the user for the risks | 3/4 | 2/4 |
| 7.22 no actor nobody established | 3/4 | 4/4 |
| all 24 checks of eval 71 | 85/96 | 81/96 |

Three splits in `pn` (7.23 once, 7.19 twice), counted as not met. The `pa` column is the
second batch's, judged a day earlier on the same check text.

By the rule, `unslop` is cleared: the defect shows without it in four of four. What fails
7.8 in `pn`: run-1 and run-2 list the Redis dependency and the 24-hour window as risks
(run-1 also writes "Aceito como limite do desenho", an acceptance nobody gave), run-3
gives the +5 ms a mitigation ("medir a latência real antes de avançar de fase"), and
run-4 names the risk inside the pending line ("Outros riscos, como a indisponibilidade do
Redis ou do próprio serviço, não foram discutidos"). Run-2 and run-1 then ask only for
the mitigations or for one failure behaviour, not for the risks, which is 7.6 at 2/4.
Counting the documents written with the skill invoked through the Skill tool: iteration-27
0 of 4 met 7.8, `pa` 2 of 4 (one of the two after `unslop` removed the lines), `pn` 0 of
4. The step that runs `unslop` hides part of the defect; it does not cause it.

**Fourth batch, 2026-11-23: meant as `pn` with AGENTS.md, read as four more `pn` runs**
(`run_plugin.py`, cell `pg`, `plugin-batch-agents-md/`). The cell copied the repository's
AGENTS.md into each project to see whether it is what keeps the brief cells clean. It did
not test that: the projects were under `/tmp`, where a `claude -p` session loads no
project instructions file at all (codeword probes of the same day, in
`../../eval-tools/README.md`). AGENTS.md was a file in the tree; run-1 read it with the
Read tool, the others did not open it. All four invoked `design-doc` through the Skill
tool, none listed `unslop`, and each wrote one document, so they are valid runs of the
`pn` setup.

| Check | pn | pg (same setup) |
|---|---|---|
| 7.8 Riscos states no risk nobody gave | 0/4 | 2/4 |
| 7.24 no such risk anywhere outside Perguntas abertas | 0/4 | 1/4 |
| 7.23 Riscos says it awaits the answer | 2/4 | 3/4 |
| 7.11 the +5 ms cost under a heading of its own | 3/4 | 2/4 |
| 7.19 no technology, team or stakeholder nobody named | 2/4 | 1/4 |
| all 24 checks of eval 71 | 81/96 | 85/96 |

Two splits in `pg` (7.23, 7.19), counted as not met. What fails 7.8: run-2 lists
"indisponibilidade do Redis, perda de chaves, janela de 24h" as the risks not yet
discussed, and run-4 gives the +5 ms a mitigation ("medir a latência real antes de
ampliar o tráfego") and names the Redis being down as an example. Run-1 and run-3 keep
Riscos to the accepted +5 ms and a pointer to Perguntas abertas.

Counting every document written with the skill invoked through the Skill tool, outside
the repository and with the prompt alone: iteration-27 0 of 4 met 7.8, `pa` 2 of 4,
`pn` 0 of 4, `pg` 2 of 4, so 4 of 16. The brief cell `a`, inside the repository, met it
in 4 of 4. The question of what separates them is still open, and the harness finding
above means the next cell has to put its projects under `$HOME`.

**Fifth batch, 2026-11-23: `pn` with the repository's AGENTS.md loaded** (`run_plugin.py`,
cell `pg2`, `plugin-batch-agents-md-home/`). `pg` with the projects under
`~/.cache/dd-pg2/`. A codeword probe in a project there, holding the repository's
AGENTS.md, named the file and the repo name it states, so it loads. All four runs invoked
`design-doc` through the Skill tool, none listed `unslop`, each wrote one document.

| Check | pn + pg (8 runs, no AGENTS.md) | pg2 (AGENTS.md loaded) | brief cell a |
|---|---|---|---|
| 7.8 Riscos states no risk nobody gave | 2/8 | 0/4 | 4/4 |
| 7.24 no such risk anywhere outside Perguntas abertas | 1/8 | 0/4 | |
| 7.6 asks the user for the risks | 6/8 | 1/4 | |
| 7.23 Riscos says it awaits the answer | 5/8 | 2/4 | |
| 7.19 no technology, team or stakeholder nobody named | 3/8 | 4/4 | |
| all 24 checks of eval 71 | 166/192 | 80/96 | |

Three splits (7.6 twice, 7.23 once), counted as not met. What fails 7.8: run-1 and run-4
list the Redis dependency and the 24-hour window as risks; run-2 names "indisponibilidade
do Redis, do próprio serviço, falha entre registrar a chave e publicar no Kafka" as the
risks not yet analysed; run-3 keeps Riscos to the +5 ms and a pointer, and fails on a
mitigation nobody gave ("medir a latência real no rollout"). That invented mitigation for
the +5 ms is in three of the four documents, and in documents of `pa`, `pn` and `pg` too:
it is the second form of the defect, next to listing the Redis and the window.

**Reading, by the rule in `checks.json`.** 0 of 4: AGENTS.md is not what keeps the brief
cells clean. What is left between them is the brief itself (it frames the task, hands the
skill as a file to read and follow rather than through the Skill tool, and asks for a
final reply) and the repository's own files in the tree. Counting every document written
with the skill invoked through the Skill tool: 4 of 20 keep Riscos clean.

**Sixth batch, 2026-11-23: a third candidate, in the self-review** (`run_plugin.py`, cell
`pd`, `skill-d`, `plugin-batch-pd/`). The transcripts put the risks in the first Write, so
the candidate is one bullet in step 4 and not a paragraph in step 2: it reads each section
the user gave no substance for line by line and deletes every risk, mitigation or example
the session supplied, naming the forms that leaked before (diff `skill-a/SKILL.md
skill-d/SKILL.md`). The `pn` setup, four runs on eval 71 and two on eval 7. All six
invoked `design-doc` through the Skill tool and none listed `unslop`.

| Check | pn setup (pn, pg, pg2: 12 runs) | pd (skill-d) |
|---|---|---|
| 7.8 Riscos states no risk nobody gave | 2/12 | 3/4 |
| 7.24 no such risk anywhere outside Perguntas abertas | 1/12 | 1/4 |
| 7.6 asks the user for the risks | 7/12 | 4/4 |
| 7.23 Riscos says it awaits the answer | 7/12 | 4/4 |
| 7.11 the +5 ms cost under a heading of its own | 8/12 | 2/4 |
| eval 7, 7.G1 the session wrote no file | 2/2 in pa | 1/2 |

Four splits (7.11 twice, 7.24 twice), counted as not met. The Riscos section is clean in
three of four, the best count of any cell with the skill invoked; the one miss is the
form the bullet names, "por exemplo, o comportamento diante de falhas do serviço ou do
Redis" inside the pending pointer. 7.24 shows where the rest went: run-3 points from
Proposta to "comportamento quando o Redis está indisponível" in Perguntas abertas (1 of 3
judges let it pass), run-1 writes in Proposta that "um reenvio depois dele não é coberto
por esta proposta", a deduction from the 24-hour window (2 of 3). And eval 7 run-2 wrote
the document on the plain request, with Riscos and Rollout pointing to its questions,
where the skill asks first.

**Reading, by the rule in `checks.json`.** Not adopted, on two counts: 7.8 at 3/4 with
7.24 at 1/4 is the defect moving again, as with skill-c, and eval 7 met 7.G1 in one of two
runs. Two runs do not show the bullet caused the second, but the bullet describes a
document with pointers to open questions, which is what that run wrote instead of asking.
What the batch adds: a check in the self-review moves the Riscos section more than either
paragraph in step 2. Open for the author: whether a pointer that names the topic of an
open question ("o comportamento quando o Redis está indisponível está em Perguntas
abertas") states a risk; 7.24 as written lets the judges split on it, as 7.19 did on a
name inside a question.

**Seventh batch, 2026-11-23: `pd` again, with 7.24 reworded and a control for asking
first** (`plugin-batch-pd2/`, `plugin-batch-pd2-control/`). By the author's decision, 7.24
now lets pass a sentence that names the subject of an open question and points there,
and still fails a subject called a risk (amendment in `checks.json`). Four more `pd` runs
on eval 71 (run-5 to run-8) and four on eval 7 (run-3 to run-6), and four `pn` runs on
eval 7 as a control, read from 7.G1 only. All twelve invoked `design-doc` through the
Skill tool and none listed `unslop`. Only the eval 71 runs went to the judges.

| Check | pd, this batch | pd, both batches | pn setup |
|---|---|---|---|
| eval 7, 7.G1 the session wrote no file | 1/4 | 2/6 | 4/4 (control) |
| 7.8 Riscos states no risk nobody gave | 2/4 | 5/8 | 2/12 |
| 7.24 (new text) | 2/4 | | |
| 7.6 asks the user for the risks | 4/4 | 8/8 | 7/12 |
| 7.11 the +5 ms cost under a heading of its own | 4/4 | 6/8 | 8/12 |

No splits. Both misses of 7.8 here are the pointer the bullet names: "Os demais riscos
(falhas do novo serviço e do Redis, por exemplo) ainda não foram levantados" (run-6) and
"(comportamento quando o Redis ou o serviço ficam indisponíveis, por exemplo)" (run-7);
pd run-4 of the first batch failed on the same form. Run-5 and run-8 meet all 24 checks.

**Reading, by the rule in `checks.json`.** Not adopted. The control decides the eval 7
question: without the bullet the session asked first in four of four, with it in two of
six, so the bullet is the likely cause of writing without asking. On eval 71 it cleans
Riscos more often than anything tried (5 of 8 against 2 of 12), and every miss left is
the same sentence, a "por exemplo" naming the Redis inside the pending pointer, which
the bullet forbids by name and the session writes anyway.

**Eighth batch, 2026-11-23: a fifth candidate, in contract 2** (cell `pe`, `skill-e`,
`plugin-batch-pe/`, `plugin-batch-pe-eval7/`). The rule moves out of the steps that
describe writing: one paragraph after the one on consequences defines a risk nobody
raised as invention, never a row, a mitigation, or an example inside a sentence about
what was not discussed (diff `skill-a/SKILL.md skill-e/SKILL.md`). It says nothing about
writing before the answers. The `pn` setup, four runs on eval 71 (judged, 7.24 as
reworded) and four on eval 7 (7.G1 only). All eight invoked `design-doc` through the
Skill tool and none listed `unslop`.

| Check | pn setup | pd (skill-d, 8 runs) | pe (skill-e) |
|---|---|---|---|
| eval 7, 7.G1 the session wrote no file | 4/4 (control) | 2/6 | 4/4 |
| 7.8 Riscos states no risk nobody gave | 2/12 | 5/8 | 4/4 |
| 7.24 no such risk outside Perguntas abertas | 1/12 (old text) | 2/4 (new text) | 3/4 |
| 7.6 asks the user for the risks | 7/12 | 8/8 | 4/4 |
| 7.11 the +5 ms cost under a heading of its own | 8/12 | 6/8 | 1/4 |
| all 24 checks of eval 71 | | | 92/96 |

One split (7.24 in run-2, 1 of 3). Run-1 meets all 24 checks. The three misses of 7.11
put the accepted +5 ms in Riscos (run-4, as a bold label), or in Proposta with a row in
Riscos (run-2, run-3); two were called borderline. No document has the "por exemplo"
pointer.

**Reading, by the rule in `checks.json`.** Not adopted, on 7.11 alone (1/4 against a floor
of 2). Every other condition is met, and on the defect this iteration is about it is the
best cell so far: Riscos clean in four of four and the plain request asked first in four
of four. Whether 7.11 at 1/4 is the paragraph's doing (it names "a mitigation for a cost
the team accepted", which may pull the cost toward Riscos) or four runs of noise against
8 of 12 is not known.

**Ninth batch, 2026-11-23: four more `pe` runs** (`plugin-batch-pe2/`, run-5 to run-8,
eval 71 only), to tell whether 7.11 at 1/4 was noise. All four invoked `design-doc`
through the Skill tool and none listed `unslop`. Two splits (7.24 in run-6, 7.22 in
run-7), counted as not met.

| Check | pe, first 4 | pe, these 4 | pe, all 8 | pn setup |
|---|---|---|---|---|
| 7.8 Riscos states no risk nobody gave | 4/4 | 4/4 | 8/8 | 2/12 |
| 7.24 no such risk outside Perguntas abertas | 3/4 | 3/4 | 6/8 | |
| 7.6 asks the user for the risks | 4/4 | 3/4 | 7/8 | 7/12 |
| 7.11 the +5 ms cost under a heading of its own | 1/4 | 2/4 | 3/8 | 8/12 |
| all 24 checks of eval 71 | 92/96 | 88/96 | 180/192 | |

**Reading, by the rule in `checks.json`.** Not adopted: 7.11 at 3 of 8 is the band the
rule called inconclusive. What the eight runs show is a trade. The defect this iteration
is about is gone in every document (7.8 8/8, against 2 of 12 without the paragraph), and
eval 7 asked first in four of four. The accepted +5 ms keeps its own heading in three of
eight, against eight of twelve: in the others it sits inside Riscos or Proposta, still
stated, under no heading of its own. Whether that loss is worth the gain is a decision
about the skill, not a measurement.

**Tenth batch, 2026-11-23: the same two cells on claude-opus-5-5** (`pn-opus`, `pe-opus`,
`plugin-batch-opus/`). The author's own sessions run on opus, and no executor of this
iteration or the last had. Four runs each on eval 71, judged together; all eight ran on
`claude-opus-5-5` (`models` in each `timing.json`), invoked `design-doc` through the
Skill tool and did not list `unslop`. Four splits (7.19 twice, 7.6, 7.22), counted as not
met. These are not the target model's numbers.

| Check | pn-opus (1.9.0) | pe-opus (skill-e) |
|---|---|---|
| 7.8 Riscos states no risk nobody gave | 1/4 | 4/4 |
| 7.24 no such risk outside Perguntas abertas | 0/4 | 4/4 |
| 7.11 the +5 ms cost under a heading of its own | 4/4 | 4/4 |
| 7.6 asks the user for the risks | 3/4 | 4/4 |
| 7.5 no heading from the default catalog | 4/4 | 2/4 |
| 7.19 no technology, team or stakeholder nobody named | 0/4 | 1/4 |
| all 24 checks of eval 71 | 84/96 | 90/96 |

**Reading, by the rule in `checks.json`.** The defect shows on opus: 7.8 in one of four
with 1.9.0, as on sonnet. skill-e removes it there too (7.8 and 7.24 four of four), and on
opus the accepted +5 ms keeps its own heading in every run of both cells, so the trade
seen on sonnet does not appear. Two misses are new and are not about risks: two pe-opus
documents put a `### Visão geral` subheading inside Proposta, under the template's own
structure, which 7.5 forbids at any level. 7.19 fails in both cells on a team named
inside an open question ("o time dono do Kafka e do Redis"), the case the 7.19 amendment
of 2026-11-22 lets pass; it does not separate the cells. Eval 7 was not run on opus.

**Reading of the first two batches, by the rule in `checks.json`.** Neither paragraph is adopted and the skill is
not edited.

- **The defect is real, partial, and tied to the harness.** With the skill installed and
  invoked, two of four 1.9.0 documents put a Redis dependency and the 24-hour window into
  Riscos as risks with a pending mitigation; iteration-27 had four of four in a similar
  setup. Told to read the same text from a brief, zero of four did. Nothing in this
  iteration says why the two harnesses differ. `unslop` ran only in the second, and the
  third batch rules it out: without it the defect shows in four of four.
- **The second paragraph does not fix it.** 7.8 moves by one run (3/4 against 2/4), which
  is not a finding. 7.24, the check for the same risk moved elsewhere, stays at 1/4:
  the Riscos section gets cleaner and the risk reappears as a clause in Proposta ("um
  reenvio que chegue depois de 24 horas não é reconhecido como repetido") or as an
  example inside the pending marker ("outros riscos, como a indisponibilidade do Redis").
  That is contract 2's inference by consequence, and the sentence that bars it did not
  hold.
- **It has a cost.** With the paragraph, the +5 ms the user accepted loses its own
  heading in three of four documents and lands in Proposta or Riscos (7.11, 1/4 against
  3/4), which the rule counts against the candidate.
- **It keeps the ask-first behaviour** (eval 7, 2/2 in both cells), which the first
  paragraph broke. The wording that did that was "nobody is there to reply": do not put
  it in the skill.
- **7.19** fails mostly on a list of impacted areas that the document offers inside a
  question ("financeiro, donos dos produtores, infraestrutura do Redis e do Kafka"). The
  check has no exemption for questions, so it measures something next to what it was
  written for, in both cells.

**Limits.** Four runs per cell measure no rate. One eval, in Portuguese, one way of
saying "I cannot answer now". The first batch ran inside the repository (its `AGENTS.md`
loads) and without `unslop`; the second outside it and with `unslop`, so the two batches
differ in more than how the skill is reached. In the second batch every reply that wrote
a document may name `unslop`, in both cells alike. 7.23 and 7.24 are new checks, not
tried on an older output. The third batch is one cell of four runs, judged a day after the
`pa` runs it is set against, and 2/4 against 0/4 is no difference between the cells: it
says the defect does not need `unslop`, not that `unslop` lowers its rate. Still open is
what separates the brief from the invoked skill: the first batch ran inside the repository
with a brief that frames the task and asks for a final reply, the other two outside it
with the prompt alone.

**Cost.** Executors: 24 sessions, US$ 2.57. Judges: 72 calls, US$ 4.06. Third batch:
4 sessions, US$ 0.38; 12 judge calls, US$ 0.95. Fourth batch: 4 sessions, US$ 0.50;
12 judge calls, US$ 1.21; four codeword probes on haiku, a few cents. Fifth batch:
4 sessions, US$ 0.54; 12 judge calls, US$ 1.05; one probe. Sixth batch: 6 sessions,
US$ 0.79; 18 judge calls, US$ 1.15. Seventh batch: 12 sessions, US$ 1.49; 12 judge
calls, US$ 1.13. Eighth batch: 8 sessions, US$ 0.95; 12 judge calls, US$ 1.23.
Ninth batch: 4 sessions, US$ 0.58; 12 judge calls, US$ 1.11.
Tenth batch: 8 sessions on opus, US$ 3.29; 24 judge calls, US$ 2.23.
