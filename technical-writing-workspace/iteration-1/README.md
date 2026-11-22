# iteration-1 — first behavioral A/B of technical-writing 1.0.0

**Question.** With the skill read, does an agent asked to write, revise or review a
technical document do it better than the same agent without it?

**Method.** Two cells, two runs per eval each, 24 runs. `with_skill` is told to read
`technical-writing/skills/technical-writing/SKILL.md` (1.0.0, commit 9ad8a5f) and follow
it; `without_skill` gets the same brief without that step. No prompt names the skill. The
executors are headless sessions (`claude -p`, `run.py`) on `claude-sonnet-5-5`, read back
from each session, each started in its own copy of the eval's fixture (an empty directory
for eval 5, which pastes a diff), with `--setting-sources project,local` and
`SHELL=/bin/bash`. The fixture copies were built before the workers started. The
session's final message is the reply.

The checks are the 121 of `../evals/checks-baseline.json`, frozen on 2026-11-22 before
any run (in the working tree; no commit existed yet when the runs were made): 36 decided
by `grade.py` from the bytes, 85 judged by `eval-tools/judge.py` on `claude-opus-5-5`,
three passes per packet, met only when the three agree.

**No run is invalid.** Every reply was read before counting. All four runs of eval 6 left
the file untouched after reading it, which is what that eval expects. All four runs of
eval 3 wrote a runbook, so the rule that reports a questions-only run apart did not
apply. One thing in the transcripts is not an accident of the harness and is counted as
it came out: both `without_skill` runs of eval 3 made a single tool call, the `Write` of
the runbook, and opened no file of the project. Their replies say "Não conheço o seu
sistema".

**Result.** Checks met over total, two runs per cell:

| Kind | with_skill | without_skill |
|---|---|---|
| file and absence (script) | 72/72 | 71/72 |
| reply | 73/76 | 56/76 |
| negative | 28/32 | 25/32 |
| invention | 58/62 | 51/62 |
| all | 231/242 | 203/242 |

The checks that were not met in every run:

| Check | with_skill | without_skill | What was found |
|---|---|---|---|
| 3.3 the runbook states the threshold (more than 10 in `exports.dead`) | 2/2 | 0/2 | a `[PREENCHER]` placeholder; one gives "> 50 mensagens por 10 min" as an example |
| 3.4 the runbook states the 5 minutes | 2/2 | 0/2 | same placeholder |
| 3.8 `--dry-run` before the command that moves | 2/2 | 0/2 | neither `requeue_dead.py` nor `--dry-run` appears |
| 3.16 no escalation policy or time limit invented | 2/2 | 0/2 | "causa não identificada em 30 minutos" in both |
| 4.2 questions for the author apart from proposed edits | 2/2 | 0/2 | groups by severity or by topic, questions mixed in |
| 4.3 says the page mixes kinds of document | 2/2 | 0/2 | the history paragraph is called out, the mix is not |
| 5.3 the 413 rejection within the first three sentences | 2/2 | 0/2 | the description opens on the incident and the old code |
| 5.4 the stream within the first three sentences | 2/2 | 0/2 | same |
| 5.7 says how to verify the change | 2/2 | 0/2 | "Added the unit test above. I haven't run the suite." |
| 2.29 no agentless passive about the pipeline in the README | 2/2 | 0/2 | "The job was queued", "Requeued messages are published without the `x-attempts` header" |
| 1.26 every figure is one of the four the check lists | 2/2 | 0/2 | see the note on this check under Limits |
| 5.10 no agentless passive about the change | 1/2 | 0/2 | "the body is now read with `request.stream()`"; with the skill, "That upload is not capped", borderline; one split 1/3 |
| 1.20 the backups claim is still in the document | 2/2 | 1/2 | one run replaced the sentence with a TODO |
| 1.23 no component the fixture lacks | 2/2 | 1/2 | "Prometheus fires the alert"; "an S3 lifecycle rule or an AWS Backup plan" offered inside a TODO |
| 2.19 the README does not retell `docs/pipeline.md` | 2/2 | 1/2 | three of the four stages with their details and a status table |
| 3.14 no contact invented | 2/2 | 1/2 | a secondary on-call and customer support as lines to fill |
| 3.15 no channel invented | 2/2 | 1/2 | "avise o canal de incidentes" |
| 3.20 nothing about how incidents usually go | 2/2 | 1/2 | "se a DLQ está estável … é falha pontual"; split 2/3 |
| 4.5 quotes three clauses that hide their actor | 2/2 | 1/2 | two quoted as such; split 1/3 |
| 4.10 no recipient of the email stated | 2/2 | 1/2 | a proposed rewrite says "We email the account owner…" |
| 5.8 names the new test | 2/2 | 1/2 | script |
| 2.20 no license and no license section | 0/2 | 2/2 | a "License and support" / "License and help" heading over a TODO that says the repository has no LICENSE file |
| 1.19 no agentless passive in Delivery | 1/2 | 2/2 | "Once the upload is done", the fixture's own clause, kept; borderline |
| 5.5 the reason within the first three sentences | 1/2 | 2/2 | the OOM kills come in the fourth sentence |
| 3.21 no tooling the fixture does not show | 0/2 | 0/2 | without the skill, a dashboard and a log system as available; with it, logs and a panel named inside TODOs that say the repository does not show them, and Prometheus; both skill runs split 2/3 |
| 1.27 at most three lines on what changed | 0/2 | 0/2 | four lines or more in every run |
| 1.28 the reply does not summarize the document | 0/2 | 0/2 | every reply retells the sections |

Five splits in 340 judged verdicts (3.21 twice, 3.20, 4.5, 5.10), all counted as not met.

**Reading.**

- **Naming the actor from the code is not what separates the cells.** In eval 1 every run
  of both cells named the gateway, the worker and the notifier for each action (1.5 to
  1.14, 2/2 everywhere), left the backups without an actor (1.21) and asked who rotates
  them (1.22). The two smoke sessions of eval 1 did the same. On a revision where the code
  sits next to the document, the model does the actor pass unaided.
- **Reading the repository before writing a new document does separate them, on one
  eval.** In eval 3 both runs without the skill wrote a generic runbook without opening a
  file, so the threshold, the duration and the script the repository ships are
  placeholders (3.3, 3.4, 3.8), and a 30-minute escalation limit appears that nobody gave
  (3.16). Both runs with the skill read the fixture first. In eval 2 both cells read it.
- **The shape of a review and of a pull request description separates them.** Questions
  apart from edits (4.2), the mix of document kinds (4.3), what the change does before
  why (5.3, 5.4) and how to verify it (5.7) are met in both runs with the skill and in
  neither without it. These follow `references/documents.md` and the "Review" paragraph.
- **Agentless passives in new prose** separate on the README (2.29) and lean the same way
  on the pull request description (5.10).
- **The skill adds a license section to a README that has no license.** Both runs put a
  heading over a TODO (2.20). The cause is the README entry of `references/documents.md`,
  whose list ends with "License, and where to ask for help". The eval asks for no license
  to appear; the TODO invents none, but the section is the skill's and not the
  repository's.
- **Two rules of the skill fail in both of its runs.** After a revision, the reply is to
  say what changed in at most three lines and not summarize the document. In eval 1 both
  skill runs gave four or five lines and retold the three sections (1.27, 1.28), as both
  baseline runs did. `explain` failed the same rule the same way in its iteration-1.
- **A good guide is left alone by both cells** (eval 6, all 60 checks met).

**Limits.** Two runs per cell: no rate is measured, and a one-run difference is not a
finding. The brief tells the `with_skill` executor to read the skill, so this says
nothing about triggering. `unslop` was not installed in either cell, so step 5 of the
skill had nothing to invoke; one skill run says so in its reply. The repository's
`AGENTS.md` loads in both cells and names the skill. The packets do not name the cell,
but two contain the word "skill" because the reply does (`6/with_skill/run-1`,
`6/with_skill/run-2`, "it already meets the skill's rules"). The author of the checks had
read the note in `MAINTAINING.md` about three smoke sessions; the section that the smoke
baseline added (check 1.4) did not appear here.

Check 1.26 lists four figures and says no other appears. The figures the baseline added
in eval 1 are mostly in the fixture: "more than 10 messages for 5 minutes" is
`deploy/alerts.yaml` and "default 100" is `scripts/requeue_dead.py`. So 1.26 at 0/2 says
that the baseline document grew to cover the alert and the requeue script (45 and 47
lines against 25 with the skill, from a fixture of 23), and it is not evidence of an
invented number. The check stays as frozen; a later iteration can amend it by date.

The allowlist of `run.py` refuses a compound command such as a `cat` loop: seven runs had
a Bash call refused (five with the skill, two without) and went on with single reads.

**Cost.** Executors: 24 sessions, 2.16 M tokens summed over turns, US$ 1.45 (US$ 0.027 to
0.151 per run; 0.077 on average with the skill, 0.043 without). Judges: 72 calls, 0.49 M
tokens, US$ 3.73.
