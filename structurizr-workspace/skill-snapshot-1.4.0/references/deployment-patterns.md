# Deployment patterns — gateways, load balancers, cloud nesting, environments

Read this only when the task involves deployment environments / infrastructure. Derived
from [docs.structurizr.com/dsl/patterns](https://docs.structurizr.com/dsl/patterns/)
(MIT) — see NOTICE.md.

**Path rule (applies to everything here):** with `!identifiers hierarchical`, reference
deployment-nested elements by the full dotted path of bound ancestor identifiers
(`aws.region.alb`), never bare (`alb`) — bind an identifier to every ancestor
`deploymentNode` you traverse. See dsl-reference §6.

## 1. API gateway / load balancer / firewall (`-/>`)

These are **deployment concepts** — model as `infrastructureNode` in a deployment
environment and reroute the logical relationship with `-/>`. Never put them on container
views. (Exception: a gateway you *built*, doing real business logic, may be a container.)

```
env = deploymentEnvironment "Production" {
    deploymentNode "User's Computer" {
        deploymentNode "Web Browser" {
            instanceOf ss.ui
        }
    }
    gw = deploymentNode "API Gateway Server" {
        apiGateway = infrastructureNode "API Gateway"
    }
    deploymentNode "Server 1" {
        instanceOf ss.service1
    }

    ss.ui -/> ss.service1 {
        ss.ui -> gw.apiGateway
        gw.apiGateway -> ss.service1
    }
}
```

`a -/> b { … }` removes the inherited a→b instance relationship and substitutes the
block's relationships. A second `-/>` for another backend reuses the already-routed hop
(`gw.apiGateway -> ss.service2` only). Lightweight alternative — keep the relationship,
annotate it: `!relationships "ss.ui -> ss.service1" { technology "via API Gateway" }`.

## 2. Cloud/runtime nesting (Docker, Kubernetes, AWS)

Nest `deploymentNode`s from provider down to runtime; `instanceOf` at the innermost
level; `instances` for replicas; theme tags for icons.

Docker (dev): Laptop → `"Docker"` → App Container (`"Docker Container"`) → `instanceOf`.
Kubernetes: Cluster (`"Kubernetes Cluster"`) → Node (`instances 2`) → Pod
(`"Kubernetes Pod"`) → Container (`"Docker Container"`) → `instanceOf`.

AWS, with ALB reroute and bundled theme:

```
live = deploymentEnvironment "Live" {
    aws = deploymentNode "Amazon Web Services" {
        tags "Amazon Web Services - Cloud"
        region = deploymentNode "us-east-1" {
            tags "Amazon Web Services - Region"
            alb = infrastructureNode "Load Balancer" "" "Application Load Balancer" {
                tags "Amazon Web Services - Elastic Load Balancing"
            }
            deploymentNode "Amazon ECS" "" "AWS Fargate" {
                deploymentNode "API Task" "" "Docker Container" {
                    instances 2
                    instanceOf ss.api
                }
            }
            deploymentNode "Amazon RDS" {
                tags "Amazon Web Services - RDS"
                deploymentNode "PostgreSQL" {
                    instanceOf ss.db
                }
            }
        }
    }

    ss.spa -/> ss.api {
        ss.spa -> aws.region.alb "Makes API calls to" "JSON/HTTPS"
        aws.region.alb -> ss.api "Forwards requests to" "JSON/HTTPS"
    }
}
views {
    deployment * live "Deployment-Live" {
        include *
        autoLayout lr
    }
    theme amazon-web-services-2025.07
}
```

Use bundled theme names (dsl-reference §10) — `static.structurizr.com` URLs die with the
cloud EOL on 2026-09-30.

## 3. Multiple environments

One `deploymentEnvironment` per environment, one deployment view each
(`deployment ss dev "Deployment-Development"`, `deployment ss live "Deployment-Live"`).

Same container deployed as several isolated stacks? Use `deploymentGroup` so instances
only wire within their copy:

```
production = deploymentEnvironment "Production" {
    inst1 = deploymentGroup "Instance 1"
    inst2 = deploymentGroup "Instance 2"
    deploymentNode "Server 1" {
        containerInstance api inst1
        containerInstance db inst1
    }
    deploymentNode "Server 2" {
        containerInstance api inst2
        containerInstance db inst2
    }
}
```

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
