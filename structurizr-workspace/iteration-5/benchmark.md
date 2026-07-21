# iteration-5 — full eval set against 1.2.0, MCP connected

**Question.** 1.2.0 moved the house-conventions skeleton into `dsl-reference.md` §15, and
eval 5 (degraded environment, no validator at all) had never been run. Does the whole set
still pass with a Structurizr MCP server connected?

**Method.** All five evals, one `with_skill` run each, against the working-tree skill (not
the installed plugin). Structurizr MCP live at `http://localhost:3000/mcp`. Eval 5 is a
degraded-environment case, so its run was told to treat the host as having no MCP, no
Docker and no CLI, and forbidden to install anything. No baseline: iteration-4 already
gated 1.2.0 against the previous version; this run measures the current version against
the assertions.

Grading was done by an independent agent that re-validated every DSL itself.

## Result — 28/28 (100%), no failures

| Eval | Passed | Tokens | Wall clock |
|---|---|---|---|
| 1 ambiguous-spec-asks-instead-of-inventing | 5/5 | 33,156 | 196s |
| 2 complete-workspace-from-clear-spec | 6/6 | 42,597 | 299s |
| 3 evolve-existing-dsl-deployment-dynamic-adrs | 6/6 | 52,207 | 1139s |
| 4 system-landscape-fintech | 6/6 | 43,177 | 293s |
| 5 no-validator-available-says-so | 5/5 | 39,165 | 167s |

Wall clock is not comparable across iterations: all 17 runs of this session (three skills)
executed concurrently, so the numbers carry queueing delay. Tokens are the meaningful cost
figure — 210,302 total, 42,060 mean.

## What the runs confirmed

- **Independent validation.** The grader re-ran `mcp__structurizr__validate` on evals 2, 4
  and 5 → `OK` for all three, and the Docker CLI on eval 3 → exit 0.
- **Eval 3 is a minimal diff.** Diffed against the seed `workspace.dsl`: purely additive.
  No identifier, view key, style or original relationship was touched.
- **Eval 1 asked instead of writing**, which `expected_output` sanctions, and said outright
  that no file had been written or validated — no fabricated validation.
- **Eval 5 (degraded)** produced the DSL, called no MCP tool, ran no `docker`, installed
  nothing, stated plainly that the file was not validated, and handed over the validate
  command.

## Environment finding: the MCP rejects `!adrs`

`mcp__structurizr__validate` fails on a workspace containing `!adrs docs/adr` with
`feature structurizr.feature.dsl.decisions is not enabled`. Eval 3 hit this, fell back to
the Docker CLI, and validated exit 0 there — the fallback chain works, but any workspace
that imports a decision log cannot be validated through this MCP server.

Also worth recording: the Docker image is `structurizr/structurizr`, not
`structurizr/structurizr-cli` (which does not exist on Docker Hub).

## Known-acceptable inspector warnings

Evals 2 and 4 ran `inspect` and surfaced its findings — missing `!docs`/`!adrs`, missing
relationship technologies — as open questions rather than inventing content. That is the
never-invent rule working, at the cost of shipping workspaces with known warnings.
