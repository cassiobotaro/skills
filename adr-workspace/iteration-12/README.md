# iteration-12 — ablation: three step-4 bullets removed (adr 1.4.1, no skill change)

**Question.** Do the Title, Decision and Length bullets of step 4 change what gets
written, or does the rest of the skill (the template of "The format", the examples file,
the self-review line) already carry it? Asked because the tech-leads-club repository
removed step-by-step writing instructions from its lean skills on the claim that current
models no longer need them; this checks that claim on our own text before editing
anything.

**Method.** Two arms, four runs per cell, two executor models. `skill-a` is a
byte-identical copy of the working tree (1.4.1). `skill-b` is the same minus three
bullets:

```
- **Title**: a short noun phrase ("Use ISO 8601 format for dates"), not a sentence.
- **Decision**: active voice, concrete and specific — name the technology, format, or
  mechanism.
- **Length**: the canonical ADRs run 15–40 lines; one or two pages is the absolute
  ceiling. Shorter records get read and kept up to date.
```

The Context and Consequences bullets stay in both arms, as do the template (which reads
`"We will ..."`) and the self-review line `Decision says "We will …"`. The prompt is
eval 11's, word for word, on the `english-log` fixture; eval 7 was avoided because the
removed Title bullet quotes "Use ISO 8601 format for dates" and eval 7 is about ISO 8601.
The executor brief names the skill copy by a neutral path (`skill-a`, `skill-b`), forbids
the Skill tool so the installed plugin cannot stand in for the copy, and says the user
cannot reply in this turn. Executor aliases `sonnet` and `haiku`, which this session maps
to claude-sonnet-5-5 and claude-haiku-5-5; the ids were not read back from the
transcripts. Checks frozen in `checks.json` before the first run, with the prediction
written in them; every check is decided by `grade.py` from bytes (`script-checks.json`).
No judge. Not added to `evals.json` or `checks-baseline.json`.

**Results** (runs meeting the check / runs).

| Check | a-sonnet | b-sonnet | a-haiku | b-haiku |
|---|---|---|---|---|
| F.1 one new file, fixture untouched | 4/4 | 4/4 | 4/4 | 4/4 |
| F.2 H1, date, four headings, Accepted | 4/4 | 4/4 | 4/4 | 4/4 |
| F.3 slug derived from the title | 4/4 | 4/4 | 4/4 | 4/4 |
| T.1 title is a short phrase | 4/4 | 4/4 | 4/4 | 4/4 |
| T.2 Decision says "We will" and names S3 | 4/4 | 4/4 | 4/4 | 4/4 |
| T.3 40 lines or fewer | 4/4 | 4/4 | 4/4 | 4/4 |
| lines per run | 21, 21, 21, 21 | 21, 21, 21, 21 | 21, 23, 23, 19 | 19, 21, 21, 22 |
| words per run | 94, 100, 97, 95 | 98, 105, 103, 98 | 129, 123, 106, 81 | 94, 116, 104, 89 |
| Decision words per run | 16, 16, 16, 16 | 16, 16, 16, 16 | 16, 19, 16, 16 | 15, 14, 14, 15 |
| passives in Decision | 0 | 0 | 0 | 0 |

- **Title.** All sixteen records carry the same title, "Store user-uploaded files in S3",
  in both arms and on both models.
- **Length.** 19 to 23 lines everywhere, about half the ceiling.
- **Consequences on haiku.** Three of eight haiku runs write a Consequences section of 11
  to 15 words that restates the trade-off and stops ("Every file read becomes a network
  call. We accept this downside."): one in arm a, two in arm b. The Consequences bullet
  is in both arms, so this is not the ablation's doing. Sonnet writes 31 to 42 words
  there in all eight.

**Reading.** The arms are indistinguishable on every check, and both are at the ceiling.
On this prompt the three bullets add nothing that the template, the examples file and
the self-review line do not already produce, on sonnet and on haiku alike. What that
licenses is narrow: the bullets are redundant here, not that they are redundant
everywhere. Eval 11 is a well-formed English request with one decision and one
trade-off; it does not tempt a sentence-shaped title or a long record, so a ceiling on it
is weak evidence about a prompt that would (a rambling request, two decisions in one
message, a Portuguese log). The prediction in `checks.json` named the case that would
show the bullets working; it occurred in 0 of 16 runs.

**Limits.** Four runs per cell measure no rate (AGENTS.md); they separate "every time"
from "never", and this is "never" on one eval. One prompt, in English. The invention
checks of eval 11 were not judged, so nothing here says whether removing the bullets
moves invention; the Context bullet, which carries that rule, was left in place. T.2 is
not a clean ablation of "We will": two other places in the skill still say it.

**Cost.** Executors 16 runs, 0.84 M tokens (sonnet 0.42 M, haiku 0.43 M; about 52 k per
run, nearly all of it fixed overhead). No judge calls.
