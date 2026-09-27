# Modeling patterns — microservices, messaging, landscapes, composition

Read this only when the task involves microservices, queues/topics, multiple systems /
landscapes, hardware or devices the software talks to, or splitting the model across
files. Derived from
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
`!identifiers hierarchical` + `group` + `!include` so each container gets its own copy
(referenced as `s.app1.loggingComponent`, `s.app2.loggingComponent`).
`!include` = compose one workspace from parts; `workspace extends` = layer a new
workspace on an existing base.

## 5. Hardware systems and devices

Cameras, robots, PLCs, sensors, kiosks, medical devices — physical things the software
controls or listens to. They are **not** software systems (nobody deploys code into a
Basler camera from this repo) and not people. C4 has no box for them, so use a **custom
element** via an archetype, and style it so it reads as hardware:

```
model {
    archetypes {
        hardwareSystem = element {
            metadata "Hardware System"
            tags "Hardware"
        }
    }
    platform = softwareSystem "Factory Monitoring" "Watches the floor, commands the arms."
    camera = hardwareSystem "Industrial Camera" "Basler camera with closed firmware."
    arm = hardwareSystem "Robotic Arm" "KUKA arm."

    camera -> platform "Streams video frames to" "RTSP"
    platform -> arm "Sends control commands to" "OPC UA"
}
views {
    styles {
        element "Hardware" {
            shape robot
            background #6b6b6b
            color #ffffff
        }
    }
}
```

`metadata` is the type line rendered under the name (the slot "Software System" occupies
for systems). Custom elements appear on system-context views through their relationships;
inside a container view they show as external neighbours of the containers they talk to.
Firmware you *do* write and deploy is different: that is a container (or system) of yours
running on the device, and the device is then a `deploymentNode` in a deployment view.

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
