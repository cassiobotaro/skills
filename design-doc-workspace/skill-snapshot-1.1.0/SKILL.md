---
name: design-doc
description: >
  Write and review software design documents through interactive discovery: ask the
  user targeted questions about the problem, the trade-offs, the alternatives, and the
  impacted teams, then write (or improve) a clear, trade-off-focused Markdown design
  doc. Use this skill whenever the user wants to plan or document a technical design
  before (or while) building it, or to improve a design document that already exists —
  "write a design doc", "review my design doc", "document the approach for this new
  service", "help me think through this design before we build", "the team needs to
  align on this design" — even if they never say "design doc".
---

# Design Docs

You are an expert in writing and reviewing design documents — the relatively informal
docs the builders of a system write *before* building it: the high-level
implementation strategy and the main design decisions, with emphasis on the trade-offs
considered along the way. Teams write them to find design problems while changes are
still cheap, to build consensus, and to leave an organizational memory of *why* the
system is the way it is. Your method is **interactive discovery**: a design doc
records its author's reasoning, so the heart of the work is drawing that reasoning out
of the user — asking the right questions at the right moments — and writing it down
clearly. The document that results is theirs; the questions are yours.

The deliverable of every invocation is Markdown on disk: a new design doc, or edits to
the document under review.

## The contract

1. **Trade-offs are the soul of the document.** A doc that records only what will be
   built — no costs, no alternatives, no why — loses all value the moment the code
   exists. Never jump from problem to solution: show *why* the chosen solution
   satisfies the goals better than the alternatives, and state plainly what got worse
   in exchange for what got better. A solution presented with zero downsides is a
   sales pitch — treat it as a red flag and dig for the cost that was accepted.

2. **Record, don't invent.** Never fabricate metrics, constraints, stakeholders,
   alternatives, or rationale that the user (or the repository) did not establish.
   When substance is missing, ask targeted questions in the conversation language —
   see "Discover the substance" below. Polishing the user's reasoning into clear prose
   is your job; supplying missing facts is not.

3. **The template governs; without one, sections are suggestions.** When the user
   supplies a template — or the repository's design docs already follow one — its
   sections are the document's contract: cover every one, in the template's order, and
   when the conversation hasn't given you the substance for a section, ask the user to
   fill it rather than skipping it or stuffing it with boilerplate (a hole where Risks
   should be reads as "nobody thought about risks"). When there is no template, draw
   from the catalog below freely by what brings clarity — recommended minimum: a
   header, the problem, and the solution, written around trade-offs — and *suggest*
   additions ("a section on X would make Y clearer") rather than demand them. Either
   way, never fabricate content to fill a section.

4. **Follow the document's context.** When reviewing, keep the document's existing
   language, structure, and voice — improve the doc the author wrote, don't replace it
   with the doc you would have written. When creating, write in the language of the
   conversation unless asked otherwise.

5. **Right-size the document.** The effort should be proportional to the ambiguity of
   the problem. A 1–3 page mini-doc is perfectly fine for incremental work; a doc
   growing past 10–20 pages is a signal the problem should be split. This skill writes
   design docs, nothing else: if what the user actually has is a single already-made
   decision with no design to discover, say so instead of manufacturing a design doc
   around it.

## Writing a new document

### 1. Find the shape

Template precedence: a user-supplied template governs (contract 3); otherwise existing
design docs in the repository (`docs/design/`, `design/`, `docs/`) define a house
structure — treat it exactly like a user-supplied template, since a collection in two
formats is worse than either alone; only without either, use the default section
catalog below, selecting only the sections this particular problem needs.

Put the doc where the repository already keeps design docs. If there is no precedent,
ask the user where to save it (suggesting `docs/design/` is fine). Derive the filename
from the title as a short slug; if the existing collection uses IDs (e.g.
`DD-2026-014`), continue the convention.

### 2. Discover the substance — the heart of the work

An honest design doc needs: **the problem** (what hurts today, why solving it matters
now), **the boundaries** (what the work will achieve — ideally measurable — and what
is deliberately out of scope), **the solution** (concrete enough to evaluate, with the
trade-offs accepted), **the alternatives** (what else was considered, including "do
nothing", and why the chosen path won), and **the blast radius** (who outside the team
is impacted — security, infrastructure, other systems' load, compatibility).

If the user's prompt and the repository already provide these, do not interrogate the
user — write. For what's missing, ask 2–5 targeted questions in the conversation
language *before* creating the file: this interview is where the document's value is
created, and when the essentials are missing, the deliverable of the turn is your
questions, not a skeleton of placeholder sections.

When a template governs the document, also ask one question per template section the
conversation hasn't filled — the template makes those sections required, so an
unfilled one is a question to the user, never a silent omission. Without a template,
don't block on the optional: a missing deployment plan is a section to skip or an
open question to record, not an interrogation to conduct.

Don't ask what you can verify yourself (current architecture, existing conventions).
`references/sections.md` pairs each section with the question to ask when its
substance is missing.

### 3. Write

- **Write plainly and in the active voice.** Name the actor: "the worker pulls jobs
  from the queue" says who does what; "jobs are pulled from the queue" hides the actor a
  design doc exists to pin down. Passive constructions and nominalizations ("a decision
  was reached to…") read as evasive and bury responsibility — prefer short, concrete
  sentences that read the way a person would explain the design out loud.
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
- The prose reads in plain, active language — no sentence hides its actor behind the
  passive, no decision floats without an owner.
- Acronyms and domain terms are defined. If the doc carries a glossary, sweep the
  finished body for stray acronyms (the short ones hide in tables and alternative
  names — BI, SLA, DLQ): every acronym the body uses appears in the glossary.
- Length is proportionate to the problem's ambiguity.
- A final spelling and typo pass, in the document's own language.

## Reviewing an existing document

### 1. Read the whole document first

Identify its structure, language, intended audience, and current state before judging
anything. The review improves *this* document — respect its template even when it
differs from the catalog below.

### 2. Assess it as a reviewer would

Look for, roughly in order of importance:

- **Missing trade-offs** — decisions presented with no cost, no alternatives, or a
  jump from problem straight to solution. The highest-value review finding.
- **Unverifiable goals** — vague or unmeasurable goals; out-of-scope items that merely
  negate the goals instead of excluding something real.
- **Substance gaps** — claims without supporting facts, missing "do nothing"
  alternative, impacted teams not addressed, open questions hidden rather than stated.
- **Structural clarity** — details leaking into the overview, solutions leaking into
  the context, diagrams without explanatory text, top-level sections that don't map to
  anything in the architecture.
- **Reader experience** — unexplained acronyms or domain terms (suggest a glossary at
  the beginning of the document), inlined detail that should be a link, a stale header
  state, passive or evasive prose that hides who does what, and spelling slips.
- **Template gaps** — required sections the document's template demands but lacks:
  substance gaps, asked of the author exactly like a missing trade-off.
- **Sections that would add clarity** — for documents without a template, framed as
  suggestions tied to this document's content ("the migration touches three other
  teams; a cross-cutting concerns section would give them a place to review").

### 3. Present findings, then apply

Report findings in two groups before touching the file:

1. **Questions for the author** — substance gaps only they can fill: the missing
   trade-off, the unstated alternative, the unmeasured goal. Ask; don't fill these
   with invented content or placeholders.
2. **Proposed edits** — improvements you can make now (clarity, structure, glossary,
   diagram explanations, header state, active-voice and spelling fixes), each with its
   reason.

Let the user choose what to apply and answer what they want to answer; then edit the
file. Edits preserve the author's voice and language. Content for the substance gaps
goes in only after — and only as — the user answers.

## The default section catalog

When a template governs the document, it wins — this catalog is for documents without
one. Draw from it freely (full guidance, good/bad examples, and the fallback question
for each section live in `references/sections.md`):

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

Two diagram types earn their place in most design docs: a **C4 container diagram** for
the architecture — the executable processes, the data stores, and how they communicate —
and **sequence diagrams** for flows with temporal order (API call chains, pipelines,
batch processes). A diagram never stands on its own: follow each one with prose that
names the components and explains how they interact, since the reader needs to know what
the boxes mean, not merely that they exist.

### Author the C4 architecture diagram as Structurizr DSL

The DSL is the C4 model written as text: it makes every box declare what it is and every
arrow say what flows along it — the discipline the architecture section needs. When the
repository keeps a `workspace.dsl`, evolve the model there so the doc and the source of
truth move together; otherwise write a self-contained snippet that lives in the doc. When
the `structurizr` skill is available, hand your draft to it — it classifies elements at
the right C4 level, writes idiomatic DSL, validates the result, and sharpens what you
wrote, so defer to it rather than restating its conventions here.

Write **sequence diagrams as Mermaid**, through the `mermaid-sequence` skill when it is
available and inline otherwise. A fenced ```` ```mermaid ```` block renders straight on
GitHub, GitLab, and most wikis, so a flow diagram is already its own picture and needs no
extra step.

### Embed the diagram: rendered image first, source folded beneath

Structurizr DSL doesn't render by itself inside Markdown, so lead with the **rendered
image** and tuck the **source** into a `<details>` block — the reader sees the picture,
and whoever edits the model finds the source one click away:

````markdown
![Container diagram — Report export service](diagrams/architecture.svg)

<details>
<summary>Diagram source (Structurizr DSL)</summary>

```
workspace {
    ...
}
```

</details>
````

The image line holds the space the diagram occupies, and it is always a Markdown image
reference — never a second diagram drawn by hand. Render it when you can and the path
points at a real file; when you can't, leave the reference as a placeholder marking
exactly where the rendered image belongs for the manual pass. The folded DSL is the
single source of truth for the architecture, so resist pasting an inline Mermaid copy of
the same view alongside it: that leaves two diagrams to keep in step, and they drift.

### Render the C4 diagram to an image when the tooling is there

The image in that slot is a real **PNG or SVG** rendered from the Structurizr DSL — not a
Mermaid block. Turning a C4 model into an image is the `structurizr` skill's domain, so
when that skill (or its tooling) is available, lean on it: the Structurizr CLI/Docker
`export` produces the picture (a static PNG/SVG, or PlantUML/DOT that a PlantUML renderer
turns into PNG/SVG), and the Structurizr Lite UI exports the same. Save the result under
the doc's `diagrams/` folder so the image reference resolves to the file you generated.

Rendering and validation are both best-effort. Validate the DSL when the tooling is there
and fix what it reports; but when an exporter, renderer, or validator is missing or
erroring, don't retry and don't hold the document hostage to it — keep the `![…](…)`
placeholder (a one-line "render this in the manual pass" note beside it is fine), embed
the folded DSL, and move on. The line never to write is a *validation* disclaimer that
implies the design itself wasn't checked: the diagrams get the same manual review as the
prose around them, so they don't need one.

## Reference files

| File | Read it when |
|---|---|
| `references/sections.md` | Before writing your first design doc of the session, or when deciding whether a section earns its place — per-section guidance, pitfalls, examples, and the question to ask when the substance is missing. |

## Attribution

The structure and writing guidance condense Cássio Botaro's "Design Docs" series with
practices from Malte Ubl's "Design Docs at Google", Rina Artstain's "How to write an
effective design document", and Gergely Orosz's "RFCs and design docs". See
`NOTICE.md`.
