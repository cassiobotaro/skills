# C4 diagrams — which to create, notation rules, review checklist

When each diagram type earns its place, how to make any diagram self-describing, and the
full pre-delivery checklist. Derived from c4model.com (Simon Brown, CC BY 4.0) — see
NOTICE.md.

## Diagram types

### System Context (level 1) — recommended for all teams
- **Scope:** one software system, drawn as the central box.
- **Shows:** the system + the people who use it + the external systems it talks to.
- **Audience:** everybody, technical and non-technical.
- **Exclude:** technologies, protocols, low-level detail — this is the zoomed-out view.

### Container (level 2) — recommended for all teams
- **Scope:** one software system, opened up.
- **Shows:** the containers, their major technology choices, and how they communicate;
  plus the people/external systems touching them.
- **Audience:** technical people in and around the team (devs, architects, ops).
- **Exclude:** deployment concerns — clustering, load balancers, replication, failover —
  these vary per environment and belong in deployment diagrams.

### Component (level 3) — only if it adds value
- **Scope:** one container, opened up into components with responsibilities and
  technologies.
- C4's own advice: most teams shouldn't hand-maintain these; consider generating them from
  code if they're needed long-term.

### Code (level 4) — effectively never
- Auto-generate on demand from an IDE for the most critical components only. Not for
  long-lived documentation.

### System Landscape — recommended, especially for larger organizations
- **Scope:** an organization/department: people + software systems, no containers.
- It is a context diagram with no single system in focus — a map of the portfolio.
- In Structurizr: a landscape-scoped workspace (`configuration { scope landscape }`)
  must not define containers; per-system detail lives in each system's own workspace.

### Dynamic — use sparingly
- **Shows:** how elements collaborate at runtime for one scenario/use case, with numbered
  steps; elements may be systems, containers, or components.
- Reserve for genuinely interesting or complicated interactions. Every step must
  correspond to a relationship that exists in the model.

### Deployment — recommended, one per environment
- **Shows:** how container/system instances map onto infrastructure (deployment nodes,
  nested as needed) for a *single* environment (Production, Staging, …).
- Infrastructure nodes (DNS, load balancers, firewalls) and instance counts live here.
- Cloud-provider icons are welcome — via themes — as long as the meaning stays clear.

### Quick matrix

| Diagram | Create it? |
|---|---|
| System Context | Always |
| Container | Always (system-scoped workspaces) |
| Component | Only on request / clear value |
| Code | No — IDE on demand |
| System Landscape | When modelling multiple systems |
| Dynamic | Sparingly, per meaningful scenario |
| Deployment | One per described environment |

## Notation rules (what makes a diagram readable)

C4 is notation-independent; these recommendations make diagrams self-describing. In
Structurizr most of them translate to: fill in every description/technology field and use
consistent tag-based styles.

- Every diagram needs a **title** describing type and scope. (Structurizr auto-generates
  one from the view type + element; add `title` only to override.)
- Every diagram needs a **key/legend** (Structurizr renders one from your styles — which
  is why ad-hoc per-element colors are a bad idea).
- **Element type** should be explicit (the metadata line under the name).
- **Every element gets a short description** — the "at a glance" responsibility.
- **Every container/component states its technology.**
- **Every line is unidirectional with a specific label**; the wording must match the
  arrow direction. Avoid "Uses" — prefer "Sends customer update events to". Show two
  arrows when two directions genuinely matter; don't double-head one line.
- **Inter-container relationships state technology/protocol** (e.g. "JSON/HTTPS").
- **Acronyms** must be ones the audience knows — or spelled out in descriptions.
- **Colors are free but must be consistent** within and across diagrams; mind color-blind
  readers and black-and-white printing — never encode meaning in color alone (pair it
  with shape or tag metadata).

### Lines: dependency or data flow?
Your choice per diagram — "A uses B" or "A sends X to B" — but the label must match the
arrow head, and stay consistent within a diagram.

## Review checklist (run before delivering)

General
- [ ] Does the diagram have a title (auto-generated or explicit)?
- [ ] Is the diagram type and scope obvious?
- [ ] Is there a key/legend covering the notation (styles → legend)?

Elements
- [ ] Every element has a name?
- [ ] The abstraction level of every element is clear (person/system/container/…)?
- [ ] Every element has a description saying what it does?
- [ ] Technology stated wherever applicable (containers, components)?
- [ ] All acronyms/abbreviations understandable?
- [ ] Meaning of every color, shape, icon, border style, and size is clear (and used
      consistently)?

Relationships
- [ ] Every arrow has a label describing intent?
- [ ] Every label reads correctly in the arrow's direction?
- [ ] Technology/protocol on inter-process relationships?
- [ ] Meaning of every line style/arrowhead/color is clear?

Structurizr-specific additions
- [ ] DSL validates cleanly (MCP or `structurizr/structurizr validate`)?
- [ ] No legacy keywords (`enterprise`, `!extend`, `!ref`, `branding`, plural `themes`,
      `dashed true`)?
- [ ] View keys stable and descriptive?
- [ ] `configuration { scope … }` matches the workspace type?
- [ ] Dynamic-view steps all backed by model relationships?
- [ ] ADRs linked via `!adrs` when the repo has them?

## Will diagrams rot?
Context diagrams change slowly; container diagrams relatively slowly (faster with heavy
microservices/serverless churn); component diagrams change often; code diagrams rot
immediately. That ordering is exactly why the lower levels are de-emphasized — and why
the DSL file should live in the repo, evolving with the code it describes.

---
*Derived from the C4 model by Simon Brown ([c4model.com](https://c4model.com)),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); condensed and adapted.*
