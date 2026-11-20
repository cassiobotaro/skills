# iteration-13 — the same ablation on a request that rambles (adr 1.4.1, no skill change)

**Question.** iteration-12 removed the Title, Decision and Length bullets of step 4 and
found the arms indistinguishable, but on eval 11, a short well-formed request that tempts
none of the three. Does the result hold on a request built to tempt all of them?

**Method.** Same two arms (`skill-a` byte-identical to the working tree, `skill-b` minus
the three bullets; both copied unchanged from iteration-12), same fixture
(`english-log`), same executor brief, four runs per cell, executor aliases `sonnet` and
`haiku` (claude-sonnet-5-5 and claude-haiku-5-5 by this session's mapping; ids not read
back from the transcripts). The prompt is new and is in `checks.json`, not in
`evals.json`: one decision told as a story, stated in the passive ("it was agreed that
pdf generation is going to be moved out of the request"), the mechanism named in passing
(Sidekiq), far more material than a short record needs (three incidents, 41 tickets, two
rejected alternatives, two accepted costs, two people by name) and one unrelated tangent
(renaming the billing module). Checks frozen before the first run: those of iteration-12
with Sidekiq in place of S3, plus two observations. Every check by `grade.py` from bytes
(`script-checks.json`). No judge.

One change to the script after the runs, none to the checks: the title of a record whose
H1 number is not 3 was being read with the number in it, which would have failed F.3 and
inflated T.1 for the mis-numbered run below. The title is now read without the number;
F.2 still fails that run for the number itself.

**Results** (runs meeting the check / runs).

| Check | a-sonnet | b-sonnet | a-haiku | b-haiku |
|---|---|---|---|---|
| F.1 one new file 0003, fixture untouched | 4/4 | 3/4 | 4/4 | 4/4 |
| F.2 H1 `# 3.`, date, four headings, Accepted | 4/4 | 3/4 | 4/4 | 4/4 |
| F.3 slug derived from the title | 4/4 | 4/4 | 4/4 | 4/4 |
| T.1 title is a short phrase | 4/4 | 4/4 | 4/4 | 4/4 |
| T.2 Decision says "We will" and names Sidekiq | 4/4 | 4/4 | 4/4 | 4/4 |
| T.3 40 lines or fewer | 4/4 | 4/4 | 4/4 | 4/4 |
| title words per run | 7, 6, 6, 6 | 6, 6, 6, 6 | 7, 7, 7, 7 | 6, 8, 7, 6 |
| lines per run | 27, 27, 31, 27 | 31, 29, 31, 29 | 25, 29, 27, 27 | 31, 28, 27, 31 |
| words per run | 248, 238, 283, 263 | 264, 272, 278, 272 | 272, 298, 304, 302 | 328, 299, 284, 302 |
| Decision words per run | 46, 46, 61, 70 | 55, 63, 63, 65 | 67, 58, 68, 70 | 72, 67, 41, 66 |
| passives in Decision per run | 0, 1, 0, 1 | 1, 1, 0, 1 | 1, 1, 1, 1 | 1, 2, 1, 1 |
| rename tangent in the record | 0 | 0 | 0 | 0 |
| people named in the record | 0 | 0 | 0 | 0 |

- **Title.** Sixteen short imperative phrases. Twelve are "Generate invoice PDFs in
  background jobs" or "…in a background job". The four that differ are all haiku without
  the bullet ("Generate invoice PDFs in the background" twice, "Move invoice PDF
  generation to a background job", "…to background jobs"): more varied, none
  sentence-shaped, none over eight words.
- **Decision.** All sixteen open with "We will" and name Sidekiq; none keeps the user's
  "it was agreed that". The one recurring passive, in both arms, is the file that "will
  be stored" or "is stored" in the documents bucket.
- **Length.** 25 to 31 lines and 238 to 328 words, overlapping across arms within each
  model. The longer request made the records about three times longer than in
  iteration-12, in both arms alike, and none came near the 40-line band.
- **Tangent and names.** The billing-module rename and both people's names are out of
  all sixteen records. Neither depends on the removed bullets.
- **The one failure is elsewhere.** b-sonnet run-4 did not find the existing log: its
  reply says "There was no decision log in the repo", it rewrote 0001 as a fresh seed
  (the date changed from 2026-05-10 to 2026-11-20) and wrote the decision as
  `0002-generate-invoice-pdfs-in-background-jobs.md` beside the untouched
  `0002-use-postgresql-for-persistence.md`. That is step 1 of the workflow, which the
  ablation does not touch. It is 1 of the 32 runs on this fixture across iterations 12
  and 13, so nothing here says which arm it belongs to; it is the first time the pilot
  runs show a log being missed, and it overwrote a file.

**Reading.** Indistinguishable again, on a request written to break it. Across both
iterations that is 32 runs, two prompts and two models with no check on which the
bullets show an effect. What carries the behaviour is still in both arms: the template
with its example H1 and its `"We will ..."`, the model ADR in `references/examples.md`,
and the self-review line. The three bullets restate what those already show. This is the
opposite of the `design-doc` result of the same day (`design-doc-workspace/iteration-26`),
where the removed guidance told the model to work against its default and did change the
output.

**Limits.** Four runs per cell measure no rate; this is "never" twice, not a proof of
absence. Both prompts are English on an English log: a Portuguese log, where the title
is prose in another language, is untested. Invention was not judged in either iteration.
The self-review line `Decision says "We will …"` stayed, so the Decision bullet was
never tested without its duplicate.

**Cost.** Executors 16 runs, 0.87 M tokens (sonnet 0.42 M, haiku 0.45 M). No judge calls.
