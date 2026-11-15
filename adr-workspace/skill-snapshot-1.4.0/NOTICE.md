# Notices and attribution

This skill contains material condensed and adapted from third-party sources. Changes
were made in all cases (condensation, reorganization, added guidance).

## Documenting Architecture Decisions — Michael Nygard

The ADR concept, the four-section structure (Status, Context, Decision, Consequences),
and the writing guidance (value-neutral context, "We will …" decisions, all
consequences listed, one–two page length) are condensed from **Michael Nygard**'s
article *Documenting Architecture Decisions* (November 15, 2011):
<https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
(originally published at thinkrelevance.com).

## adr-tools — Nat Pryce

The file conventions (sequential 4-digit numbering, `NNNN-slug.md` filenames, `doc/adr`
default directory, `.adr-dir` override, Status-section link lines for
supersede/amend/clarify) and the texts reproduced in `references/examples.md` (the
default template, the `adr init` seed ADR, and example ADRs from the project's own
decision log) are derived from **adr-tools** by **Nat Pryce**:
<https://github.com/npryce/adr-tools>

Per the adr-tools `LICENSE.txt`:

- The tool itself is © 2016 Nat Pryce, licensed **GPL-3.0-or-later**. This skill does
  **not** include or redistribute any of the adr-tools scripts; it only reproduces
  file-format conventions (which it re-implements independently).
- "Content that this tool adds to your project" — the template and seed-ADR text this
  skill reproduces — is licensed **Creative Commons Attribution 4.0 (CC BY 4.0)**:
  <https://creativecommons.org/licenses/by/4.0/>

One deliberate deviation: this skill writes the dictionary spelling "Superseded by" /
"Supersedes" in status links (adr-tools emits the legacy spelling "Superceded by" /
"Supercedes"); both spellings are recognized when reading.
