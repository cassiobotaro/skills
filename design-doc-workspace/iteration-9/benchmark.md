# iteration-9 — gate for the progressive-disclosure cut (1.3.0)

**Question.** The `## Diagrams` section (~68 lines: the Structurizr-DSL convention, the
image-plus-folded-source embedding, the rendering fallbacks) moved out of `SKILL.md` into
a new `references/diagrams.md`, leaving a short contract in the body and a trigger row in
the reference table. Does the agent still reach for the reference and follow it?

**Method.** Eval 1 (`rich-write-new-doc`), one foreground run against the working-tree
skill (not the installed plugin). `with_skill/` holds the output.

**Result — pass.** The agent read `references/diagrams.md` (and `sections.md`) and applied
the convention end to end:

| Behavior | Held? |
|---|---|
| C4 architecture authored as Structurizr DSL | yes — validated clean, exit 0 |
| Embedded as Markdown image with DSL folded in `<details>` | yes |
| Image reference resolves to a real file | yes — `diagrams/arquitetura.svg`, 43 KB, exported via PlantUML |
| Sequence flow as a fenced ` ```mermaid ` block | yes |
| Every diagram followed by explanatory prose | yes |
| No validation disclaimer in the document | yes — grep for "não validad"/"ilustração do texto" is empty |

It also delegated to the `structurizr` and `mermaid-sequence` skills as
`references/diagrams.md` instructs, rather than restating their conventions.

Unrelated behaviors that stayed correct: the glossary carries stumble terms (CSV/XLSX,
PII, BI, S3) and excludes both universally-known terms and the doc's own authoring
scaffolding (C4/DSL/Structurizr appear only inside the `<details>` summary) — the 1.2.1
rule; "do nothing" appears among the alternatives; unestablished facts (authors,
reviewers, worker technology, link TTL) became open questions instead of inventions.

**Body size.** `SKILL.md` 316 → 259 lines (−57, −18%).
