# Skill Benchmark: structurizr

**Model**: <model-name>
**Date**: 2026-09-28T23:48:35Z
**Evals**: 2, 3 (3 runs each per configuration)

## Summary

| Metric | Old Skill | With Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 179.2s ± 25.2s | 185.6s ± 9.9s | -6.4s |
| Tokens | 72869 ± 6979 | 69418 ± 3768 | +3452 |
**Method.** Token-economy pass, 1.5.1 → 1.5.2: the self-review checklist moved from
`references/diagrams.md` into SKILL.md step 7 (so `diagrams.md` is no longer read on every
run), the "Why these conventions" list left `dsl-reference.md` §15 (SKILL.md step 4 keeps
it), rare options (terminology, animation, healthCheck, server-only configuration) moved to
`dsl-advanced.md` §6, and the scope table became a paragraph. Evals 2 and 3, one run per
arm, `old_skill/` = snapshot 1.5.1, `with_skill/` = working tree. Both arms 12/12; both
validated through the `structurizr/structurizr` Docker image with a negative control.
Reference files read (from the executors' reports): old arm read `diagrams.md` in both
evals; new arm read it in neither. Always-read reference size: `dsl-reference.md`
−1,443 chars (≈−360 tok); `diagrams.md` no longer read (≈−1,340 tok). n = 1 per arm: the
end-to-end token delta (−3.4k mean) is directional, not a measurement.
