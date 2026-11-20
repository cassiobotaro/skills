# iteration-14 — the same ablation, in Portuguese on a fresh log (adr 1.4.1, no skill change)

**Question.** Iterations 12 and 13 removed the Title, Decision and Length bullets of
step 4 and found no effect, both times in English. The bullets speak English ("a short
noun phrase", the example "Use ISO 8601 format for dates", "active voice"), and so does
the model ADR in `references/examples.md`. Does the result hold when the record has to
be written in another language?

**Method.** Same two arms (`skill-a` byte-identical to the working tree, `skill-b` minus
the three bullets; both copied unchanged from iteration-12), same executor brief, four
runs per cell, executor aliases `sonnet` and `haiku` (claude-sonnet-5-5 and
claude-haiku-5-5 by this session's mapping; ids not read back from the transcripts). The
prompt is the rambling request of iteration-13 put into Brazilian Portuguese
(`checks.json`; not in `evals.json`), on an empty repository, so the log is born in
Portuguese: translated seed as 0001, the decision as 0002, scaffolding in English by
rule 2. Language and fresh log change together against iteration-13. Checks frozen
before the first run; the Portuguese forms T.1 and T.2 accept were chosen after reading
four earlier eval-5 outputs (iterations 4 to 7). Every check by `grade.py` from bytes
(`script-checks.json`). No judge.

**Results** (runs meeting the check / runs).

| Check | a-sonnet | b-sonnet | a-haiku | b-haiku |
|---|---|---|---|---|
| F.1 exactly 0001 and 0002, nothing else | 2/4 | 1/4 | 4/4 | 3/4 |
| F.2 `# 2.`, English `Date:` and headings, Accepted | 4/4 | 4/4 | 4/4 | 4/4 |
| F.3 0002 slug derived from the title | 4/4 | 4/4 | 4/4 | 4/4 |
| F.4 prose in Portuguese | 4/4 | 4/4 | 4/4 | 4/4 |
| T.1 title is a short phrase | 4/4 | 4/4 | 4/4 | 4/4 |
| T.2 Decision in the first person plural, names Sidekiq | 4/4 | 4/4 | 4/4 | 4/4 |
| T.3 40 lines or fewer | 4/4 | 4/4 | 4/4 | 4/4 |
| title words per run | 7, 6, 8, 8 | 8, 8, 8, 8 | 8, 8, 10, 6 | 6, 6, 8, 8 |
| lines per run | 31, 27, 27, 25 | 25, 27, 27, 29 | 25, 33, 29, 29 | 33, 27, 31, 31 |
| words per run | 324, 268, 276, 285 | 266, 279, 280, 305 | 268, 351, 321, 307 | 314, 311, 338, 303 |
| Decision words per run | 64, 41, 46, 50 | 48, 46, 61, 49 | 47, 69, 63, 49 | 49, 68, 71, 63 |
| passives in Decision per run | 1, 1, 1, 1 | 1, 1, 1, 1 | 1, 1, 1, 1 | 1, 1, 1, 1 |
| "ficou decidido" kept | 0 | 0 | 0 | 0 |
| rename tangent, people named | 0 | 0 | 0 | 0 |

- **Title.** Sixteen infinitive phrases, all starting "Gerar PDF(s) de fatura em
  background" or "…em segundo plano", most ending "com Sidekiq" or "via Sidekiq". The
  longest, ten words, is in arm a ("Gerar PDFs de fatura em background, fora da request
  web", haiku run-3).
- **Decision.** All sixteen open with "Vamos tirar a geração de/do PDF … da request"
  (or "da requisição");
  none keeps "ficou decidido" or "vai ser tirada". The one passive in each is the file
  that "será gravado", "será colocado" or "é gravado" in the bucket, the same sentence
  that carried the one passive in iteration-13.
- **Length.** 25 to 33 lines and 266 to 351 words, overlapping across arms.
- **Scaffolding.** `Date:`, the four headings and `Accepted` in English in all sixteen;
  prose in Portuguese in all sixteen.

**F.1 is not about the ablation.** Six runs miss it, for three unrelated reasons:

- Five sonnet runs (a: run-3, run-4; b: run-1, run-2, run-4) wrote the harness's own
  `reply.md` inside `outputs/` instead of beside it. Without that file each has exactly
  the two ADRs. A brief-compliance slip of the executor, on sonnet only, in both arms.
- b-haiku run-1 named the seed `0001-registrar-decisões-de-arquitetura.md`, accent kept.
  The other fifteen fold it to `decisoes`. `SKILL.md` says "every run of
  non-alphanumeric characters collapsed to a single hyphen" and is silent on accented
  letters, which are alphanumeric by one reading and not by another. adr-tools' own
  pipeline (`tr -Ccs [:alnum:] -`) gives `decis-es` under the three Linux `tr`
  implementations tried afterwards (GNU, BusyBox, uutils); macOS was not tried. One run in sixteen, and the rule that produced it is in "The
  format", not in the removed bullets.
- Not caught by F.1 but found reading the tree: a-haiku run-3 kept the English filename
  `0001-record-architecture-decisions.md` over a seed whose title and body it
  translated, against step 5 ("derive the filename slug from the translated title").

**Reading.** Indistinguishable a third time. Across iterations 12 to 14 that is 48 runs,
three prompts, two languages and two models, and the three bullets show an effect on no
check. In Portuguese the behaviour is carried by the same things as in English: the
template's `"We will ..."` comes out as "Vamos …", and the infinitive title follows the
imperative of the template's own H1 and of the examples file. The bullets can be removed
on this evidence; what they would save is 54 words, 2% of the body.

What the Portuguese run did surface is outside the ablation: the slug rule says nothing
about accented letters, and one run in sixteen in each of two different ways got the
seed's filename wrong.

**Limits.** Four runs per cell measure no rate; this is "never" three times. Invention
was not judged in any of the three iterations, and at least one sentence here would
deserve a judge ("foi vetado pelo jurídico" for the user's "o jurídico não quer"). The
self-review line `Decision says "We will …"` stayed in both arms throughout, so the
Decision bullet was never tested without its duplicate. A Portuguese request on an
existing Portuguese log was not run; no such fixture exists.

**Cost.** Executors 16 runs, 0.88 M tokens (sonnet 0.43 M, haiku 0.45 M). No judge calls.
