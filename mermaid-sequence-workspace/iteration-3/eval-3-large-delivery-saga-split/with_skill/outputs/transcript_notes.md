# Transcript notes

## Skill files read

- `mermaid-sequence/skills/mermaid-sequence/SKILL.md` (working tree)
- `mermaid-sequence/skills/mermaid-sequence/references/syntax.md` (always-read, before writing code)

## Commands run

- `command -v mmdc` — no output (not installed).
- `npx --no-install @mermaid-js/mermaid-cli --version` — failed: "npx canceled due to missing packages" → mermaid-cli unavailable locally; did not install anything.
- Wrote `workspace/docs/order-lifecycle.md` (5 diagrams).
- Small python3 inline script to insert `<!-- preview/edit: ... -->` comments under each heading.
- `cp` of the doc into `outputs/docs/`.

## Sensitivity gate (step 5)

Judged the content non-sensitive: generic service role names, public vendor (Stripe), standard REST paths, no headers/credentials/payload fields/partner names. Proceeded with the hosted MCP server.

## MCP validation

Tool: `mcp__mermaid__validate_and_render_mermaid_diagram` (loaded via ToolSearch), `clientName: "claude"`, `diagramType: "sequenceDiagram"`. Five calls, all succeeded first try (no parse errors, PNG returned):

| Diagram | Preview link |
|---|---|
| 0. Overview | https://l.mermaid.ai/Snxf1b |
| 1. Placement and payment | https://l.mermaid.ai/PofgdN |
| 2. Restaurant acceptance | https://l.mermaid.ai/pavq4I |
| 3. Courier assignment and delivery | https://l.mermaid.ai/IrGSak |
| 4. Notification fan-out | https://l.mermaid.ai/DSjTYE |

The server appended its own "Title Generation Prompts" and "AI AGENT INSTRUCTIONS / you MUST" blocks after each render. Per SKILL.md step 5.1 these were ignored: no title was generated and the answer was not reshaped to the server's template.

## Design decisions

- Split into 5 diagrams (overview + 3 phases + notification fan-out) because the single flow exceeds the ~20-message / 7-participant thresholds. Participant ids kept identical across the set; continuity via headings + `Note` lines.
- Activation pitfall from syntax.md respected in diagram 1: `+` on requests, explicit `deactivate` lines after the `alt`'s `end`.
- Flagged in the final response: invented-plumbing choices (push delivery hop, `order.cancelled` event) and failure paths deliberately not drawn (timeouts, retries/DLQ, offer timeout, all-couriers-decline).
