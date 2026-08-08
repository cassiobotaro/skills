---
name: adr
description: >
  Write and maintain a project's Architecture Decision Record log — the files, not just the
  prose. Every change to the log carries invariants a hand edit breaks silently: the next
  number must be monotonic, the filename must be NNNN-slug.md derived from the title, a
  supersede touches two files and rewrites the old one's Status section only (never its body),
  and adr-tools plus Structurizr's !adrs importer parse the exact English literals (Date:,
  ## Status / ## Context / ## Decision / ## Consequences, the status words) even when the prose
  is in another language. Michael Nygard format, file-compatible with Nat Pryce's adr-tools,
  .adr-dir discovery. Use this skill for any work on a decision log — including the
  operations that look like a one-line edit: "write an ADR", "document this decision", "we
  decided to use X over Y", "ADR 7 is out of date, mark it superseded and write the
  replacement", "amend the existing record", "we changed our minds about Z", "start a decision
  log" — even if the user never says "ADR".
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

2. **Prose follows the log's language; the adr-tools scaffolding stays canonical English.**
   Write the *human prose* in the language of the conversation — the H1 title text and the
   Context / Decision / Consequences bodies. But the *scaffolding* stays exactly as adr-tools
   emits it, in English: the `Date:` label, the four `## Status` / `## Context` / `## Decision`
   / `## Consequences` headings, the status word (`Accepted`, `Proposed`, …), and the
   supersede/amend/clarify verbs. adr-tools has no localization — its template is English — and
   Structurizr's `!adrs` importer and `adr generate` parse those exact English literals: a
   translated `Data:` makes the date silently default to today, and a translated `## Status`
   makes the status silently default to `Proposed` and drops every supersede/amend link. One
   thing still outranks the conversation language for the prose: consistency — match an existing
   log's title/prose language (a log in two languages is worse than either). If an existing log
   translated its scaffolding too, keep new ADRs' scaffolding English anyway so the log stays
   importable, and tell the user.

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
- In a non-English log, only the **prose** is translated (rule 2) — the H1 title text and the
  section bodies. The date *value* stays ISO 8601 and the structure stays exactly as above.
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
  The bracketed text copies the target's H1 exactly, number included (so its title text is in
  the log's language); the verb stays English (rule 2). Keep these links inside the Status
  section — the importer scans only the lines between `## Status` and `## Context` to build
  decision relationships.
- Supersede pair: the new ADR keeps `Accepted` and gains `Supersedes […]`; the old ADR's
  status word is *removed* and replaced by `Superseded by […]` (the link line becomes
  its status).
- `Amends` / `Amended by` and `Clarifies` / `Clarified by` use the same mechanism, but
  both files keep their status word — only supersession removes it. Use Amends when the
  new decision adjusts part of an old one that otherwise stands; Supersedes when it
  replaces it.
- Write the modern spelling `Superseded by` / `Supersedes`; on read, treat the legacy
  adr-tools spelling `Superceded` as the same relation, and leave it alone in files you
  aren't otherwise required to edit.

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

Peek at one existing ADR before writing. If the log visibly follows a different
template (e.g. MADR with YAML frontmatter) or a different language than the
conversation, match the log's own format and language and tell the user.

### 2. Read the neighbors

Read the most recent two or three ADRs and any ADR the new one will supersede or amend.
This gives you the next number, the exact H1 titles you'll need for link text, and the
house tone to match.

### 3. Get the substance — or ask

An honest ADR needs three ingredients: **the decision** (what we will do, concretely),
**the forces** (why now — the technical, political, social, or project pressures in
tension, and what's wrong with the status quo), and **the trade-offs** (what becomes
harder, riskier, or more expensive).

If the user already gave all three, do not interrogate them — write. If any are
missing, ask 2–4 targeted questions in the conversation language before writing: what
is replacing the current choice, and why now? what alternatives were on the table?
what downside did the team accept? who hasn't agreed yet (Accepted vs Proposed)?

Don't ask what the repository already answers (numbering, directory, existing titles).
And treat a decision with zero downsides as a red flag: ask for the accepted trade-off
rather than writing a sales pitch — Consequences must list *all* of them, not just the
positive ones.

### 4. Write the ADR

Write as if in conversation with a future developer — full sentences organized into
paragraphs, good prose. Beyond what the template already embeds:

- **Title**: a short noun phrase ("Use ISO 8601 format for dates"), not a sentence.
- **Context**: don't advocate or foreshadow the answer; posing the motivating question
  is fine ("How can a user find out about available commands?").
- **Decision**: active voice, concrete and specific — name the technology, format, or
  mechanism.
- **Consequences**: every one — positive, negative, neutral — as a short standalone
  paragraph or sentence; bullets are visual style for full sentences, never an excuse
  for fragments.
- **Length**: the canonical ADRs run 15–40 lines; one or two pages is the absolute
  ceiling. Shorter records get read and kept up to date.

### 5. Initialize a fresh log

When no ADR log exists anywhere, mirror `adr init`: create `doc/adr/`, seed it with the
canonical "record architecture decisions" ADR (content in `references/examples.md`),
and the user's decision becomes `0002`. In an English conversation, use the seed
verbatim as `0001-record-architecture-decisions.md` — only the date changes. In any
other language, translate the seed's **title and body** but not its scaffolding (rule 2), so
the log reads in the language it will be kept in, and derive the filename slug from the
translated title. Tell the user
about the seed file. If the user asked for a non-default directory, also write a
`.adr-dir` file at the repo root containing that path so adr-tools and future
invocations find it.

### 6. Supersede / amend an old ADR

When the new decision replaces ADR N:

1. In the new ADR's Status section: `Accepted`, blank line,
   `Supersedes [N. Old title](NNNN-old-slug.md)` (one such line per superseded ADR).
2. In each old ADR: append `Superseded by [M. New title](MMMM-new-slug.md)` as the last
   line of its Status section, then delete its standalone status word (`Accepted` or
   `Proposed`) and the doubled blank line that deletion leaves. Touch nothing else —
   verify with a diff that only the Status section changed.

For Amends/Clarifies, do step 1–2 with the right verb pair (`Amends` / `Amended by`,
`Clarifies` / `Clarified by`) but keep both status words.

### 7. Self-review

Before declaring done, check the new file and every edited file:

- Four sections in order, one-blank-line discipline; the title text and section bodies in the
  log's language, and every piece of scaffolding in canonical English — the `Date:` label, the
  four headings, the status word, the link verbs (rule 2).
- H1 number (un-padded) matches the filename number (padded); slug derived correctly.
- The `Date:` value is today's real date, ISO 8601.
- Context is neutral; Decision says "We will …"; Consequences include at least one
  negative or trade-off.
- Nothing in the file that the user or the repository didn't establish.
- Link text matches the target's H1 exactly; href is a bare basename.
- Superseded/amended files: diff shows changes in the Status section only.

### 8. Hand off

Report every file created or edited, by path. The files are plain adr-tools format, so
`adr list`, `adr generate toc` / `graph`, and Structurizr's `!adrs doc/adr`
(https://docs.structurizr.com/server/decisions) import them unchanged. Mention this only if
the user brings those tools up. Don't suggest installing anything.

## Reference files

| File | Read it when |
|---|---|
| `references/examples.md` | Before writing your first ADR of the session — the canonical seed ADR (verbatim), a model well-written ADR, and a complete before/after supersede pair showing the exact Status sections. |

## Attribution

The format and writing guidance are condensed from Michael Nygard's article
"Documenting Architecture Decisions" (2011) and the conventions of Nat Pryce's
[adr-tools](https://github.com/npryce/adr-tools), whose project-content template is
licensed CC BY 4.0. See `NOTICE.md`.
