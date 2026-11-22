# iteration-17 — a no-skill baseline, the trade-off wording, and a cut (adr 1.6.0)

**Questions.** (1) Which parts of the skill does a session without it already get right?
The last no-skill baseline was iteration-1, on evals 1 to 4; every A/B since compared the
skill with an older copy of itself. (2) 1.5.0 asked for "at least one negative"
consequence and treated "zero downsides" as a red flag. The point of that rule is that a
record saying only "this is how we will do it" is worth little, and what it lacks is a
trade-off, which is not necessarily a negative consequence. Does rewording it that way
keep the ask-first behaviour? (3) Does a cut of what repeats inside the skill cost
anything?

**Change under test (1.6.0).**

- Step 2: the third ingredient is "the trade-off (what the decision gives up in exchange
  for what it gets: an alternative passed over, a cost, a constraint taken on)". When it
  is missing the skill asks what was given up or passed over, once, never supplies one,
  and if the user says there was none it writes the record with what they gave and says in
  the reply that it carries no trade-off. The self-review line "Consequences include at
  least one negative or trade-off" became "Consequences carry the trade-off the user gave.
  If they gave none and you have not asked, ask now instead of adding one."
- Steps 1 and 2 merged; step 6 (supersede/amend) folded into "Link lines", which already
  said most of it; the self-review went from eight bullets to six. Steps renumbered 1 to 6.
- `references/examples.md` lost the 30-line model ADR, and `SKILL.md` now says to read
  the file when the task needs one of its parts (seed, another language, a link pair,
  the slug table) instead of "before writing your first ADR of the session".
- `SKILL.md` 15,503 → 15,414 characters (283 → 274 lines); `examples.md` 6,561 → 4,867.
  The body did not get smaller in any way that matters: the trade-off paragraph took back
  what the merges freed.

**Method.** Three cells: `no_skill`, `skill_150` (`../skill-snapshot-1.5.0`), `skill_160`
(the working tree). Evals 1 to 7, 11 and the new eval 12, three runs per cell, one
headless session per run (`run.py`), executor `claude-sonnet-5-5` read back from each
session. Each run starts from the eval's fixture in a git repository of its own outside
this repository, so no `AGENTS.md` and no neighbouring skill is in reach of the baseline;
project directories are numbered and the skills copied to `s1` and `s2`, so no path names
the cell. User-scope plugins not loaded: no session listed an `adr` or `unslop` skill, so
the `unslop` pass of step 3 never ran. Eval 12 is two turns: a session that wrote no file
is answered once with a fixed line ("nothing else was discussed. Please record it now").

Checks frozen before any output was read: `checks.json` for evals 1 to 7 (all from bytes,
`grade.py`, results in `mech.json`), `../evals/checks-baseline.json` for evals 11 and 12
(script plus `../../eval-tools/judge.py`, `claude-opus-5-5`, three passes, unanimous;
`results.json`). Eval 6 was repeated to nine runs in both skill cells after its first
three, to look at one slug miss.

**Results** (runs meeting the check / runs).

| | no_skill | skill_150 | skill_160 |
|---|---|---|---|
| **Fresh log** (evals 1, 5, 7): decision at `doc/adr/0002-`, H1, `Date:`, English headings, Status, slug | 0/9 on each (H1 1/9) | 9/9 | 9/9 |
| seed `0001` present, well-formed, translated (1, 5) or verbatim (7) | 0/9 | 9/9 | 9/9 |
| **Existing log** (evals 3, 4, 6, 11): directory and number, H1, date, headings, blank lines, language of the log, fixtures untouched | 12/12 on each | 12/12 | 12/12 |
| supersede pair on eval 3: both Status sections, body of 0002 untouched | 3/3 | 3/3 | 3/3 |
| slug derived from the title (3, 4, 6, 11; eval 6 at nine runs) | 6/12 | 17/18 | 16/18 |
| Status holds only `Accepted` (4, 6, 11) | 4/9 | 15/15 | 15/15 |
| **Vague request** (eval 2): no file, asks | 3/3 | 3/3 | 3/3 |
| **Invention** (11.9 Context, 11.10 Decision and Consequences, 12.5) | 0/9 | 7/9 | 9/9 |
| **Eval 12**: first turn writes nothing and asks (12.1, 12.2) | 0/3 | 3/3 | 3/3 |
| final reply says the record has no trade-off (12.6) | 0/3 | 3/3 | 3/3 |
| Tokens per run, thousands | 75 | 128 | 123 |
| Runs that read `references/examples.md` | 0/27 | 32/33 | 22/33 |

No judge split in 54 calls.

**Reading.**

- **The skill is the format of a fresh log.** Without it, all nine fresh-log runs wrote
  `docs/adr/0001-<slug>.md` in a template of their own: `# ADR-0001: …` or `# 1. …`,
  Status and date as a bullet list, headings translated in Portuguese, `### Positivas` /
  `### Negativas` under Consequences, no seed. None would be read by adr-tools or `!adrs`
  as written.
- **In an existing log the baseline copies what it sees.** Directory (the `.adr-dir`
  one included), number, H1, date, headings, the log's language over the conversation's,
  and the whole supersede pair were right in every run. Two predictions in `checks.json`
  were wrong here: it did not write Portuguese into an English log, and it did remove
  `Accepted` from the superseded record. What it gets wrong is what it cannot copy: the
  slug is shortened instead of derived (6/12), and it adds Status links of its own making
  ("Builds on [2. …]" in 3/3 runs of eval 4, "Complements [2. …]: …" in 2/3 of eval 6).
- **Invention is the largest gap.** The baseline never asked for a trade-off and added
  consequences nobody stated in all six runs of evals 11 and 12 ("We take on CloudFront as
  a new dependency, including its configuration and cost"). Both skill versions asked
  first on eval 12 and then wrote only what they were given.
- **The rewording kept the behaviour and changed the question.** 1.5.0 asked "What
  downside did the team accept?"; 1.6.0 asks "What did you give up or pass over?" and
  names alternatives beside costs. On eval 11, 1.5.0 added a consequence of its own in two
  runs of three ("Files already on the app servers' local disks will need to be moved to
  S3 before those instances are replaced", which its reply called "my inference") and
  1.6.0 in none. Three runs per cell: suggestive, consistent with the old self-review line
  asking for a negative, not a measured rate.
- **The cut cost nothing that these checks see**, and bought little: 4% fewer tokens.
  Sessions in an existing English log with no link (evals 11, 12) stopped reading
  `examples.md`; the Portuguese conversations still read it.
- **A slug slip exists in both versions**: one run of nine in 1.5.0 and two of nine in
  1.6.0 dropped an article from a long title in the filename (eval 6). Not a difference.

**What this says about cutting further.** The parts a baseline already gets right in an
existing log (locating it, numbering, the template, the supersede mechanics) are the same
parts it gets wrong in a fresh one, where there is nothing to copy, so they cannot go.
What repeats inside the skill is now mostly gone. A smaller body would need an ablation
of rule 2's rationale or of the scope section, both of which were measured as carrying
weight (iterations 7, 9 and 16).

**Limits.** Three runs per cell (nine on eval 6): no rate is measured, and the invention
difference between the two skill versions rests on two runs. One executor model. Evals 8
to 10 were not run; the scope section and the hand-off they exercise were not edited. The
trigger description was not edited, so no trigger sweep was run. Language is decided by
counting function words. No check here reads tone, so these runs cannot say whether the
model ADR removed from `examples.md` mattered to it.

**Cost.** Executors 93 sessions, US$ 6.00 (no_skill 1.00, skill_150 2.59, skill_160
2.41). Judges 54 calls, 0.20 M tokens, US$ 1.19. The executor transcripts were not kept.
