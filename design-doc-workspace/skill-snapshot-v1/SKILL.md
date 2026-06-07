---
name: design-doc
description: >
  Write and review software design documents — design docs, RFCs, technical design
  documents — as trade-off-focused Markdown files. Use this skill whenever the user
  wants to plan or document a non-trivial technical effort before building it, or to
  improve a design document that already exists — "write a design doc", "draft an RFC
  for the migration", "review my design doc", "is this design document clear?",
  "document the approach for this new service", "we need buy-in from other teams on
  this design" — even if they never say "design doc". For recording a single
  already-made decision an ADR fits better; for proposing and explaining how something
  will be built, use this.
---

# Design Docs

A design doc is a relatively informal document written by the people who will build a
system, before they build it: the high-level implementation strategy and the main
design decisions, with emphasis on the trade-offs considered along the way. Teams
write them to find design problems while changes are still cheap, to build consensus
across teams, to make sure cross-cutting concerns are considered, and to leave an
organizational memory of *why* the system is the way it is.

The deliverable of every invocation is Markdown on disk: a new design doc, or edits to
the document under review.

## The contract

1. **Trade-offs are the soul of the document.** A doc that records only what will be
   built — no costs, no alternatives, no why — is an implementation manual that loses
   all value the moment the code exists. What gives a design doc long-term value is the
   record of the trade-offs made along the way. So never jump from problem to solution:
   given the context and the goals, show *why* the chosen solution satisfies them
   better than the alternatives, and state plainly what got worse in exchange for what
   got better. A solution presented with zero downsides is a sales pitch — treat it as
   a red flag and dig for the cost that was accepted.

2. **Record, don't invent.** The document captures the author's real reasoning. Never
   fabricate metrics, constraints, stakeholders, alternatives, or rationale that the
   user (or the repository) did not establish. When substance is missing, ask targeted
   questions in the conversation language — see "Get the substance" below. Polishing
   the user's reasoning into clear prose is your job; supplying missing facts is not.

3. **Sections are suggestions, never requirements.** There is no mandatory template.
   The catalog below is a set of sections that tend to bring clarity — use, adapt, or
   discard them according to the problem's size and shape. The one recommended minimum
   is: a header, the problem, and the solution, written around trade-offs. Beyond
   that, *suggest* sections ("a section on X would make Y clearer"), never demand
   them, and never pad a document with empty or placeholder sections just to match a
   template.

4. **Follow the document's context.** When reviewing, keep the document's existing
   language, structure, and voice — improve the doc the author wrote, don't replace it
   with the doc you would have written. When creating, write in the language of the
   conversation unless asked otherwise, and prefer a template the user supplies or a
   structure the repository's existing design docs already follow over the default
   catalog.

5. **Right-size the document.** The effort should be proportional to the ambiguity of
   the problem. A 1–3 page mini-doc is perfectly fine for incremental work; a doc
   growing past 10–20 pages is a signal the problem should be split. And if the
   solution is genuinely obvious — no real trade-offs, no contention — say so: a short
   doc, or a single ADR (the `adr` skill), may serve the user better than a design doc.

## Writing a new document

### 1. Find the shape

- If the user supplied a template, follow it.
- Otherwise, look for existing design docs in the repository (`docs/design/`,
  `docs/rfcs/`, `design/`, `docs/`); if a house structure exists, match it — a
  collection in two formats is worse than either format alone.
- Otherwise, use the default section catalog below, selecting only the sections this
  particular problem needs.

For the file location: put the doc where the repository already keeps design docs. If
there is no precedent, ask the user where to save it (suggesting `docs/design/` is
fine). Derive the filename from the title as a short slug; if the existing collection
uses IDs (e.g. `DD-2026-014`), continue the convention.

### 2. Get the substance — or ask

An honest design doc needs:

1. **The problem** — what hurts today, and why solving it matters now.
2. **The boundaries** — what the work will achieve (ideally measurable) and what is
   deliberately out of scope.
3. **The solution** — concrete enough to evaluate, with the trade-offs accepted.
4. **The alternatives** — what else was considered, including "do nothing", and why
   the chosen path won.
5. **The blast radius** — who outside the team is impacted (security, infrastructure,
   other systems' load, compatibility).

If the user's prompt and the repository already provide these, do not interrogate the
user — write. For what's missing, ask 2–5 targeted questions in the conversation
language before writing. Ask *before* creating the file: when the essentials above are
missing, the deliverable of the turn is your questions, not a skeleton of placeholder
sections. Don't ask what you can verify yourself (current architecture, existing
conventions), and don't block on the optional: a missing deployment plan is a section
to skip or an open question to record, not an interrogation to conduct.
`references/sections.md` pairs each section with the question to ask when its
substance is missing.

### 3. Write

- Start the design with an **overview, then details**. The design is not one section
  but a *series* of sections, each with its own heading: the solution itself, the
  architecture (typically a C4 container diagram), the flows (sequence diagrams),
  APIs and payloads, data and its sensitivity, pseudocode (rarely — only novel
  algorithms). What unites them is showing why this solution best meets the goals.
- **Diagrams complement text, they never replace it.** Always follow a diagram with
  prose explaining the components and their interactions — see "Diagrams" below.
- Show only the **relevant fragments** of APIs, schemas, and payloads. Copy-pasting a
  full schema buries the decision under detail that goes stale; link to the source of
  truth instead.
- Prefer **measurable goals** (numbers make success verifiable) and goals that name
  the mechanism, not just the outcome. Write out-of-scope items as explicit exclusions
  someone might reasonably have expected, not negated goals.
- When the document leans on acronyms or domain-specific terms, **suggest a glossary
  at the beginning of the document** — right after the header — so readers meet the
  terms before the terms meet them.
- Support decisions with facts and data the user established; avoid vague
  justifications ("more scalable", "cleaner") that don't survive a reviewer's "why?".

### 4. Self-review

Before declaring done, check:

- Nothing in the document that the user or the repository didn't establish.
- The header's state reflects reality, and dates are real (`date +%Y-%m-%d`).
- The overview is one–two paragraphs with no details; the context section contains
  background only — no goals, no solutions.
- Every significant decision carries its trade-offs; alternatives include "do
  nothing"; at least one accepted cost is stated plainly.
- Every diagram is followed by explanatory text.
- Acronyms and domain terms are defined. If the doc carries a glossary, sweep the
  finished body for stray acronyms (the short ones hide in tables and alternative
  names — BI, SLA, DLQ): every acronym the body uses appears in the glossary.
- Length is proportionate to the problem's ambiguity.

## Reviewing an existing document

### 1. Read the whole document first

Identify its structure, language, intended audience, and current state before judging
anything. The review improves *this* document — respect its template even when it
differs from the catalog below.

### 2. Assess it as a reviewer would

Look for, roughly in order of importance:

- **Missing trade-offs** — decisions presented with no cost, no alternatives, or a
  jump from problem straight to solution. This is the highest-value review finding.
- **Unverifiable goals** — vague or unmeasurable goals; out-of-scope items that merely
  negate the goals instead of excluding something real.
- **Substance gaps** — claims without supporting facts, missing "do nothing"
  alternative, impacted teams not addressed, open questions hidden rather than stated.
- **Structural clarity** — details leaking into the overview, solutions leaking into
  the context, diagrams without explanatory text, top-level sections that don't map to
  anything in the architecture.
- **Reader experience** — unexplained acronyms or domain terms (suggest a glossary at
  the beginning of the document), inlined detail that should be a link, a stale header
  state ("in review" for four months confuses newcomers).
- **Sections that would add clarity** — framed as suggestions tied to this document's
  content ("the migration touches three other teams; a cross-cutting concerns section
  would give them a place to review"), never as missing mandatory items.

### 3. Present findings, then apply

Report findings in two groups before touching the file:

1. **Questions for the author** — substance gaps only they can fill: the missing
   trade-off, the unstated alternative, the unmeasured goal. Ask; don't fill these
   with invented content or placeholders.
2. **Proposed edits** — improvements you can make now (clarity, structure, glossary,
   diagram explanations, header state), each with its reason.

Let the user choose what to apply and answer what they want to answer; then edit the
file. Edits preserve the author's voice and language. Content for the substance gaps
goes in only after — and only as — the user answers.

## The default section catalog

When no template is given, draw from this catalog (full guidance, good/bad examples,
and the fallback question for each section live in `references/sections.md`):

| Section | What it gives the reader | Worth having when |
|---|---|---|
| Header | Authors, reviewers (with their areas), state, dates, tags | Recommended minimum |
| Glossary | Acronyms and domain terms, defined before first use | The doc leans on acronyms or domain vocabulary |
| Overview | One–two paragraphs: what this doc is about, no details | Recommended minimum |
| Scope and context | Background facts that situate the reader — no goals, no solutions | The reader needs situating (current tech, debt, motivators) |
| Goals and out of scope | Measurable goals; explicit exclusions | The boundaries aren't obvious |
| The design (a series of sections) | Solution overview → details: architecture (C4 container), flows (sequence), APIs/payloads, data sensitivity, pseudocode (rarely) | Recommended minimum — the core |
| Trade-offs of the chosen solution | The pros *and* the cons, explicitly | Whenever there was a real decision — the doc's long-term value |
| Alternatives considered | Each alternative's trade-offs, including "do nothing", and why the winner won | Real alternatives existed (they almost always did) |
| Cross-cutting concerns | Security, infrastructure, compatibility, load imposed on other teams | Anyone outside the team is impacted |
| Testability and observability | How success will be verified and observed in production | Closing section, when relevant |
| Deployment plan | Incremental, safe delivery steps | Closing section, when relevant |
| Open questions | What is still unknown — honesty that invites collaboration | Closing section, when anything is unresolved |

## Diagrams

Two diagram types earn their place in most design docs: a **C4 container diagram**
for the architecture (the executable processes, data stores, and how they
communicate) and **sequence diagrams** for flows with temporal order (API call
chains, pipelines, batch processes).

- In a Markdown doc, prefer fenced ```` ```mermaid ```` blocks — they render directly
  on GitHub, GitLab, and most wikis.
- When the `mermaid-sequence` skill is available, use it for sequence diagrams. When
  the `structurizr` skill is available and the project keeps a `workspace.dsl`, evolve
  the model there and embed an exported view. Without them, write the Mermaid inline.
- Validation tooling is best-effort. If a validation server or CLI is unavailable or
  erroring, don't retry and don't block the document on it: write the diagram inline,
  mention once that it wasn't machine-validated, and move on. The diagram is an
  illustration inside a prose document, not the deliverable.
- A diagram is never self-explanatory, even when it feels clear: always follow it
  with text describing the components and their interactions.

## Reference files

| File | Read it when |
|---|---|
| `references/sections.md` | Before writing your first design doc of the session, or when deciding whether a section earns its place — per-section guidance, pitfalls, examples, and the question to ask when the substance is missing. |

## Attribution

The structure and writing guidance condense Cássio Botaro's "Design Docs" series with
practices from Malte Ubl's "Design Docs at Google", Rina Artstain's "How to write an
effective design document", and Gergely Orosz's "RFCs and design docs". See
`NOTICE.md`.
