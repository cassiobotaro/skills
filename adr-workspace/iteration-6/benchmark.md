# iteration-6 — full eval set against 1.2.1

**Question.** 1.2.1 shipped after iteration-4, and iteration-5 only re-ran eval 5. Does the
whole set still hold against the current version?

**Method.** All seven evals, one `with_skill` run each, against the working-tree skill (not
the installed plugin). No baseline: the question is "does it still pass?", not "did it
improve?". Grading by an independent agent that diffed every produced file against the
pristine fixtures rather than eyeballing.

## Result — 34/38 under the assertions as they stood; **41/41** after correcting them

The first grading pass ran against the assertion set as it was, and scored 34/38. Every one
of the four failures turned out to be an assertion contradicting either another assertion or
the skill's own rule 2 (detail below). The set was corrected in
`adr-workspace/evals/evals.json` and a second independent grader re-scored the *same outputs*
against the corrected wording: **41/41**, no failures. The per-eval table below is the
original pass; the corrected totals are 8/8, 4/4, 6/6, 6/6, 8/8, 5/5, 4/4.

### Original pass — 34/38 (89%)

| Eval | Passed | Tokens |
|---|---|---|
| 1 clear-decision-fresh-repo | 5/7 | 30,011 |
| 2 vague-decision-asks | 4/4 | 26,264 |
| 3 supersede-existing-adr | 6/6 | 30,961 |
| 4 custom-dir-detection | 6/6 | 30,106 |
| 5 fresh-log-portuguese | 4/6 | 29,968 |
| 6 existing-english-log-pt-conversation | 5/5 | 30,277 |
| 7 english-regression | 4/4 | 29,770 |

Total 207,357 tokens, mean 29,622. Wall clock is not reported: the runs executed
concurrently across three skills and the numbers carry queueing delay — several agents were
killed by a stall watchdog and re-run, so elapsed time measures the harness, not the skill.

## All four failures are eval-set defects, not skill defects

The grader found no behavioral defect. Every mechanical check passed: eval 3 changed exactly
one line in ADR 2 (`Accepted` → `Superseded by [4. …]`) and touched nothing else; eval 4 left
`.adr-dir`, 0001 and 0002 untouched; eval 6's two existing ADRs are byte-identical; eval 7's
seed is the canonical text with only the date substituted. All dates 2026-07-21, all H1s
un-padded, all section orders canonical, no double blank lines.

The four failed assertions are all the language rule, and they contradict each other:

- **eval 1 a3** demands the ADR prose be **English**; **eval 5 a3** demands it be
  **Portuguese**. Both prompts are Portuguese against a fresh repo, so no single behavior can
  satisfy both. Per CLAUDE.md ("generated artifacts follow the conversation language"),
  eval 1 is the wrong one — and eval 7 already covers the English regression with an English
  prompt.
- **eval 1 a1** hardcodes the English seed filename `0001-record-architecture-decisions.md`,
  which is unreachable when the prose language is Portuguese — and eval 5 a2 explicitly
  requires the *translated* slug.
- **eval 5 a2 / a3** require the `## Status/Context/Decision/Consequences` headings and the
  status word to be **translated**. That is the exact opposite of SKILL.md rule 2 and
  CLAUDE.md: the scaffolding stays canonical English so Structurizr's `!adrs` importer and
  `adr generate` can parse it. The runs kept it English, correctly, and were marked down.

With those four assertions corrected the set scores 41/41 (the corrected set is slightly
larger: the language split that used to hide inside one assertion is now two, on evals 1 and
5, so the scaffolding rule is tested separately from the prose rule). They are stale relative to the
skill's current rule 2, which is why iteration-4 could report 100% on the same wording — the
behavior, not the assertions, moved.

## Eval-set hygiene finding

`adr-workspace/evals/evals.json` lists **5** evals, four of them with empty `assertions`,
while the iteration directories carry **7** fully-asserted evals. The JSON — nominally the
spec — is not the source of truth; the per-iteration `eval_metadata.json` files are. Any
future run has to reconstruct the set from a previous iteration, as this one did.
