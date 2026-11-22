# The update clause of design-doc 1.9.0 — routine checks before and after

2026-11-22, claude-sonnet-5-5, serial, through `eval-tools/run_trigger_eval.py --routine`.

**Change.** The description gains "update" among its opening verbs and one clause for a
design doc that has to follow a design that changed (`update-request-2026-11-22/`,
candidate b): 642 characters become 1013. The reason is the miss found the same day: the
request of eval 9 invoked no skill in 16 of 16 sessions and the approved document was
rewritten in all of them; with the candidate, 8 of 8 invoked `design-doc`.

**The set.** Two queries were added before either sweep, so both sweeps run on the same
22: a positive with the request of eval 9 and the document pasted in the message, and a
negative that asks to update a page that is not a design doc, also pasted.

**Rule, written before the sweeps.**

- The canary scores full marks in both sweeps, or the sweep is void.
- Positives: the ten old ones are a regression guard. The change is kept if they stay at
  90% or more after it and do not lose more than three triggers of thirty against the
  sweep taken before it, which is what two identical sweeps move.
- The new positive is reported for both texts. Three runs do not rank it; the claim that
  the clause wins that request rests on the plugin probe (0/16 against 8/8), and this
  harness may answer it in prose, as it did with other pasted-text queries.
- Negatives: a query that fires after the change and did not fire before it is probed on
  its own at ten runs with each text before it is called a false fire. The change is not
  kept if such a probe separates the texts by five runs of ten or more.

## Results

One sweep with each text, Claude Code 2.1.330, 69 sessions each
(`serial-2026-11-22-routine-sonnet-before-update-clause.json` and
`serial-2026-11-22-routine-sonnet-after-update-clause.json`).

| | 1.8.0 text (642 characters) | 1.9.0 text (1013 characters) |
|---|---|---|
| the ten old positives | 30/30 | 30/30 |
| the new positive (eval 9's request, document pasted) | 3/3 | 3/3 |
| the ten old negatives | 0/30 | 0/30 |
| the new negative (update a page that is not a design doc) | 0/3 | 0/3 |
| canary | 3/3 | 3/3 |

**Reading, by the rule above.** The canary is at full marks in both sweeps, the positives
lose nothing, and no negative fires with either text, the new one included. The change is
kept, as `design-doc` 1.9.0.

Both texts sit at the ceiling, so this pair shows no regression and could not show a
small one. It also does not show the defect the clause is for: the old text scores 3/3 on
the new positive here and 0/16 on the same request in the plugin probe. In this harness
the document is pasted and there is no file to edit, so the session has nothing to do but
consult the skill; in a project where the file exists it edits the file. A request to
change a file that is in the project cannot be measured by this harness, and the evidence
that the clause wins it is `update-request-2026-11-22/` (8/8 against 0/16, eight sessions
with the candidate, no body rewritten).

## The haiku number for 1.9.0

One sweep on claude-haiku-5-5 with the 1.9.0 text, positives at 5 runs and negatives at
3 (`serial-2026-11-22-routine-haiku-1.9.0.json`, 91 sessions, Claude Code 2.1.330).

| | 1.9.0, 2026-11-22 | old text, 2026-11-20 (`serial-2026-11-20-routine-haiku.json`) |
|---|---|---|
| the ten old positives | 40/50 (80%) | 31/50 (62%) |
| the new positive | 5/5 | not in the set |
| negatives | 0/33, the new one included | 0/10 |
| canary | 3/3 | 5/5 |

Per query, old positives in the order of the set: 5, 4, 0, 5, 5, 5, 4, 5, 2, 5 against
5, 1, 0, 5, 3, 5, 5, 5, 0, 2. The RFC query stays at 0/5 on both days.

This is the early-warning number the release asks for, and it shows no warning. The 18
points between the two sweeps are not a measured effect of the clause: the sweeps are two
days apart, one each, and no haiku sweep was taken on the old text the same day. Two
identical sweeps move 4 to 6 points at this size, so the difference is larger than that
noise and still not attributable. Do not tune the description to it.
