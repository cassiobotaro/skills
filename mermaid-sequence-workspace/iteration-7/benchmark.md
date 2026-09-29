# Skill Benchmark: mermaid-sequence

**Model**: <model-name>
**Date**: 2026-09-28T23:48:35Z
**Evals**: 1 (3 runs each per configuration)

## Summary

| Metric | Old Skill | With Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 93.0s ± 0.0s | 90.6s ± 0.0s | +2.4s |
| Tokens | 51743 ± 0 | 50333 ± 0 | +1410 |
**Method.** Token-economy pass, 1.2.0 → 1.2.1: contract 5 reduced to a pointer at step 5,
the step-5 closing paragraph folded into the hand-off bullet, Podman/ghcr lines condensed,
and the side-by-side ASCII block table in `references/syntax.md` §Blocks replaced by a
one-line-per-block list. Eval 1, one run per arm, `old_skill/` = snapshot 1.2.0,
`with_skill/` = working tree. Both 6/6; the grader re-rendered both blocks with the
mermaid-cli Docker image (exit 0). Body −231 chars, `syntax.md` −503 chars (≈−180 tok
per invocation). n = 1 per arm: the end-to-end delta is not a measurement.
