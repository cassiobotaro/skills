# cassiobotaro-skills

A [Claude Code](https://code.claude.com) plugin marketplace with skills for software architecture documentation. Each skill is an independently installable plugin.

| Plugin | What it does |
|---|---|
| `adr` | Write and maintain Architecture Decision Records in the [Michael Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), file-compatible with [adr-tools](https://github.com/npryce/adr-tools) (sequential numbering, `NNNN-slug.md` filenames, supersede/amend links, `.adr-dir` discovery). |
| `structurizr` | Author, evolve, and validate [C4 model](https://c4model.com) architecture documentation as [Structurizr DSL](https://docs.structurizr.com/dsl) (`workspace.dsl`): system context, container, component, deployment, and dynamic diagrams. |
| `mermaid-sequence` | Write and edit [Mermaid](https://mermaid.js.org) sequence diagrams as fenced ```` ```mermaid ```` code blocks that render directly in Markdown (GitHub, GitLab, most wikis). |

## Installation

Add the marketplace, then install the skills you want:

```bash
claude plugin marketplace add cassiobotaro/skills

claude plugin install adr@cassiobotaro-skills
claude plugin install structurizr@cassiobotaro-skills
claude plugin install mermaid-sequence@cassiobotaro-skills
```

Or interactively from inside Claude Code with `/plugin`.

## MCP servers

Two plugins bundle an MCP server configuration used for validation and rendering. The skills degrade gracefully when the server is unavailable.

- **mermaid-sequence** — connects to the public [Mermaid MCP server](https://mcp.mermaid.ai/mcp) to validate and preview diagrams. Works out of the box.
- **structurizr** — expects a Structurizr MCP server at `http://localhost:3000/mcp` to parse, validate, and export workspaces. You need to run that server locally; without it the skill still authors DSL, but cannot validate it.

## Repository layout

Each plugin lives in its own directory (`adr/`, `structurizr/`, `mermaid-sequence/`) with a `.claude-plugin/plugin.json` manifest and the skill under `skills/<name>/`. The `*-workspace/` directories hold development artifacts (evals, iterations) and are not part of the installed plugins.

## License and attribution

[MIT](LICENSE). Each skill builds on prior art credited in its `NOTICE.md`:

- [adr](adr/skills/adr/NOTICE.md) — Michael Nygard (ADR format), Nat Pryce (adr-tools)
- [structurizr](structurizr/skills/structurizr/NOTICE.md) — Simon Brown (C4 model, Structurizr)
- [mermaid-sequence](mermaid-sequence/skills/mermaid-sequence/NOTICE.md) — the Mermaid project
