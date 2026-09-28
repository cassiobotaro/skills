# Iteration 16 — design-doc 1.3.6 vs 1.3.7: typography rule (no-ai-slop patterns)

**Question.** Does adding a "keep the typography plain" rule (Write §3) and a typography sweep
(Self-review §4) remove the AI-slop patterns that a 1.3.6 run tripped, without changing what the
skill records or invents?

**Method.** Eval 1 (rich write-new-doc, Portuguese prompt, empty project root, no `structurizr`
skill, no renderer), one foreground subagent per version, 2026-09-28. Detection follows the
*detect* job of [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (`SKILL.md`
patterns, `eval.md` checks), applied by hand and with `slopscan.sh` (pattern counts adapted to
Portuguese). `old_skill/` = 1.3.6, `with_skill/` = 1.3.7. **n = 1 per arm**; the numbers below are
one sample each, not rates.

## Pattern counts

| Pattern (no-ai-slop) | 1.3.6 | 1.3.7 |
|---|---|---|
| Em dashes, total | 21 | 0 |
| Em dashes in running prose | 11 | 0 |
| Colon reveals ("O trade-off central: o usuário perde…") | 2 | 0 |
| Emphasis bold mid-sentence (`**toda** exportação`) | 1 | 0 |
| "This document covers…" paragraph | 1 | 0 |
| Gap-marker sentence repeated ("O time ainda não…") | 7 | 1 |
| Passive voice in prose | 1 (adjectival) | 2 (adjectival) |
| Banned words / puffery / weasel attribution | 0 | 0 |
| Words | 2,068 | 2,205 |

Both runs: no banned vocabulary, no superficial-analysis clauses, no fake-profound ending, no
emoji headings, alternatives include "do nothing", accepted cost stated, diagrams followed by
prose, unknowns pushed to Open questions (10 and 11 respectively).

## Content check (contract 2, record don't invent)

- 1.3.6: self-review reported removing an exclusivity claim ("a única das opções") and six
  passives. No invented technology; data source and e-mail sender left without technology.
- 1.3.7: one inference slipped through — "RabbitMQ … **mantido pelo time de Plataforma**"
  (Contexto and DSL). The prompt says the change *impacts* the Platform team because the queue is
  shared; it does not say Platform maintains RabbitMQ. Not attributable to the typography rule at
  n = 1; recorded so a later iteration can probe it.
- 1.3.7 dropped the "Compatibilidade" cross-cutting section (who calls the export endpoint today)
  that 1.3.6 had, keeping only part of it as open question 3. Run-to-run variation; the section is
  from the optional catalog.

## Reading

The rule hit every pattern it names, in one run: the five typography patterns went from
21/2/1/1/7 to 0/0/0/0/1, with the surviving gap marker being the single allowed statement. Nothing
in the contract regressed that can be tied to the change. A per-query claim needs more runs
(AGENTS.md: n ≥ 10); this iteration only shows that the effect exists and is large.
