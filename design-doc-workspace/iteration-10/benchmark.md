# iteration-10 — full eval set against 1.3.0, MCP connected

**Question.** 1.3.0 moved the diagram convention out of `SKILL.md` into
`references/diagrams.md`, and eval 6 (no renderer available) had never been run. Does the
full set still hold with both MCP servers connected — and does the no-renderer path keep
the placeholder without sliding into a validation disclaimer?

**Method.** All six evals, one `with_skill` run each, against the working-tree skill (not
the installed plugin). Structurizr and Mermaid MCP servers live. Eval 6 is a
degraded-environment case, so its run was told to treat the host as having no MCP, no
Docker, no Structurizr CLI and no `mmdc`, and forbidden to install anything. No baseline —
iteration-9 already gated 1.3.0 against the previous version.

Grading was done by an independent agent, which ran the disclaimer greps itself and
checked the diagram files on disk.

## Result — 41/42 (98%)

| Eval | Passed | Tokens | Wall clock |
|---|---|---|---|
| 1 rich-write-new-doc | 9/9 | 85,805 | 1224s |
| 2 vague-write-asks-questions | **3/4** | 32,802 | 142s |
| 3 review-flawed-doc | 10/10 | 63,158 | 1352s |
| 4 house-template-repo | 7/7 | 48,400 | 328s |
| 5 template-gaps-asks-to-fill | 5/5 | 36,121 | 259s |
| 6 no-renderer-keeps-placeholder-no-disclaimer | 7/7 | 68,051 | 321s |

Wall clock is not comparable across iterations: all 17 runs of this session (three skills)
ran concurrently, so the numbers carry queueing delay. Tokens: 334,337 total, 55,723 mean
— the most expensive of the three skills, which follows from it delegating to both
`structurizr` and `mermaid-sequence` and rendering real images.

## The one failure — the interview skipped trade-offs

**Eval 2, assertion 1.** The interview covers four of its five required grounds: current
pain and why now, measurable goal plus out-of-scope, alternatives (including do-nothing and
a modular monolith), and blast radius with suggested reviewers. Nothing asks what costs the
team is willing to accept for the chosen approach — trade-offs appear only as an assertion
in the preamble, never as a question.

This matters more than a single point suggests: trade-offs are the skill's own headline
contract (zero cons is a red flag), and the vague-prompt path is exactly where the
questions *are* the deliverable. The discovery question list is worth checking for an
explicit accepted-cost question.

## What the runs confirmed

- **Eval 6 (no renderer) held on every count.** The grep for `não validad` /
  `not machine-validated` / `ilustração do texto` over the document returned no matches;
  the image reference is a placeholder with a one-line HTML comment deferring the render to
  the manual pass, and the DSL is folded in a `<details>` block. The "not validated" caveat
  lives only in the hand-off to the user, correctly outside the document. Nothing was
  installed and no MCP tool was called.
- **The full diagram pipeline works when the tooling is there.** Evals 1 and 3 authored the
  C4 as Structurizr DSL, validated it through the MCP, exported PlantUML and rendered real
  SVGs — verified on disk at 35 KB and 67 KB — then embedded image plus folded source.
- **Template governance held both ways.** Eval 4 derived the house template from the single
  sibling doc and continued the ID sequence; the two sections it added beyond that shape
  carry user-supplied substance and the deviation is flagged in the reply. Eval 5 refused to
  fill four governed sections with filler and asked instead.
- **Eval 3's review** replaced the flowchart with a validated C4 diagram, split the
  overloaded overview, cut the sales-pitch sentence, and left the ten judgment calls — led
  by the doc's missing trade-offs — as questions for the author.
