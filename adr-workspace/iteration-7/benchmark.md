# iteration-7 — gate for the redundancy cut (1.2.2)

**Question.** Rule 2 (the adr-tools scaffolding stays canonical English while the prose follows
the log's language) was restated with its full rationale in eight places across `SKILL.md`:
the contract rule itself, two bullets in "The format — exact", the link-line bullet, the
fresh-log step, the supersede step, the self-review checklist, and the hand-off. 1.2.2 keeps
the canonical statement — including its concrete failure modes — and replaces the seven
re-explanations with short `(rule 2)` pointers, so the *reminder* survives at every point of
use while the repeated *reasoning* goes away.

Does the skill still apply the rule when it is only pointed at rather than re-argued?

**Method.** All seven evals, one `with_skill` run each, against the working-tree skill (not the
installed plugin). Run in two batches of four and three to stay under the concurrency ceiling.
Each eval was then run a **second** time (see "Variance" below). No baseline runs: iteration-6 already scored the full set at 41/41 against 1.2.1 with the
corrected assertions, so that is the comparison.

Grading combined a mechanical script (`check_mechanical.py`, committed alongside) with
file-level inspection. The script decides everything reducible to bytes — canonical heading
set and order, the English `Date:` label, ISO date equal to today for new files and *unchanged*
for fixture files, H1/filename number agreement, slug derivation, Status-section shape, link
line well-formedness, legacy `Superceded` spelling, blank-line discipline. Prose language,
"nothing invented", and question quality stayed with human inspection.

## Result — 41/41 (100%), no regressions; reproduced on a second pass

| Eval | Passed | Tokens |
|---|---|---|
| 1 clear-decision-fresh-repo | 8/8 | 31,232 |
| 2 vague-decision-asks | 4/4 | 24,976 |
| 3 supersede-existing-adr | 6/6 | 30,852 |
| 4 custom-dir-detection | 6/6 | 29,929 |
| 5 fresh-log-portuguese | 8/8 | 30,628 |
| 6 existing-english-log-pt-conversation | 5/5 | 29,836 |
| 7 english-regression | 4/4 | 30,875 |

Total 208,328 tokens, mean 29,761. **Mechanical failures: 0.**

## What the cut was, and what held

`SKILL.md` 14,093 → 13,035 chars (−1,058, ≈−264 tokens, **−7.5% of the body**); 260 → 249 lines.

The rule survived every place it could have been dropped:

- **Both directions of the language split.** Eval 5 (Portuguese conversation, fresh log)
  translated the seed's title and body while leaving `Date:`, the four headings and `Accepted`
  in English. Eval 7 (English conversation) reproduced the canonical seed **verbatim** — a diff
  against the reference with the date normalized is empty — proving the cut did not push the
  skill toward over-translating in the other direction.
- **Consistency outranking the conversation language.** Evals 3, 4 and 6 all faced a Portuguese
  conversation over an English log, and all three wrote English prose. Eval 6 additionally told
  the user in Portuguese *why*, and offered a whole-log migration as a separate decision.
- **The supersede mechanics.** Eval 3's edit to `0002` is a one-line diff — `Accepted` replaced
  by the `Superseded by [...]` link — with everything outside the Status section byte-identical
  and `0001`/`0003` untouched. Modern spelling; href a bare basename.
- **`.adr-dir` discovery.** Eval 4 wrote into `docs/architecture/decisions/`, created no stray
  `doc/adr`, and left both fixtures and `.adr-dir` pristine.
- **Record-don't-invent.** Eval 2 wrote no file and returned five questions. Three runs
  volunteered content they had *cut* for being unestablished — eval 6 removed "which logs every
  user out", eval 7 removed an explanation of the timezone-bug mechanism.

## Token accounting — read the two numbers separately

The **deterministic** saving is the body reduction: ≈264 tokens off every invocation that
triggers the skill, forever.

The **end-to-end** run cost did not move: 208,328 tokens here versus 207,357 in iteration-6,
a +0.5% drift *against* the direction of the saving. That is noise — per-run cost is dominated
by task work and by reading `references/examples.md`, not by the body. This reproduces the
repo's standing lesson: for an optimization A/B, the SKILL.md body delta is the metric; the
subagent `total_tokens` delta is not.

## Variance — a second independent pass

One run per eval cannot separate "the skill holds the rule" from "it got lucky". The whole set
was run a second time against the same 1.2.2 working tree, with fixtures re-seeded from
pristine (`with_skill_run2/`).

**Result — 41/41 again, 0 mechanical failures.** Every structural dimension reproduced exactly:

| Eval | Reproduced across both passes |
|---|---|
| 1 | 2 files, seed translated to PT, scaffolding EN |
| 2 | no file written, questions in PT |
| 3 | EN prose over the EN log, one-line diff on `0002`, `Supersedes` link identical |
| 4 | `.adr-dir` honored, EN prose, fixtures + `.adr-dir` pristine |
| 5 | seed translated to PT, scaffolding EN, same slug |
| 6 | EN prose despite the PT conversation, user told in PT |
| 7 | canonical seed **verbatim** both times, all EN |

Prose wording varies between passes, as it must — each run writes from scratch. What had to be
stable is the *behavior*, and it was.

### The one substantive difference

Eval 1's Decision section:

- run 1: "Vamos usar PostgreSQL como banco de dados do serviço de pedidos, **hospedado no RDS que
  a empresa já contrata**."
- run 2: "Vamos usar PostgreSQL como banco de dados do serviço de pedidos." — with RDS left in
  Context, the run stating outright that concluding the service runs *on* RDS would be its own
  inference.

The user said the company already pays for RDS *as a motive*, not that this service deploys
there. Run 1's clause is a mild, defensible inference; run 2 declined it. Both were graded as
passing "no invented facts" — the fact is in the prompt — but this is exactly the failure shape
`design-doc` 1.3.3 named: a claim nobody made, derived from one they did. It is non-determinism
in the invention dimension, not a regression from the cut (nothing in the removed text bore on
it). Worth watching in a future iteration; not worth a skill change on one observation.

### Token stability

| Pass | Total | Mean |
|---|---|---|
| run 1 | 208,328 | 29,761 |
| run 2 | 208,229 | 29,747 |

−99 tokens (−0.05%) between passes — reinforcing that end-to-end run cost is inert to a change
of this size, and that the body delta is the only meaningful number.

## Caveat on scope

−264 tokens is 7.5% of the body, well short of the ~500 initially estimated. The gap is
deliberate: the aggressive version deletes the reminders at the point of use entirely, and
evals 1, 5 and 7 exist precisely because that is where the language split gets dropped. The
pointers were kept. No further cut in this file looks worth another gate — contract rule 5
(three lines restating the tooling compatibility already covered by rule 2 and the hand-off)
is the only remaining candidate, and removing it renumbers the contract for ~30 tokens.
