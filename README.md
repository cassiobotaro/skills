# cassiobotaro-skills

Agent skills for software architecture documentation: decision records, design docs, and diagrams. The skills follow the open [Agent Skills](https://agentskills.io) standard, so they work in any compatible agent — Claude Code, GitHub Copilot, Google Antigravity, OpenCode, and others. The repository is also a [Claude Code](https://code.claude.com) plugin marketplace, where each skill is an independently installable plugin.

| Skill | What it does |
|---|---|
| `adr` | Write and maintain Architecture Decision Records in the [Michael Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), file-compatible with [adr-tools](https://github.com/npryce/adr-tools) (sequential numbering, `NNNN-slug.md` filenames, supersede/amend links, `.adr-dir` discovery). |
| `design-doc` | Write and review software design documents through interactive discovery — targeted questions about the problem, trade-offs, alternatives, and impacted teams — producing trade-off-focused Markdown, condensing the [Design Docs series](https://cassiobotaro.dev/posts/design-docs-parte-1/) and industry practice (Google, Pragmatic Engineer). |
| `structurizr` | Author, evolve, and validate [C4 model](https://c4model.com) architecture documentation as [Structurizr DSL](https://docs.structurizr.com/dsl) (`workspace.dsl`): system context, container, component, deployment, and dynamic diagrams. |
| `mermaid-sequence` | Write and edit [Mermaid](https://mermaid.js.org) sequence diagrams as fenced ```` ```mermaid ```` code blocks that render directly in Markdown (GitHub, GitLab, most wikis). |

## Installation

### Claude Code

Add the marketplace, then install the skills you want:

```bash
claude plugin marketplace add cassiobotaro/skills

claude plugin install adr@cassiobotaro-skills
claude plugin install design-doc@cassiobotaro-skills
claude plugin install structurizr@cassiobotaro-skills
claude plugin install mermaid-sequence@cassiobotaro-skills
```

Or interactively from inside Claude Code with `/plugin`.

### Other agents (Copilot CLI, Antigravity, OpenCode, …)

The skills follow the open [Agent Skills](https://agentskills.io) standard, so they also work outside Claude Code. The [skills CLI](https://github.com/vercel-labs/skills) installs into whichever agents it detects — GitHub Copilot, Google Antigravity (IDE and CLI), OpenCode, and many others:

```bash
npx skills add cassiobotaro/skills                 # interactive: pick skills and agents
npx skills add cassiobotaro/skills --skill adr -g  # a specific skill, globally
```

With the [GitHub CLI](https://cli.github.com/manual/gh_skill) (v2.90.0+, preview), which installs for Copilot by default or another host via `--agent`:

```bash
gh skill install cassiobotaro/skills adr
```

Any other Agent Skills host works too: copy a skill folder (e.g. `adr/skills/adr/`) into the agent's skills directory. The MCP servers below are registered through Claude Code; in other hosts the diagram skills degrade gracefully without them.

## MCP servers

The diagram skills can validate and render through an MCP server, and degrade gracefully when none is connected.

- **mermaid-sequence** — renders natively on GitHub, GitLab, and most wikis. It will validate and preview through the public [Mermaid MCP server](https://mcp.mermaid.ai/mcp) *if you have one registered*, but the plugin does **not** bundle it: that server renders your diagrams remotely, so opting in is left to you (see below). Without it, the skill still produces ready-to-paste diagrams and falls back to mermaid-cli or mermaid.live to preview.
- **structurizr** — validates, parses, and exports workspaces through a Structurizr MCP server at `http://localhost:3000/mcp` *if you have one running and registered*. The plugin does **not** bundle it (a `localhost` config only does anything on a machine already running the server). You run the server locally (e.g. `docker run -p 3000:3000 structurizr/mcp`) and register it yourself (see below); without it, the skill still authors DSL but cannot validate it.

To register an MCP server yourself, add it at user scope:

```bash
claude mcp add --scope user --transport http structurizr http://localhost:3000/mcp
claude mcp add --scope user --transport http mermaid https://mcp.mermaid.ai/mcp
```

## Repository layout

Each plugin lives in its own directory (`adr/`, `design-doc/`, `structurizr/`, `mermaid-sequence/`) with a `.claude-plugin/plugin.json` manifest and the skill under `skills/<name>/`. The `*-workspace/` directories hold development artifacts (evals, iterations) and are not part of the installed plugins.

## License and attribution

[MIT](LICENSE). Each skill builds on prior art credited in its `NOTICE.md`:

- [adr](adr/skills/adr/NOTICE.md) — Michael Nygard (ADR format), Nat Pryce (adr-tools)
- [design-doc](design-doc/skills/design-doc/NOTICE.md) — Cássio Botaro (Design Docs series), Malte Ubl, Rina Artstain, Gergely Orosz, Tech Leads Club
- [structurizr](structurizr/skills/structurizr/NOTICE.md) — Simon Brown (C4 model, Structurizr)
- [mermaid-sequence](mermaid-sequence/skills/mermaid-sequence/NOTICE.md) — the Mermaid project
