# iteration-4 — gate for the progressive-disclosure cut (1.2.0)

**Question.** The house-conventions skeleton (~85 lines of example DSL plus its rationale)
moved out of `SKILL.md` §4 into `references/dsl-reference.md` §15, leaving a one-paragraph
summary in the body. `dsl-reference.md` is already always-read, so the guidance costs no
new trigger — but does the agent still *apply* it?

**Method.** Eval 2 (`complete-workspace-from-clear-spec`), one foreground run against the
working-tree skill (not the installed plugin). `with_skill/` holds the output.

**Result — pass.** Every convention held:

| Convention | Held? |
|---|---|
| `!identifiers hierarchical` | yes |
| Description on every element, technology on every container | yes |
| Tags + `styles` instead of ad-hoc colors | yes (`Database`, `Cache`, `Queue`, `External`, `Browser`, `Person`) |
| Stable descriptive view keys | yes (`SystemContext`, `Containers`, `Redirecionamento`) |
| `autoLayout` on every view | yes (`autoLayout lr` on the dynamic view) |
| `configuration { scope softwaresystem }` | yes |

The DSL validated clean through the Docker CLI fallback (no MCP connected), exit 0.
Reference files read: `dsl-reference.md`, `diagrams.md`, `modeling-patterns.md` — the
conditional files it skipped (`c4-classification.md`, `deployment-patterns.md`,
`dsl-advanced.md`) are exactly the ones this task didn't need, which is the reading
discipline working as intended.

Modeling was also correct on the traps: nginx as the SPA's *technology* rather than a
container, RabbitMQ as a queue container, Google Workspace as the only external system,
and all dynamic-view steps backed by relationships that exist in the model.

**Body size.** `SKILL.md` 305 → 234 lines (−71, −23%).
