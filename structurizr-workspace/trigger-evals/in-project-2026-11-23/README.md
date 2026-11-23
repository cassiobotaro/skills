# Does structurizr fire when the workspace is in the project?

**Why.** Every trigger number of this skill comes from the trigger harness, which runs in
this repository with no fixture, so a request to evolve a `workspace.dsl` that already
exists has never been measured where the file exists. That is the situation in which
`design-doc` was found to lose its update requests (0/16 in a project,
`design-doc-workspace/trigger-evals/README-update-clause-2026-11-22.md`): the session
edits the file directly.

**Method.** `eval-tools/probe_in_project.py`, `claude -p` on `claude-sonnet-5-5`, one
session per run in a fresh git repository under the session scratchpad holding the
eval's fixture (`--strip 2`, fixtures are `files/legacy-billing/<path>`), `structurizr`
and `unslop` loaded with `--plugin-dir` from copies outside the project, the eval's
prompt alone. Four sessions each for the two evals of `../../evals/evals.json` with a
fixture: 3 (evolve the existing `workspace.dsl`: production deployment on AWS and more)
and 11 (write ADR 0004 and make the `workspace.dsl` point at the ADRs). Two contrasts
without a fixture, four sessions each: eval 5 (write a new `workspace.dsl`), the
situation of the trigger harness, and eval 10 (an AWS diagram with real service icons),
which the description excludes, so the expected count there is zero. The sessions are
allowed no Docker, so the skill's validation step cannot run; this counts invocations
and grades nothing.

Counted from the transcript: T, the Skill tool was called with `structurizr`, and
whether that was the session's first tool call.

**Canary.** Two sessions get eval 3's prompt with "Use the structurizr skill." before it.
If they do not invoke the skill the harness is broken and the zeros mean nothing.

**Rule, written before the runs.** Four sessions per request rank nothing; the claim is
about the pool. Over evals 3 and 11 (8 sessions): the skill is reached in a project if
T is 6 or more, it is not if T is 2 or fewer, and in between there is no claim beyond
the count. Each eval is also named if at 0/4 or 4/4. Eval 11 asks for an ADR as well and
`adr` is not installed, so a hit there says nothing about which skill would win with
both installed. Eval 5 is reported apart. Eval 10 at 1/4 or more is listed as a false
fire to probe on its own; at 0/4 it says only that four sessions did not fire. `unslop`
invoked without `structurizr` before it is a defect of `unslop`'s description. Nothing
here is a rate.

## Results

`results.json`, 18 sessions, every one on `claude-sonnet-5-5` with both skills listed, no
errors.

| Request | T invoked | as the first tool call |
|---|---|---|
| canary (eval 3, the skill named) | 2/2 | 2 |
| eval 3 evolve the existing `workspace.dsl` | 4/4 | 4 |
| eval 11 ADR 0004 and `!adrs` in the existing workspace | 4/4 | 4 |
| evals 3 and 11 | 8/8 | 8 |
| eval 5 new `workspace.dsl` (no fixture) | 4/4 | 4 |
| eval 10 AWS diagram with real icons (excluded) | 0/4 | 0 |

**Reading, by the rule above.** The skill is reached in a project: 8 of 8, where the rule
asked for 6, as the first tool call in every one. Both evals are at 4/4. Eval 10 did not
fire in four sessions; two of them wrote a `diagrams` script (`aws_architecture.py`) and
two stopped at blocked commands. `unslop` was invoked in none of the 18 sessions.

**What the projects show, not graded.** Every session that invoked the skill tried
`docker run` for validation, was refused by the harness's permissions, and said in the
first sentence of its reply that the workspace was not validated; the two eval 5 runs
that did not try said so because the prompt states there is no Docker. That is the
skill's no-tooling path, reached because the probe allows no Docker; it is not evidence
about validation. In eval 11 the four projects have the same diff outside the new ADR:
ADR 0003's status line went from `Accepted` to `Superseded by [4. …](0004-….md)`, and
`workspace.dsl` gained `!adrs docs/adr`. `adr` was not installed, so this says nothing
about which skill takes that request when both are.

**Limits.** Four sessions per request measure no rate. One model. Only `structurizr` and
`unslop` installed.

**Cost.** 18 sessions, US$ 2.26.
