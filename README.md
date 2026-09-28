# cassiobotaro-skills

Agent skills for software architecture documentation: design docs and diagrams. The skills follow the open [Agent Skills](https://agentskills.io) standard, so they work in any compatible agent — Claude Code, GitHub Copilot, Google Antigravity, OpenCode, and others. The repository is also a [Claude Code](https://code.claude.com) plugin marketplace, where each skill is an independently installable plugin.

| Skill | What it does |
|---|---|
| `design-doc` | Write and review software design documents through interactive discovery — targeted questions about the problem, trade-offs, alternatives, and impacted teams — producing trade-off-focused Markdown, condensing the [Design Docs series](https://cassiobotaro.dev/posts/design-docs-parte-1/) and industry practice (Google, Pragmatic Engineer). |
| `structurizr` | Author, evolve, and validate [C4 model](https://c4model.com) architecture documentation as [Structurizr DSL](https://docs.structurizr.com/dsl) (`workspace.dsl`): system context, container, component, deployment, and dynamic diagrams. |
| `mermaid-sequence` | Write and edit [Mermaid](https://mermaid.js.org) sequence diagrams as fenced ```` ```mermaid ```` code blocks that render directly in Markdown (GitHub, GitLab, most wikis). |

**Record, don't invent.** Every skill documents only what you or your repository established — no invented metrics, technologies, relationships, endpoints, or failure paths. When a request is too vague to fill honestly, the skill asks a few targeted questions (batched, in the conversation language) instead of guessing, and those questions are the deliverable: a gap gets asked about, a fabrication gets believed.

## Installation

| Host | Install with | Without Docker |
|---|---|---|
| Claude Code | `claude plugin install <skill>@cassiobotaro-skills`, or `/plugin` | DSL and Mermaid are authored but not validated; you get the command to run later |
| GitHub Copilot CLI | `gh skill install cassiobotaro/skills <skill>` | same |
| Antigravity, OpenCode, others | `npx skills add cassiobotaro/skills` | same |
| Any Agent Skills host | copy the skill folder (e.g. `design-doc/skills/design-doc/`) into the agent's skills directory | same |

No skill *requires* Docker, and none uses an MCP server: `design-doc` needs no external tooling, `structurizr` and `mermaid-sequence` validate through Docker images (mermaid-sequence falls back to a local mermaid-cli), and both diagram skills degrade gracefully, as the last column says.

### Claude Code

Add the marketplace, then install the skills you want:

```bash
claude plugin marketplace add cassiobotaro/skills

claude plugin install design-doc@cassiobotaro-skills
claude plugin install structurizr@cassiobotaro-skills
claude plugin install mermaid-sequence@cassiobotaro-skills
```

Or interactively from inside Claude Code with `/plugin`.

### Other agents (Copilot CLI, Antigravity, OpenCode, …)

The [skills CLI](https://github.com/vercel-labs/skills) (requires Node.js) installs into whichever agents it detects — GitHub Copilot, Google Antigravity (IDE and CLI), OpenCode, and many others:

```bash
npx skills add cassiobotaro/skills                        # interactive: pick skills and agents
npx skills add cassiobotaro/skills --skill design-doc -g  # a specific skill, globally
```

With the [GitHub CLI](https://cli.github.com/manual/gh_skill) (v2.90.0+, preview), which installs for Copilot by default or another host via `--agent`:

```bash
gh skill install cassiobotaro/skills design-doc
```

Any other Agent Skills host works too: copy a skill folder (e.g. `design-doc/skills/design-doc/`) into the agent's skills directory.

## External tooling

The diagram skills validate and render through tooling you provide, and degrade gracefully when it is missing. Nothing is bundled and no MCP server is involved — installing Docker is your opt-in, and nothing you diagram leaves your machine.

- **mermaid-sequence** — renders natively on GitHub, GitLab, and most wikis. It validates diagrams with [mermaid-cli](https://github.com/mermaid-js/mermaid-cli): first through its Docker image ([`minlag/mermaid-cli`](https://hub.docker.com/r/minlag/mermaid-cli), pulled on first use), then through a local `mmdc` install if Docker is missing. Without either, the skill still produces ready-to-paste diagrams, tells you they were not validated, and gives you the Docker command to run later.
- **structurizr** — validates, previews, and exports workspaces with the [`structurizr/structurizr`](https://hub.docker.com/r/structurizr/structurizr) Docker image (`structurizr/structurizr validate`, `local`, `export`), pulled on first use. Without Docker, the skill still authors the DSL, tells you it was not validated, and gives you the `validate` command to run later.

## Repository layout

Each skill ships as a plugin in its own directory (`design-doc/`, `structurizr/`, `mermaid-sequence/`) with a `.claude-plugin/plugin.json` manifest and the skill under `skills/<name>/`. The `*-workspace/` directories hold development artifacts (evals, iterations) and are not part of the installed plugins.

## License and attribution

[MIT](LICENSE). Each skill builds on prior art credited in its `NOTICE.md`:

- [design-doc](design-doc/skills/design-doc/NOTICE.md) — Cássio Botaro (Design Docs series), Malte Ubl, Rina Artstain, Gergely Orosz, Tech Leads Club
- [structurizr](structurizr/skills/structurizr/NOTICE.md) — Simon Brown (C4 model, Structurizr)
- [mermaid-sequence](mermaid-sequence/skills/mermaid-sequence/NOTICE.md) — the Mermaid project
