# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`cassiobotaro-skills` — a Claude Code **plugin marketplace** of architecture-documentation skills.
There is no application code: the "source" is the skills' Markdown instructions (`SKILL.md` +
`references/`). Each plugin is independently installable. The four plugins are `adr`,
`design-doc`, `structurizr`, and `mermaid-sequence`.

## Layout

- `.claude-plugin/marketplace.json` — root marketplace manifest listing the four plugins and their `source` dirs.
- `<plugin>/.claude-plugin/plugin.json` — per-plugin manifest (name, version, description, license, keywords).
- `<plugin>/skills/<name>/` — the actual skill: `SKILL.md` (frontmatter `name` + `description`, then the body), `NOTICE.md` (upstream attribution), and `references/*.md` (loaded on demand).
- `<plugin>-workspace/` — eval/benchmark artifacts only. **Committed but not part of the installed plugin.** Never reference a workspace path from inside a `skills/` file.

A plugin's `description` lives in three places that must stay in sync when edited: `marketplace.json`, `plugin.json`, and the `SKILL.md` frontmatter.

## Conventions specific to this repo

- **Versioning**: the `version` field lives **only** in each `plugin.json`, never in `marketplace.json` entries. Setting both causes drift (plugin.json silently wins). Bump the plugin.json version on any shipped skill change and use it in the commit subject (e.g. `adr 1.2.0: …`).
- **No bundled MCP servers**: plugins must not ship a `.mcp.json`. A skill may *use* an MCP when one is connected but must degrade gracefully without it; registering a server is the user's opt-in (`claude mcp add --scope user …`). This is why `structurizr` and `mermaid-sequence` dropped their bundles in 1.1.0.
- **Language**: skill content (`SKILL.md`, `references/`) is written in **English**. Generated *artifacts* follow the conversation language. The one nuance (see `adr/skills/adr/SKILL.md`): tool-parsed scaffolding — adr-tools' `Date:` label, the `## Status/Context/Decision/Consequences` headings, status words, and supersede/amend verbs — stays canonical English even in a non-English log, because Structurizr's `!adrs` importer and `adr generate` parse those exact literals; only the prose is translated.
- **Record, don't invent** is the shared contract across every skill: document only what the user/repository established; when the request is too vague to fill the sections honestly, ask 2–4 targeted questions instead of fabricating. The questions are the deliverable on a vague ask.
- **Attribution**: every skill credits its prior art in `NOTICE.md` and an Attribution footer in `SKILL.md`. Preserve these and the root `LICENSE` (MIT) when editing.

## Validating a plugin

```bash
claude plugin validate <plugin-dir>     # e.g. claude plugin validate adr
```

There is no build or unit-test step. Correctness is measured by **evals**, not asserts.

## Evals / benchmarks

Evals are authored and run through the **skill-creator** skill (`/skill-creator`), not by
scripts in this repo. Each skill has:

- `<plugin>-workspace/evals/evals.json` — the eval set (prompt, `expected_output`, optional `files/`, optional `assertions`). This is the spec for what the skill must do; read it before changing a skill's behavior.
- `<plugin>-workspace/iteration-N/` — per-run outputs, `with_skill/` vs `without_skill/` configs, `grading.json`, `benchmark.md` (the A/B summary: pass-rate, time, tokens).

Gotchas when running evals in this repo (learned the hard way):

- Spawn eval subagents in the **foreground** (parallel calls in one message). Background agents (`run_in_background: true`) are blocked from Write/Edit in the main checkout regardless of allowlist; if you must, salvage outputs from their final messages.
- The Write/Edit allowlist that lets foreground eval agents save outputs is scoped to `*-workspace/**` in `.claude/settings.local.json` (gitignored). Extend it there for new skills, not in tracked settings.
- When transcribing Mermaid output from an agent's message, HTML-unescape `&gt;`/`&lt;`/`&amp;`.
- The reliable token metric for an optimization A/B is the deterministic `SKILL.md` body reduction; the end-to-end subagent `total_tokens` delta is in the noise (dominated by task work + reading `references/`).

## Per-skill notes

- **adr** — adr-tools-compatible decision log (`NNNN-slug.md`, `doc/adr` default, `.adr-dir` override, `adr init`-style seed on fresh logs, supersede/amend by editing the *old* ADR's Status section only — ADRs are otherwise immutable). Modern spelling `Superseded`/`Supersedes` on write; legacy `Superceded` recognized on read.
- **design-doc** — writes *and* reviews design docs via interactive discovery; trade-offs are mandatory (zero-cons = red flag). A user-supplied or house template **governs** (its sections become required); only without a template are sections suggestions. Diagram convention (1.1.0): the C4 architecture is authored as **Structurizr DSL** (delegating to the `structurizr` skill when present for classification/validation/idiomatic DSL), embedded as a **PNG/SVG image reference with the DSL folded in a `<details>` block** — render to PNG/SVG via structurizr's export tooling when reachable, otherwise leave the image as a placeholder (a one-line "render in the manual pass" note is fine); sequence flows stay Mermaid (they render natively). No "not machine-validated / ilustração do texto" disclaimer — manual review is assumed; only a *validation* disclaimer is banned. Generated prose is plain active-voice and gets a spelling pass in self-review.
- **structurizr** — authors/edits `workspace.dsl` (C4 model, Structurizr DSL v6+); references split into always-read core (`dsl-reference`) plus conditional pattern files for token economy.
- **mermaid-sequence** — Mermaid sequence diagrams as fenced ` ```mermaid ` blocks; never invent the flow or failure paths; technical detail (endpoint/headers/payload/status) goes in Notes. `references/syntax.md` is always-read (version-portability + escaping gotchas).
