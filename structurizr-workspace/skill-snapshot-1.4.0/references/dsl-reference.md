# Structurizr DSL — core syntax reference (v6+)

Condensed from [docs.structurizr.com/dsl](https://docs.structurizr.com/dsl) (MIT) — see
NOTICE.md. Current as of DSL v6.2.x (2026). Anything marked **LEGACY** must not appear in
generated DSL. Rare features (archetypes, workspace extension, scripts/plugins,
filtered/custom/image views, perspectives) live in `dsl-advanced.md` — read that only
when the task needs them.

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
- Constants: `!const NAME value`, referenced as `${NAME}`.
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

Inside any element body: `description "…"`, `technology "…"`, `tags "T1" "T2"`,
`url https://…`, `properties { "name" "value" }`.

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

Valid at model level, inside systems, inside containers. Nested groups need
`properties { "structurizr.groupSeparator" "/" }` at the top of `model`. Style targets:
`element "Group"`, `element "Group:Team A"`, `element "Group:Parent/Child"`.

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
| instanceOf | `instanceOf <identifier> [deploymentGroups] [tags]` |
| deploymentGroup | `<id> = deploymentGroup <name>` — isolates instance wiring per copy |
| healthCheck | `healthCheck <name> <url> [interval] [timeout]` (in an instance block) |

`instances` takes a count (`instances 2`) or range (`"1..N"`). Relationships between
instances are inherited from the model.

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
include <*|id|expression> …
exclude <id|expression> …
autoLayout [tb|bt|lr|rl] [rankSeparation] [nodeSeparation]   // defaults: tb 300 300
title <text>
description <text>
default                       // marks the default view
```

**Dynamic views** — each line is an ordered step, and **must be backed by a model
relationship** between the two elements (description may be overridden per step):

```
dynamic s "Feature" {
    u -> s.api "Requests X from"
    s.api -> s.db "Reads X from"
    autoLayout lr
}
```

Parallel steps: explicit numbering (`1:`, `2:`, same number = parallel) or nested brace
blocks.

Gotchas: a `deployment` view's environment must match a defined `deploymentEnvironment`;
`include *` in a container view shows only the scoped system's containers — include other
systems' containers explicitly.

## 8. Include/exclude expressions

```
->id   id->   ->id->                       // element + incoming/outgoing/both relationships
element.type==<Person|SoftwareSystem|Container|Component|DeploymentNode|InfrastructureNode|ContainerInstance>
element.parent==<id>      element.tag==<tag>[,tag]      element.tag!=<tag>
*->*   id->*   *->id                       // relationships
relationship.tag==<tag>   relationship.source==<id>   relationship.destination==<id>
```

Combine with `&&`/`||`: `include "element.type==Container && element.parent==s"`.
Exclude a relationship: `exclude "u -> s.api"`.

## 9. Styles

```
styles {
    element "<tag>" {
        shape <Box|RoundedBox|Circle|Ellipse|Hexagon|Diamond|Cylinder|Bucket|Pipe|Person|Robot|Folder|WebBrowser|Window|Terminal|Shell|MobileDevicePortrait|MobileDeviceLandscape|Component>
        icon <file|url>
        width <int>   height <int>
        background <#rrggbb|name>   color <#rrggbb|name>
        stroke <#rrggbb|name>   strokeWidth <1-10>
        fontSize <int>   border <solid|dashed|dotted>   opacity <0-100>
        metadata <true|false>   description <true|false>
    }
    relationship "<tag>" {
        thickness <int>   color <#rrggbb|name>
        style <solid|dashed|dotted>      // modern; LEGACY: dashed true|false
        routing <Direct|Orthogonal|Curved>
        fontSize <int>   width <int>   position <0-100>   opacity <0-100>
    }
}
```

Styles match by tag — tag elements (`tags "Database"`) and style the tag. ADR status
styling: `element "Decision:<Status>"` (literal status string, no fixed enum). Element
styles render fully in Structurizr; PlantUML/Mermaid exports support a subset.

## 10. Themes

```
theme <installed-name|url|file>     // repeatable, one per line
```

**Prefer installed theme names** — the `structurizr/structurizr` image bundles them at
`/usr/local/structurizr-themes` (verified): `amazon-web-services-2025.07`,
`microsoft-azure-2025.11`, `google-cloud-platform-2025.09`, `kubernetes`,
`oracle-cloud-infrastructure-2023.04`. They resolve only when the container has
`STRUCTURIZR_THEMES=/usr/local/structurizr-themes` set — pass
`-e STRUCTURIZR_THEMES=/usr/local/structurizr-themes` on `validate`/`export` runs.

Avoid `https://static.structurizr.com/themes/...` URLs: the Structurizr cloud service
reaches end-of-life on 2026-09-30 and they will stop resolving.

Tag elements with the theme's tag names (e.g. `tags "Amazon Web Services - RDS"`) for
icons. Local `styles` combine with themes.

**LEGACY:** `themes a b c` (plural), `theme default`, and `branding { }` (removed in v6).

## 11. Documentation and ADRs

```
!docs <path> [fqcn]
!adrs <path> [adrtools|madr|log4brains|fqcn]
```

Valid at workspace, softwareSystem, and container scope; path relative to the DSL file
(same dir or subdir). `!adrs` default importer is **adrtools** (Nygard format: `# N. Title`,
`Date:`, `## Status`); files import alphabetically, so `NNNN-title.md` ordering holds.

## 12. Implied relationships, !include

- `!impliedRelationships <true|false>` — default **true**: `user -> s.api` also implies
  `user -> s`. Leave it on.
- `!include <file|directory|url>` — textually inlines DSL fragments (monorepo pattern:
  see `modeling-patterns.md`).

## 13. Workspace configuration

```
configuration {
    scope <softwaresystem|landscape|none>
}
```

`scope softwaresystem` for one-system workspaces; `scope landscape` for landscape
workspaces (these must not define containers).

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

Why these conventions:

- `!identifiers hierarchical` — lets container names repeat across systems and keeps the
  workspace extendable later.
- **Every element gets a description; every container gets a technology.** The C4 review
  checklist demands both; diagrams must be readable by someone who wasn't in the room.
- **Relationship labels are specific and directional** — "Publishes click events to", not
  "Uses". The label must read correctly along the arrow's direction. Inter-process
  relationships also get a technology/protocol.
- **Tags + styles, not ad-hoc colors**: `Database` → cylinder, `Queue` → pipe, `External` →
  grey, person shape for people. Consistent encodings double as the diagram legend.
- **Stable, descriptive view keys** (`"SystemContext"`, `"Containers"`,
  `"Deployment-Live"`) — keys identify views across exports and layout sessions; changing
  them later orphans saved layout.
- `autoLayout` on every view (direction `lr`/`tb` as fits the flow) — the user can still
  drag elements in the UI, which then persists to `workspace.json`.
- `configuration { scope softwaresystem }` for one-system workspaces,
  `scope landscape` for landscape workspaces (these must not define containers).
- Write element names and descriptions in the language the user used to describe their
  system; DSL keywords are always English.

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
