# iteration-1 — first behavioral A/B of unslop 1.0.0

**Question.** With the skill read, does an agent asked to "unslop" a text do it better than
the same agent left with the word alone?

**Method.** Two cells, two runs per eval each, 24 runs. `with_skill` is told to read
`unslop/skills/unslop/SKILL.md` (1.0.0, commit 6a43580) and follow it; `without_skill`
gets the same brief without that step. Every eval's prompt names unslop, because the skill
is explicit only, so the second cell measures what the model makes of the word on its
own. The executors are headless sessions (`claude -p`, `run.py`) on `claude-sonnet-5-5`,
read back from each session, each started in its own copy of the eval's fixture (an empty
directory when the eval pastes its text), with `--setting-sources project,local` so that
no user-scope skill loads in either cell. The session's final message is the reply.

The checks are the 55 of `../evals/checks-baseline.json`, frozen on 2026-11-21 before any
run (commit 44f7aea): 18 decided by `grade.py` from the bytes, 37 judged by
`eval-tools/judge.py` on `claude-opus-5-5`, three passes per packet, met only when the
three agree.

**One run is invalid.** `3/without_skill/run-1` replied that the repository was empty and
edited nothing. The files were there. The machine's `~/.zshrc` has `alias ls="eza"`, and
`eza` given no path lists nothing when its input is not a terminal, which is every
headless session. The run issued `ls -la` and `ls -A | wc -l`, got nothing back, and
stopped. Four other runs of this iteration issued a bare `ls` too
(`2/without_skill/run-1`, `2/without_skill/run-2`, `3/with_skill/run-1`,
`3/without_skill/run-2`) and went on with `cat` or `find`. The invalid run is kept on disk
and in `results.json` as it came out, and the totals below are given with and without it.
It was not rerun: the other run of that cell met all eight checks of eval 3.

**Result.** Checks met over total, two runs per cell:

| Kind | with_skill | without_skill | without_skill, invalid run left out |
|---|---|---|---|
| file and absence (script) | 36/36 | 33/36 | 31/31 |
| reply | 39/40 | 33/40 | 32/37 |
| negative | 22/22 | 21/22 | 21/22 |
| invention | 12/12 | 11/12 | 11/12 |
| all | 109/110 | 98/110 | 95/102 |

The checks that were not met in every valid run:

| Check | with_skill | without_skill | What was found |
|---|---|---|---|
| 1.9 still says the service was designed to be faster | 2/2 | 0/2 | "foi projetado para ser muito mais rápido" became "é mais rápido que o anterior", a stronger claim |
| 5.2 tells the user there is no vocabulary list for Spanish | 2/2 | 0/2 | no reply without the skill mentions it |
| 1.12 the experts claim is not left standing unflagged | 2/2 | 1/2 | one run cut the attribution and kept "Caches reduzem custos." as a bare fact |
| 1.13 the reply says what it did with that claim | 2/2 | 1/2 | same run; the judges split 2/3 |
| 2.13 README.md gains no claim the original lacked | 2/2 | 1/2 | one run added "it compares both sides and reports the differences" |
| 1.8 still says the platform team built the service | 1/2 | 2/2 | one run wrote "projetado pelo time de plataforma"; the judges split 1/3 |

Two splits in 148 judged verdicts, both listed above and both counted as not met.

**Reading.**

- Both cells remove the tells. Every check that a phrase or a construction is gone was
  met in every valid run of both cells: the em dash, "não é apenas … mas também", "Vale
  ressaltar que", the five phrases of the README, the three of `notes.md`, "no es solo …
  sino", "It is important to note that". Both cells left the code block, the inline code,
  the quotation and the accepted ADR untouched.
- What the skill adds is on the other side of its contract, "without changing its meaning
  and without adding a fact". Check 1.9 separates in both runs; 1.12, 1.13 and 2.13
  separate in one run each, all in the same direction.
- Check 5.2 rests on something only the skill knows, the vocabulary files it ships, so
  its separation says the skill was read and nothing more.
- The skill does not rewrite a clean text (eval 4) and invents no actor (eval 6); neither
  does the model without it.

**Limits.** Two runs per cell: no rate is measured, and a one-run difference is not a
finding. The brief tells the `with_skill` executor to read the skill, so this is about
what the skill does once read. The packets do not name the cell, but four contain the word
"skill" because the reply talks about the skill the user named
(`2/without_skill/run-1`, `2/without_skill/run-2`, `3/with_skill/run-1`,
`5/without_skill/run-2`): a reply that says "there is no unslop skill in this session"
tells the judge which cell it is. Check 1.8 turns on "built" against "designed", which the
judges did not read the same way.

**Cost.** Executors: 24 sessions, 1.30 M tokens summed over turns, US$ 0.75 (US$ 0.019 to
0.049 per run). Judges: 72 calls, 0.16 M tokens, US$ 1.07.
