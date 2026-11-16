# iteration-24 — pilot: template sections the template itself marks as dispensable (design-doc 1.5.3, no skill change)

**Question.** Contract 3 says a governing template's sections are all required and an
unfilled one is a question to the user. Read against real templates that mark sections
`optional` or "delete if X" (RabbitMQ, FoundationDB, Magento, from designdocs.dev), that
text predicts the skill would keep such sections and demand content for them. A rule
exempting them was proposed. This pilot checks the prediction before any edit.

**Method.** One arm: the working tree, 1.5.3, unchanged. New fixture
`../evals/files/optional-template/docs/design/TEMPLATE.md`: the eval-7 template plus two
sections marked `*(opcional)*` with no substance in the prompt (Histórias de usuário,
Plano de rollout), two conditional ones whose condition the prompt does not establish
(Critérios de aceite, Estratégia de migração), and one optional section the prompt does
fill (Métricas de sucesso). The prompt is eval 7's, word for word, including "segue ele à
risca". Four runs in one batch, executor alias `sonnet` (the transcripts hold the id; it
was not read back here). `checks.json` was frozen before the first run. File checks by
`grade.py` (`script-checks.json`); reading checks by the session that ran the pilot, one
reader, not blind (there is one arm). Not added to `evals.json` or `checks-baseline.json`.

**Results** (runs / runs, or sections / sections).

| Check | 1.5.3 |
|---|---|
| 11.1 one new doc, template untouched | 4/4 |
| 11.2 required headings present, in order | 4/4 |
| 11.3 Métricas de sucesso present with the 0,1% target | 4/4 |
| 11.4 Riscos (required, not given) asked of the user | 4/4 |
| O.1 dispensable section without substance kept in the document | 0/16 |
| O.3 placeholder or invented body in such a section | 0/16 (none present) |
| O.4 reply names the sections left out | 4/4 |
| O.2 user asked about a dispensable section | 9/16 |

O.2 by section: Plano de rollout 4/4, Critérios de aceite 3/4, Estratégia de migração
2/4, Histórias de usuário 0/4. Every question sits in Perguntas abertas or the reply as
"does this apply?", never as a blocking demand, and never as a kept heading.

**Reading.** The prediction was wrong. On this fixture the skill already omits every
dispensable section it has nothing for and says which ones it left out, in all four
runs. The proposed rule would change one thing only, the 9 questions, and those are
mostly defensible: a conditional section hangs on a fact the user did not give, so
asking is the "record, don't invent" answer. The one run that did not ask about migration
asserted the condition instead: its reply says "não há dados existentes a migrar", which
nobody said (run-2). A rule of "no question for a dispensable section" pushes toward
that. Rollout is asked 4/4 because the catalog's own deployment question applies to a new
hop on a critical path, template or not.

**Limits.** Four runs measure no rate (AGENTS.md). One executor model; a weaker one may
keep the headings. One fixture, with explicit markings and a prompt full of substance;
"segue ele à risca" did not make the runs keep the sections, which is the harder
direction. Unrelated to the question, run-4's Riscos table lists a risk the user did not
state (retries after 24h); it was not graded here.

**Cost.** Executors 4 × ~58 k = 0.23 M tokens. No judge calls.
