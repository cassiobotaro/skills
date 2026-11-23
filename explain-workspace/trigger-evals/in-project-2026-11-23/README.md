# Does explain fire when the file is in the project?

**Why.** Every trigger number of this skill comes from the routine harness, which runs in
this repository with no fixture. Its one positive that named a file ("why does
internal/sync/worker.go take the lock twice in drain()?") scored 0/10 there because the
file did not exist, and the set now pastes the code instead
(`../serial-2026-11-21-workergo-probe-sonnet-n10.json`). So nothing says whether the
skill is reached when the file the user names is in the project. On 2026-11-22 the same
question gave 0/16 for `code-comments` and 20/20 for `technical-writing`.

**Method.** `eval-tools/probe_in_project.py`, `claude -p` on `claude-sonnet-5-5`, one
session per run in a fresh git repository under the session scratchpad holding the
eval's fixture (`--strip 1`, since this workspace's fixtures are `files/<path>`),
`explain` and `unslop` loaded with `--plugin-dir` from copies outside the project, the
eval's prompt alone. Four sessions each for the three evals of `../../evals/evals.json`
that have a fixture: 3 (why `TokenBucket` refills inside `allow()`), 7 (simplify
`estudo/resumo.md` for the family group) and 9 (improve the reply in `suporte/thread.md`).
Eval 1 ("explica o que é um mutex", no fixture) runs four times as the contrast, the
situation of the trigger harness.

Counted from the transcript: T, the Skill tool was called with `explain`, and whether
that was the session's first tool call.

**Canary.** Two sessions get eval 3's prompt with "Use the explain skill." before it. If
they do not invoke the skill the harness is broken and the zeros mean nothing.

**Rule, written before the runs.** Four sessions per request rank nothing; the claim is
about the pool. Over the three evals with a fixture (12 sessions): the skill is reached
in a project if T is 9 or more, it is not if T is 3 or fewer, and in between there is no
claim beyond the count. Per-eval counts are listed, and an eval at 0/4 or 4/4 is named
as such. Eval 1 is reported apart. `unslop` is explicit, so an invocation of it without
`explain` before it is listed as a defect of `unslop`'s description. Nothing here is a
rate.

## Results

`results.json`, 18 sessions, every one on `claude-sonnet-5-5` with both skills listed, no
errors, no permission denials, no file changed in any project.

| Request | T invoked | as the first tool call |
|---|---|---|
| canary (eval 3, the skill named) | 2/2 | 2 |
| eval 3 "why does TokenBucket refill inside allow()" | 4/4 | 4 |
| eval 7 simplify `estudo/resumo.md` for the family group | 4/4 | 3 |
| eval 9 improve the reply in `suporte/thread.md` | 4/4 | 4 |
| the three evals with a fixture | 12/12 | 11 |
| eval 1 "explica o que é um mutex" (no fixture) | 4/4 | 4 |

**Reading, by the rule above.** The skill is reached in a project: 12 of 12, where the
rule asked for 9. All three evals are at 4/4. In the one run where it was not the first
call (eval 7, run 1) the session read `estudo/resumo.md` and then invoked the skill.

`unslop` was invoked in none of the 18 sessions, so its description did not fire on its
own. That includes the four runs of eval 7, a text the skill drafts for third parties,
where `explain` says to invoke `unslop` when it is installed; this probe does not grade
the replies, so whether that step was skipped or judged unnecessary is not measured. Eval
9 asks to improve the user's own draft, where the skill does not call `unslop`. In eval 9
every session gave the improved reply in the conversation and left `suporte/thread.md`
as it was, which fits "antes de eu mandar".

**Limits.** Four sessions per request measure no rate. Only `explain` and `unslop` were
installed: this says nothing about which skill wins against `technical-writing` (eval 7
and 9 border it) or `code-comments` (eval 3). One model.

**Cost.** 18 sessions, US$ 1.34.
