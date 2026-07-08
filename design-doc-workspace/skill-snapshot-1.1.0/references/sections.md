# The default section catalog

This catalog applies when no template governs the document. A user-supplied template —
or the structure the repository's design docs already follow — takes precedence: its
sections are required content, filled by asking the user for what's missing, never
swapped for the catalog below. (The per-section questions here still help: reuse them
for whichever template sections they match.)

Within the catalog, the order below is a sensible default order for the document
itself. None of these sections is mandatory — each entry explains what the section
buys the reader, how to write it well, and what to ask the user when its substance is
missing. Skip any section whose entry doesn't apply; a skipped section needs no
apology and no placeholder.

## Header

A small key–value table identifying the document and its lifecycle.

| | |
|---|---|
| **Document** | DESIGN-DOC · DD-2026-014 |
| **State** | Draft |
| **Title** | Stock replenishment recommender |
| **Authors** | Ana Souza |
| **Reviewers** | Bruno Lima (Security), Carla Reis (Platform) |
| **Created** | 2026-06-07 |
| **Last updated** | 2026-06-07 |
| **Tags** | forecasting, pipeline |

- Typical states: **draft → in review → proposed → approved / rejected**. Some teams
  add *implemented* or *cancelled*. Whatever the vocabulary, keep the state current —
  a doc "in review" for four months confuses everyone who arrives later.
- Reviewers are named *with their area* (Security, Platform, Infrastructure…).
  Suggest reviewers from the areas the design touches and from the impacted teams —
  they see problems the authoring team cannot.
- The document ID is optional; if the collection uses one (`DD-<year>-<seq>`),
  continue the sequence.
- Tags pay off later, when someone searches for "how did we decide X".
- Dates are real dates (`date +%Y-%m-%d`), never guessed.

**If missing, ask:** who are the authors, and which areas or teams should review this?

## Glossary

Definitions for the acronyms and domain-specific terms the document relies on.

- Place it **at the beginning of the document**, right after the header, so readers
  meet the terms before the terms meet them — a glossary the reader finds only at the
  end has already failed its purpose.
- Include it when the document leans on acronyms (SLA, CDC, P99) or domain vocabulary
  (stockout, replenishment lead time) that a newcomer or a reviewer from another team
  would stumble on. A doc that needs no glossary shouldn't carry one.
- Keep entries to one line each. If a term needs a paragraph, it probably deserves a
  link to a fuller source instead.
- Once the document carries a glossary, cover *every* acronym and domain term the body
  actually uses — readers who needed the glossary stumble precisely on the entry that
  was skipped, and an undefined acronym sitting next to a glossary reads as an
  oversight. Sweep the finished document for acronyms before closing the list.
- When writing or reviewing: if undefined acronyms or domain terms accumulate,
  *suggest* adding a glossary — point at the specific terms that triggered the
  suggestion.

**If missing, ask:** nothing — derive the term list from the document itself, and ask
the user only for definitions you cannot establish from the repository or the
conversation.

## Overview

One paragraph — two at most — telling any reader what the document is about and what
to expect from reading it.

- No details: details belong to the sections that follow. The test: a person with no
  context should still understand the subject.
- Don't waste the reader's first paragraphs on technicalities; say what problem is
  being solved and what kind of solution is proposed, in plain language.

**If missing, ask:** in one or two sentences, what is this work about, and what does
it deliver?

## Scope and context

The scenario the system lives in: the motivators for writing the document, the
current technology, the relevant technical debt — objective background facts that
bring the reader up to speed.

- Be succinct: the *minimum* context needed to understand the problem.
- No goals and no proposed solutions here — this section situates, it doesn't decide.
  Background written to foreshadow the answer reads as advocacy, and reviewers notice.
- Assume some prior knowledge, and link to detailed information rather than copying
  it in.

**If missing, ask:** what exists today, and what is motivating this work now?

## Goals and out of scope

Two lists: what the work will achieve, and what it deliberately will not.

- Prefer **measurable goals** — numbers make success verifiable. "Reduce stockouts of
  high-turnover items by 30%" can be checked; "improve availability" cannot.
- Name the **mechanism**, not just the outcome: "reduce stockouts *by prioritizing
  replenishment of the highest-turnover items*" tells the reader what the design must
  actually do.
- Out-of-scope items are things someone could reasonably expect this work to cover,
  explicitly excluded — "real-time recommendations are out; the pipeline runs daily".
  Merely negating the goals ("the system shouldn't be slow") excludes nothing and
  helps no one.

**If missing, ask:** how will you know this worked — is there a number? And what
related problem are you explicitly *not* solving this time?

## The design (a series of sections)

The core of the document — not one section but a *set* of sections, each with its own
heading. What unites them: given the context and the goals, they show **why this
solution best meets the requirements**.

Start with a **solution overview**: the main components, how they relate, and the
first statement of the key trade-off. Then go into details, choosing among:

- **Architecture** — typically a C4 container diagram: the executable processes, the
  data stores, and how they communicate. High-level; no implementation detail.
- **Flows** — sequence diagrams for interactions with temporal order: API call
  chains, daily pipelines, batch processes.
- **APIs and payloads** — only the fragments relevant to the decision. A full
  copy-pasted schema is verbose, buries the point, and goes stale; link to the source
  of truth and show the two fields the design actually hinges on.
- **Data and its sensitivity** — what is stored, in what rough form, and whether any
  of it is sensitive (PII, financial), since that constrains the design.
- **Pseudocode** — rarely. Only when a novel algorithm is itself the design.

Two tests for whether a detail belongs:

- *Longevity*: if the team changed frameworks, would this still apply? If yes, it's a
  design decision — include it. If no, it's implementation — leave it to the code.
- *Freedom*: could someone implement it differently and still meet the requirement?
  If yes, state the requirement, not the implementation.

**If missing, ask:** what are the main components of the solution, and which decision
in it are you least sure about?

## Trade-offs of the chosen solution

The pros and the cons of the chosen solution, stated explicitly — the section that
gives the document long-term value.

- A convenient convention: `✓` for what the solution buys, `✗` for what it costs.
- Every design involves trade-offs. If the list of cons is empty, the section isn't
  done — dig until the accepted cost is on the page. "Simpler operations in exchange
  for a 24h recommendation delay" is a trade-off; "scalable and maintainable" is a
  sales pitch.
- Support claims with facts and data the team actually has (a benchmark, a load
  number, a prototype result). "I tried it and it handled 2× peak load" beats
  adjectives.

**If missing, ask:** what got worse, riskier, or more expensive in exchange for the
benefits — what cost did the team accept?

## Alternatives considered

The other solutions that could reasonably have achieved similar outcomes, each with
its trade-offs and the reason it lost.

- Focus on the **trade-offs of each option and how they led to the final choice** —
  that's what makes the decision auditable later.
- Always include **"do nothing"** as an alternative and say why it was discarded. If
  doing nothing isn't even worth refuting, the problem statement is probably too
  weak.
- Be succinct: a focused paragraph or two per alternative. A comparison table works
  well when there are several options and shared criteria — use textual markers
  (✓ / ✗ / ⚠) rather than color alone, so the table survives printing and colorblind
  readers.
- Mark the chosen option clearly.

**If missing, ask:** what else did the team consider — and why is doing nothing not
acceptable?

## Cross-cutting concerns

What this design touches *beyond the authoring team*: security, infrastructure,
compatibility with existing APIs, load imposed on other teams' systems.

- One short subsection per concern that actually applies (Security, Infrastructure,
  Compatibility…) — a paragraph each is usually enough.
- This section exists for collaboration: it tells impacted teams what to look at.
  Involve them as early as possible — late surprises cause rework — and suggest them
  as reviewers in the header.

**If missing, ask:** who outside your team is impacted — does this add load to a
shared system, expose a new surface, or change an API someone depends on?

## Testability and observability

A short closing section: how the solution will be tested, and how it will be observed
in production.

- Cover what verifies the design *before* shipping (backtesting, integration tests in
  CI) and what watches it *after* (success metrics, alerts).
- Tie the metrics back to the measurable goals when possible — the goal "reduce
  stockouts by 30%" implies the metric that proves it.

**If missing, ask:** how will you verify this works before shipping, and what will
tell you it's working (or broken) in production?

## Deployment plan

A short closing section: the segmentation of deliveries — the steps that put the
design in production incrementally and safely.

- A numbered list of phases with rough timeframes is enough; this is a design doc,
  not a project plan.
- Worth having when delivery is risky or staged (migrations, rollouts behind flags,
  data backfills); skip it for changes that ship in one step.

**If missing, ask:** does this ship all at once, or in stages — and is there a
rollback story if a stage goes wrong?

## Open questions

A short closing section: the points still undefined or unknown.

- Stating unknowns signals honesty and invites collaboration — pretending certainty
  invites being wrong alone. "Awaiting alignment with the Data Engineering team on
  pipeline ownership" is a perfectly good entry.
- When a question is resolved, fold the answer into the body and remove it from the
  list (updating the header's *Last updated*).

**If missing, ask:** what do you still not know — what are you waiting on someone
else to confirm?
