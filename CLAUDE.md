# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`cassiobotaro-skills` — architecture-documentation skills in the open **Agent Skills** standard
(`SKILL.md`), installable in any compatible host (Claude Code, GitHub Copilot, Google Antigravity,
OpenCode, … — via `npx skills add` or `gh skill install`). The repository is also a Claude Code
**plugin marketplace** where each skill ships as an independently installable plugin. There is no
application code: the "source" is the skills' Markdown instructions (`SKILL.md` + `references/`).
The four plugins are `adr`, `design-doc`, `structurizr`, and `mermaid-sequence`.

## Layout

- `.claude-plugin/marketplace.json` — root marketplace manifest listing the four plugins and their `source` dirs.
- `<plugin>/.claude-plugin/plugin.json` — per-plugin manifest (name, version, description, license, keywords).
- `<plugin>/skills/<name>/` — the actual skill: `SKILL.md` (frontmatter `name` + `description`, then the body), `NOTICE.md` (upstream attribution), and `references/*.md` (loaded on demand).
- `<plugin>-workspace/` — eval/benchmark artifacts only. **Committed but not part of the installed plugin.** Never reference a workspace path from inside a `skills/` file.

A plugin's `description` lives in three places, and they serve **two different jobs** — do not blindly sync them. `marketplace.json` and `plugin.json` carry the short *showcase* text (what a human reads when browsing plugins); those two must match each other. The `SKILL.md` frontmatter carries the *trigger* text, which is what the model actually reads to decide whether to invoke the skill — it is longer, measured against a trigger eval set, and changes to it are a behavioral change deserving a version bump. Editing the trigger text does not oblige you to touch the showcase text.

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
- **Cap the fan-out at ~4-6 concurrent runs.** Launching a whole multi-skill eval sweep in one message (19 agents, iteration-6/12) had 8 of them killed by the stall watchdog with no progress for 600s, and the survivors reported wall-clock in the millions of ms — pure queueing. Batch the runs and re-seed any fixture directory before re-running a killed agent, since a partial run may have edited it. Wall clock from a contended sweep is not a comparable metric; tokens are.
- The allowlist that lets foreground eval agents save outputs is scoped to `*-workspace/**` in `.claude/settings.local.json` (gitignored). Extend it there for new skills, not in tracked settings. Write it as an `Edit(path)` rule — file-permission checks only match `Edit(...)`, which covers every file-editing tool (Write, Edit, NotebookEdit); a `Write(path)` rule matches nothing and triggers a startup warning.
- When transcribing Mermaid output from an agent's message, HTML-unescape `&gt;`/`&lt;`/`&amp;`.
- The reliable token metric for an optimization A/B is the deterministic `SKILL.md` body reduction; the end-to-end subagent `total_tokens` delta is in the noise (dominated by task work + reading `references/`).
- **Score a trigger eval by aggregate trigger rate, not by the sweep's pass/fail count.** With the default 3 runs per query, a query whose true trigger probability sits near the threshold flips pass/fail between identical sweeps: the same description scored 19/20 and then 15/20 on the same set, same day. That 4-query swing is noise, and any conclusion drawn from a single sweep's headline is worthless. Pool `triggers`/`runs` across sweeps and compare rates over a group of queries — 0/27 versus 5/18 on the same three queries is a signal; "19 beat 17" is not.
- **Run trigger evals (`run_eval.py` / `run_loop.py`) from the repo root**, with `PYTHONPATH` pointing at the skill-creator directory — never by `cd`-ing into skill-creator first. The script injects the candidate description as a temp command under `<project_root>/.claude/commands/` and runs `claude -p` there, and it derives `project_root` by walking up from the cwd to the first directory containing `.claude/`. From inside the skill-creator plugin cache that resolves to `$HOME`, so the temp command lands in the *user* commands dir while the nested session evaluates a different project: every query scores 0/3, positives and negatives alike. The tell is a uniform `trigger_rate` of 0.0 with the negatives "passing" — that is a broken harness run, not a description regression. Smoke-test one obvious positive before paying for a full 20-query set.

## Per-skill notes

- **adr** — adr-tools-compatible decision log (`NNNN-slug.md`, `doc/adr` default, `.adr-dir` override, `adr init`-style seed on fresh logs, supersede/amend by editing the *old* ADR's Status section only — ADRs are otherwise immutable). Modern spelling `Superseded`/`Supersedes` on write; legacy `Superceded` recognized on read.
- **design-doc** — writes *and* reviews design docs via interactive discovery; trade-offs are mandatory (zero-cons = red flag). A user-supplied or house template **governs** (its sections become required); only without a template are sections suggestions. A review (1.2.0) must *establish* the governing template before judging structure — always ask the author for a template reference (templates normally live outside the repo; what the repo shows is a hint, not the answer) — and until one is confirmed the default catalog is the yardstick (suggestions, not demands). Diagram convention (1.1.0): the C4 architecture is authored as **Structurizr DSL** (delegating to the `structurizr` skill when present for classification/validation/idiomatic DSL), embedded as a **PNG/SVG image reference with the DSL folded in a `<details>` block** — render to PNG/SVG via structurizr's export tooling when reachable, otherwise leave the image as a placeholder (a one-line "render in the manual pass" note is fine); sequence flows stay Mermaid (they render natively). No "not machine-validated / ilustração do texto" disclaimer — manual review is assumed; only a *validation* disclaimer is banned. Generated prose is plain active-voice and gets a spelling pass in self-review.
- **structurizr** — authors/edits `workspace.dsl` (C4 model, Structurizr DSL v6+); references split into always-read core (`dsl-reference`) plus conditional pattern files for token economy.
- **mermaid-sequence** — Mermaid sequence diagrams as fenced ` ```mermaid ` blocks; never invent the flow or failure paths; technical detail (endpoint/headers/payload/status) goes in Notes. `references/syntax.md` is always-read (version-portability + escaping gotchas).
