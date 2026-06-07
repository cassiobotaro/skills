# Notices and attribution

This skill condenses and adapts guidance from the sources below. Changes were made in
all cases (condensation, reorganization, translation from Portuguese, added guidance).

## Design Docs series — Cássio Botaro

The default section catalog and its order (header fields and document states,
overview, scope and context, goals and out of scope, the design as a *series* of
sections, C4 container and sequence diagrams, trade-offs of the chosen solution,
alternatives considered including "do nothing", cross-cutting concerns, and the
closing trio of testability/observability, deployment plan, and open questions), the
"sections are examples, not a mold" stance, and the ✓/✗ convention are drawn from the
**Design Docs** series (in Portuguese):

- <https://cassiobotaro.dev/posts/design-docs-parte-1/>
- <https://cassiobotaro.dev/posts/design-docs-parte-2/>
- <https://cassiobotaro.dev/posts/design-docs-parte-3/>

## Design Docs at Google — Malte Ubl

The trade-off-first framing, the warning against jumping from problem to solution,
non-goals as deliberately rejected goals, "overview then details", showing only
relevant API/schema fragments, pseudocode only for novel algorithms, the length
guidance (1–3 page mini-docs; split past 10–20 pages), and the "when (not) to write
one" ambiguity test are condensed from **Malte Ubl**'s *Design Docs at Google*:
<https://www.industrialempathy.com/posts/design-docs-at-google/>

## How to write an effective design document — Rina Artstain

The intro written for a distracted reader, the glossary for domain terms, limiting
feedback requests to key decisions, accessible comparison tables (markers, not color
alone), and the reviewer logistics (named approvers with their areas, status
tracking) are condensed from **Rina Artstain**'s *How to write an effective design
document*: <https://rinaarts.com/how-to-write-an-effective-design-document/>

## RFCs and design docs — Gergely Orosz

The proportionate-effort principle (no doc for trivial changes, split tiers for big
ones), the explicit document-state lifecycle, named approvers, open questions as a
first-class section, and the cross-company perspective (Google, Uber, Monzo,
Sourcegraph, Stedi, and others) are condensed from **Gergely Orosz**'s *RFCs and
design docs*: <https://blog.pragmaticengineer.com/rfcs-and-design-docs/> and
<https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs>

## create-technical-design-doc — Tech Leads Club

The "longevity test" heuristics for separating design decisions from implementation
detail ("if we change frameworks, does this still apply?" / "could someone implement
this differently and still meet the requirement?") and the pattern of pairing each
section with a fallback question to ask instead of fabricating content are adapted
from the **Tech Leads Club** skill *create-technical-design-doc*:
<https://github.com/tech-leads-club/agent-skills/blob/main/packages/skills-catalog/skills/(creation)/create-technical-design-doc/SKILL.md>

This skill deliberately departs from that one on a key point: it imposes no mandatory
sections and no minimum-quantity checklists.
