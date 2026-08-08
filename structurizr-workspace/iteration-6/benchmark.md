# iteration-6 — evals 2 and 3 against 1.2.1, gating the `dsl-reference.md` index

**Question.** 1.2.1 inserted a 16-entry section index at the top of
`references/dsl-reference.md` (359 lines), which `SKILL.md` requires reading before writing any
DSL. The index tells the model it may jump to the section the task needs instead of reading
straight through — and that is exactly the nudge that could cost it a convention it would
otherwise have absorbed in passing. House conventions (`!identifiers hierarchical`, technology on
every container, directional relationship labels with protocols, tag-plus-style over ad-hoc
colors, `autoLayout`, stable view keys) live scattered across those sections; §15 carries the
skeleton for a workspace built from scratch.

Two evals cover the two ways that could go wrong: **eval 2** writes a workspace from nothing (it
needs §15 and the conventions), **eval 3** evolves an existing one (it needs the deployment and
`!adrs` sections while touching nothing else).

**Method.** One `with_skill` run each against the working-tree skill. No Structurizr MCP was
connected, so both runs took the Docker fallback from the skill's validation chain. No baseline:
iteration-5 scored the full set 28/28 against 1.2.0 with these assertions.

## Result — 12/12, no regression

| Eval | Passed | Tokens |
|---|---|---|
| 2 complete-workspace-from-clear-spec | 6/6 | 47,352 |
| 3 evolve-existing-dsl-deployment-dynamic-adrs | 6/6 | 52,672 |

Total 100,024 tokens, mean 50,012.

## The conventions survived selective reading

This is what the run was for, and it is worth being specific, because "it still passed" would not
distinguish a model that read the index and jumped well from one that ignored the index entirely.

**Eval 2, from scratch.** `!identifiers hierarchical`, `configuration { scope softwaresystem }`,
`autoLayout` on all three views, descriptive view keys (`SystemContext`, `Containers`,
`RedirecionamentoDeLink`), every container carrying a technology, and kinds encoded as tags plus
`styles` — `Database` → cylinder, `Queue` → pipe, `External` → grey — rather than ad-hoc colors.
Relationship labels are directional and specific, and **every inter-process hop carries a
protocol**: `JSON/HTTPS` SPA→API, `SQL/TCP` to Postgres, `RESP/TCP` to Redis, `AMQP` to and from
RabbitMQ. Zero legacy keywords. The queue is modeled as a container, per the classification rules.

**Eval 3, evolving.** The diff against the seed `workspace.dsl` is **purely additive**: 44 `+`
lines, **zero** lines removed or modified. Original identifiers, styles and the existing view keys
(`Contexto`, `Containers`) are untouched, so no saved layout is orphaned. `docs/adr/` is
byte-identical to the fixture. The deployment model gets the idiomatic shape rather than a naive
one: the ALB is an `infrastructureNode` wired through the `portal -/> api` reroute — a load
balancer as a deployment concept, never a container on a container view — with `instances 2` on
the API task and the database instanced under an `Amazon RDS` node.

## Never-invent held in both

- **Eval 2** left the Google Workspace SSO relationship at `HTTPS` and refused to name OAuth 2.0
  or SAML, flagging the gap to the user along with the absent deployment information.
- **Eval 3** left RabbitMQ out of the production environment entirely, because its production home
  was never stated, and fabricated no AWS region node to hang it from. The gap went to the user as
  a question.

Both runs validated through the Docker CLI (exit 0), and **both independently ran a negative
control first** — a deliberately broken DSL — to prove the validator's silence on success was a
genuine pass rather than a no-op. Neither claimed validation it had not performed.

## Scope

Two evals, one run each — a targeted gate for a navigational change, not a variance measurement.
Evals 1, 4 and 5 were not re-run; 1.2.1 touches only `dsl-reference.md`, and these two are the
cases with the most exposure to it. Eval 3's first attempt died mid-task on an account spend
limit after validating; the fixture was re-seeded from `evals/files/` and the run repeated from
scratch, so the numbers above are a clean run.
