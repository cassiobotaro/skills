# Does a candidate description win the request to update a shipped design doc?

**Why.** `technical-writing-workspace/trigger-evals/border-design-doc-2026-11-22/` gave
eval 9 ("…mudou onde os arquivos gerados ficam… Atualiza a documentação.", a design doc
of a system in production) to sixteen sessions with `design-doc` 1.8.0 loaded as a
plugin. None invoked it and all sixteen rewrote the body of the approved document. That
is the reference for the current description (642 characters), taken the same day with
the same harness.

**Candidate.** `candidate-a.txt`, 982 characters. It adds "update" to the
opening verbs and one clause in the form that worked for `code-comments` 1.1.0: it names
the request, says that it looks like a plain edit and is not one, and says what comes
first (consult the skill before touching the file). Nothing of the current text is
removed. The shipped `SKILL.md` is not changed by this probe: the candidate is written
into a copy of the plugin outside the repository.

**Method.** `run.py`, `claude -p` on `claude-sonnet-5-5`, each session in a project of
its own outside the repository, `design-doc` (with the candidate), `unslop` and
`technical-writing` 1.0.1 loaded with `--plugin-dir`, the prompt alone.

- `update`: eval 9 of `design-doc`, word for word, its fixture. Eight sessions.
- `near`: a request to update a document that is not a design doc, in the `exporter`
  fixture of `technical-writing` (a `docs/pipeline.md` that describes a running
  service): "A gente subiu o limite do export de 100 mil pra 250 mil linhas. Atualiza a
  documentação." Four sessions.

Counted from the transcript and the files: D, the Skill tool was called with
`design-doc`; T, with `technical-writing`; in `update`, B, the body of the shipped
document changed, and N, a new file exists under `docs/design/`.

**Rule, written before the runs.** The candidate wins the request if D is 6/8 or more in
`update`, against 0/16 for the current text. 2/8 or less means it does not. In `near`, D
should be 0/4: a session that invokes `design-doc` there is a false fire and is listed.
Eight and four sessions measure no rate. This probe is not the routine trigger check: it
says nothing about the ten positives and ten negatives of `trigger_eval.json`, which
have to be swept before and after if the candidate is adopted.

## Results

A second candidate was written after the first results, before its own runs:
`candidate-b.txt`, 1013 characters. It differs from the first only in the clause: the
quoted requests name the design doc ("update the design doc", "o design mudou, atualiza
o design doc") where the first quoted "update the docs" and "atualiza a documentação",
and it ends "before touching a design doc". The question for it was whether the narrower
wording keeps the request of eval 9, which says "Atualiza a documentação", and loses the
false fire. Four more `near` sessions were added for the first candidate, so that both
have eight.

| | current text (border probe, same day) | candidate a | candidate b |
|---|---|---|---|
| `update`: D `design-doc` invoked | 0/16 | 8/8 | 8/8 |
| `update`: B body of the shipped document changed | 16/16 | 0/8 | 0/8 |
| `update`: N new file | 0/16 | 0/8 | 0/8 |
| `near`: D `design-doc` invoked (false fire) | not run | 2/8 | 0/8 |
| `near`: T `technical-writing` invoked | not run | 0/8 | 1/8 |

**Reading, by the rule above.** Both candidates win the request: 8/8 against 0/16, and
no session touched the body of the approved document. Every `update` session with a
candidate asked its questions first and wrote no file, as the skill does on this request
without a brief (iteration-27). Candidate a fired on the neighbouring request in two of
eight sessions; in both the session invoked the skill, said that `docs/pipeline.md` is
not a design doc, and made the same edit as the others, so the cost there was one skill
read. Candidate b did not fire on it in
eight. Candidate b is the one to take forward.

**Limits.** One request per cell, both in Portuguese, on `claude-sonnet-5-5`; eight
sessions measure no rate. The `near` request was not run with the current description.
The ten positives and ten negatives of `trigger_eval.json` were not swept with either
candidate, and candidate b is eleven characters under the limit `scripts/validate.py`
enforces.

**Cost.** 32 sessions, US$ 1.52.
