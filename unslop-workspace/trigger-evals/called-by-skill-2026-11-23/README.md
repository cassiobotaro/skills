# Why is unslop skipped when another skill says to apply it?

**Why.** `technical-writing` step 5 and `explain` section 5 say: when `unslop` is
installed, invoke it on the prose you drafted. In the in-project probes it rarely
happens: after `technical-writing`, 1 of 17 sessions on sonnet and 3 of 17 on haiku
(`technical-writing-workspace/trigger-evals/in-project-haiku-2026-11-23/README.md`);
after `explain` on eval 7, 0 of 4
(`explain-workspace/trigger-evals/in-project-2026-11-23/README.md`).

**What the transcripts say, before any new run.** The thinking blocks of those
transcripts are redacted (empty text, signature only), so the evidence is the replies.
Of the sonnet sessions of 2026-11-22 that invoked `technical-writing` and skipped
`unslop`, seven say in the reply that they did not run it, and two give the reason: "I
didn't run `unslop`, since you didn't ask for it" (canary run-2) and "I didn't run the
`unslop` skill, since you didn't ask for it by name" (eval 2 run-4). Two review sessions
offer to run it after the edits are applied. No haiku session that skipped it mentions
it. That reason is the wording of `unslop`'s own description: "Explicit only. Use this
skill when the user asks for it by name …, or when another skill tells you to apply it
…. Do not use it for a general request to write, review, improve …". A session following
`technical-writing` has a general request to write, so the description says no and the
calling skill says yes.

**Hypothesis.** The description of `unslop` is what stops the call.

**Method.** An A/B where the one variable is `unslop`'s description. Cell A loads
`unslop` from the repository. Cell B loads a copy whose description drops "Explicit
only." and says that an instruction from a skill being followed is the request (text
below; the body and references are byte-identical). `eval-tools/probe_in_project.py`
with `--plugin-src unslop=<copy>` for B, `claude -p` on `claude-sonnet-5-5`, each
session in a fresh git repository under the session scratchpad. Two pairs of runs:

- `technical-writing` 1.0.1 and `unslop`, evals 1, 2 and 3 of
  `technical-writing-workspace/evals/evals.json` (revise a page, write a README, write a
  runbook), four sessions each per cell, `--strip 2`.
- `explain` 1.0.2 and `unslop`, eval 7 of `explain-workspace/evals/evals.json` (simplify a
  summary for the family group), four sessions per cell, `--strip 1`.

Each run also has its two canary sessions (the calling skill named), which count the
calling skill and are not part of U.

Counted from the transcript: U, `unslop` invoked with the Skill tool after the calling
skill, over the sessions that invoked the calling skill.

**Rule, written before the runs.** Over the twelve `technical-writing` sessions per cell:
the description is the cause if B has U ≥ 6 and A has U ≤ 3; it is not the cause, or not
alone, if B has U ≤ 3; in between there is no claim beyond the counts. Eval 7 of
`explain` (four per cell) is reported apart. Every reply that mentions `unslop` is quoted
when it gives a reason. Nothing here is a rate, and nothing here says whether the B text
fires `unslop` on requests that do not name it: that is the routine trigger check, to run
before any change ships.

**Cell B's description:**

> Edit prose to remove the patterns that mark a text as machine-written, in English or
> Brazilian Portuguese, without changing its meaning and without adding a fact. Use this
> skill in two cases. When the user asks for it by name ("unslop this", "/unslop", "run
> unslop on the README", "passa o unslop nesse texto"). And whenever a skill you are
> following tells you to apply it to prose that skill produced: that instruction is the
> request, and the user does not have to name unslop. Outside those two cases, do not use
> it for a general request to write, review, improve, shorten, translate, or proofread a
> text.

## Results

`tw-a/`, `tw-b/`, `explain-a/`, `explain-b/`: 40 sessions, every one on
`claude-sonnet-5-5`, no errors. The calling skill was invoked in every session (canaries
2/2 in each run), and every `technical-writing` session wrote its document.

| Request | U, cell A (current text) | U, cell B |
|---|---|---|
| `technical-writing` eval 1, revise `docs/pipeline.md` | 0/4 | 0/4 |
| `technical-writing` eval 2, write the README | 0/4 | 0/4 |
| `technical-writing` eval 3, write the runbook in Portuguese | 1/4 | 3/4 |
| `technical-writing`, the twelve | 1/12 | 3/12 |
| `explain` eval 7, simplify the summary | 0/4 | 0/4 |

**Reading, by the rule above.** B has U = 3, so the description is not the cause, or not
alone. The difference is two sessions, both on eval 3, and it separates nothing.

**What the replies say.** In cell A, one of the skipped sessions gives the reason seen on
2026-11-22: "Não rodei o `unslop` no texto, porque você não o pediu" (eval 3 run-3); three
others say they did not run it, with no reason. In cell B no reply gives that reason or
any other; three say they did not run it ("Skills not run: `unslop` and the skill's
`documents.md` reference"). No `explain` reply in either cell mentions `unslop` at all.
So B removed the stated reason without making the step happen: what the replies say about
a skip is not what decides it.

**Where the step happens.** Every invocation, in both cells, is on eval 3; pooled, 4 of
8 there against 0 of 16 on evals 1 and 2. With the sonnet probe of 2026-11-22 (the same
setup as cell A), it is 5 of 12 on eval 3 and 0 of 24 on evals 1 and 2. Eval 3 is the one
request for a long new document in Portuguese; eval 1 is a revision and eval 2 a README,
both in English. This probe cannot say which of those differences matters, and no run
varied them.

**Limits.** Four sessions per request measure no rate. One model. In every session the
plugin's `references/` were refused (no `--add-dir`), so `technical-writing` worked
without `references/documents.md` and every `unslop` pass without its vocabulary file;
several replies say so. Whether that loss of the references changes how much of the
skill a session follows was not tested. The thinking blocks are redacted.

**What this leaves.** The next variable is the calling skill's own text: step 5 sits at
the end of a long procedure, and in `explain` the instruction is one paragraph after the
section on texts for other people. Not run here. B is not adopted, and the routine
trigger check that a change to `unslop`'s description would need was not run.

**Cost.** 40 sessions, US$ 4.81.

## Second variable: the calling skill's text (cell C)

**Decided by the author on 2026-11-23:** `unslop` should run when another skill calls it.
So the next variable is the instruction in the calling skill, with `unslop` as it is.

**Cell C.** `technical-writing` and `explain` loaded from copies (`--plugin-src`) whose
instruction to invoke `unslop` is reworded and moved; `unslop` from the repository.
Everything else is the setup of cell A, which is the control: same day, same CLI, same
evals and counts.

- `technical-writing`, step 5: "invoke it now, before you reply, … The user's request for
  the document is the request for this step: they will not name `unslop`, and they do not
  have to. Skip it only when it is not installed or when the turn wrote no prose." The
  Deliver section opens with "Deliver after step 5, `unslop` included when it is
  installed."
- `explain`, section 5: the paragraph that came after **Deliver** becomes step 9 of the
  numbered pass, before delivering, with the same two sentences about the request and the
  same exclusions (an explanation, the user's own draft); "Before sending" says "steps 8
  and 9".

**Rule, written before the runs.** Over the twelve `technical-writing` sessions: the text
is the fix if C has U ≥ 8 (A had 1); it has no effect if C has U ≤ 3; in between there is
no claim beyond the count. `explain` eval 7, four sessions: reported apart, named if 0/4
or 4/4 (A had 0/4). What `unslop` changed is read from the transcripts, not judged; a pass
that removes a fact, an actor, a command or a TODO is listed. Before a change ships: a
behavioral run of the affected evals, since a new step now runs on every document.

### Cell C, results

`tw-c/`, `explain-c/`: 20 sessions, no errors, canaries 2/2 and 2/2, US$ 2.39.

| Request | U, A (control) | U, C |
|---|---|---|
| `technical-writing` eval 1, revise `docs/pipeline.md` | 0/4 | 0/4 |
| `technical-writing` eval 2, write the README | 0/4 | 1/4 |
| `technical-writing` eval 3, write the runbook in Portuguese | 1/4 | 4/4 |
| `technical-writing`, the twelve | 1/12 | 5/12 |
| `explain` eval 7 | 0/4 | 0/4 |

**Reading, by the rule.** U = 5 sits between 3 and 8: no claim beyond the count. Eval 3
is at 4/4 and eval 1 at 0/4.

**The tool sequences.** Every `explain` session of C is `Read`, then `Skill(explain)`,
then the final reply, which holds the text: the text exists only in the reply, so a pass
"before delivering" needs a tool call between drafting and replying, and none made it.
The `technical-writing` sessions that skipped it are the same shape one step longer: one
`Write` of the document, then the reply ("I didn't run anything, and I didn't run
`unslop`", eval 1 run-2). The one eval 2 session that called it did so after the `Write`
and changed nothing ("I checked it against the unslop rules and made no edits").

**What this points at.** A pass placed after the draft asks for one more turn after the
work looks done. pstack, the source of `unslop`'s catalog, does not schedule one: its
callers say "Write it through `unslop`" where they define the output
(`cursor/plugins`, `pstack/skills/teach`, `blast-radius`, `recall`; read on 2026-11-23,
not measured there). Cell D tests that order: load `unslop` before drafting and write by
its rules.

## Third variable: unslop before the draft (cell D)

**Cell D.** `technical-writing` and `explain` from copies; `unslop` from the repository;
setup of cell A, which stays the control.

- `technical-writing`: step 4 opens with "When the `unslop` skill is installed, invoke
  it before you draft, and write the draft by its rules: the user's request for the
  document is the request for this, and they will not name `unslop`." Step 5's first
  paragraph becomes a check that the prose follows those rules, with the same sentences
  on the catalog and on a missing fact.
- `explain`: in section 5, the sentence "Then draft, and pass over the draft in this
  order" is preceded by the same instruction to invoke `unslop` before drafting; the
  paragraph after **Deliver** is removed, its exclusions moved with it.

**Rule, written before the runs.** U now counts `unslop` invoked after the calling skill
and before the reply, at any point. Over the twelve `technical-writing` sessions: D is
the fix if U ≥ 8; no effect if U ≤ 3. `explain` eval 7 apart, named at 0/4 or 4/4. The
order (before or after the first `Write`) is listed per session.

### Cell D, results

`tw-d/`: 14 sessions, canaries 2/2, US$ 1.64. U = 0/12 (0/4 on each of evals 1, 2 and
3, eval 3 included, where A had 1/4 and C 4/4): no session invoked `unslop` before or
after drafting. By the rule, D has no effect, and it lost what C gained on eval 3.
`explain-d/`: invalid, every session ended with an error and no transcript content
(canary 0/2, US$ 0), probably the account's usage limit; not re-run.

**Standing after A, B, C and D.** Only C moved the count (5/12, between the bounds).
Nothing is adopted; the skills are unchanged. Open: re-run `explain-d`, and a C variant
for evals 1 and 2 or more runs of C before any decision.
