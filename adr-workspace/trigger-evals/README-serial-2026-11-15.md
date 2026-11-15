# adr on Haiku 5.5: serial sweep (2026-11-15)

`adr` was out of the repository when the four-model sweep of 2026-10-31 ran
(`structurizr-workspace/trigger-evals/README-model-sweep-2026-10-31.md`), so it had no
number on the current haiku. This is that number, by the same method:
`./eval-tools/run_trigger_eval.py` from the repo root, `--num-workers 1`, `--timeout 120`,
positives at `--runs-per-query 5`, negatives at `--runs-per-query 3` with the strongest
positive of the August baseline spliced in as a canary, one sweep at a time, under
`systemd-inhibit`. Files: `serial-2026-11-15-{positives-haiku-n5,negatives-haiku-n3}.json`.

Model `claude-haiku-5-5` (the `haiku` alias, id read from a one-shot session right after
the sweeps). Claude Code 2.1.325. Description: the 1.3.1 text, unchanged through 1.4.1.

| | result |
|---|---|
| positives | **28/50 (56%)**, per-query `[5, 0, 5, 5, 1, 3, 5, 1, 1, 2]` |
| negatives | 0/30 |
| canary | 3/3 |

Four queries score 5/5, so this is not the degraded-sweep signature.

**Reading.** One sweep. Two identical serial sweeps move ±4-6pp at n=50, and a 12pp gap
between two skills on haiku did not separate (AGENTS.md); against design-doc's 37/50 and
structurizr's 31/45 from 2026-10-31 this is 13-18pp lower, measured two weeks and nine CLI
releases later. It says `adr` is not above the other two on Haiku 5.5; it does not rank
it below them.

The August baseline (43/50, 86%) was `claude-haiku-4-5` and is a different model. The
shape of the change is still worth noting: the queries that name the artifact or an
operation on the log ("write an ADR", "ADR 0007 is out of date", "amend the existing
record", "we finally settled the debate … capture this") stay at 5/5, and the ones that
describe a decision without the word hold 0-3/5 ("start a decision log" 0/5, "registra aí
a decisão" 1/5, "write up why we chose to deprecate the v1 API" 1/5). A per-query claim
needs ten or more runs each; five do not rank queries.

**Not controlled.** While the sweep ran, files under `adr-workspace/` and
`structurizr-workspace/trigger-evals/` were edited in the same checkout (no `AGENTS.md`,
no `SKILL.md`, no session running in parallel). Sessions that read the repository before
acting could have seen those edits.
