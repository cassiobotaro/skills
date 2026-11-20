# AGENTS.md text and the trigger rate of indirect queries: A/B on Haiku 5.5 (2026-11-20)

**Question.** The routine sweep of this date (`../README-routine-2026-11-20.md`) put
`adr` and `mermaid-sequence` 14 to 16 points under their earlier numbers, with the whole
drop in queries that do not name the artifact. The earlier numbers had the old
`AGENTS.md` in every session's context. Did the text removed from it raise the trigger
rate of those queries?

**Method.** Eight queries: the six `adr` positives that scored 0-3 of 5 on 2026-11-15 and
the two `mermaid-sequence` positives that fell from 4/5 to 0/5. Two arms, ten runs per
query and arm, `claude-haiku-5-5` (the id passed to `--model`), serial, 120 s timeout,
under `systemd-inhibit`. Arm a starts each session in a directory holding `AGENTS.md` as
committed at 2bc0e04, arm b in one holding the trimmed file; both sit below the repository
root, whose trimmed file loads too, so the arms differ by the removed text only (probed:
"## Per-skill notes" in context in arm a, 32,345 tokens; absent in arm b, 26,750). Two
blocks of five runs per skill and arm in the order a b b a. One 5/5 positive per skill
rides in every block as canary. `agentsmd_ab.py` reuses the patched `run_eval.py` of
`eval-tools/run_trigger_eval.py` with one more patch for the start directory. Prediction
and reading rule frozen in `prediction.json` before the first session. The two start
directories were deleted afterwards. Because sessions start in a nested directory, these
rates compare between arms, not with a sweep started at the root.

**Results** (triggers / runs).

| Skill | Query | a: old AGENTS.md | b: trimmed |
|---|---|---|---|
| adr | start a decision log for the platform-team repo… | 1/10 | 5/10 |
| adr | document the decision to adopt feature flags via LaunchDarkly… | 2/10 | 1/10 |
| adr | the tech lead wants every significant tech choice written up in doc/adr… | 8/10 | 3/10 |
| adr | registra aí a decisão de a gente padronizar em OpenTelemetry… | 3/10 | 0/10 |
| adr | i need to write up why we chose to deprecate the v1 API… | 5/10 | 5/10 |
| adr | create a record explaining our choice of hexagonal architecture… | 0/10 | 0/10 |
| mermaid-sequence | diagram the retry/backoff interaction between our worker and the third-party API… | 0/10 | 0/10 |
| mermaid-sequence | show the message flow for our async order processing: producer publishes to Kafka… | 8/10 | 0/10 |
| | adr, six queries | 19/60 (32%) | 14/60 (23%) |
| | mermaid-sequence, two queries | 8/20 (40%) | 0/20 (0%) |
| | pooled, eight queries | 27/80 (34%) | 14/80 (18%) |
| | canaries | 19/20 | 20/20 |

Pooled difference 16 points, Fisher p = 0.029. Queries higher in arm a: four; higher in
arm b: one; equal: three.

**Reading, by the frozen rule.** Not shown. The rule asked for a pooled difference of 15
points, p < 0.05 and six of the eight queries moving the same way; the first two are met
and the third is not (four of eight, one against). The removed text is not a general
boost for indirect queries.

What the table does show is narrower and was not what the rule was written for:

- **One query depends on it.** "show the message flow for our async order processing…"
  fires 8/10 with the old file and 0/10 with the trimmed one (Fisher p = 0.0007, 0.006
  after correcting for eight queries; ten runs per arm, the size AGENTS.md asked for on a
  per-query claim). That one query carries the whole `mermaid-sequence` difference, and
  with "the tech lead wants…" (8/10 against 3/10) most of the pooled one.
- **One query goes the other way.** "start a decision log…" is 1/10 against 5/10.
- **`adr` as a set does not separate** (19/60 against 14/60, p = 0.41), and the other
  `mermaid-sequence` query is 0/10 in both arms: its earlier 4/5 was not the old file.
- **The repository's own instructions are part of what a trigger number measures.** A
  rate taken in this checkout describes the description plus whatever `AGENTS.md` says
  about the skills; a user's project has neither file. The trimmed file is the closer of
  the two to that, which is one more reason to quote only numbers taken after the split.

**Limits.** One model, ten runs per query and arm, eight queries chosen from earlier
results. The per-query reading is post hoc. The old file differs from the trimmed one by
the eval rules as well as the per-skill notes, so this does not say which part moves the
Kafka query. Cost not recorded (200 sessions, about ten minutes).
