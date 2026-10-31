# Structurizr DSL — core syntax reference (v6+)

Condensed from [docs.structurizr.com/dsl](https://docs.structurizr.com/dsl) (MIT) — see
NOTICE.md. Current as of DSL v6.2.x (2026). Anything marked **LEGACY** must not appear in
generated DSL. Rare features (archetypes, workspace extension, scripts/plugins,
filtered/custom/image views, perspectives, terminology, animations, health checks,
server-only configuration) and the exhaustive tables (include/exclude expression
grammar, style properties) live in `dsl-advanced.md` — read that only when the task
needs them.

**Sections** — jump to what the task needs rather than reading straight through:

1. File basics · 2. Elements · 3. Relationships · 4. Groups · 5. Identifiers ·
6. Deployment · 7. Views · 8. Include/exclude expressions · 9. Styles · 10. Themes ·
11. Documentation and ADRs · 12. Implied relationships, `!include` ·
13. Workspace configuration · 14. Defaults and gotchas ·
**15. House template for a new workspace** (copy this to start from scratch)

## 1. File basics

- Structure: `workspace [name] [description] { model { … } views { … } }`.
- Keywords case-insensitive; quotes required only for values with spaces.
- **Opening `{` must end its statement's line; closing `}` sits alone on its line.**
- Comments `//`, `#`, `/* … */`; line continuation with trailing `\`.
- Skip an earlier optional argument with an empty string: `container "DB" "" "PostgreSQL"`.
- Constants and variables: `!const NAME value` (immutable) / `!var NAME value`
  (reassignable), names `a-zA-Z0-9-_.`, referenced as `${NAME}`. `${NAME}` also resolves
  environment variables; an unknown name is left as-is, silently.
- **No forward references** — define an element before naming it in a relationship.
  Workaround: inside the source element's block, `-> x "Uses"` (implicit `this`).

```
workspace {
    model {
        u = person "User"
        ss = softwareSystem "Software System"
        u -> ss "Uses"
    }
    views {
        systemContext ss {
            include *
        }
    }
}
```

## 2. Elements

Argument order is always **name, description, technology, tags**; all trailing args and
the `{ … }` body optional.

| Element | Signature |
|---|---|
| person | `person <name> [description] [tags]` |
| softwareSystem | `softwareSystem <name> [description] [tags]` |
| container | `container <name> [description] [technology] [tags]` |
| component | `component <name> [description] [technology] [tags]` |
| element (custom) | `element <name> [metadata] [description] [tags]` |

Nesting: persons/systems in `model`; containers in a softwareSystem; components in a
container. Default tags: `Element` plus `Person` / `Software System` / `Container` /
`Component`.

Inside any element body: `description "…"`, `technology "…"`, `tags "T1" "T2"` (also
`tags "T1,T2"` or singular `tag "T1"`), `url https://…`, `properties { "name" "value" }`.

## 3. Relationships

```
<source> -> <destination> [description] [technology] [tags]
-> <destination> [description] [technology]      // implicit source: enclosing element
```

Default tag `Relationship`. In deployment environments, `a -/> b { … }` removes the
inherited a→b relationship and substitutes the block's relationships (rerouting through a
gateway/load balancer — see `deployment-patterns.md`).

## 4. Groups

```
group "Team A" {
    a = softwareSystem "A"
}
```

Valid at model level, inside systems, inside containers, inside deployment nodes. A group
only holds elements of one abstraction level. Nested groups need
`properties { "structurizr.groupSeparator" "/" }` at the top of `model`. Style targets:
`element "Group"`, `element "Group:Team A"`, `element "Group:Parent/Child"`. A component
can also name its group as a property: `component "X" { group "Name" }`. Groups carry no
identifier and `!identifiers hierarchical` does not apply to them.

**LEGACY:** `enterprise { }` and `location` were removed — use groups.

## 5. Identifiers

- `id = <element|relationship>`; chars `a-zA-Z_0-9`. Default scope is flat (globally
  unique). Prefer `!identifiers hierarchical`: names scope to their parent, referenced by
  dotted path (`shop.api` and `billing.api` can coexist).
- `this` = the element in scope.

## 6. Deployment

```
production = deploymentEnvironment "Production" {
    aws = deploymentNode "Amazon Web Services" {
        region = deploymentNode "us-east-1" {
            alb = infrastructureNode "Load Balancer" "Routes traffic." "ALB"
            deploymentNode "ECS Cluster" "" "AWS ECS Fargate" {
                deploymentNode "API Task" "" "Docker Container" {
                    instances 2
                    instanceOf s.api
                }
            }
            deploymentNode "Amazon RDS" {
                deploymentNode "PostgreSQL" {
                    instanceOf s.db
                }
            }
        }
    }
}
```

| Keyword | Signature |
|---|---|
| deploymentEnvironment | `deploymentEnvironment <name> { … }` |
| deploymentNode | `deploymentNode <name> [description] [technology] [tags] [instances] { … }` — nestable |
| infrastructureNode | `infrastructureNode <name> [description] [technology] [tags]` |
| instanceOf | `instanceOf <identifier> [deploymentGroups] [tags]` — generic; the classic `containerInstance <id>` / `softwareSystemInstance <id>` forms are equally valid |
| deploymentGroup | `<id> = deploymentGroup <name>` — isolates instance wiring per copy; assign per instance (`containerInstance api grp`) or once on a node (`deploymentGroup grp` inside the `deploymentNode` block, applying to everything beneath it) |

`instances` takes a count (`instances 2`) or range (`"1..N"`). Relationships between
instances are inherited from the model. An instance can carry an identifier
(`webInst = containerInstance webapp`) so infrastructure nodes can point at it directly
(`elb -> webInst "Forwards requests to" "HTTPS"`) — the lighter alternative to `-/>` when
you only need to draw the hop, not remove the inherited relationship. The hierarchical
path rule below applies to the instance too: `aws.region.ec2.vm.webInst`, with an
identifier bound to every node on the way (verified: skipping one fails with
`destination element … does not exist`).

**Hierarchical-identifier gotcha (verified against the parser).** With
`!identifiers hierarchical`, an element nested inside deployment nodes can be referenced
ONLY through the full dotted path of *bound* identifiers: `aws.region.alb` from inside the
environment block (or `production.aws.region.alb` absolutely). Bare `alb` and partial
`region.alb` fail with `element "alb" does not exist`. Bind an identifier to **every
ancestor deployment node on the path** you reference through.

## 7. Views

```
systemLandscape [key] [description] { … }
systemContext <system-id> [key] [description] { … }
container <system-id> [key] [description] { … }
component <container-id> [key] [description] { … }
dynamic <*|system-id|container-id> [key] [description] { … }
deployment <*|system-id> <environment> [key] [description] { … }
```

Always pass an explicit, stable `key` — keys identify views across exports and saved
layout. (filtered/custom/image views: see `dsl-advanced.md`.)

View body:

```
include <*|*?|id|expression> …
exclude <id|expression> …
autoLayout [tb|bt|lr|rl] [rankSeparation] [nodeSeparation]   // defaults: tb 300 300
title <text>
description <text>
default                       // marks the default view
properties { "name" "value" }
```

(`animation { … }` steps: `dsl-advanced.md` §6.)

`*?` (reluctant wildcard; context/container/component views only) includes the same
elements as `*` but only relationships to/from the elements in scope — handy when the
outside systems talk to each other and clutter the view.

**Dynamic views** — each line is an ordered step, and **must be backed by a model
relationship** between the two elements (description and technology may be overridden
per step). A step can also name an identified relationship instead of a pair:
`rel1 "Description"`.

```
dynamic s "Feature" {
    title "Request past orders"
    u -> s.api "Requests past orders from"
    s.api -> s.db "Queries orders in"
    autoLayout lr
}
```

Give each dynamic view a `title` — several scenarios over the same elements are
indistinguishable otherwise. Parallel steps: explicit numbering (`1:`, `2:`, same number =
parallel) or nested brace blocks.

Gotchas: a `deployment` view's environment must match a defined `deploymentEnvironment`;
`include *` in a container view shows only the scoped system's containers (plus external
systems it depends on) — to show another system's containers, name them
(`include s1.c1 s2.c2`) or use an expression (`include element.type==container`, or
`include element.parent==s1 element.parent==s2`).

## 8. Include/exclude expressions

`include *` plus identifiers covers most views. When it doesn't, the expressions that
come up in practice:

```
->id->                                     // element + its relationships (->id / id-> for one direction)
element.type==Container                    // Person|SoftwareSystem|Container|Component|DeploymentNode|…
element.parent==<id>      element.tag==<tag>
exclude "u -> s.api"                       // drop one relationship; * allowed on either side
```

Combine with `&&`/`||` and quote any expression containing whitespace:
`include "element.type==Container && element.parent==s"`. Relationship expressions only
act on elements already in the view. The full grammar (technology, group, and property
filters; `relationship.source`/`destination`; group-aware `element==->id`) is in
`dsl-advanced.md` §7.

## 9. Styles

```
styles {
    element "<tag>" {
        shape <Box|RoundedBox|Circle|Ellipse|Hexagon|Diamond|Cylinder|Bucket|Pipe|Person|Robot|Folder|WebBrowser|Window|Terminal|Shell|MobileDevicePortrait|MobileDeviceLandscape|Component>
        background <#rrggbb|name>   color <#rrggbb|name>   icon <file|url>
    }
    relationship "<tag>" {
        style <solid|dashed|dotted>      // REMOVED: dashed true|false
        color <#rrggbb|name>   routing <Direct|Orthogonal|Curved>
    }
}
```

Styles match by tag — tag elements (`tags "Database"`) and style the tag; `colour` is an
alias of `color`. The house template in §15 carries the usual set. The remaining
properties (size, stroke, border, opacity, font, metadata/description toggles, `light`/`dark`
blocks), ADR status styling, and export caveats are in `dsl-advanced.md` §8.

## 10. Themes

```
theme <installed-name|url|file>     // repeatable, one per line (house style)
themes <a> [b] …                    // also valid; leave it alone in existing files
```

A name must be installed; a URL is loaded when rendering; a file is inlined into the
workspace.

**Prefer installed theme names** — the `structurizr/structurizr` image bundles them at
`/usr/local/structurizr-themes` (verified): `amazon-web-services-2025.07`,
`microsoft-azure-2025.11`, `google-cloud-platform-2025.09`, `kubernetes`,
`oracle-cloud-infrastructure-2023.04`. They resolve only when the container has
`STRUCTURIZR_THEMES=/usr/local/structurizr-themes` set — pass
`-e STRUCTURIZR_THEMES=/usr/local/structurizr-themes` on `validate`/`export` runs.

Avoid `https://static.structurizr.com/themes/...` URLs: the Structurizr cloud service
is being retired (the docs list it under "End of life") and those URLs depend on it.

Tag elements with the theme's tag names (e.g. `tags "Amazon Web Services - RDS"`) for
icons. Local `styles` combine with themes.

**REMOVED:** `theme default` and `branding { }` (gone in v6).

## 11. Documentation and ADRs

```
!docs <path> [fqcn]
!adrs <path> [adrtools|madr|log4brains|fqcn]        // !decisions is the same keyword
!adrs <path> [type] {
    exclude <filename|regex> [filename|regex]       // skip README.md, nnnn-template.md …
}
```

Valid at workspace, softwareSystem, and container scope; path relative to the DSL file
(same dir or subdir). `!adrs` default importer is **adrtools** (Nygard format: `# N. Title`,
`Date:`, `## Status`); files import alphabetically, so `NNNN-title.md` ordering holds.
Every Markdown/AsciiDoc file in the directory is imported, so a `README.md` or an ADR
template in the folder breaks the parse — exclude it with the block form (same for
`!docs`). `!decisions` is the parser's primary name for `!adrs` since v6.2; both work.

## 12. Implied relationships, !include

- `!impliedRelationships <true|false|fqcn>` — default **true**: `user -> s.api` also
  implies `user -> s`. Leave it on. With the default strategy **only one implied
  relationship is created per element pair** (the first defined): two `user -> s.api`
  lines with different labels give the context view a single arrow with the first label.
  Prefer one relationship whose label summarizes ("Browses and purchases using") and put
  the specifics in dynamic-view steps. If both arrows must show, switch strategy:
  `!impliedRelationships com.structurizr.model.CreateImpliedRelationshipsUnlessSameRelationshipExistsStrategy`
  (implies unless the *same* relationship exists), rather than duplicating parent-level
  relationships by hand.
- `!include <file|directory|url>` — textually inlines DSL fragments (monorepo pattern:
  see `modeling-patterns.md`).

## 13. Workspace configuration

```
configuration {
    scope <softwaresystem|landscape|none>
    properties { "name" "value" }
}
```

`scope softwaresystem` for one-system workspaces; `scope landscape` for landscape
workspaces (these must not define containers). Server-only settings (`visibility`,
`users`): `dsl-advanced.md` §6.

## 14. Defaults and gotchas

- No views defined → auto-created landscape/context/container views. Define views
  explicitly anyway, with stable keys.
- Keep `workspace.json` ≤ 1–2 MB; don't embed big images.
- Recommended scope: one workspace per software system; a landscape workspace maps the
  portfolio (`modeling-patterns.md`).
- The most common deployment parse error is the hierarchical-path rule in §6.

## 15. House template for a new workspace

Start here when creating a workspace from scratch.

```
workspace "Name" "One-line description." {

    !identifiers hierarchical

    model {
        u = person "User" "Why they use the system."

        s = softwareSystem "System" "What value it delivers." {
            api = container "API" "What it is responsible for." "Go"
            db = container "Database" "What it stores." "PostgreSQL" {
                tags "Database"
            }
        }

        ext = softwareSystem "Payment Provider" "Third-party PSP." {
            tags "External"
        }

        u -> s.api "Manages orders using" "HTTPS"
        s.api -> s.db "Reads from and writes to" "SQL/TCP"
        s.api -> ext "Authorizes payments using" "HTTPS"
    }

    views {
        systemContext s "SystemContext" {
            include *
            autoLayout
        }

        container s "Containers" {
            include *
            autoLayout
        }

        styles {
            element "Element" {
                background #1168bd
                color #ffffff
            }
            element "Person" {
                shape person
            }
            element "Database" {
                shape cylinder
            }
            element "Queue" {
                shape pipe
            }
            element "External" {
                background #999999
                color #ffffff
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
```

The conventions this template encodes (hierarchical identifiers, descriptions and
technologies everywhere, specific directional labels, tags + styles, stable view keys,
`autoLayout`, scope) are explained in SKILL.md step 4; `autoLayout` direction (`lr`/`tb`)
follows the flow, and the user can still drag elements in the UI, which persists to
`workspace.json`.

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
