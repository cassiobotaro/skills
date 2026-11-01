# Four-model serial sweep: haiku, sonnet, fable, opus (2026-10-31)

Shipped descriptions on the day: `design-doc` 1.4.3, `structurizr` 1.6.3, `mermaid-sequence`
1.3.0. Same method as `README-serial-baseline.md`: `./eval-tools/run_trigger_eval.py` from the
repo root, `--num-workers 1`, `--timeout 120`, positives at `--runs-per-query 5`, negatives at
`--runs-per-query 3` with the skill's strongest positive spliced in as a canary, one sweep at a
time, wrapped in `systemd-inhibit`. Files: `serial-2026-10-31-{positives,negatives}-<model>-n{5,3}.json`
in each `<skill>-workspace/trigger-evals/`.

Claude Code 2.1.316. The project instructions file is `AGENTS.md` (loaded by the CLI since
2.1.277 whenever no `CLAUDE.md` exists), so the nested sessions see the same contract the August
sessions read from `CLAUDE.md`.

## Positives

| skill | haiku | sonnet | fable | opus |
|---|---|---|---|---|
| design-doc | 37/50 (74%) | 49/50 (98%) | 50/50 (100%) | 50/50 (100%) |
| structurizr | 31/45 (69%) | 45/45 (100%) | 45/45 (100%) | 45/45 (100%) |
| mermaid-sequence | 46/50 (92%) | 50/50 (100%) | 50/50 (100%) | 50/50 (100%) |
| all three | 114/145 (79%) | 144/145 (99%) | 145/145 (100%) | 145/145 (100%) |

Every canary scored 3/3 and no kept sweep showed the degraded signature.

**structurizr is 9 queries, not 10.** The ADR-linking positive ("link our decision records from
doc/adr …") was removed from `trigger_eval.json` during this session, after the haiku sweep had
already run it (0/5). The haiku number above is the remaining 45 runs; every later model ran the
9-query set.

## Negatives

| skill | haiku | sonnet | fable | opus |
|---|---|---|---|---|
| design-doc | 0/30 | 0/30 | 0/30 | 0/30 |
| structurizr | 0/30 | 0/30 | 0/30 | **1/30** |
| mermaid-sequence | 0/30 | 0/30 | 0/30 | **1/30** |

Both false fires are on opus, 1/3 each, on the same shape of query — a *design doc* request that
mentions the other skill's artifact:

- structurizr: "write a design doc for the new recommendations service, including an architecture overview"
- mermaid-sequence: "write a design doc for the new event pipeline, with the flow of data between services"

Same class as the August exception (`design-doc`/opus on a PRD): the adjacent-artifact query,
at a rate far below the pass threshold. Rate across all four models: 2 in 360 negative samples.

## The haiku alias changed model, so the August haiku column is not comparable

`design-doc` and `structurizr` ship the **byte-identical description** they shipped in August
(checked against the 1.3.6 and 1.3.0 frontmatter); only `mermaid-sequence`'s changed (the MCP
sentence became the local mermaid-cli sentence). Yet haiku moved:

| skill | haiku, 2026-08-20 | haiku, 2026-10-31 |
|---|---|---|
| design-doc | 48/50 (96%) | 37/50 (74%) |
| structurizr | 37/50 (74%) | 31/45 (69%) |
| mermaid-sequence | 45/50 (90%) | 46/50 (92%) |

The transcripts explain it. The August captures (`transcripts-pt/`) record
`claude-haiku-4-5-20251001`; today's (`design-doc-workspace/trigger-evals/transcripts-rfc-haiku/`)
record `claude-haiku-5-5`. **The `haiku` alias points at a different model.** The 22pp design-doc
drop is a model change, not a description regression, and from here on a haiku number must name
the model id, not the alias. The August haiku column of the serial baseline is a Haiku 4.5
number and should not be compared with anything measured on 5.5.

**Haiku 5.5 misses differently.** Six captures of the design-doc RFC query ("write an RFC for
migrating our monolith's billing module …", 0/5 in the sweep, 5/5 in August):

| outcome | runs |
|---|---|
| `strict_trigger` | 1 |
| `prose_only`, wrote the whole RFC itself with `[bracketed]` placeholders | 4 |
| `prose_only`, asked 4 scoping questions | 1 |

In August every miss was the scoping-questions kind: the model hesitated and asked, which is the
repo's own contract performed without the skill. Haiku 5.5 instead does the job by hand — a full
RFC with the facts it lacks marked as placeholders — and skips the skill. The three queries it
lost are the ones that do not say "design doc" (RFC, design proposal) or that name a file to
review. That is the same boundary class the baseline identified, now lost to a model that trusts
itself to know the format rather than one that asks.

## What this sweep can and cannot say

- Sonnet, Fable and Opus sit at the ceiling: 99-100% on positives. Nothing in the three
  descriptions can be ranked on those models, and a change to a description cannot be measured
  there except through negatives.
- Haiku 5.5 is the only discriminating model. design-doc vs mermaid-sequence separates
  (74% vs 92%, p = 0.03, Fisher); structurizr vs design-doc does not (69% vs 74%, p = 0.65).
- The usual caveats hold: ±4-6pp between identical sweeps at n=50, so a skill-level gap under
  ~12pp is not a finding, and n=5 per query ranks nothing.

## Discarded files

`serial-2026-10-31-*-fable-*-DEGRADED-DISCARDED.json` (one per skill and kind): the first fable
attempt hit the account's usage limit mid-sweep. design-doc positives scored 23/50 with the
distribution `[0,0,0,0,0,3,5,5,5,5]` — healthy for the first five queries, then floor — and every
later sweep scored 0 with the wrapper's degraded-sweep warning. Kept as the record of what a
usage-limit cut looks like from inside a sweep: **the first sweep to hit it does not trip the
warning**, because its early queries are fine. Check the ordered per-query list, not only the
warning, before pooling a sweep that ran near a limit. The clean fable re-run above was done
after the limit reset, from a fresh smoke test.
