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

**Reading, by the rule in `checks.json`.** Neither paragraph is adopted and the skill is
not edited.

- **The defect is real, partial, and tied to the harness.** With the skill installed and
  invoked, two of four 1.9.0 documents put a Redis dependency and the 24-hour window into
  Riscos as risks with a pending mitigation; iteration-27 had four of four in a similar
  setup. Told to read the same text from a brief, zero of four did. Nothing in this
  iteration says why the two harnesses differ; `unslop` runs only in the second.
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
tried on an older output.

**Cost.** Executors: 24 sessions, US$ 2.57. Judges: 72 calls, US$ 4.06.
