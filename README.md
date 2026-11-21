# cassiobotaro-skills

Agent skills for software architecture, engineering, communication, and learning. The skills follow the open [Agent Skills](https://agentskills.io) standard, so they work in any compatible agent — Claude Code, GitHub Copilot, Google Antigravity, OpenCode, and others. The repository is also a [Claude Code](https://code.claude.com) plugin marketplace, where each skill is an independently installable plugin.

## Skills

### Architecture

| Skill | What it does | Builds on |
|---|---|---|
| [`adr`](adr/skills/adr/SKILL.md) | Write and maintain Architecture Decision Records in the [Michael Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), file-compatible with [adr-tools](https://github.com/npryce/adr-tools). | Michael Nygard, Nat Pryce ([NOTICE](adr/skills/adr/NOTICE.md)) |
| [`structurizr`](structurizr/skills/structurizr/SKILL.md) | Author, evolve, and validate [C4 model](https://c4model.com) architecture documentation as [Structurizr DSL](https://docs.structurizr.com/dsl). | Simon Brown ([NOTICE](structurizr/skills/structurizr/NOTICE.md)) |

### Engineering

| Skill | What it does | Builds on |
|---|---|---|
| [`design-doc`](design-doc/skills/design-doc/SKILL.md) | Write and review software design documents through interactive discovery, producing trade-off-focused Markdown. | Cássio Botaro ([Design Docs series](https://cassiobotaro.dev/posts/design-docs-parte-1/)), Malte Ubl, Rina Artstain, Gergely Orosz, Tech Leads Club ([NOTICE](design-doc/skills/design-doc/NOTICE.md)) |
| [`mermaid-sequence`](mermaid-sequence/skills/mermaid-sequence/SKILL.md) | Write and edit [Mermaid](https://mermaid.js.org) sequence diagrams as fenced code blocks that render directly in Markdown. | The Mermaid project ([NOTICE](mermaid-sequence/skills/mermaid-sequence/NOTICE.md)) |
| [`code-comments`](code-comments/skills/code-comments/SKILL.md) | Keep the comments in code an agent writes or changes useful, precise, and compact: comment what the reader cannot get from the code, never what they can. | Dustin Boswell and Trevor Foucher, *The Art of Readable Code* ([NOTICE](code-comments/skills/code-comments/NOTICE.md)) |

### Communication and learning

| Skill | What it does | Builds on |
|---|---|---|
| [`unslop`](unslop/skills/unslop/SKILL.md) | Remove the patterns that mark prose as machine-written, in English or Brazilian Portuguese. It runs only when you ask for it by name or another skill calls it. | Lauren Tan, pstack ([NOTICE](unslop/skills/unslop/NOTICE.md)) |
| [`explain`](explain/skills/explain/SKILL.md) | Explain a topic to one specific reader, and write or revise messages, emails, and replies, choosing the device by the reader's situation instead of running one fixed format. | Research on instruction, plain language, and science communication; Diátaxis; Julia Evans ([NOTICE](explain/skills/explain/NOTICE.md)) |

## Record, don't invent

No skill states as fact something that you or your repository did not establish: no invented metrics, technologies, relationships, endpoints, failure paths, or reasons. A gap is shown to you and never filled with a guess, because a gap gets asked about and a fabrication gets believed. How the gap is shown depends on what the skill delivers:

- A skill that writes a document or a diagram asks: when a request is too vague to fill honestly, you get a few targeted questions (batched, in the conversation language), and those questions are the deliverable.
- A skill that works inside a code change does not stop to ask: a reason nobody established stays out of the file and is reported in the reply.
- A skill that explains, or writes a message for you, has to build examples and analogies, so it separates the two: facts are recorded, illustrations are built and shown as illustrations, and a fact a message needs and nobody gave is left as a bracketed gap.
- A skill that edits a text that already exists removes and never supplies: when a fix would need a fact the text lacks, it deletes the claim or asks.

## Installation

| Host | Install with | Without Docker |
|---|---|---|
| Claude Code | `claude plugin install <skill>@cassiobotaro-skills`, or `/plugin` | DSL and Mermaid are authored but not validated; you get the command to run later |
| GitHub Copilot CLI | `gh skill install cassiobotaro/skills <skill>` | same |
| Antigravity, OpenCode, others | `npx skills add cassiobotaro/skills` | same |
| Any Agent Skills host | copy the skill folder (e.g. `design-doc/skills/design-doc/`) into the agent's skills directory | same |

No skill *requires* Docker, and none uses an MCP server. Only `structurizr` and `mermaid-sequence` use external tooling: they validate through Docker images (`mermaid-sequence` falls back to a local mermaid-cli) and degrade gracefully without them, as the last column says.

### Claude Code

Add the marketplace, then install each skill you want by its name under [Skills](#skills):

```bash
claude plugin marketplace add cassiobotaro/skills
claude plugin install design-doc@cassiobotaro-skills   # one command per skill
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
- **structurizr** — validates, previews, and exports workspaces with the [`structurizr/structurizr`](https://hub.docker.com/r/structurizr/structurizr) Docker image (`structurizr/structurizr validate`, `local`, `export`), pulled on first use; PNG/SVG export needs the image's `<version>-playwright` variant, which the skill names when it hands over the command. Without Docker, the skill still authors the DSL, tells you it was not validated, and gives you the `validate` command to run later.

## Repository layout

Each skill ships as a plugin in its own directory (`<skill>/`) with a `.claude-plugin/plugin.json` manifest and the skill under `skills/<skill>/`. The `<skill>-workspace/` directories hold development artifacts (evals, iterations) and are not part of the installed plugins.

## License and attribution

[MIT](LICENSE). Each skill builds on prior art: the tables under [Skills](#skills) name it, and the skill's `NOTICE.md` credits it in full.
