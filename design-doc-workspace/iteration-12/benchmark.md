# iteration-12 — full eval set against 1.3.1

**Question.** Iterations 10 and 11 left the set half-measured: 10 failed one assertion, 11
re-ran only that eval. Does the full set hold against 1.3.1?

**Method.** All six evals, one `with_skill` run each, against the working-tree skill. Both
MCP servers (Structurizr, hosted Mermaid) connected and Docker available, except eval 6,
whose prompt declares a degraded machine and whose run was held to it (no MCP calls, no
Docker, no installs). Grading by an independent agent that diffed produced docs against the
seeded fixtures.

## Result — 42/42 under the old assertions, **43/46** under the corrected ones

The first pass scored a clean 42/42 — and that clean score was the finding, because the
grader simultaneously reported three "record, don't invent" leaks that no assertion covered.
A generic invention assertion was added to evals 1, 3 and 4 (plus a template-extensibility
assertion on eval 4), and a second independent grader re-scored the *same outputs* against
the corrected set: **43/46**. The three new failures are exactly the three leaks. The set
now discriminates.

| Eval | Old | Corrected | Tokens |
|---|---|---|---|
| 1 rich-write-new-doc | 9/9 | **9/10** | 79,537 |
| 2 vague-write-asks-questions | 4/4 | 4/4 | 31,014 |
| 3 review-flawed-doc | 10/10 | **10/11** | 57,781 |
| 4 house-template-repo | 7/7 | **8/9** | 57,462 |
| 5 template-gaps-asks-to-fill | 5/5 | 5/5 | 34,518 |
| 6 no-renderer-keeps-placeholder-no-disclaimer | 7/7 | 7/7 | 63,081 |

Total 323,393 tokens, mean 53,898 — the most expensive of the three skills, driven by the
diagram-authoring path (eval 1 alone used 79k across 24 tool calls, validating DSL through
the Structurizr MCP and rendering PNG through Docker).

## The score was clean; the outputs were not

A 100% pass rate here meant the assertion set had stopped discriminating, not that the skill
was finished. The grader found three "record, don't invent" leaks that no assertion covered —
all of them on the **diagram-authoring path**, which is where the pressure to invent lives:
Structurizr's `container` syntax has a technology slot, and a model filling that slot will
guess rather than leave it empty.

- **eval 3 — invented a database.** The review inserted
  `banco = container "Banco de notificações" … "PostgreSQL" "Database"` into a document whose
  original never names any database (`grep -rin postgres` over the fixture: no hit). This is
  the clearest defect found in the whole run: a *review* that adds a technology choice the
  author never made.
- **eval 1 — invented protocols.** Relationship technologies `AMQP` and `HTTPS` were added;
  the user named RabbitMQ and S3 but never a protocol. Milder — they follow mechanically —
  but still unsourced.
- **eval 4 — an unsupported exclusivity claim.** "O Redis usado hoje para sessão é a única
  infraestrutura de contadores rápidos já disponível no caminho do gateway". The "única" is
  the run's inference.

None cost a point at first, because eval 1's invention assertion was scoped to *metrics*,
eval 3's to *cons, alternatives and metrics*, and eval 4 had no invention assertion at all.
Under the corrected set all three fail, and the re-grader added a fourth instance in the same
family: eval 4's `cliente -> gateway "Chama a API pública com um token de API" "HTTPS"` — TLS
is nowhere in the prompt and is never raised as a question.

The re-grader also sharpened the eval 3 diagnosis: the broker in that same diagram *was*
left generic ("Broker de mensageria") and the reply does ask about "escolha do broker". So
the datastore leak is not a blanket habit of naming everything — it is a targeted slip on
one slot, which is what makes it worth a rule rather than a scolding.

## Settled: a governing template is a floor, not a ceiling

**eval 4** added `## Objetivos` and `## Alternativas consideradas`, which the house template
DD-2026-007 does not have. The old assertion was silent on whether that is allowed. It is now
decided in favour of the observed behavior — extending is fine when the user supplied the
substance, the house skeleton and order survive, and the reply says it stepped outside — and
1.3.2 writes that into SKILL.md rule 3 with a matching assertion on eval 4. The re-grader
checked all three conditions and passed it, quoting the reply: "Duas seções a mais que o
DD-2026-007 não tem… é só me dizer que eu dobro as duas."

## Assertions worth rewording

- **eval 3, "the mermaid diagram is now followed by explanatory text"** — the run replaced
  the author's Mermaid flowchart with a Structurizr C4 diagram per the 1.1.0 convention, so
  there is no mermaid block left to follow. Graded on intent (no orphan diagram) and passed,
  but as written it will read as a false pass forever. Reword to "the architecture diagram".
- **eval 3, "out-of-scope items are no longer mere negations of goals"** — the document's
  `## Fora de escopo` is untouched; only the reply raises it as a question. The "or turned
  into a question" escape hatch makes it a pass, but the phrasing implies an edit that never
  happened.
