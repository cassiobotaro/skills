# Does technical-writing fire in a project on haiku?

**Why.** The haiku number of the trigger set is 11/50 on the positives
(`../README-full-sweep-2026-11-22.md`), and twelve captured sessions say it comes from the
harness: the queries name files and projects that are not in this repository, haiku
searches for them first, and the harness reads the first tool call. The note in
`MAINTAINING.md` says a fair haiku number needs the in-project probe on haiku. This is
that probe.

**Method.** The probe of `../in-project-2026-11-22/` with one change, the model:
`eval-tools/probe_in_project.py` on `claude-haiku-5-5`, one session per run in a project
of its own outside the repository, `technical-writing` 1.0.1 and `unslop` loaded with
`--plugin-dir` from copies outside the project, the prompt of the eval alone. Evals 1, 2,
3, 4 and 6 (with a fixture) and 5 (the diff pasted, no fixture), four sessions each, and
the canary on eval 1 twice.

**Rule, written before the runs.** As in the sonnet probe. If the canary does not invoke
the skill in both sessions the harness is broken and nothing is read. Over the five evals
with a fixture (20 sessions): the skill is reached in a project on haiku if T is 15 or
more, it is not if T is 5 or fewer, and in between there is no claim beyond the count.
Per-eval counts are listed; eval 5 is reported apart. Nothing here is a rate, and the
number replaces the 11/50 only as the in-project figure, not as a trigger-set number.

## Results

`results.json`, 26 sessions, every one on `claude-haiku-5-5` with both skills listed.
US$ 0.25 in all.

| Request | T invoked | as the first tool call |
|---|---|---|
| canary (eval 1, the skill named) | 2/2 | |
| eval 1 "improve docs/pipeline.md, …" | 4/4 | 0 |
| eval 2 "this repo has no README. write one" | 4/4 | 4 |
| eval 3 runbook for an alert, in Portuguese | 3/4 | 0 |
| eval 4 "can you review docs/webhooks.md before I publish it?" | 1/4 | 0 |
| eval 6 "improve docs/rotate-signing-key.md" | 4/4 | 1 |
| the five evals with a fixture | 16/20 | 5 |
| eval 5 PR description, the diff pasted (no fixture) | 4/4 | 4 |

**Reading, by the rule above.** The skill is reached in a project on haiku: 16 of 20,
where the rule asked for 15. The 11/50 of the trigger set is the harness, as the captured
sessions said, and not the description. Haiku reads the files first more often than
sonnet did (5 of 20 as the first call, against 16 of 20), which is the habit that made the
trigger harness score it low.

The review is the weak request: eval 4 at 1/4, against 4/4 on sonnet. The three sessions
that did not invoke the skill read the page, searched the project for code to check it
against, found none, and wrote the review directly: blocking gaps first (no steps to
verify the signature, the encoding of `X-Signature`, the retry policy), and none edited
the file. The run of eval 3 without the skill read the alert, the script and the code
and wrote the runbook in Portuguese. What the skill would have added to those four
documents is not measured here: this probe counts invocations and grades nothing.

`unslop` was invoked after `technical-writing` in three sessions of eval 1 (runs 1 to 3),
so on haiku step 5 is reached. Whether it did what step 5 asks was not read.
At least 12 of the refused calls are Reads of the plugin's `references/`, as in the
sonnet probe, because the plugins load without `--add-dir`; the others were not
classified.
