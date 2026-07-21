# iteration-13 — targeted verification of the 1.3.2 never-invent fix

**Scope.** Not a full set. Iteration-12 scored 42/42 on the assertions but the grader found
three "record, don't invent" leaks that no assertion covered, all of them on the
diagram-authoring path. 1.3.2 adds "A diagram is not a licence to invent" to
`references/diagrams.md` and a clause to SKILL.md rule 2. This run re-executes the two evals
that leaked and diffs the DSL against iteration-12.

**Method.** One `with_skill` run each of evals 1 and 3 against the working-tree skill, both
MCP servers connected and Docker available — the same environment iteration-12 had, so the
DSL is comparable. Both runs were then scored by an independent grader against the corrected
assertion sets, and iteration-12's outputs were re-scored against those same sets, so the two
versions are measured with one yardstick.

## Result — 21/21, against 19/21 for 1.3.1 on the same two evals

| Eval | 1.3.1 (iteration-12) | 1.3.2 (iteration-13) |
|---|---|---|
| 1 rich-write-new-doc | 9/10 | **10/10** |
| 3 review-flawed-doc | 10/11 | **11/11** |

The single failure in each case was the invention assertion, and it is the assertion that now
passes. Across the full six-eval set 1.3.1 scores 43/46; the three failures are all invented
technology inside a diagram.

## Result — both leaks closed

**eval 1 — invented protocols are gone.**

| | 1.3.1 (iteration-12) | 1.3.2 (iteration-13) |
|---|---|---|
| relationship technologies | `"HTTPS"` ×4, `"AMQP"` ×2 — all six arrows | none; every slot omitted |
| container technologies | `"RabbitMQ"`, `"Amazon S3"` | `"RabbitMQ"`, `"Amazon S3"` |

The user named RabbitMQ and S3, so those stay. They never named a protocol, so the arrows now
carry a description and nothing else. The run reported leaving the API, worker and e-mail
service technologies empty deliberately and routing them to open questions.

**eval 3 — the invented database is gone.**

Iteration-12 wrote, into a document whose original never names a datastore:

```
banco = container "Banco de notificações" "Tabela notifications, …" "PostgreSQL" "Database"
```

Iteration-13 writes:

```
tabela = container "Tabela notifications" "Notificações de domínio gravadas pelo serviço de mensageria." {
    tags "Database"
}
```

`grep -n "PostgreSQL"` over the produced document: no match. The remaining `"Database"` is a
**tag**, used for styling and C4 classification — it asserts that the element is a datastore,
which the author's own text established, not which product it runs on. That distinction is
exactly the line 1.3.2 draws. The run also added "unstated technologies" to the questions it
put back to the author.

The grader's own verdict: "the 1.3.2 fix holds — unstated technology slots are left empty and
surfaced as questions in both the write and the review path, with no residual invention in
DSL, Mermaid, SVG or prose." It confirmed the runs say so out loud rather than silently
omitting: eval 1's doc reads "Duas caixas do diagrama estão sem tecnologia de propósito… (ver
Questões em aberto)", and eval 3's question 7 raises its three blanks.

## What this run does not establish

- **Two runs, one each.** The fix is visible in both the write path and the review path,
  which are the two shapes that matter, but this is not a variance measurement — one sample
  per eval.
- **Eval 4 was not re-run.** It carries two of 1.3.1's failures: the `"HTTPS"` relationship
  label (same family as eval 1, so the fix plausibly covers it) and "a única infraestrutura
  de contadores rápidos", an unsupported exclusivity claim in *prose* rather than in a
  diagram. That second one is a different failure mode, and nothing in 1.3.2 targets it —
  the new generic invention assertion is what should catch it, but it has not yet been
  measured against a 1.3.2 run.
- The other four evals were not re-run at 1.3.2 either; they passed unchanged at 1.3.1 under
  the corrected set.

Tokens: eval 1 86,965; eval 3 58,824.
