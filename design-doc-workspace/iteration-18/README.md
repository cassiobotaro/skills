# iteration-18 — coverage evals 7 and 8 against the shipped skill (1.4.2)

**Question.** Two gaps in the eval set had never been exercised: a user-supplied template that
*governs* (contract 3) and a single already-made decision that is not a design (contract 5).
Do the shipped instructions already produce the right behaviour, so the new evals start green?
Single arm, `with_skill` = working tree (1.4.2), one run per eval, no baseline: the purpose is
to validate the specs, not to A/B a change. Graded by a subagent following `agents/grader.md`;
DSL and Mermaid blocks re-validated by the grader through the Docker images.

| Eval | Result | What happened |
|---|---|---|
| 7 user template governs (new fixture `files/template/`) | 7/7 | All six template sections, in order; Riscos and Plano de rollout left as pending markers with one question each; alternatives and the +5 ms cost under dedicated H3s inside Proposta, deviation named to the user; C4 DSL validated and rendered to SVG; 0 em dashes |
| 8 single decision, English | 4/4 | No file written; says a settled Terraform-vs-Pulumi choice is an ADR, not a design doc; offers the adjacent real design (module layout, state, CI apply) as the doc worth writing |

Tokens: eval 7 89,128 (278 s), eval 8 49,319 (60 s).

**Spec changes made from the grader's feedback** (applied to `evals/evals.json`, not to the
`eval_metadata.json` files, which record what was graded): eval 7's "section of their own" now
says a dedicated heading at any level with the template's top-level skeleton intact, and gains a
diagram assertion (DSL validates, technology slots only for Redis/Kafka, no invented Mermaid
detail); eval 8's fabrication assertion distinguishes *asking* about OpenTofu from *asserting* it.
Not adopted: enforcing a 2–4 question cap on eval 7 — a governing template asks one question per
unfilled section on top of the essentials, so five is the contract, not a violation.
