# iteration-15 — adr 1.4.2 checked after the edit: the cut, and accents in the slug

**Change under test.** 1.4.2 does two things. It removes the Title, Decision and Length
bullets of step 4, which iterations 12 to 14 found without effect in 48 runs. And it
settles what iteration-14 found unsettled: the Filename rule now says that
"alphanumeric" means ASCII letters and digits, as adr-tools computes the slug, so an
accented letter becomes a hyphen, never transliterated and never kept ("Registrar
decisões de arquitetura" → `0001-registrar-decis-es-de-arquitetura.md`). The same rule
and two rows went into the slug table of `references/examples.md`, and the assertions of
evals 1 and 5 in `../evals/evals.json` were reworded to state it.

**What "as adr-tools computes it" rests on.** `src/adr-new` in npryce/adr-tools builds
the slug with `tr -Ccs [:alnum:] - | tr [:upper:] [:lower:]` and trims the edges. Run on
"Registrar decisões de arquitetura", that pipeline gives
`registrar-decis-es-de-arquitetura` under GNU tr (debian:stable-slim), BusyBox tr
(alpine:3) and uutils tr (this machine), with and without a UTF-8 locale. It was not run
on macOS, whose `tr` is a different implementation and may treat `õ` as alphanumeric in
a UTF-8 locale; if it does, adr-tools on a Mac keeps the accent and this rule matches
adr-tools on Linux only.

**Method.** One arm: `skill-a`, a copy of the working tree as edited (still identical to
it when the runs were graded). Same prompt, empty repository and executor brief as
iteration-14. Four runs each on `sonnet` and `haiku` (claude-sonnet-5-5 and
claude-haiku-5-5 by this session's mapping; ids not read back from the transcripts).
Checks frozen in `checks.json` before the first run; every check by `grade.py` from bytes
(`script-checks.json`). No judge. The "before" column is the sixteen runs of
iteration-14 (1.4.1 and its ablated copy, which share the Filename rule) put through this
iteration's grader, not re-run.

**Results** (runs meeting the check / runs).

| Check | sonnet | haiku | before (iteration-14, 16 runs) |
|---|---|---|---|
| F.1 exactly 0001 and 0002 under doc/adr/ | 4/4 | 4/4 | 16/16 |
| F.2 `# 2.`, English `Date:` and headings, Accepted | 4/4 | 4/4 | 16/16 |
| S.1 seed slug is the ASCII-only derivation of its title | 4/4 | 4/4 | 0/15 where the title has an accent |
| S.2 the same for 0002 | 4/4 | 4/4 | 16/16, no title had an accent |
| S.3 every filename pure ASCII | 4/4 | 4/4 | 15/16 |
| T.1 title is a short phrase (10 words or fewer) | 4/4 | 3/4 | 16/16 |
| T.2 Decision in the first person plural, names Sidekiq | 4/4 | 4/4 | 16/16 |
| T.3 40 lines or fewer | 4/4 | 4/4 | 16/16 |
| title words per run | 8, 8, 8, 8 | 6, 10, 10, 11 | 6 to 10 |
| lines per run | 31, 29, 27, 27 | 27, 25, 27, 25 | 25 to 33 |

- **The slug rule took.** All eight seeds are `0001-registrar-decis-es-de-arquitetura.md`
  over an H1 that keeps "decisões". Before the edit no run with an accented seed title
  produced that name: thirteen folded to `decisoes`, one kept the accent, and one kept
  the English filename. The only 0002 title with an accent in this iteration ("Mover a
  geração de PDFs de fatura para segundo plano", haiku run-3) became `…-gera-o-…`: two
  accented letters in a row, one hyphen, as the rule says.
- **One title is a word over.** haiku run-4: "Gerar o PDF da fatura em background, fora
  da request web", eleven words against the ten of T.1. Two more haiku titles sit at ten.
  It is a phrase, not a sentence, and the same tail ("…, fora da request web", ten words)
  appeared once in iteration-14 with the Title bullet in place. Pooling the Portuguese
  haiku runs: 6 to 11 words in the eight without the bullet (four ablated in
  iteration-14, four here), 6 to 10 in the four with it. That is one run over a
  threshold borrowed from English, in a language that spends more words on articles and
  prepositions; it is not evidence that the bullet was holding titles short, and it is
  not nothing either. Sonnet's four titles are eight words each.
- **Decision and length** as in iterations 13 and 14: "Vamos tirar a geração…", Sidekiq
  named, 25 to 31 lines.
- **Harness.** Two sonnet runs again wrote `reply.md` inside `outputs/` (O.5). F.1 in
  this iteration counts only what is under `doc/adr/`.

**Reading.** The accent rule works as written on both models: the sentence and the
example were enough against a default that fifteen of sixteen runs had followed the
other way. The cut holds on every check but T.1 on haiku, where one title in four is one
word past the line. If short titles in Portuguese matter more than the 14 words the
Title bullet costs, restoring that one bullet is the cheap guard; nothing here says the
Decision or Length bullets are missed.

**Limits.** Eight runs, one prompt, one fixture state (empty repository). The slug rule
was exercised on one seed title and one decision title; a supersede link to a file with
a hyphenated accent was not exercised. Invention not judged. macOS behaviour of
adr-tools not verified.

**Cost.** Executors 8 runs, 0.44 M tokens (sonnet 0.21 M, haiku 0.23 M). No judge calls.
