# iteration-10 — scope and ADR-boundary evals 10–12 against the shipped skill (1.6.2)

**Question.** The "Check the scope first" section and the step-5 ADR boundary had never been
exercised by a behaviour eval (only by trigger negatives). Three new evals: a vendor-icon AWS
picture (10, English), "write ADR 0004 and link the ADRs" on the legacy-billing fixture (11),
and a checkout sequence with a declined-payment branch (12). Single arm, `with_skill` = working
tree, one run per eval, no baseline: the purpose is to validate the specs. Graded by a subagent
following `agents/grader.md`; `validate`/`inspect` and the Mermaid block re-run by the grader.

| Eval | Result | What happened |
|---|---|---|
| 10 AWS icons | 5/5 | No `.dsl`; one-paragraph scope statement; names draw.io / `diagrams` / the icon pack; offers a C4 deployment view conditionally, not built |
| 11 ADR authoring + link | 6/6 | Diff against the fixture is exactly `!adrs docs/adr` (+ comment); `docs/adr` byte-identical, no 0004 written; routes authoring to `adr new -s 3`; asks whether the model should show Kafka now or after the migration; `validate` clean, `inspect` findings reported, not silenced |
| 12 checkout sequence | 5/5 | No `.dsl`; says a dynamic view cannot express the declined branch; delivers the Mermaid sequence itself (validated) and leaves the declined-payment aftermath as questions |

Tokens: 48,274 (49 s), 60,836 (115 s), 62,738 (146 s).

**Spec changes made from the grader's feedback** (in `evals/evals.json`): eval 10 drops the
non-discriminating "replies in English"; eval 11 names the fixture's English ADR headings and
tells the grader to re-run `validate` from `outputs/`; eval 12 states that reply arrows on the
named calls are fine while endpoints/status codes/aftermath are not, and gains a "never claims a
validation that did not run" assertion.
