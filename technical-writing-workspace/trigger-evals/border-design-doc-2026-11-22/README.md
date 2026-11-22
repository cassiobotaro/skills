# Border with design-doc — who gets "atualiza a documentação" of a shipped design doc

**Why.** `design-doc-workspace/iteration-27/` gave eval 9 of `design-doc` to eight sessions
that had `design-doc`, `technical-writing` and `unslop` installed. None invoked
`design-doc`, four invoked `technical-writing`, and one of those rewrote the body of the
shipped document. No session had run with `design-doc` installed without
`technical-writing`, so those eight do not say whether `technical-writing` takes the
request or whether `design-doc` never got it in the first place.

**Method.** Two cells, eight sessions each, order interleaved, `claude -p` on
`claude-sonnet-5-5`, serial rules do not apply (this is not the trigger harness: the
skills are really installed and the session does the work). Each session starts in a
project of its own outside the repository, a fresh git repository with the fixture of
eval 9 and the skills under `.claude/skills/`, and gets the prompt of eval 9 word for
word, as in iteration-27.

- `alone`: `design-doc` 1.8.0 and `unslop`.
- `both`: the same two and `technical-writing` 1.0.0.

**What is counted** (from the transcript and the files, by `run.py`; no judge):

- D: the Skill tool was called with `design-doc`.
- T: the Skill tool was called with `technical-writing`.
- B: the body of `docs/design/exportacao-de-relatorios.md`, from `## Visão geral` on,
  changed.
- N: a new file exists under `docs/design/`.

**Rule, written before the runs.** Eight sessions measure no rate; they tell "nearly
every time" from "nearly never".

- `technical-writing` takes the request from `design-doc` if D is 6/8 or more in `alone`
  and 2/8 or less in `both`.
- If D is 2/8 or less in both cells, the request does not reach `design-doc` with or
  without `technical-writing`, and the description to look at is `design-doc`'s.
- Anything else is no claim about D.
- B is reported per cell whatever D says: a rewritten body is the harm, whoever caused it.

**Known artifact.** The skills sit inside the project, so a search of the project finds
their files, and a session can read `design-doc`'s files without invoking it. Both cells
have it.

## First attempt: confounded, kept as `results-in-project.json`

Sixteen sessions with the skills copied into the project's `.claude/skills/` and committed
there gave D 0/8 in `alone` and 1/8 in `both`, T 1/8, B 0/8 in both, N 3/8 and 0/8. The
count of D means nothing: the first command of nearly every session is `git ls-files`
with a `grep -r`, which lists the skill's files, and 15 of the 16 then read
`design-doc`'s files without calling the Skill tool. All 16 replies open by saying the
body of the shipped document stays as it is, which is `design-doc`'s rule. The session
reached the skill through the file system. The eight eval 9 sessions of iteration-27 have
the same defect, so its "invoked in none of eight" says nothing about triggering either.

**Second attempt, same cells, counts and rule, decided before running it:** each plugin
is loaded with `--plugin-dir` from a copy outside the project, so the project holds only
the fixture and the Skill tool is the only way to the skill. One more count: F, the
session touched a skill's files without the Skill tool (expected 0).

## Second attempt: `results.json`

| | `alone` | `both` |
|---|---|---|
| D `design-doc` invoked | 0/8 | 0/8 |
| T `technical-writing` invoked | – | 0/8 |
| B body of the shipped document changed | 8/8 | 8/8 |
| N new file under `docs/design/` | 0/8 | 0/8 |
| F a skill's files touched without the Skill tool | 0/8 | 0/8 |

Every session listed the installed skills (`design-doc:design-doc` and the others) and
had the Skill tool. None called it. All sixteen edited the approved document in place,
below its header; the two replies read in full say they rewrote Solução and the
trade-offs and moved the old design into the alternatives.

**Canary.** A zero from a broken harness looks the same, so two sessions got eval 6 of
`design-doc` ("Escreve o design doc do nosso serviço de webhooks de saída…") with the
three plugins loaded the same way. Both invoked `design-doc:design-doc` and then
`unslop:unslop` and wrote the document (`transcripts/canary-run-*.jsonl`). The skill
fires in this harness when the request is a clear one.

**Reading, by the rule above.** D is 0/8 in both cells, so `technical-writing` does not
take this request from `design-doc`: nothing takes it, and the description to look at is
`design-doc`'s. Its quoted requests are about writing and reviewing; the update of a
document whose system already shipped, which the skill handles since 1.5.0 (amend, never
rewrite), is the case the description does not win. The cost of the miss is the harm
that rule exists to prevent, in 16 of 16 sessions.

`technical-writing` fired in none of eight sessions here and in one of eight in the first
attempt; the four of eight in iteration-27 came from the same confounded setup as the
first attempt. On this evidence its description needs no exclusion for this request.

**Limits.** One request, in Portuguese, on `claude-sonnet-5-5`; eight sessions per cell
measure no rate, and 0/16 against 2/2 is of the "never against every time" kind. Loaded
with `--plugin-dir`, a plugin's `references/` are outside the project and a Read of them
is refused without `--add-dir` (both canary sessions had such refusals), so this harness
is good for counting invocations and not for grading documents. Every session of the
second attempt had at least one Bash call refused (a `python3` heredoc that edits the
file) and went on with Edit.

**Cost.** First attempt: 16 sessions, US$ 1.07. Second: 16 sessions, US$ 1.35. Canary: 2
sessions, US$ 0.31.
