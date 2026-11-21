# AGENTS.md

Guidance for any coding agent working in this repository. This is the single instructions file
a host loads by itself: there is no separate `CLAUDE.md`, and everything here applies to every
host. Two more files are read on demand; see "Read on demand" at the end.

## What this repo is

`cassiobotaro-skills` — architecture-documentation skills, one code-comments skill, and one prose-editing skill, in the open **Agent Skills** standard
(`SKILL.md`), installable in any compatible host (Claude Code, GitHub Copilot, Google Antigravity,
OpenCode, … — via `npx skills add cassiobotaro/skills` or `gh skill install cassiobotaro/skills <skill>`).
The repository is also a Claude Code **plugin marketplace** where each skill ships as an
independently installable plugin. There is no application code: the "source" is the skills'
Markdown instructions (`SKILL.md` + `references/`). The six plugins are `adr`, `design-doc`,
`structurizr`, `mermaid-sequence`, `unslop`, and `code-comments`.

## Layout

- `.claude-plugin/marketplace.json` — root marketplace manifest listing the six plugins and their `source` dirs.
- `<plugin>/.claude-plugin/plugin.json` — per-plugin manifest (name, version, description, license, keywords).
- `<plugin>/skills/<name>/` — the actual skill: `SKILL.md` (frontmatter `name` + `description`, then the body), `NOTICE.md` (upstream attribution), and `references/*.md` (loaded on demand).
- `<plugin>-workspace/` — eval/benchmark artifacts only. **Committed but not part of the installed plugin.** Never reference a workspace path from inside a `skills/` file.
- `eval-tools/` — Python helpers for trigger evals (`run_trigger_eval.py`, `capture_trigger_transcripts.py`) and for grading (`judge.py`). They drive the Claude Code CLI. `eval-tools/README.md` holds how the evals are run and read.
- `MAINTAINING.md` — the contract the skills share and one note per skill.
- `README.md` — user-facing installation and tooling guide. Keep it in sync when a skill's external tooling or install path changes.

A plugin's `description` lives in three places, and they serve **two different jobs** — do not
blindly sync them. `marketplace.json` and `plugin.json` carry the short *showcase* text (what a
human reads when browsing plugins); those two must match each other. The `SKILL.md` frontmatter
carries the *trigger* text, which is what the model reads to decide whether to invoke the skill —
it is longer, measured against a trigger eval set, and changes to it are a behavioral change
deserving a version bump. Editing the trigger text does not oblige you to touch the showcase text.

## Conventions

- **Versioning**: the `version` field lives **only** in each `plugin.json`, never in `marketplace.json` entries. Setting both causes drift (plugin.json silently wins). Bump the plugin.json version on any shipped skill change and use it in the commit subject (e.g. `design-doc 1.2.0: …`).
- **Commit subjects** follow `<plugin> <version>: <what changed>` for skill changes; other changes use a plain imperative subject.
- **No bundled MCP servers**: plugins must not ship a `.mcp.json`. A skill may *use* an MCP when one is connected but must degrade gracefully without it; registering a server is the user's opt-in. How each skill validates today is in `MAINTAINING.md`.
- **Language**: skill content (`SKILL.md`, `references/`) is written in **English**. Generated *artifacts* follow the conversation language.
- **Attribution**: every skill credits its prior art in `NOTICE.md` and an Attribution footer in `SKILL.md`. Preserve these and the root `LICENSE` (MIT) when editing.
- **Token economy**: keep `SKILL.md` bodies lean. Material that is only sometimes needed goes in `references/*.md` and is loaded on demand; the body says when to read each file.
- **Host portability**: a skill must work in any Agent Skills host. Do not depend on Claude-Code-only features (slash commands, hooks, settings) inside `skills/` files.

## Validating a change

There is no build or unit-test step. Before committing a skill change:

```bash
claude plugin validate <plugin-dir>     # e.g. claude plugin validate design-doc
```

Check by hand that:

- `SKILL.md` frontmatter has `name` (matching the directory) and `description`.
- `marketplace.json` and `plugin.json` descriptions still match each other.
- `plugin.json` `version` was bumped if anything under `skills/` changed.
- No `skills/` file references a `*-workspace/` path.

Correctness is measured by **evals**, not asserts.

## Read on demand

Two files hold the rest of the guidance. They are kept out of this file on purpose. A host loads
this file into every session started in the repository, and that includes each eval executor and
each trigger-eval session: whatever is written here costs tokens on every run and is read by both
arms of every A/B. Do not copy their content back here, and do not describe a skill's expected
behavior in this file.

- `MAINTAINING.md` — the contract the skills share, how each one validates, and one note per skill
  (what it does and the decisions behind it). **Read it before changing anything under a `skills/`
  directory.**
- `eval-tools/README.md` — where the evals live, how to run them, and the rules for reading their
  numbers. **Read it before running an eval or quoting a number from one.** Each
  `<plugin>-workspace/evals/evals.json` is the spec for what its skill must do; read it before
  changing that skill's behavior.

When you are the executor of an eval run (a brief that hands you a skill path and an outputs
directory), read neither file: the brief and the skill are the whole input.
