# Is unslop skipped when called on opus too?

**Why.** Every count of `../called-by-skill-2026-11-23/README.md` (cells A to D) ran on
`claude-sonnet-5-5`, and the earlier probe on haiku. The author's own sessions run on
opus, and no session on opus has had `unslop` installed (the opus batches of
`design-doc-workspace/iteration-28/` ran without it). If opus follows the current text,
the skip is a sonnet behavior, and that weighs on whether the calling skills' text should
change.

**Method.** Cell A of the A/B, on `claude-opus-5-5`: `technical-writing` and `unslop`
from the repository (`technical-writing` 1.0.1, `explain` 1.0.2, texts unchanged),
`eval-tools/probe_in_project.py --model claude-opus-5-5`, each session in a fresh git
repository under the session scratchpad.

- `technical-writing` evals 1, 2 and 3, four sessions each, `--strip 2`.
- `explain` eval 7, four sessions, `--strip 1`.

Each run has its two canary sessions. Counted: U, `unslop` invoked with the Skill tool
after the calling skill and before the reply, over the sessions that invoked the calling
skill. The model is read back from each transcript.

**Rule, written before the runs.** Over the twelve `technical-writing` sessions: opus
skips it as sonnet does if U ≤ 3 (sonnet, cell A: 1/12); opus follows the current text if
U ≥ 8; in between there is no claim beyond the count. `explain` eval 7 is reported
apart, named at 0/4 or 4/4 (sonnet: 0/4). Replies that give a reason for a skip are
quoted. Four sessions per request measure no rate.

## Results

`tw-a/`, `explain-a/`: 20 sessions, every one on `claude-opus-5-5` (read back from each
transcript), no errors, canaries 2/2 and 2/2.

| Request | U, sonnet (cell A) | U, opus |
|---|---|---|
| `technical-writing` eval 1, revise `docs/pipeline.md` | 0/4 | 4/4 |
| `technical-writing` eval 2, write the README | 0/4 | 4/4 |
| `technical-writing` eval 3, write the runbook in Portuguese | 1/4 | 4/4 |
| `technical-writing`, the twelve | 1/12 | 12/12 |
| `explain` eval 7, simplify the summary | 0/4 | 4/4 |

The canaries invoked `unslop` too (4 of 4).

**Reading, by the rule above.** Opus follows the current text: U = 12/12, where the rule
asked for 8. `explain` eval 7 is at 4/4.

**The order.** Every `technical-writing` session is `Skill(technical-writing)`, the
repository read, the first `Write` (sometimes one `Edit`), then `Skill(unslop)`, and in
ten of twelve one or more `Edit`s after it: the pass of step 5, after the draft is on
disk, as the text asks. Every `explain` session is `Skill(explain)`, `Read` of the
summary, `Skill(unslop)`, then the reply: `unslop` loaded before the text is written,
which is the order cell D had to ask for on sonnet. What the `unslop` edits changed was
not read or judged here.

**What this says.** The skip measured in cells A to D is a sonnet behavior (and haiku's,
3 of 17 in the earlier probe): the same texts that sonnet skips are followed by opus in
every session. A change to the calling skills' text is a change for the smaller models;
it would need to keep opus at this count, which no run of C or D on opus has checked.

**Limits.** Four sessions per request measure no rate. `references/` refused, as in every
probe. Thinking blocks redacted.

**Cost.** 20 sessions, US$ 6.33 (`technical-writing` 5.10, `explain` 1.23).
