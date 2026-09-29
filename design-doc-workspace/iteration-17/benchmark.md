# Skill Benchmark: design-doc

**Model**: <model-name>
**Date**: 2026-09-28T23:51:55Z
**Evals**: 1, 3 (3 runs each per configuration)

## Summary

| Metric | Old Skill | With Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 842.6s ± 107.6s | 750.9s ± 187.8s | +91.8s |
| Tokens | 91813 ± 28259 | 87300 ± 29496 | +4513 |
**Method.** Token-economy pass, 1.4.0 → 1.4.1: intro and contracts 2–3 tightened without
dropping a rule (the inference paragraph halved, the typography sweep and glossary bullets
in self-review now point at their source instead of restating it), and
`references/diagrams.md` no longer recommends the deprecated Structurizr Lite UI (it names
the `structurizr/structurizr` image and defers to the structurizr skill's hand-off). Evals 1
and 3, one run per arm, `old_skill/` = snapshot 1.4.0, `with_skill/` = working tree. Both
arms 21/21. Grader notes outside the assertions: in eval 3 the old arm deleted an author
sentence (disclosed) while the new arm left it as a question; in eval 1 the old arm stated
the S3 upload streams (not in the prompt) while the new arm flagged its one inference. The
two eval-1 runs shared a scratch directory while rendering; the grader confirmed each SVG
carries its own DSL's names. Body −882 chars (≈−220 tok). n = 1 per arm.
