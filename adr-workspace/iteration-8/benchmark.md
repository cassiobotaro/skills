# iteration-8 — eval 1 against 1.2.3, gating the `examples.md` index

**Question.** 1.2.3 added a one-paragraph index at the top of `references/examples.md`, naming its
six parts and when each applies. `SKILL.md` sends the model there "before writing your first ADR
of the session", but most tasks need one or two parts: a supersede-only task has no use for the
seed ADR, and initializing a fresh log has none for the amend pair.

The change is navigational, not behavioural — but a reference file's opening paragraph is the
first thing the model reads, and telling it that it may read selectively is exactly the kind of
nudge that can cost you the part it *did* need. Eval 1 is the case that reads the most of the
file: a fresh repository, so it must reproduce the seed ADR faithfully **and** write the
decision record.

**Method.** One `with_skill` run against the working-tree skill. No baseline: iteration-7 scored
the full set 41/41 against 1.2.2 with these assertions, so that is the comparison. Grading used
`check_mechanical.py` (copied from iteration-7 with `TODAY` advanced) plus file inspection.

## Result — 8/8, no regression

| Eval | Passed | Tokens |
|---|---|---|
| 1 clear-decision-fresh-repo | 8/8 | 32,990 |

The mechanical script reports one FAIL, and it is an artifact of this run's layout, not of the
skill: the script globs `outputs/**/*.md` and therefore judges `response.md` — the saved chat
reply — against the `NNNN-slug.md` filename rule. Both actual ADRs pass every mechanical check.

## What the run established

- **The seed survived selective reading.** `0001-registrar-decisoes-de-arquitetura.md` carries the
  canonical content intact — the Nygard article link and the Nat Pryce adr-tools link both
  present — with title and body translated to Portuguese and the filename slug derived from the
  *translated* title, accents transliterated (`decisoes`). That is precisely the part of
  `examples.md` the new index invites the model to skip when it doesn't apply; here it applied,
  and it was read.
- **The language split held.** Prose in Portuguese; `Date:`, the four `##` headings and `Accepted`
  in canonical English, and the run told the user why.
- **Numbering and dates.** `0002` follows the seed, H1 uses the un-padded `# 2.`, `Date:` is the
  real `2026-08-07` from `date +%Y-%m-%d`.
- **Consequences carry the cost.** Both downsides the user stated — the schema gets more rigid,
  migrations become a deploy step — appear as standalone paragraphs alongside the upsides.
- **Nothing invented.** No metrics, no benchmarks, no alternatives beyond the PostgreSQL/MongoDB
  pair the user named. Context reproduces the three forces he gave (ACID across order/stock/
  payment, team experience, RDS already paid for) and stops there.

## Scope

One eval, one run — a targeted gate for a navigational change, not a variance measurement or a
full-set regression. The other six evals were not re-run; 1.2.3 touches only `examples.md`, and
eval 1 is the case with the most exposure to it.
