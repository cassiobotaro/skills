# AGENTS.md

Guidance for any coding agent working in this repository. This is the single instructions file:
there is no separate `CLAUDE.md`, and everything here applies to every host.

## What this repo is

`cassiobotaro-skills` — architecture-documentation skills in the open **Agent Skills** standard
(`SKILL.md`), installable in any compatible host (Claude Code, GitHub Copilot, Google Antigravity,
OpenCode, … — via `npx skills add cassiobotaro/skills` or `gh skill install cassiobotaro/skills <skill>`).
The repository is also a Claude Code **plugin marketplace** where each skill ships as an
independently installable plugin. There is no application code: the "source" is the skills'
Markdown instructions (`SKILL.md` + `references/`). The three plugins are `design-doc`,
`structurizr`, and `mermaid-sequence`.

## Layout

- `.claude-plugin/marketplace.json` — root marketplace manifest listing the three plugins and their `source` dirs.
- `<plugin>/.claude-plugin/plugin.json` — per-plugin manifest (name, version, description, license, keywords).
- `<plugin>/skills/<name>/` — the actual skill: `SKILL.md` (frontmatter `name` + `description`, then the body), `NOTICE.md` (upstream attribution), and `references/*.md` (loaded on demand).
- `<plugin>-workspace/` — eval/benchmark artifacts only. **Committed but not part of the installed plugin.** Never reference a workspace path from inside a `skills/` file.
- `eval-tools/` — Python helpers for trigger evals (`run_trigger_eval.py`, `capture_trigger_transcripts.py`). They drive the Claude Code CLI; see "Evals" below.
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
- **No bundled MCP servers**: plugins must not ship a `.mcp.json`. A skill may *use* an MCP when one is connected but must degrade gracefully without it; registering a server is the user's opt-in. Today no skill uses an MCP at all: `structurizr` validates, previews, and exports through the `structurizr/structurizr` Docker image, and `mermaid-sequence` validates through the `minlag/mermaid-cli` Docker image with a local `mmdc` as fallback. Without Docker (or the CLI), both ship the artifact with an explicit "not validated" notice plus the command to run later — **never an install attempt, never a remote validator**.
- **Language**: skill content (`SKILL.md`, `references/`) is written in **English**. Generated *artifacts* follow the conversation language.
- **Record, don't invent** is the shared contract across every skill: document only what the user/repository established; when the request is too vague to fill the sections honestly, ask 2–4 targeted questions instead of fabricating. The questions are the deliverable on a vague ask.
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

## Evals

Evals are authored and run through the **skill-creator** skill, not by scripts in this repo. Each skill has:

- `<plugin>-workspace/evals/evals.json` — the eval set (prompt, `expected_output`, optional `files/`, optional `assertions`). This is the spec for what the skill must do; **read it before changing a skill's behavior**.
- `<plugin>-workspace/iteration-N/` — per-run outputs, `with_skill/` vs `without_skill/` configs, `grading.json`, `benchmark.md` (the A/B summary).
- `<plugin>-workspace/trigger-evals/` — trigger-rate sweeps. The reference numbers are in `structurizr-workspace/trigger-evals/README-serial-baseline.md`; compare new numbers against those, never against an older figure.

Gotchas when running evals in this repo (learned the hard way). They are written against the Claude Code CLI, which is what the eval tooling drives, but the statistical rules hold for any harness:

- Spawn eval subagents in the **foreground** (parallel calls in one message). Background agents (`run_in_background: true`) are blocked from Write/Edit in the main checkout regardless of allowlist; if you must, salvage outputs from their final messages.
- **Cap the fan-out at ~4-6 concurrent runs.** Launching a whole multi-skill eval sweep in one message (19 agents, iteration-6/12) had 8 of them killed by the stall watchdog with no progress for 600s, and the survivors reported wall-clock in the millions of ms — pure queueing. Batch the runs and re-seed any fixture directory before re-running a killed agent, since a partial run may have edited it. Wall clock from a contended sweep is not a comparable metric; tokens are.
- The allowlist that lets foreground eval agents save outputs is scoped to `*-workspace/**` in `.claude/settings.local.json` (gitignored). Extend it there for new skills, not in tracked settings. Write it as an `Edit(path)` rule — file-permission checks only match `Edit(...)`, which covers every file-editing tool (Write, Edit, NotebookEdit); a `Write(path)` rule matches nothing and triggers a startup warning.
- When transcribing Mermaid output from an agent's message, HTML-unescape `&gt;`/`&lt;`/`&amp;`.
- The reliable token metric for an optimization A/B is the deterministic `SKILL.md` body reduction; the end-to-end subagent `total_tokens` delta is in the noise (dominated by task work + reading `references/`).
- **`--num-workers` is an experimental variable, not a speed knob.** Sweeps at different worker counts are not comparable, and the bias is not uniform: it falls on queries that make the session touch the repository before acting. Same query, same code, same description — 7/10 at `--num-workers 1` against 4/10 at 10. Across a whole set it moved `structurizr` from 60% to 78% while leaving the since-removed `adr` skill at ~80%, manufacturing a 21pp "gap" that does not exist. **Use `--num-workers 1` for any number you will quote**; reserve concurrency for rough smoke tests, and never mix worker counts in one table. Every trigger number recorded here before the serial baseline of 2026-08-20 was measured at ten workers, **on every skill and both models** — the largest correction found was the removed `adr` skill on opus at 67% → 98% (+31pp), bigger than structurizr's own. See `structurizr-workspace/trigger-evals/README-21pp-analysis.md`.
- **Three runs per query cannot rank descriptions — and pooling two such sweeps does not fix it.** Per-query trigger probabilities cluster between 0.4 and 0.7, where a 3-run sample carries almost no information and the 0.5 threshold is a coin flip. Two `structurizr` queries scored 0/6 pooled across two sweeps, read as a reproducible defect, and drove two failed description rewrites; at 30 runs each they score 33% and 40%. "Reproducible across two sweeps" is an ordinary outcome at p≈0.35, not confirmation. For a **per-query** claim use `--runs-per-query 10` or more; for a **skill-level** comparison the 10-query aggregate at 3 runs (n=30) is usable but still moved 12pp on the removed `adr` skill when resampled at n=10. See `structurizr-workspace/trigger-evals/README-haiku-investigation.md`.
- **The serial baseline is `structurizr-workspace/trigger-evals/README-serial-baseline.md`** (2026-08-20): the four skills of the time (including the since-removed `adr`) on haiku and opus, `--num-workers 1`, positives at 5 runs/query and negatives at 3. Haiku: design-doc 96%, mermaid-sequence 90%, structurizr 74%. Opus: 98-100% across the board, i.e. no measurable difference between the descriptions. Compare new numbers against these, never against a pre-baseline number.
- **Two identical serial sweeps move ±4-6pp at n=50** (structurizr 78% then 74%; the removed `adr` skill 80% then 86%). A skill-level difference smaller than ~12pp at that sample size is not a finding — a 12pp gap between two skills on haiku did not separate (p = 0.21; p = 0.29 pooling two sweeps).
- **False fires are near-zero, not zero.** 1 in 240 serial negative samples: `design-doc`/opus on "write a PRD for the new referral program", 3/18 (17%) when probed. Everything else stayed at 0. Say "one adjacent-artifact query at ~17%", not "never over-triggers".
- **A negatives-only sweep cannot tell a clean zero from a broken harness** — both print 0. Splice the skill's strongest positive into the set as a canary and check it scores full marks before believing the zeros.
- **Wrap long sweeps in `systemd-inhibit --what=idle:sleep --mode=block`.** A laptop suspend mid-sweep expires the in-flight session's wall-clock timeout and records it as a non-trigger; the sweep still looks healthy. One baseline sweep was discarded for this (kept as `serial-baseline-positives-haiku-n5-SUSPENDED-DISCARDED.json`).
- **Score a trigger eval by aggregate trigger rate, not by the sweep's pass/fail count.** With the default 3 runs per query, a query whose true trigger probability sits near the threshold flips pass/fail between identical sweeps: the same description scored 19/20 and then 15/20 on the same set, same day. That 4-query swing is noise, and any conclusion drawn from a single sweep's headline is worthless. Pool `triggers`/`runs` across sweeps and compare rates over a group of queries — 0/27 versus 5/18 on the same three queries is a signal; "19 beat 17" is not.
- **Use `eval-tools/run_trigger_eval.py`, not the cached `run_eval.py` directly.** The cached script is wrong here in two ways, and each one reports a healthy-looking sweep of near-zero triggers that reads as a description regression: it does not pass `--setting-sources project,local` (the user-scope installed plugins then mask the injected candidate — positives score 0/30 on opus), and it counts a trigger only when the session picks the calling worker's own uuid, so with `--num-workers 10` recall comes out divided by ~10 (2/30 vs 14-20/30). The wrapper applies both patches to a throwaway copy and fails loudly if upstream changes. **Sweeps also degrade intermittently** — a baseline scored 22/30 and the very next sweep of the same text scored 2/30 with distribution `[0,0,0,0,0,0,0,0,1,1]`. The wrapper prints the per-query distribution and warns when no positive reaches a full run; never pool a degraded sweep into a result.
- **Run trigger evals from the repo root**, with `PYTHONPATH` pointing at the skill-creator directory — never by `cd`-ing into skill-creator first. The wrapper enforces this. The script injects the candidate description as a temp command under `<project_root>/.claude/commands/` and runs `claude -p` there, and it derives `project_root` by walking up from the cwd to the first directory containing `.claude/`. From inside the skill-creator plugin cache that resolves to `$HOME`, so the temp command lands in the *user* commands dir while the nested session evaluates a different project: every query scores 0/3, positives and negatives alike. The tell is a uniform `trigger_rate` of 0.0 with the negatives "passing" — that is a broken harness run, not a description regression. Smoke-test one obvious positive before paying for a full 20-query set.

## Per-skill notes

- **design-doc** — writes *and* reviews design docs via interactive discovery; trade-offs are mandatory (zero-cons = red flag). A user-supplied or house template **governs** (its sections become required); only without a template are sections suggestions. A review still asks the author for a template reference (templates live outside the repo), but the template is context, not a checklist: the review **never audits section presence** — it analyzes only the sections the author wrote, and proposes a section only when the existing content calls for one, as a suggestion tied to that content, in the house template's terms when known and the default catalog's otherwise. Diagram convention: the C4 architecture is authored as **Structurizr DSL** (delegating to the `structurizr` skill when present), embedded as a **PNG/SVG image reference with the DSL folded in a `<details>` block** — render via structurizr's export tooling when reachable, otherwise leave a placeholder with a one-line "render in the manual pass" note; sequence flows stay Mermaid. No "not machine-validated" disclaimer — manual review is assumed; only a *validation* disclaimer is banned. Generated prose is plain active-voice and gets a spelling pass in self-review.
- **structurizr** — authors/edits `workspace.dsl` (C4 model, Structurizr DSL v6+); validation is Docker-only (`structurizr/structurizr validate`), and a missing Docker means "delivered, not validated, here is the command" — never an install attempt. ADR authoring is routed to the team's decision log, not written by this skill. References split into always-read core (`dsl-reference`) plus conditional pattern files for token economy.
- **mermaid-sequence** — Mermaid sequence diagrams as fenced ` ```mermaid ` blocks; never invent the flow or failure paths; technical detail (endpoint/headers/payload/status) goes in Notes. Validation is local-only and ordered: mermaid-cli Docker image → local `mmdc` → "delivered, not validated, here is the Docker command". mermaid.live may be offered for preview but it renders remotely, so for diagrams carrying internal detail that is the user's call. `references/syntax.md` is always-read (version-portability + escaping gotchas).
