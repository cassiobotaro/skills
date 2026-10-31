# iteration-19 — smoke test of the catalog-table prune (design-doc 1.4.3)

**Change under test.** The default section catalog table (three columns, twelve rows) left
`SKILL.md` and was replaced by a one-paragraph list of the section names plus the
recommended minimum and the three "worth having when" rules that matter most. The
per-section detail already lives in `references/sections.md`, which the body tells the model
to read before writing its first doc, so the table was duplicated context on every
invocation. Body size: 18 028 → 17 065 bytes (−5.3%). No change to the contracts or workflow.

**Method.** One run of eval 1 (`rich-write-new-doc`, the richest no-template write, i.e. the
path that depends on the catalog) with the pruned skill. Single arm, no baseline: the goal
is to confirm the behaviour the table carried survives in the prose, not to measure a delta.
The grader re-ran `structurizr/structurizr validate` on the folded DSL and `minlag/mermaid-cli`
on the sequence block from the delivered document.

**Result.** 11/11 assertions. The document uses nine catalog sections in catalog order
(header, glossary, overview, scope and context, goals, the design as a series, trade-offs,
alternatives, cross-cutting, open questions), skips none that the prompt calls for, and
leaves the unstated technology slots blank. Zero em dashes in the generated document.
Tokens 95 876 against 108 157 for the same eval in iteration-17 — a
single-run difference inside the noise band AGENTS.md documents; the deterministic metric is
the body reduction above.
