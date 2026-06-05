# Modeling patterns — microservices, messaging, landscapes, composition

Read this only when the task involves microservices, queues/topics, multiple systems /
landscapes, or splitting the model across files. Derived from
[docs.structurizr.com](https://docs.structurizr.com) (MIT) — see NOTICE.md.

## 1. Microservices

Owned by the same team = a **group of containers** (API + its datastore) inside one
system — not a single box, not a separate system:

```
ss = softwareSystem "Shop" {
    group "Orders Service" {
        ordersApi = container "Orders API" "Manages order lifecycle." "Go"
        ordersDb = container "Orders DB" "Order state." "PostgreSQL" {
            tags "Database"
        }
        ordersApi -> ordersDb "Reads from and writes to"
    }
}
```

Services owned by *other teams* are separate (external) software systems instead.
(Repeating many services? An archetype `microservice = group` reads nicely — see
dsl-advanced.md §1.)

## 2. Queues and async messaging

Model the queues/topics as containers (tagged, styled as pipe) — the broker itself is a
deployment concern:

```
api = container "API" "" "Go"
clickQueue = container "Click Events Queue" "Buffer of click events." "RabbitMQ" {
    tags "Queue"
}
worker = container "Metrics Worker" "Aggregates click metrics." "Go"

api -> clickQueue "Publishes click events to"
clickQueue -> worker "Delivers click events to"
```

Label so the arrow reads naturally (`queue -> consumer "Delivers … to"` or
`consumer -> queue "Consumes … from"` — pick one per diagram and stay consistent). For
minor point-to-point cases, skip the queue box and put `"Sends X to" "via RabbitMQ"` on
the relationship.

## 3. Landscape and multi-workspace

**Landscape workspace** (portfolio map): people + software systems + relationships,
**no containers**, `configuration { scope landscape }`, one `systemLandscape` view.

**Recommended general scope:** one workspace per software system, owned by its team,
living in that system's repo.

**Enterprise pattern** (many teams): a shared *system catalog* DSL with only system
definitions; each team's workspace `extends` the catalog and opens its own system with
`!element` (syntax in dsl-advanced.md §2); a central landscape workspace merges the team
workspaces. Composition over inheritance — prefer several focused workspaces to one
mega-workspace.

## 4. Monorepo / shared fragments (`!include`)

```
workspace {
    !identifiers hierarchical
    model {
        !include systems/orders.dsl
        !include systems/billing.dsl
    }
}
```

`!include <file|directory|url>` textually inlines fragments — build one model from
per-system files. Reusable fragments (e.g. a shared component) combine
`!identifiers hierarchical` + `group` + `!include` so each container gets its own copy.
`!include` = compose one workspace from parts; `workspace extends` = layer a new
workspace on an existing base.

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
