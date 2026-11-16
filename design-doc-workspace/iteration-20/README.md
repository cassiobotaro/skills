# iteration-20 — smoke test of the two behaviours added in design-doc 1.5.0

**Change under test.** After re-reading Malte Ubl's "Design Docs at Google", the skill
gained a section on updating a document whose design changed (edit in place until the
system ships, then write a linked amendment and leave the original's body alone) and an
extension of contract 5 (when nothing is ambiguous, say a doc is not needed and ask once).
Reference-only additions (constraints, privacy, system-context diagram, non-goal nuance,
prototype link) are not exercised here.

**Method.** One run each of the two new evals, 9 (`amend-shipped-doc`) and 10
(`unambiguous-change-no-doc`), with the skill, on claude-fable-5-2. Single arm, no
baseline, no frozen check list and no blind judge: the byte-decidable assertions were
checked by script (`find`, `diff` against the fixture), the rest read by the author of the
change. This confirms the new text is followed; it does not measure a delta.

**Result, eval 9.** By script: one new document under `docs/design/`; the original differs
from the fixture only in two header rows (`Última atualização`, new `Emendado por` link);
the amendment links back. By reading: it states the change and the user's reason, and
sends nine gaps to Open questions. Two phrases go beyond what was established and would
fail a strict "nothing invented" check: "às vezes" on the 404, and "roda com dois workers
sem o 404" as an achieved result. The costs listed are derived from the original
document's trade-offs and are labelled as such.

**Result, eval 10.** By script: no file created besides the reply. By reading: says no
choice is open, asks the single question, offers the mini-doc. The four example topics it
lists (validation, personal data, API consumers, migration) are phrased as questions.

Tokens: 56 094 (eval 9), 45 929 (eval 10).
