# Does adr fire when the log is in the project?

**Why.** The trigger harness runs in this repository, which has no decision log, so it
cannot measure a request about records that are in the project. On 2026-11-22 that blind
spot hid a miss of `design-doc` (a request to update a shipped design doc invoked no skill
in 16 of 16 sessions and the document was rewritten). The closest case here is the one the
description of `adr` argues about: superseding a record "looks like a one-line edit".

**Method.** `eval-tools/probe_in_project.py`, `claude -p` on `claude-sonnet-5-5`, each
session in a project of its own outside the repository with the eval's fixture, `adr` and
`unslop` loaded with `--plugin-dir`, the prompt of the eval alone. Four sessions each on
four evals of `../../evals/evals.json` that have a log in the fixture:

- 3, supersede an existing record (three files under `doc/adr`);
- 4, a new record in a project whose `.adr-dir` points elsewhere ("Documenta como ADR…");
- 6, "Registre uma decisão…" in an English log, the word ADR never said;
- 12, "Record this decision…", the word ADR never said.

Two canary sessions get eval 3 with "Use the adr skill." before it.

**Rule, written before the runs.** Over the 16 sessions: the skill is reached in a project
if it is invoked in 12 or more, it is not if 4 or fewer, and in between there is no claim
beyond the count. Per-eval counts are listed, and an eval at 0/4 is named. Four sessions
per request measure no rate. The probe counts invocations and grades nothing: whether a
session that did not invoke the skill broke the log is read from the files it changed and
reported as an observation.

## Results

`results.json`, 18 sessions, every one on `claude-sonnet-5-5` with both skills listed.

| Request | `adr` invoked | as the first tool call |
|---|---|---|
| canary (eval 3, the skill named) | 2/2 | 2 |
| eval 3, supersede an existing record | 4/4 | 4 |
| eval 4, new record, `.adr-dir` elsewhere | 4/4 | 4 |
| eval 6, "Registre uma decisão…" | 4/4 | 4 |
| eval 12, "Record this decision…" | 4/4 | 4 |
| all four | 16/16 | 16 |

**Reading, by the rule above.** The skill is reached in a project: 16 of 16, always as
the first tool call, the supersede included and the two requests that never say "ADR"
included. Nothing to change. Four sessions per request measure no rate.

**Cost.** 18 sessions, US$ 1.37.
