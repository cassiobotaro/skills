# Notices and attributions

This skill condenses and adapts third-party documentation and relies on third-party
tooling:

- **Mermaid** — syntax and feature documentation in `references/syntax.md` and the
  guidance in `SKILL.md` are condensed and adapted from the Mermaid project
  documentation at [mermaid.js.org](https://mermaid.js.org)
  ([source repository](https://github.com/mermaid-js/mermaid)), distributed under the
  **MIT License**, Copyright (c) 2014-present Knut Sveidqvist and Mermaid
  contributors.
- **mermaid-cli** (`mmdc`, used as a local validation fallback) —
  [github.com/mermaid-js/mermaid-cli](https://github.com/mermaid-js/mermaid-cli),
  **MIT License**.
- **Mermaid MCP server** (`mcp.mermaid.ai`, used for validation and preview when
  connected) — a hosted service operated by the Mermaid Chart team. Diagrams sent to
  it are rendered remotely; this skill instructs against sending sensitive flows
  there.
- **mermaid.live** (suggested for manual preview/editing) — the Mermaid Live Editor,
  [github.com/mermaid-js/mermaid-live-editor](https://github.com/mermaid-js/mermaid-live-editor),
  **MIT License**.

No Mermaid source code is included in this skill; only documentation-derived guidance.
