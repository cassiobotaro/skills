# Does code-comments fire when the code is in the project?

**Why.** The trigger set of this skill pastes the code in each query, because this
repository has no code for a session to open, and the harness then counts whether the
skill is consulted before the answer. In a project the session can open the file and
edit it, which is the situation the skill is for and the one the harness cannot show. On
2026-11-22 that blind spot hid a miss of `design-doc`.

**Method.** `eval-tools/probe_in_project.py`, `claude -p` on `claude-sonnet-5-5`, each
session in a project of its own outside the repository with the eval's fixture,
`code-comments` 1.1.0 loaded with `--plugin-dir`, the prompt of the eval alone. Four
sessions each on four evals of `../../evals/evals.json`, none of which mentions comments:

- 1, add a function to an existing file;
- 2, fix a bug (the request is in Portuguese);
- 4, change one constant ("wait 45 seconds between polls instead of 10"), the one-line
  change the 1.1.0 clause is about;
- 5, change what a function ignores.

Two canary sessions get eval 1 with "Use the code-comments skill." before it.

**Rule, written before the runs.** Over the 16 sessions: the skill is reached in a project
if it is invoked in 12 or more, it is not if 4 or fewer, and in between there is no claim
beyond the count. Per-eval counts are listed, and an eval at 0/4 is named. Whether the
call comes before the first edit is counted too, since the skill is about the comments of
the change and a call after the code is written is late. Four sessions per request
measure no rate, and nothing is graded.

## Results

`results.json`, 18 sessions, every one on `claude-sonnet-5-5` with the skill listed as
`code-comments:code-comments`.

| Request | `code-comments` invoked |
|---|---|
| canary (eval 1, the skill named) | 2/2 |
| eval 1, add a function to an existing file | 0/4 |
| eval 2, fix a bug | 0/4 |
| eval 4, change one constant | 0/4 |
| eval 5, change what a function ignores | 0/4 |
| all four | 0/16 |

**Reading, by the rule above.** The skill is not reached in a project: 0 of 16, where the
rule's floor was 4, and the canary shows the harness can invoke it. Every session opened
the file, made the change and replied. The routine check of the same description gives
27/30 on the positives, six of which never mention comments, with the code pasted in the
message: there the session cannot edit a file
and consults the skill, and here it can and does not. For this skill that is the whole
case, since "whenever you write or modify code" in a project always has a file to edit.

What this does not say: that the comments written in these sessions are bad. They were
not graded, and iteration-1 found that a session without the skill already writes no
restating or narrating comment and keeps the file's language (79/86 against 84/86); the
one thing only the skill did was to suggest a rename without making it. So the cost of
the miss is that small difference, on every code change.

## The comments these sessions wrote (2026-11-23)

**Why.** The question behind the skill is whether a session writes bad comments, not
whether it invokes the skill. The transcripts hold every `Edit` of the 16 sessions, so
the comments can be read at no cost. They were read by hand against the comment
assertions of each eval in `../../evals/evals.json`, by the maintainer's session and not
by a judge; the code-correctness assertions were looked at only as far as the edited
lines show.

**Isolation.** The probe passes `--setting-sources project,local` and the machine has no
`~/.claude/CLAUDE.md`, so no user instruction reached these sessions.

| Eval | What the assertions ask of the comments | Met |
|---|---|---|
| 1, new function | no restating or narrating comment; a docstring says what the signature does not, in English | 4/4: the suffix scheme and an input/output example in each docstring |
| 2, fix a bug | the stale "weekends included" comment rewritten or removed; English; the user's reason only; no claim about holidays | 4/4: rewritten with the bank-settles-on-business-days reason; every reply says holidays are not handled |
| 4, change one constant | no reason for 45, no "was 10" | 4/4: the line alone changed |
| 5, ignore negative rows | a comment on the condition gives the user's reason, not the condition | 4/4 |
| 5, the name `d` | the reply suggests a descriptive name without renaming | 0/4 |

One borderline: run-4 of eval 2 writes `# Saturday` and `# Sunday` next to
`weekday() == 5` and `== 6`. They decode a magic number rather than restate the line; the
other three runs wrote `>= 5` with no such comment.

**Reading.** Without the skill, on these four requests and on sonnet, the sessions wrote
no comment the skill exists to prevent. The 0/16 invocations cost the rename suggestion,
which matches iteration-1 (79/86 without the skill, 84/86 with it). This does not cover
haiku, nor code that already carries several stale comments near the change, which is
where a bad comment is most likely and which only eval 2 exercises.

**A first run was discarded** (`results-wrong-paths-DISCARDED.json`, 1/16). The fixtures
of this workspace are `files/<path>` and not `files/<fixture>/<path>`, and the probe put
`reports/usage.py` at `usage.py`, so the prompts named paths that did not exist. The
helper got `--strip` for it and the run was repeated with `--strip 1`.

**Limits.** Four sessions per request measure no rate; 0/16 against 2/2 is of the "never
against every time" kind, on four requests, with this skill installed alone, on one
model, in headless single-request sessions.

**Cost.** 18 sessions, US$ 0.51, and US$ 0.69 for the discarded run.
