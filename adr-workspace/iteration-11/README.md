# iteration-11 — rate of the padded Context (adr 1.4.1 vs 1.4.0), ten runs per arm

**Question.** iteration-10 kept the Context rule of 1.4.1 on direction only: the defect it
targets did not reproduce in the 1.4.0 arm in two runs. This iteration measures the rate.

**Method.** Eval 10 only, ten runs per arm, twenty executors (`claude-sonnet-5-5`) in
batches of at most six. `with_skill` = 1.4.1 (the shipped tree); `old_skill` =
`../skill-snapshot-1.4.0/`. No judge. The user's message establishes four things for
Context (a per-account limit, 5 per 15 minutes, the gateway as the other place, the
gateway cannot see account ids); `context_padding.py` extracts each Context, flags a
motive or a general-truth pattern, and prints all twenty so the flags can be checked by
reading. `context-padding.json` holds every Context.

**Result.**

| | 1.4.1 | 1.4.0 |
|---|---|---|
| Context says more than the user gave, by reading all twenty | **0/10** | **4/10** |
| …of which flagged by the script's patterns | 0 | 3 |
| Median Context length | 22 words | 34 words |

The four 1.4.0 cases:

- run 3: "to slow down password guessing" and "The API gateway is the usual place for
  rate limiting"
- runs 5 and 9: "The API gateway is the usual place for rate limiting"
- run 4: "The session service handles logins and knows which account each attempt
  targets" — not caught by the patterns, found by reading

Every 1.4.1 Context is the same two sentences in slightly different words: the limit is
per account; the gateway cannot see account ids.

**How strong is it.** One-sided Fisher exact on this iteration: p = 0.043 (0/10 against
4/10). Pooling every eval-10 run of the two versions (iterations 9, 10 and 11) gives 0/12
against 6/14, p = 0.013. The pooling was not planned in advance, the scorer was the
author of the change and read the arm labels, and it is one prompt on one executor model.
It is enough to say the rule removes the padding on this eval; it does not give a rate
for other prompts.

**Reading.** Under 1.4.0 the padded Context is not a rare slip: four in ten here, six in
fourteen overall. Under 1.4.1 it did not occur in twelve runs. The 715 bytes are
justified. The patterns miss one case in four, so a script alone under-counts this
defect; printing every Context and reading them is what made the count trustworthy at a
cost of twenty short lines.

**Not recorded.** No `timing.json`, `grading.json` or benchmark: this iteration scores a
single defect and nothing else. Each run cost about 48k tokens (0.96M in total).
