# iteration-16 — the AGENTS.md leak, measured on the scope A/B of iteration-9 (no skill change)

**Question.** Until 2026-11-20 `AGENTS.md` carried one note per skill, and the note on
`adr` ended: "A scope check up front hands an open design to `design-doc`, refuses to
record a choice not yet made, and leaves `!adrs` wiring to `structurizr`." A host loads
`AGENTS.md` into every session, so every executor of iteration-9 read it, in both arms,
including the 1.3.2 arm whose skill has no scope section. Did that note supply the
design-doc hand-off that 1.3.2 showed in one run of two on eval 8?

**Method.** Three cells, four runs each, eval 8's prompt and iteration-9's executor brief
word for word (paths changed). Executor `claude-sonnet-5-5`, read back from each session.

| Cell | Skill | AGENTS.md text in context |
|---|---|---|
| cell-a | 1.3.2 (`../skill-snapshot-1.3.2`) | as committed at 2bc0e04, with the per-skill notes |
| cell-b | 1.3.2 | as trimmed on 2026-11-20, no per-skill notes |
| cell-c | 1.4.0 (`../skill-snapshot-1.4.0`) | trimmed |

The executors are headless sessions (`claude -p`, `run.py`), not subagents: a probe showed
that a subagent of the session that edited `AGENTS.md` still gets the old text. Each
session starts in a directory holding one `AGENTS.md` (`ctx-a` the old file, `ctx-b` the
trimmed one) below the repository root, whose own trimmed `AGENTS.md` loads too, so the
cells differ by the removed text only. A zero-tool probe confirmed it on
claude-haiku-5-5: "scope check up front" in context from `ctx-a` (32,426 context tokens),
absent from `ctx-b` (26,819). Both directories were deleted after the runs, because a file
named `AGENTS.md` left there would load into any session that works in this folder;
`git show 2bc0e04:AGENTS.md` restores the old one. Cell and directory names are neutral so
that no path names the condition. User-scope plugins were loaded, as in iteration-9, so
the installed `design-doc` skill is in every session's skill list.

Checks: the seven of eval 8 in `../evals/checks-baseline.json`, unchanged, frozen with the
prediction in `checks.json` before the first run. 8.4 from the bytes on disk; the other
six by `claude-opus-5-5`, three passes per packet, met only when unanimous (`grade.py`).
The four eval-8 outputs of iteration-9 went through the same batch, since the packet now
carries the invention anchors. A packet does not name its cell (`judge-map.json`).

**Results** (runs meeting the check / runs).

| Check | cell-a: 1.3.2, old | cell-b: 1.3.2, trimmed | cell-c: 1.4.0, trimmed | iteration-9 1.3.2 | iteration-9 1.4.0 |
|---|---|---|---|---|---|
| 8.1 nothing decided yet | 4/4 | 4/4 | 4/4 | 2/2 | 2/2 |
| 8.2 an ADR records a made decision | 4/4 | 4/4 | 4/4 | 2/2 | 2/2 |
| 8.3 in English | 4/4 | 4/4 | 4/4 | 2/2 | 2/2 |
| 8.4 no file written | 4/4 | 4/4 | 4/4 | 2/2 | 2/2 |
| 8.5 names a design doc | 4/4 | 3/4 | 4/4 | 1/2 | 2/2 |
| 8.6 decisions become ADRs afterwards | 4/4 | 4/4 | 4/4 | 1/2 | 2/2 |
| 8.7 nothing invented | 4/4 | 4/4 | 4/4 | 2/2 | 2/2 |
| all | 28/28 | 27/28 | 28/28 | 12/14 | 14/14 |

No judge split in 96 verdicts. Observed afterwards, not frozen (`timing.json`, by script):

| Per run | cell-a | cell-b | cell-c |
|---|---|---|---|
| Bash calls inspecting the repository | 0, 0, 0, 0 | 2, 2, 2, 4 | 0, 0, 0, 0 |
| turns | 3, 3, 3, 3 | 5, 4, 4, 7 | 3, 3, 3, 3 |
| reply names the `design-doc` skill | 0/4 | 0/4 | 4/4 |
| reply words | 332, 359, 257, 301 | 292, 317, 280, 307 | 186, 212, 211, 213 |
| total tokens (thousands) | 109, 109, 109, 109 | 157, 124, 124, 192 | 92, 92, 92, 92 |

- **The frozen checks do not separate the cells.** The prediction for "the note supplied
  it" was 8.5 in 0/4 runs of cell-b; it is 3/4. The one miss (run-4) offers only a
  `Proposed` ADR and never mentions a design doc.
- **1.3.2 names a design doc without being told to.** Its `SKILL.md` does not contain the
  word "design", and seven of its eight headless runs point to a design doc anyway, with or
  without the note. The skill list and the model's own judgment are enough.
- **What the old AGENTS.md did change is the route.** With it, 1.3.2 read the skill and
  replied, as 1.4.0 does. Without it, all four runs first looked for the decision log
  (step 1 of the skill) and then declined. That is every time against never, on something
  nobody predicted; and the old file differs from the trimmed one by the eval rules as
  well as the notes, so this run cannot say which part did it.
- **The scope section's own effect** is in the second table: it names the skill (4/4
  against 0/8), skips the repository inspection, and gives a reply a third shorter for
  fewer tokens. Check 8.5 accepts any mention of a design doc, so it does not see this.
- **The lean judge agrees with iteration-9's.** Its verdicts on the four old outputs are
  the ones the subagent judges gave: 8.5 and 8.6 unmet on `old_skill/run-2`, all else met.

**Reading.** On eval 8 the leak did not manufacture the result iteration-9 reported, and
it did not hide a difference on the frozen checks: 1.3.2 meets them with either file. The
"one run of two" of iteration-9 looks like the low end of a rate that is high (7 of 8
here), not like a skill that lacks the behavior. So the scope section is not what makes
the model decline or point to a design doc on this prompt; what it buys is the named
skill and a shorter path to the answer. The leak is still real as a cost and as a change
of behavior (the inspection), which is reason enough to keep `AGENTS.md` free of it.

**Limits.** One eval, one executor model, four runs per cell: no rate is measured. The
harness differs from iteration-9's (headless against subagent), so cell-a's 4/4 against
iteration-9's 1/2 on 8.5 compares two harnesses as much as anything, and at these sizes
it is not a difference (Fisher p = 0.33). The inspection finding is post hoc. Two cell-b
runs had Bash calls denied (compound `cd … && ls`, a heredoc into `response.md`); none
was an attempt to write an ADR, so 8.4 stands. Evals 9 and 10 were not re-run, and
`design-doc` iteration-26, whose arms also shared a leaked note, was not either.

**Cost.** Executors 12 sessions, 1.40 M tokens summed over turns, US$ 0.92 (US$ 0.065 to
0.095 per run). Judges 48 calls, 0.13 M tokens, US$ 0.92: about 2.8 k tokens per call
against the ~43 k of a subagent judge. Both billed to the API key at list price. The
executor transcripts were not kept.
