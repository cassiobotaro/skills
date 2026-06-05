# Skill Benchmark: structurizr

**Model**: claude-opus-4-8[1m]
**Date**: 2026-06-04T18:07:07Z
**Evals**: 1, 2, 3, 4 (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 96% ± 8% | 69% ± 17% | +0.27 |
| Time | 105.0s ± 11.8s | 76.7s ± 12.9s | +28.3s |
| Tokens | 34570 ± 1042 | 13450 ± 2475 | +21120 |

## Notes

- Eval 3 ('validates cleanly') fails in BOTH configurations — both runs hit the identical hierarchical-identifier trap: identifiers defined inside nested deployment nodes ('alb', 'portalInstance') were referenced bare and are unreachable under !identifiers hierarchical. This is the single biggest correctness gap and it is skill-addressable (bind identifiers to ancestor deployment nodes, reference full dotted paths).
- 'Asks clarifying questions' (eval 1) passes in both configurations — the baseline also asks good questions. What actually discriminates is inventing-while-asking: the baseline put speculative stacks in a technology field ('ex.: Java/Spring, Node') and invented an actor ('Time de Pagamentos'); the with-skill run kept unknown technologies generic and asked.
- Tooling currency fully discriminates: every baseline run that gave tooling advice (3/4) recommended the deprecated structurizr/lite image; 0/4 with-skill runs did. The eval-2 baseline additionally emitted 'theme default', removed in DSL v6 (validation prints cloud-EOL warnings).
- Landscape modeling discriminates on best practices: with-skill set 'configuration { scope landscape }' and explicitly questioned the unstated Portal→Motor relationship; the baseline omitted the scope and silently added that relationship (only flagging other assumptions).
- Cost of the skill: ~2.6× tokens (mean 34.6k vs 13.5k) and +28s wall time (mean 105.0s vs 76.7s), spent reading SKILL.md + references and on self-review. Pass-rate gain: +26.6pp.
- Harness caveat: background subagents had Write/Bash auto-denied, so no run could write files or self-validate; DSLs were extracted from final responses by the orchestrator and validated by the grader. The skill mandates validation before delivery — with write/exec allowed, the with-skill eval-3 run would likely have caught its own validation error. Interpret eval-3 results with that in mind.
- Eval 3 is otherwise the least discriminating eval (5/6 vs 5/6): both configurations modeled the AWS deployment structurally well; the deciding differences elsewhere were minimal-diff discipline and ADR importer reasoning (with-skill identified the adr-tools format explicitly).