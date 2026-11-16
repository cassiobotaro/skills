# iteration-25 — pilot: a governing template with many required sections (design-doc 1.5.3, no skill change)

**Question.** `SKILL.md` asks for "one question per template section the conversation
hasn't filled" and, a paragraph earlier, for "2–5 targeted questions". Read against a
Hazelcast-shaped template the two collide. Hypothesis: the reply becomes a flat
interrogation, one undifferentiated question per empty section, or the empty sections get
boilerplate. Checked before any edit, as in iteration-24.

**Method.** One arm: the working tree, 1.5.3, unchanged. New fixture
`../evals/files/large-template/docs/design/TEMPLATE.md`: 11 header rows, 18 headings,
none marked optional. The prompt is eval 7's, word for word; it leaves 7 sections and 6
header rows with no substance (listed in `checks.json`, frozen before the first run).
Four runs in one batch, executor alias `sonnet` (id not read back from the transcripts).
File checks by `grade.py` (`script-checks.json`); reading checks by the session that ran
the pilot, one reader, not blind. Not added to `evals.json` or `checks-baseline.json`.

**Results.**

| Check | 1.5.3 |
|---|---|
| O.0 a document was written | 4/4 |
| 12.1 template untouched, one new doc | 4/4 |
| 12.2 template headings present, in order | 18/18 in all four |
| O.6 row or heading silently dropped | 0 |
| O.1 empty section kept in the document | 28/28 |
| O.2 body of those 28: boilerplate filling the section | 0/28 |
| O.3 questions in the reply | 9, 12, 10, 10 |
| O.4 empty sections the user is asked about (of 7) | 5, 7, 6, 6 |
| O.5 substance questions set apart from template-filling ones | 1/4 (run-3) |

- **Bodies (O.2).** Every one of the 28 is a pending marker pointing at a question, or
  the question itself. Eight carry one more sentence. Most derive a metric or acceptance
  criterion from the stated 0,1% goal, hedged. Two assert something nobody said, both in
  run-1: "Os consumidores do Kafka não mudam" and "Nenhum protótipo existe até aqui".
- **Header.** The six empty rows stay in the table, blank or "A preencher", and all four
  runs fold them into a single question.
- **Questions (O.3, O.5).** No run asks one question per empty item (13 items, 9 to 12
  questions, header rows always grouped). Run-2 is the flat case: twelve items in
  template order, header administration first, "what if Redis is down" eighth. Run-3
  groups all template-filling sections into one item and names two "perguntas de
  substância" apart. Runs 1 and 4 lead with substance without saying so.

**Reading.** The hypothesis holds only in its mildest form. No boilerplate, nothing
dropped, and the document is written rather than held back for an interview: contract 3
works on a large template. What exceeds the text is the count, 9 to 12 against "2–5", and
in one run of four the order buries the design questions under form-filling. Whether that
is a defect is a judgment: with 13 required items empty and a user who said "à risca",
ten grouped questions recorded in the document may be the right answer. A sentence asking
for substance questions first and template-filling grouped after would be cheap, but four
runs cannot show it helps.

**Limits.** Four runs measure no rate. One executor model. The brief told the executor
the user could not answer in this turn, which pushes toward writing the document instead
of asking first; O.0 is therefore not evidence about a live conversation. The invention
slips (run-1 above; run-2 states in 2.2 that a retry after 24h "passa como evento novo")
are the residual already tracked in iterations 21–23, not something this template caused,
as far as four runs can tell.

**Cost.** Executors 4 × ~62 k = 0.25 M tokens. No judge calls.
