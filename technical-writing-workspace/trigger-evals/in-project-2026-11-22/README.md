# Does technical-writing fire when the file is in the project?

**Why.** The trigger harness runs in this repository, without a fixture, so its positives
either paste the text or ask for a new document. On 2026-11-22 that harness could not see
that `design-doc` never won a request to update a file that was in the project
(`design-doc-workspace/trigger-evals/README-update-clause-2026-11-22.md`). The same day,
a probe run for `design-doc` gave "A gente subiu o limite do export… Atualiza a
documentação." to sixteen sessions in a project with `docs/pipeline.md` and
`technical-writing` installed: it was invoked in one. Every behavioral number of this
skill comes from a brief that tells the session to read it, so nothing so far says
whether it is reached at all in a project.

**Method.** `run.py`, `claude -p` on `claude-sonnet-5-5`, one session per run in a
project of its own outside the repository (a fresh git repository with the eval's
fixture), `technical-writing` 1.0.1 and `unslop` loaded with `--plugin-dir` from copies
outside the project, the prompt of the eval alone. The six evals of
`../../evals/evals.json`, four sessions each. Five have a fixture; eval 5 pastes a diff
and has none, which is the situation of the trigger harness and serves as the contrast.

Counted from the transcript: T, the Skill tool was called with `technical-writing`;
whether that call was the session's first tool call; F, a file of the plugin was touched
without the Skill tool (expected 0).

**Canary.** Two sessions get eval 1's prompt with "Use the technical-writing skill."
before it. If they do not invoke the skill the harness is broken and the zeros mean
nothing.

**Rule, written before the runs.** Four sessions per request rank nothing; the claim is
about the pool. Over the five evals with a fixture (20 sessions): the skill is reached in
a project if T is 15 or more, it is not if T is 5 or fewer, and in between there is no
claim beyond the count. The per-eval counts are listed, and an eval at 0/4 or 4/4 is
named as such. Eval 5 is reported apart. Nothing here is a rate.

## Results

`results.json`, 26 sessions, every one on `claude-sonnet-5-5` with both skills listed.

| Request | T invoked | as the first tool call |
|---|---|---|
| canary (eval 1, the skill named) | 2/2 | 2 |
| eval 1 "improve docs/pipeline.md, …" | 4/4 | 4 |
| eval 2 "this repo has no README. write one" | 4/4 | 4 |
| eval 3 runbook for an alert, in Portuguese | 4/4 | 4 |
| eval 4 "can you review docs/webhooks.md before I publish it?" | 4/4 | 0 |
| eval 6 "improve docs/rotate-signing-key.md" | 4/4 | 4 |
| the five evals with a fixture | 20/20 | 16 |
| eval 5 PR description, the diff pasted (no fixture) | 4/4 | 4 |

**Reading, by the rule above.** The skill is reached in a project: 20 of 20, where the
rule asked for 15. In eval 4 the session reads the file and then invokes the skill, in
all four runs. The worry that sent this probe out does not hold for the requests the
skill was written for.

F as defined counted twelve sessions (evals 2, 3 and 5, four each), and none of them is
what F was meant to catch: each is a Read of `references/documents.md` made after the
Skill call. Loaded with `--plugin-dir` and without `--add-dir`, those reads were refused
(19 refused calls on the plugin's files over those twelve sessions, 13 by Read and 6 by
Bash, next to 5 other refused Bash calls), so the sessions of evals 2, 3 and 5 worked
without the reference. That does not touch the count of invocations, and it is one more
reason not to grade a document from this harness.

**The request that raised the question** was run afterwards in the same harness, eight
sessions (`results-one-number-update.json`): "A gente subiu o limite do export de 100 mil
pra 250 mil linhas. Atualiza a documentação.", in the `exporter` fixture. T is 0/8. Every
session opened `docs/pipeline.md`, changed the one number and said so; several added
that the code still has the old limit. With the 1/16 of the `design-doc` probe that is
1 of 24. So the skill is not consulted for a change of one value in an existing page,
and it is for every request that asks to write, improve or review one. Whether that is a
miss is a decision about the skill and not a measurement: `code-comments` chose to claim
the one-line change (1.1.0), and what this skill would add to a number that changed is
not on any check of its eval set. The description was not changed.

**Limits.** Four sessions per request measure no rate; 20/20 against 0/8 separates
"every time" from "never" for these requests and no others. Only `technical-writing` and
`unslop` were installed: this says nothing about which skill wins when `explain` or
`design-doc` is installed too, apart from the 1/16 above.

**Cost.** 34 sessions, US$ 2.16.
