# Does mermaid-sequence fire when the code is in the project?

**Why.** Every trigger number of this skill comes from the trigger harness, which runs in
this repository with no fixture. Its positives describe the flow in the message. A
request to diagram code that is in the project ("look at our API's code and draw what
happens on POST /orders") has never been measured where the code exists, and in that
situation a session may read the files and write the diagram without consulting the
skill, which is what `code-comments` did (0/16,
`code-comments-workspace/trigger-evals/in-project-2026-11-22/README.md`).

**Method.** `eval-tools/probe_in_project.py`, `claude -p` on `claude-sonnet-5-5`, one
session per run in a fresh git repository under the session scratchpad holding the
eval's fixture (`--strip 2`, fixtures are `files/order-api/<path>`), `mermaid-sequence`
and `unslop` loaded with `--plugin-dir` from copies outside the project, the eval's
prompt alone. Only one eval of `../../evals/evals.json` has a fixture, eval 2 (the
`order-api` code, a diagram of POST /orders), so every request runs six times instead of
four. Two contrasts without a fixture: eval 4 (an upload flow described in the message),
the situation of the trigger harness, and eval 6 (a Mermaid flowchart), which the
description does not cover, so the expected count there is zero. The sessions are
allowed no Docker, so the validation step cannot run; this counts invocations and grades
nothing.

Counted from the transcript: T, the Skill tool was called with `mermaid-sequence`, and
whether that was the session's first tool call.

**Canary.** Two sessions get eval 2's prompt with "Use the mermaid-sequence skill."
before it. If they do not invoke the skill the harness is broken and the zeros mean
nothing.

**Rule, written before the runs.** Six sessions rank nothing; the claim is about eval 2
alone and is no rate. The skill is reached when the code is in the project if T on eval
2 is 5 or more, it is not if T is 1 or fewer, and in between there is no claim beyond
the count. Eval 4 is reported apart. Eval 6 at 1/6 or more is listed as a false fire to
probe on its own. `unslop` invoked without `mermaid-sequence` before it is a defect of
`unslop`'s description.

## Results

`results.json`, 20 sessions, every one on `claude-sonnet-5-5` with both skills listed, no
errors.

| Request | T invoked | as the first tool call |
|---|---|---|
| canary (eval 2, the skill named) | 2/2 | 2 |
| eval 2 POST /orders from the `order-api` code | 6/6 | 6 |
| eval 4 upload flow described in the message (no fixture) | 6/6 | 6 |
| eval 6 Mermaid flowchart (not covered) | 0/6 | 0 |

**Reading, by the rule above.** The skill is reached when the code is in the project: 6
of 6 on eval 2, where the rule asked for 5, as the first tool call in every one, before
any file of the project was read. Eval 6 did not fire in six sessions; each answered with
a `flowchart TD` block and no tool call. `unslop` was invoked in none of the 20 sessions.

**What the sessions show, not graded.** The plugin's `references/syntax.md` is outside
the project and was refused to every session that tried to read it, and Docker and
`mmdc` were refused too; so every diagram was written from the skill body alone, and
every reply that invoked the skill says the diagram was not validated, with the command
to run elsewhere (read in the four replies that open with the diagram; the rest say it in
their first sentence). One session of eval 2 left a `post-orders.mmd` in the project; the
others changed no file.

**Limits.** Six sessions on one request measure no rate, and eval 2 is the only request
with code in the project. One model. Only `mermaid-sequence` and `unslop` installed.

**Cost.** 20 sessions, US$ 1.65.
