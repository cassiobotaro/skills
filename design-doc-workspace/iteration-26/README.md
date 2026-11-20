# iteration-26 — ablation: prose-style guidance removed (design-doc 1.5.3, no skill change)

**Question.** Does the prose-style guidance of `SKILL.md` change what gets written, or
does a current model write that way unaided? Asked because the tech-leads-club repository
removed step-by-step writing instructions from its lean skills on the claim that current
models no longer need them; this checks that claim on our own text before editing
anything.

**Method.** Two arms, four runs per cell, two executor models. `skill-a` is a
byte-identical copy of the working tree (1.5.3). `skill-b` is the same minus 235 words:
the persona opening ("You are an expert in writing and reviewing design documents"), the
two step-3 bullets "Write plainly and in the active voice" and "Keep the typography
plain", and the two self-review lines that enforce them (`diff skill-a/SKILL.md
skill-b/SKILL.md`). The prompt is eval 6's, word for word. The executor brief names the
skill copy by a neutral path (`skill-a`, `skill-b`), forbids the Skill tool so the
installed plugin cannot stand in for the copy, and says the user cannot reply in this
turn. Executor aliases `sonnet` and `haiku`, which this session maps to claude-sonnet-5-5
and claude-haiku-5-5; the ids were not read back from the transcripts. Checks frozen in
`checks.json` before the first run, with the prediction written in them. File, style and
observation checks by `grade.py` (`script-checks.json`). R.1 by the session that ran the
ablation, over the 80 colon candidates the script extracted, shuffled, with arm and model
hidden (`judge-inputs/candidates.json`, verdicts in `judge-outputs/reading.json`,
unblinded through `judge-map.json`); one reader, one pass. Not added to `evals.json` or
`checks-baseline.json`.

**Results** (runs meeting the check / runs; then the raw counts per run).

| Check | a-sonnet | b-sonnet | a-haiku | b-haiku |
|---|---|---|---|---|
| F.1 one document written | 4/4 | 4/4 | 4/4 | 4/4 |
| F.2 mermaid, image, DSL in `<details>` | 4/4 | 4/4 | 4/4 | 4/4 |
| F.3 no validation disclaimer | 4/4 | 4/4 | 4/4 | 4/4 |
| T.1 two em dashes or fewer | 4/4 | 4/4 | 4/4 | 4/4 |
| T.2 no one-word bold | 4/4 | 3/4 | 4/4 | 4/4 |
| T.3 no self-announcing opening (as frozen) | 4/4 | 4/4 | 4/4 | 4/4 |
| R.1 no colon reveal | 4/4 | 3/4 | 4/4 | 3/4 |
| em dashes per run | 0, 0, 0, 0 | 1, 1, 0, 0 | 0, 0, 0, 0 | 1, 0, 0, 1 |
| colon candidates per run | 1, 3, 3, 2 | 4, 4, 4, 2 | 11, 7, 3, 4 | 12, 7, 6, 7 |
| O.1 spaced en dashes | 0 | 0 | 0 | 0 |
| O.2 agentless passives per run | 0, 1, 1, 1 | 6, 10, 5, 4 | 8, 15, 9, 10 | 14, 16, 18, 16 |
| O.2 per 1000 words | 0.0, 1.1, 1.2, 1.2 | 7.8, 10.3, 6.2, 5.2 | 6.9, 11.5, 8.8, 7.1 | 11.2, 14.5, 13.3, 13.2 |
| O.3 words per run | 872, 931, 827, 805 | 769, 973, 807, 771 | 1163, 1303, 1023, 1416 | 1247, 1106, 1355, 1214 |

- **Passive voice (O.2).** The one place the arms separate. On sonnet the ranges do not
  touch: 0 to 1 agentless passive per document with the guidance, 4 to 10 without. On
  haiku they barely touch: 8 to 15 with, 14 to 18 without. The hits are real passives
  ("é enviado", "foi definido", "são rotacionados"), not regex noise; the list for each
  run is in `script-checks.json`. Haiku with the guidance is about as passive as sonnet
  without it.
- **Typography (T.1, T.2, R.1).** No check fails in arm a, in sixteen runs' worth of
  checks. Arm b stays under the em-dash ceiling too, but everything that does appear
  appears there: an em dash in 4 of 8 runs against 0 of 8, the one single-word bold
  (`**DLQ**`, sonnet), and both colon reveals (sonnet run-4, "O trade-off central: a
  entrega deixa de ser imediata…", which is the skill's own example almost word for
  word; haiku run-1, borderline and counted as unmet).
- **T.3 was aimed at the wrong place.** As frozen it looks before the second level-2
  heading, and most documents put a glossary there, so it met 16/16 without reading the
  overview. A whole-document search finds "Este documento propõe um serviço único…"
  opening the overview in 16 of 16 runs, both arms. Whether that is the tic the skill
  names ("an opening paragraph that announces what the document contains") is a
  judgment: it states the proposal, it does not list the sections. Either way the
  guidance does not move it.
- **Nothing else moved.** File checks at the ceiling in both arms; document length
  overlaps within each model.

**Reading.** The prediction in `checks.json` offered three outcomes and the result is
split between two of them. For the active-voice bullet the removed text pulls weight:
the effect shows every time on sonnet and nearly every time on haiku, so "current models
write this way unaided" is false for it on both. For the typography bullet the frozen
thresholds do not separate the arms (b never breaks the em-dash ceiling), yet every
instance of every tic it names is in arm b. With four runs per cell that is a consistent
direction, not a measured effect. The ablation removed five things at once, so the
persona line and the two self-review lines cannot be told apart from the bullets they
sit beside.

So this skill gets no shorter on the strength of this run. The 235 words buy a
measurable difference in one dimension and a visible one in the others, for about 7% of
the body.

**Limits.** Four runs per cell measure no rate (AGENTS.md); the passive separation is
the "every time against never" kind, the typography one is not. One eval, in Portuguese;
the passive regex is Portuguese-only and would not transfer. O.2 is a heuristic, and a
passive is not always worse prose: the check counts constructions, it does not judge
them. R.1 had one reader and one pass. The brief told the executor the user could not
reply, as in iterations 24 and 25. Invention was not judged.

**Cost.** Executors 16 runs, 1.36 M tokens (sonnet 0.65 M, haiku 0.71 M; about 85 k per
run). No judge calls.
