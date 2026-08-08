# iteration-15 — 1.3.4 against the full set: generalizing rule 2 and cutting what `sections.md` already says

**Why this run exists.** Two things needed measuring, and one of them was overdue.

1. **1.3.4 generalizes contract 2's superlative list.** 1.3.3 closed the inference-by-exclusivity
   failure (mode b) by naming the offending words — but it named them *only in Portuguese*
   (`"a única alternativa"`, `"o único freio disponível"`, `"sempre"`, `"nunca"`), inside a skill
   body the repo keeps in English, for a skill that writes in whatever language the conversation
   uses. That is an eval-shaped fix, not a rule. 1.3.4 replaces the literal list with the class —
   words claiming exclusivity or universality, *in whatever language the document is written in* —
   and keeps the WAF worked example, which carries the reasoning and was already language-neutral.
   **The risk this run measures: does the rule still fire without its Portuguese crutch?**
2. **A redundancy cut.** Three bullets in step 3 ("Write") and the glossary item in step 4
   ("Self-review") restated `references/sections.md` nearly word for word — measurable goals,
   which API fragments to show, the glossary's two exclusions — in a file the skill already reads
   before writing its first doc. Those became pointers.
3. **1.3.3 had only ever been measured on eval 4** (iteration-14). The other five ran at 1.3.1/1.3.2.
   This is the first full-set run since.

**Method.** All six evals, one `with_skill` run each, against the working-tree skill. No baseline:
the comparison is the recorded scores at 1.3.1–1.3.3 under the same assertions. Grading combined
a mechanical script (`check_mechanical.py`, committed alongside) with file-level inspection. The
script owns the exclusivity sweep, the banned-disclaimer sweep, the diagram/orphan accounting and
the language markers; every exclusivity hit was then adjudicated by hand, since the term list
catches restatements as readily as inferences.

## Result — 46/46 (100%), no failures

| Eval | Passed | Tokens |
|---|---|---|
| 1 rich-write-new-doc | 10/10 | 81,584 |
| 2 vague-write-asks-questions | 4/4 | 33,743 |
| 3 review-flawed-doc | 11/11 | 59,597 |
| 4 house-template-repo | 9/9 | 41,432 |
| 5 template-gaps-asks-to-fill | 5/5 | 35,944 |
| 6 no-renderer-keeps-placeholder | 7/7 | 72,324 |

Total 324,624 tokens over six runs, mean 54,104.

Eval 6's first attempt was killed mid-task by an account spend limit, after writing the document
and before the sequence diagram. It was re-seeded (the partial output deleted) and re-run from
scratch; the numbers above are the complete run. Its seven assertions all hold: the C4
architecture is Structurizr DSL folded in a `<details>` block under an image reference that stays
a **placeholder** (no `diagrams/` file was generated and none was faked), the retry flow is a
fenced ` ```mermaid ` sequence diagram, no validation disclaimer appears anywhere in the document,
neither diagram is orphaned, and nothing was installed — the run honored the stated absence of
Docker even though a `docker` binary sat on the PATH.

## The exclusivity sweep — what the generalization actually bought

Hits are not failures; each was adjudicated. What matters is whether any hit *infers an absence
nobody stated*, which is the failure 1.3.3 closed and 1.3.4 had to keep closed while losing its
Portuguese wording.

| Eval | Hits in the produced document | Verdict |
|---|---|---|
| 3 review-flawed-doc | 0 | — |
| **4 house-template-repo** | **0** | the decisive one (below) |
| 1 rich-write-new-doc | 3 | all restatements |
| 6 no-renderer-keeps-placeholder | 9 | all restatements |

**Eval 4 is the one that matters.** It is where mode (b) failed at 1.3.1 (*"o Redis … é a única
infraestrutura de contadores rápidos"*) and failed again, reworded, at 1.3.2 (*"o único freio
disponível durante o incidente foi a intervenção manual"*). At 1.3.4, with the Portuguese literals
gone from the rule, the document contains **zero** exclusivity constructions — down even from the
six restatement-hits 1.3.3 produced. The run also stepped around the planted NAT trap (`0`
mentions of NAT or shared IP in the document) and reported having deleted a draft `✓` bullet
about "per token, not per IP" for re-smuggling the retracted false positive in as a selling
point. The rule survived losing its examples.

The remaining hits are the kind the rule is *not* aimed at, and every one was adjudicated
individually. Eval 1's *"um caminho único de exportação"* is the user's own words (*"pra ter um
caminho só"*) describing the design's chosen property. Eval 6's nine break down the same way:
*"um serviço único"* and *"nenhum evento perdido"* are quoted straight from the prompt,
*"passam a apenas publicar o evento"* describes the proposed design's own behaviour, and
*"Nenhum dos dois objetivos é atendido"* judges the "do nothing" alternative against the two
goals the document itself states — verifiable from the page, not inferred about the world. None
rules out an unmentioned alternative. That is exactly the distinction contract 2 asks the model
to make, and it is being made without a word list to lean on.

## What the redundancy cut did and did not cost

`SKILL.md` body 17,160 → 16,503 chars (**−657, −3.8%**, ≈−164 tokens); 270 → 260 lines. Smaller
than the `adr` 1.2.2 cut (−7.5%), and that is the honest number: `adr`'s case was one paragraph
re-argued in eight places, while `design-doc` mostly duplicated a *reference file* rather than
itself. Forcing the cut further would have meant removing rules, not repetition.

The two properties most exposed by the cut both held:

- **Measurable goals** survived losing their step-3 bullet. Eval 2 asked for them unprompted
  ("de preferência com número", with three worked examples); eval 3 flagged the document's
  unmeasurable SLA and asked the author for the figure instead of inventing one. Discovery step 2
  and `references/sections.md` were carrying that weight all along.
- **The glossary's two exclusions** survived compression to a pointer — the highest-risk edit,
  since eval 1's assertion names them explicitly. Eval 1's glossary is `PII`, `Link assinado`,
  `XLSX`, `BI`, `Job de exportação`: zero universally-known terms (no API/HTTP/URL/JSON) and zero
  authoring-tooling terms (no C4/DSL/Structurizr), in a document that folds Structurizr DSL into
  a `<details>` block and therefore had every opportunity to leak one. Eval 3's added glossary
  covers all four terms the assertion demands (CDC, DLQ, SLA, TPS).

## Other findings

- **Never-invent inside the notation held everywhere.** Eval 1's DSL gives a technology only to
  `RabbitMQ` and `Amazon S3` — both named by the user — and leaves the API and worker containers'
  technology slots empty, raising them as open questions. Eval 6's gives one only to
  `PostgreSQL`, leaving the delivery service and the DLQ blank. Eval 3, reviewing someone else's
  document, wrote **every** container with an empty technology slot. No protocol appears on any
  relationship label in any of the three.
- **The template-governs contract held in both directions.** Eval 4 reproduced the house skeleton
  in order (Resumo → Contexto → Proposta/Compensações → Riscos → Plano de entrega), continued the
  ID sequence to `DD-2026-008`, and added `Objetivos` and `Alternativas consideradas` only for
  substance the user supplied — telling the user it stepped outside the pattern. Eval 5, given a
  prompt with no cons, no risks and no delivery plan, wrote **no file at all** and returned one
  question per unfilled house section.
- **Zero orphan diagrams and zero validation disclaimers** across every produced document.
- **Review preserved the author's shape.** Eval 3's edited document still carries the author's own
  headings (`Solução`, `Plano`, `Fora de escopo`) rather than the skill's catalog names, with the
  header date refreshed to the real `2026-08-07` and the vague "mais escalável / mais fácil de
  manter" justification removed.

## Scope

Six evals, one run each — this is a regression gate, not a variance measurement. Wall clock is
omitted: five of the runs executed concurrently with two `claude -p` trigger-eval sweeps, so it
carries queueing delay. Tokens are the comparable figure.

Still unmeasured elsewhere in this sweep: the `structurizr` 1.2.1 and `adr` 1.2.3 reference-file
indexes shipped without a regression run of their own (navigational changes, low risk but
untested), and the `adr` description A/B — shipped text versus the recorded `best_description` on
the same full trigger set — has not run. See the two `trigger-evals/README-current.md` files.
