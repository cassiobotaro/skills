---
name: adr
description: >
  Write and maintain Architecture Decision Records (ADRs) in the Michael Nygard format,
  file-compatible with Nat Pryce's adr-tools (sequential numbering, NNNN-slug.md filenames,
  supersede/amend links in the Status section, .adr-dir discovery). Use this skill whenever
  the user wants to record, document, revise, supersede, or amend an architecture or
  technology decision — "write an ADR", "document this decision", "we decided to use X
  over Y", "record why we chose Z", "replace ADR N", "start a decision log" — even if
  they never say the acronym "ADR".
---

# Architecture Decision Records (adr-tools compatible)

This skill writes and maintains a project's decision log: short Markdown files, one per
architecturally significant decision (a decision that affects the structure,
non-functional characteristics, dependencies, interfaces, or construction techniques of
the system). The deliverable of every invocation is files on disk — a new
`NNNN-title.md`, plus a minimal edit to an old ADR's Status section when the new
decision supersedes or amends it.

## The contract

These rules exist because a decision log is read by future developers who weren't in the
room, to save them from blindly accepting a stale decision or blindly reversing a sound
one. Its whole value is the recorded *why* — an invented rationale poisons it.

1. **Record, don't invent.** The ADR documents a real decision and the user's actual
   reasons. Never fabricate forces, alternatives, metrics, or consequences that the user
   (or the repository) did not establish. When the decision is too vague to fill the
   sections honestly, ask — see step 3. Polishing the user's words into good prose is
   your job; supplying missing facts is not.

2. **Files follow the log's language.** New ADRs are written in the language of the
   conversation — title, date label, section headings, status words, link verbs, and
   body alike.
   The one thing that outranks the conversation language is consistency: the log must
   read consistently end to end, so when a decision log already exists, match its
   language (a log in two languages is worse than either), just as step 1 matches an
   existing log's format.

3. **One ADR, one decision.** Each record describes one set of forces and a single
   decision in response to them. If the user describes two decisions, write two ADRs.

4. **ADRs are immutable except their Status section.** Once accepted, the body is never
   edited: a reversed or changed decision gets a *new* ADR that supersedes the old one,
   because it is still relevant to know what WAS the decision and is no longer. The only
   legitimate edits to an existing ADR are status changes and status-section links.

5. **Exact adr-tools file conventions** (next section), so that `adr list`,
   `adr generate toc` / `graph`, and Structurizr's `!adrs` importer all work on the
   files unchanged.

## The format — exact

```markdown
# 4. Use stateless JWT sessions

Date: 2026-06-04

## Status

Accepted

## Context

The issue motivating this decision, and any context that influences or constrains the
decision — written as value-neutral fact.

## Decision

The change that we're proposing or have agreed to implement: "We will ..."

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change that
will need to be mitigated. All of them, not just the positive ones.
```

- Exactly these four `##` sections, in this order, plus the H1 title and the `Date:`
  line. No extra sections, no YAML frontmatter.
- The template above is in English because this skill is. In a log kept in another
  language, translate the date label, section headings, status words, and link verbs
  into that language (e.g. `Data:` in a Portuguese log — the date value itself stays
  ISO 8601) — the same rendering everywhere in the log — while keeping the structure
  identical: H1 + date line + the same four `##` sections in this order.
- **Numbering**: sequential and monotonic — next number = highest existing numeric
  filename prefix + 1 (treat `0009` as 9, not octal). Numbers are never reused and gaps
  are never backfilled, so "ADR 9" stays a stable reference forever. The H1 uses the
  un-padded number (`# 4. …`); the filename uses 4-digit zero padding.
- **Filename**: `NNNN-slug.md`. Slug = the title, lowercased, with every run of
  non-alphanumeric characters collapsed to a single hyphen and leading/trailing hyphens
  stripped: "Something About Node.JS" → `0001-something-about-node-js.md`.
- **Date**: ISO 8601. Run `date +%Y-%m-%d` — don't guess the current date.
- **Status word**: `Accepted` by default; `Proposed` when the user indicates the
  decision still awaits agreement; `Deprecated` when a decision is retired without a
  replacement. A superseded ADR carries a link line *instead of* a status word (below).
- **Blank-line discipline**: exactly one blank line between every element (after the H1,
  around `Date:`, around every heading, between paragraphs).

### Link lines (inside the Status section)

```
<Verb> [<target's H1 text without "# ">](<target filename, basename only>)
```

e.g. `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`.

- Links go at the END of the Status section, each on its own line, blank lines between.
- The bracketed text is the target's H1 line minus the leading `# ` — number included,
  copied exactly. The href is the target's basename, no path.
- Supersede pair: the new ADR keeps `Accepted` and gains `Supersedes […]`; the old ADR's
  status word is *removed* and replaced by `Superseded by […]` (the link line becomes
  its status).
- `Amends` / `Amended by` and `Clarifies` / `Clarified by` use the same mechanism, but
  both files keep their status word — only supersession removes it. Use Amends when the
  new decision adjusts part of an old one that otherwise stands; Supersedes when it
  replaces it.
- In English logs, write the modern spelling `Superseded by` / `Supersedes`. When
  reading, treat the legacy adr-tools spelling `Superceded by` / `Supercedes` as the
  same relation — and leave the legacy spelling alone in files you aren't otherwise
  required to edit.

## Workflow

### 1. Locate the decision log

In order:

1. A `.adr-dir` file (look in the repo root / walk up from the working directory): its
   contents are the ADR directory path. Honor it — that is how adr-tools pins a custom
   location.
2. `doc/adr/` if it exists (the adr-tools default).
3. An existing ADR collection elsewhere: look for `NNNN-*.md` files under `docs/adr`,
   `docs/adrs`, `docs/decisions`, `docs/architecture/decisions`, `adr/`. If found, work
   where it lives.
4. Nothing found → this is a fresh log; see step 5.

Peek at one existing ADR before writing. If the log visibly follows a different template
(e.g. MADR with YAML frontmatter and "Context and Problem Statement") or is written in a
different language than the conversation, match the log's own format and language and
tell the user — a log in two formats (or two languages) is worse than either alone.

### 2. Read the neighbors

Read the most recent two or three ADRs and any ADR the new one will supersede or amend.
This gives you the next number, the exact H1 titles you'll need for link text, and the
house tone to match.

### 3. Get the substance — or ask

An honest ADR needs three ingredients:

1. **The decision** — what we will do, concretely.
2. **The forces** — why this is being decided now: the technical, political, social, or
   project pressures in tension, and what's wrong with the status quo.
3. **The trade-offs** — what becomes harder, riskier, or more expensive.

If the user already gave all three, do not interrogate them — write. If any are missing,
ask 2–4 targeted questions in the conversation language before writing, for example:
what is replacing the current choice, and why now? what alternatives were on the table?
what downside did the team accept? who hasn't agreed yet (Accepted vs Proposed)?

Don't ask what the repository already answers (numbering, directory, existing titles).
And treat a decision with zero downsides as a red flag: ask for the accepted trade-off
rather than writing a sales pitch — the Consequences section must list *all*
consequences, not just the positive ones.

### 4. Write the ADR

Write as if in conversation with a future developer — full sentences organized into
paragraphs, good prose. Section by section:

- **Title**: a short noun phrase naming the decision ("Use ISO 8601 format for dates"),
  not a sentence.
- **Context**: value-neutral, present-tense fact. Describe the forces and call out the
  ones in tension; do not advocate or foreshadow the answer. Posing the motivating
  question is fine ("How can a user find out about available commands?").
- **Decision**: stated in full sentences, active voice: "We will …". Concrete and
  specific — name the technology, format, or mechanism.
- **Consequences**: every consequence — positive, negative, neutral — each as a short
  standalone paragraph (or a sentence). Bullets are acceptable only as visual style for
  full sentences, never as an excuse for fragments.
- **Length**: the canonical ADRs run 15–40 lines; one or two pages is the absolute
  ceiling. Shorter records get read and kept up to date.

### 5. Initialize a fresh log

When no ADR log exists anywhere, mirror `adr init`: create `doc/adr/`, seed it with the
canonical "record architecture decisions" ADR (content in `references/examples.md`),
and the user's decision becomes `0002`. In an English conversation, use the seed
verbatim as `0001-record-architecture-decisions.md` — only the date changes. In any
other language, translate the seed — title, date label, headings, status, body — so the log starts
in the language it will be kept in, and derive the filename slug from the translated
title. Tell the user about the seed file. If the user asked for a non-default
directory, also write a `.adr-dir` file at the repo root containing that path so
adr-tools and future invocations find it.

### 6. Supersede / amend an old ADR

When the new decision replaces ADR N:

1. In the new ADR's Status section: `Accepted`, blank line,
   `Supersedes [N. Old title](NNNN-old-slug.md)` (one such line per superseded ADR).
2. In each old ADR: append `Superseded by [M. New title](MMMM-new-slug.md)` as the last
   line of its Status section, then delete its standalone status word (`Accepted` or
   `Proposed`) and the doubled blank line that deletion leaves. Touch nothing else —
   verify with a diff that only the Status section changed.

For Amends/Clarifies, do step 1–2 with the right verb pair but keep both status words.

In a non-English log, the verb pairs are written in the log's language — pick a
translation once and reuse it verbatim across the log. The mechanism is identical:
links at the end of the Status section, status word removed only on supersession.

### 7. Self-review

Before declaring done, check the new file and every edited file:

- Four sections in order, one-blank-line discipline, and the whole file — date label,
  headings, status, link verbs, body — in the log's language.
- H1 number (un-padded) matches the filename number (padded); slug derived correctly.
- `Date:` is today's real date, ISO 8601.
- Context is neutral; Decision says "We will …"; Consequences include at least one
  negative or trade-off.
- Nothing in the file that the user or the repository didn't establish.
- Link text matches the target's H1 exactly; href is a bare basename.
- Superseded/amended files: diff shows changes in the Status section only.

### 8. Hand off

Report every file created or edited, by path. The files are plain adr-tools format, so
the user's existing tooling works on them unchanged: `adr list`, `adr generate toc`,
`adr generate graph`, and Structurizr's `!adrs doc/adr`. One caveat for non-English
logs: `adr list` and the numbering conventions are language-neutral, but `adr generate
toc` / `graph` and Structurizr's importer parse the English status words and link
verbs, so they may not follow translated links — mention this only if the user brings
up those tools. Don't suggest installing anything.

## Reference files

| File | Read it when |
|---|---|
| `references/examples.md` | Before writing your first ADR of the session — the canonical seed ADR (verbatim), a model well-written ADR, and a complete before/after supersede pair showing the exact Status sections. |

## Attribution

The format and writing guidance are condensed from Michael Nygard's article
"Documenting Architecture Decisions" (2011) and the conventions of Nat Pryce's
[adr-tools](https://github.com/npryce/adr-tools), whose project-content template is
licensed CC BY 4.0. See `NOTICE.md`.
