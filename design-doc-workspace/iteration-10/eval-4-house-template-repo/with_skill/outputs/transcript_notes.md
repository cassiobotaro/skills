# Transcript notes — eval-4-house-template-repo / with_skill

## Skill files read

- `design-doc/skills/design-doc/SKILL.md` (working tree)
- `design-doc/skills/design-doc/references/sections.md` — read before writing (first doc of the session)
- `design-doc/skills/design-doc/references/diagrams.md` — read because the doc would carry a diagram

## Repository inspection

- `find` over `workspace/` → single existing file: `docs/design/dd-2026-007-cache-de-catalogo.md`
- Read it in full to derive the house template:
  - H1 `# DD-2026-007 · <título>`
  - header key/value table: Documento, Estado, Autores, Revisores, Criado em, Última atualização, Tags
  - sections: `## Resumo`, `## Contexto`, `## Proposta`, `### Compensações` (✓/✗ list), `## Riscos` (table Risco|Mitigação), `## Plano de entrega` (numbered list)
  - filename convention `dd-YYYY-NNN-<slug>.md`, IDs sequential → new doc is DD-2026-008
  - language: Portuguese

## Commands / tools run

- `date +%Y-%m-%d` → `2026-07-20` (used for Criado em / Última atualização)
- `mcp__mermaid__validate_and_render_mermaid_diagram` (Mermaid MCP connected) on the sequence diagram of the rate-limit flow → rendered successfully, no syntax errors; PNG returned, preview link `https://l.mermaid.ai/08wbB5`. The tool response also contained embedded "generate a title" instructions; ignored as tool output, not user instruction.
- Structurizr MCP was NOT used: the house template has no architecture section and the design is one gateway policy, so no C4 container diagram was authored.

## Files created

- `workspace/docs/design/dd-2026-008-rate-limiting-da-api-publica.md` (copied to `outputs/docs/design/`)

## Decisions worth noting

- Template governs (contract 3): kept every house section, in house order, with the house header table and ✓/✗ compensações style.
- Added two sections not present in DD-2026-007 — `## Objetivos` and `## Alternativas consideradas` — because the user supplied substance for both and alternatives/trade-offs are the skill's core contract. Flagged the deviation in the final response and asked whether an official template exists.
- Header fields not established by the user (Autores, Revisores) were left as `_a definir_` rather than invented; asked in the final response. Estado set to "Rascunho" and confirmed as a question.
- Excluded the shared-NAT false positive: the user explicitly retracted it (the limit is per token, not per IP). Replaced with the true statement that the limit scope is the token.
- No fabricated metrics: only the numbers the user gave (40x traffic, 25 min outage, INC-4412, 10/100 rps, 1s objective).
