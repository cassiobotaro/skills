# iteration-27 — design-doc 1.7.0 against 1.6.0: the technical-writing pass in the write step

**Change under test.** 1.7.0 (commit cb8c72e) adds one bullet to step 3 and one line to
the self-review: once the document is on disk, invoke the `technical-writing` skill on the
prose written in this turn, when that skill is installed, and then `unslop`. 1.6.0 (commit
53c2dae) invokes `unslop` only. 1.7.0 shipped without an eval.

**Question.** Does the added pass change what the frozen checks can see in the document,
and what does it cost?

**Method.** The change only acts "when installed" and through the Skill tool, so the
sessions do not get a brief that says "read this SKILL.md". Each run is a headless session
(`claude -p`, `run.py`) on `claude-sonnet-5-5`, read back from each session, started in a
project of its own outside this repository: a fresh git repository with the eval's fixture
and three skills under `.claude/skills/`, `design-doc` at the cell's version and
`technical-writing` 1.0.0 and `unslop` as they are at cb8c72e, the same in both cells.
The session gets the eval's prompt word for word, with `--setting-sources project,local`
and `SHELL=/bin/bash`. No `AGENTS.md` is in reach. Evals 1, 4, 6, 7 and 9, the ones whose
expected output is a written document; cells `v160` and `v170`; two runs per cell.

Checks: `checks.json`, 87 checks, frozen on 2026-11-22 before any run of this iteration,
local to it. Eval 9 keeps the twelve checks and the anchors of
`../evals/checks-baseline.json`; evals 1, 4, 6 and 7 had no atomic checks and got them
from their assertions; each eval ends with one check for what 1.7.0 claims (no actor named
that nobody established), which overlaps the other invention checks and is reported on its
own line. 31 checks by `grade.py`, 56 by `eval-tools/judge.py` on `claude-opus-5-5`, three
passes, unanimous. All 28 runs were judged in one batch. `grade.py` also counts, outside
the met/unmet table, the agentless passives of each document (the regex of iteration-26)
and which skills each session invoked.

**What the first 20 runs showed, and the amendment.** The prompt alone does not reach the
write step on two of the five evals:

- **Eval 7.** Two of the first four sessions never invoked `design-doc` and wrote the
  document unaided. They were set aside as invalid and rerun once, as the frozen rule
  says. All four valid sessions invoked `design-doc`, asked for the risks and the rollout
  plan, and wrote no file.
- **Eval 9.** `design-doc` was invoked through the Skill tool in none of eight sessions
  (four, and their four reruns). `technical-writing` fired on its own in four of the
  eight, one of four in `v160` and three of four in `v170`, which says nothing about the
  versions: both cells list the same three descriptions. Six sessions asked first and
  wrote nothing, one wrote the amendment as `design-doc` describes it with no skill
  invoked (`9/v170/run-1`), and one, with `technical-writing` invoked and `design-doc`
  not, rewrote the body of the shipped document (`9/v160/run-2`). All eight stay invalid
  for the comparison and are kept in the batch only as a record.

So the amendment of 2026-11-22 in `checks.json` adds cells `v160w` and `v170w` for evals 7
and 9, two runs each. They append one sentence to the user's message ("Não vou conseguir
responder perguntas agora: escreve o documento com o que eu já disse e deixa as perguntas
no final.") and, on eval 9, name the skill first ("Usa a skill design-doc."). No check
changed. One `v160w` run of eval 7 did not invoke `design-doc` and was rerun once. The
seven invalid first attempts are in `invalid-first-attempt/`, each with its transcript.

**Results** (checks met over total, two runs per cell). Evals 1, 4 and 6, prompt alone,
`design-doc` invoked and a document written in all twelve runs:

| Kind | 1.6.0 | 1.7.0 |
|---|---|---|
| file and absence (script) | 36/38 | 36/38 |
| reply | 40/40 | 40/40 |
| negative | 13/14 | 14/14 |
| invention, without the actor check | 6/6 | 6/6 |
| the actor check (1.20, 4.22, 6.10) | 3/6 | 2/6 |
| all | 98/104 | 98/104 |

Evals 7 and 9 with the sentence of the amendment (`v160w`, `v170w`), a document written
in all eight runs:

| | 1.6.0 | 1.7.0 |
|---|---|---|
| eval 7: file | 14/14 | 14/14 |
| eval 7: reply | 12/14 | 12/14 |
| eval 7: invention, without the actor check | 12/14 | 12/14 |
| eval 7: the actor check (7.22) | 2/2 | 0/2 |
| eval 9: file 9.1 to 9.5 | 10/10 | 10/10 |
| eval 9: reply 9.6 to 9.9 | 8/8 | 8/8 |
| eval 9: 9.10 nothing invented | 1/2 | 2/2 |
| eval 9: 9.11 download path not asserted | 1/2 | 2/2 |
| eval 9: 9.12 "do nothing" reason is the user's | 2/2 | 2/2 |
| eval 9: the actor check (9.13) | 1/2 | 2/2 |

9.10 to 9.13 overlap and are not summed. Eight splits in 316 judged verdicts (4.20, 6.10
twice, 7.12 twice, 7.22, 9.10, 9.13), all counted as not met.

Every check on which the versions differ:

| Check | 1.6.0 | 1.7.0 | What was found |
|---|---|---|---|
| 7.22 no actor nobody established (`w` cells) | 2/2 | 0/2 | "O time ainda não discutiu falha do Redis…" (split 2/3) and "Vamos medir a latência real no rollout" |
| 6.10 no actor nobody established | 1/2 | 0/2 | "A equipe passa a operar mais um serviço…", "ele envia o evento para a DLQ e registra isso no banco"; both 1.7.0 misses are 2/3 splits |
| 9.11 download path not asserted (`w` cells) | 1/2 | 2/2 | one 1.6.0 document says in the present tense that the worker serves the download |
| 9.10 nothing invented (`w` cells) | 1/2 | 2/2 | the same sentence; split 2/3 |
| 9.13 no actor nobody established (`w` cells) | 1/2 | 2/2 | "Time de Relatórios" as author of the change; split 1/3 |
| 4.20 extra sections hold only the user's substance | 1/2 | 2/2 | a suggestion of reviewers under open questions; split 2/3 |
| 7.11 the +5 ms cost under a heading of its own (`w` cells) | 2/2 | 1/2 | one 1.7.0 document records it under Riscos |
| 7.12 the reply names the added heading (`w` cells) | 1/2 | 2/2 | split 2/3 |

Checks that fail the same way in both: 1.20 (0/2 each: the worker named as what sends the
e-mail, or a team as what operates the queue), 1.12 and 1.13 (1/2 each: one document per
version has no `<details>` block and no image), 7.8 in the `w` cells (0/2 each: risks
nobody gave, written once the user said they could not answer), 7.6 (1/2 each).

Outside the table, per document:

| | 1.6.0 | 1.7.0 |
|---|---|---|
| agentless passives, evals 1, 4, 6 | 2, 2, 0, 0, 4, 3 | 2, 1, 0, 1, 1, 3 |
| agentless passives, evals 7, 9 (`w`) | 1, 3, 3, 1 | 2, 1, 1, 2 |
| words, evals 1, 4, 6 | 861, 1217, 610, 641, 1079, 1067 | 1030, 1054, 636, 550, 1053, 1086 |
| `technical-writing` invoked through the Skill tool | 0/10 | 9/10 |
| `unslop` invoked | 9/10 | 10/10 |
| `technical-writing` before `unslop` | – | 9/9 |
| tokens per run, evals 1, 4, 6 | 238 k | 308 k |
| US$ per run, evals 1, 4, 6 | 0.179 | 0.205 |
| US$ per run, evals 7, 9 (`w`) | 0.146 | 0.169 |

The tenth 1.7.0 run (`6/v170/run-2`) opened `technical-writing/SKILL.md` with Read, did
not invoke it, and told the user it had applied it. Between the `technical-writing` call
and the `unslop` call, the nine sessions made 0 to 3 edits to the document (0, 2, 1, 3, 2,
2, 1, 2, 3). Each edit turns one sentence around a subject: "A rejeição acontece no
gateway" became "O gateway rejeita a requisição", "Cada tentativa fica registrada" became
"O serviço de entrega registra cada tentativa".

**Reading.** By the rule written in `checks.json` before the runs, the checks do not
separate the versions. No check differs by two runs out of two on more than one eval, and
the totals are 98/104 against 98/104 on the prompt alone.

- **The passive count did what the prediction said.** 0 to 4 per document in both
  versions, ranges overlapping in every eval. 1.6.0 already leaves little to remove.
- **The actor check does not favor 1.7.0.** It is the check written for what the change
  claims, and it is met in 6 of 10 documents with 1.6.0 and in 4 of 10 with 1.7.0, with
  four of the misses on a split. The one two-out-of-two difference of the whole batch is
  this check on eval 7, against 1.7.0. One of those sentences is the pass's own work: the
  draft said "não foram discutidos" and the edit after the `technical-writing` call wrote
  "O time ainda não discutiu…". The skill turned a passive into an active sentence by
  supplying "o time", where its contract says to look the actor up or ask.
- **Eval 9 leans the other way by one run** on 9.10 and 9.11. That check moved by one run
  between adjacent versions before (iteration-23, 3/4 against 2/4) with no text about it
  changed, so one run here is not attributed to the pass.
- **Structure was not harmed.** Headings, the house pattern, the template order and the
  diagram checks are equal in both versions.
- **The cost is one more skill per document:** about 29% more tokens and 15% more US$ per
  run on evals 1, 4 and 6.

**Two findings that are not about the versions.**

- With `technical-writing` installed next to `design-doc`, the request of eval 9
  ("Atualiza a documentação" for a shipped design doc) never reached `design-doc` through
  the Skill tool in eight sessions, reached `technical-writing` in four, and in one of
  those the shipped document's body was rewritten, which is what `design-doc` exists to
  prevent on this eval. No session ran with `design-doc` installed alone, so this does not
  show that `technical-writing` took the request from it. The trigger sweep of
  `technical-writing` loads only the candidate and cannot see this case.
- Given the prompt alone, `design-doc` asks before writing on eval 7 in both versions (4
  of 4), where `evals.json` expects a document with the missing sections marked as
  pending. Earlier iterations ran this eval with a brief that said the user could not
  reply.

**Limits.** Two runs per cell measure no rate. The judge could tell the version in every
1.7.0 packet with a document: all ten replies say that `technical-writing` was applied.
The `w` cells change the user's message, and the judge packet shows it without the added
sentence. The skills sit inside the project, so a search of the project finds their files:
several eval 9 sessions read `design-doc`'s files without invoking it, which a user-scope
install would not allow. Only three skills were installed; `structurizr` and
`mermaid-sequence` were not, and no session had Docker, so every architecture image is a
placeholder in both versions. The checks for evals 1, 4, 6 and 7 are new and were not
tried on an older output. The entry of the amendment was written into `checks.json` right
after the eight `w` runs and not before, because the script that was to record it stopped
on an unrelated assertion; the decision is in a comment of `run.py` written before them,
and no output of those runs had been read. `grade.py` was written after the first 1.7.0
run (the probe, `6/v170/run-1`) had been read, from checks frozen before it. "The
Structurizr DSL validates" (eval 7) was not checked.

**Cost.** Executors: 35 sessions, the seven invalid first attempts included, US$ 4.56
(US$ 0.05 to 0.26 per run). Judges: 84 calls, 0.67 M tokens, US$ 4.77.
