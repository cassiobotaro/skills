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
block's relationships. Both ends need an instance in the environment: with none of `a`
deployed, the parser answers that the relationship does not exist. A second `-/>` for
another backend reuses the already-routed hop (`gw.apiGateway -> ss.service2` only).
Lightweight alternative — keep the relationship, annotate it: `!relationships "ss.ui -> ss.service1" { technology "via API Gateway" }`.
A firewall sits the same way, typically as an `infrastructureNode` *inside* the server
node it protects. Make infrastructure nodes read differently from servers:
`element "Infrastructure Node" { shape ellipse }` in `styles`.

## 2. Cloud/runtime nesting (Docker, Kubernetes, AWS)

Nest `deploymentNode`s from provider down to runtime; `instanceOf` at the innermost
level; `instances` for replicas; theme tags for icons. Runtimes (Docker, Kubernetes,
Fargate, App Runner, EKS) are deployment concepts — they never appear on a container view.
The official shapes, outermost to innermost; drop a layer when it says nothing
(the catalog itself shows Docker with and without the runtime node, Kubernetes with and
without worker nodes):

| Runtime | Nesting (`deploymentNode` unless noted) |
|---|---|
| Docker (dev) | Laptop (`"macOS"`) → `"Docker"` → App Container (`"Docker Container"`) → `instanceOf` — or skip the `"Docker"` node |
| Kubernetes | Cluster (`"Kubernetes Cluster"`) → Node (`"Kubernetes Worker Node"`, `instances 2`) → Pod (`"Kubernetes Pod"`) → Container (`"Docker Container"`) → `instanceOf` — or skip Node and put `instances` on the Pod |
| AWS EKS | `"Amazon Web Services"` → `"Elastic Kubernetes Service"` → Cluster → Pod (`instances N`) → Container → `instanceOf`: EKS and the cluster are two nodes |
| AWS Fargate | `"Amazon Web Services"` → `"Amazon ECS"` (technology `"AWS Fargate"`) → Task (`"Docker Container"`, `instances N`) → `instanceOf` |
| AWS App Runner | `"Amazon Web Services"` → (region) → `"App Runner"` → `"Docker Container"` (`instances N`) → `instanceOf` |

Pin the image on a Docker-container node when the user gives it:
`properties { "Image URI" "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest" }`.
A language runtime layer (`"Java Virtual Machine"` / `"Eclipse Temurin"`) between the
container and the instance is optional — include it only when the user cares.

AWS, with ALB reroute and bundled theme:

```
live = deploymentEnvironment "Live" {
    deploymentNode "Web Browser" {
        instanceOf ss.spa
    }
    aws = deploymentNode "Amazon Web Services" {
        tags "Amazon Web Services - AWS Cloud"
        region = deploymentNode "us-east-1" {
            tags "Amazon Web Services - Region"
            alb = infrastructureNode "Load Balancer" "" "Application Load Balancer" {
                tags "Amazon Web Services - Load Balancing"
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

Use bundled theme names (dsl-reference §10) — the Structurizr cloud service is being
retired, and `static.structurizr.com` theme URLs depend on it.

**Theme tags.** A tag draws an icon only when the theme named in `views` defines it, and
`validate` does not report one that it doesn't. `amazon-web-services-2025.07` renamed
tags that the older themes and most examples online still use (`Cloud` is now
`AWS Cloud`, `Elastic Load Balancing` is `Load Balancing`), and no version has the
abbreviations (`S3`, `SQS`, `ECS`): the names are spelled out. Its names for the usual
services, each prefixed with `Amazon Web Services - `:

`AWS Cloud` · `Region` · `Virtual private cloud VPC` · `Public subnet` ·
`Private subnet` · `Route 53` · `CloudFront` · `API Gateway` · `Load Balancing` · `WAF` ·
`EC2` · `Auto Scaling group` · `Elastic Container Service` · `Fargate` ·
`Elastic Kubernetes Service` · `App Runner` · `Lambda` · `RDS` · `Aurora` · `DynamoDB` ·
`ElastiCache` · `Simple Storage Service` · `Simple Queue Service` ·
`Simple Notification Service` · `EventBridge` · `Cognito` · `Secrets Manager`

For a service not listed, or another theme (Azure, Google Cloud, Kubernetes), read the
tags from the theme file in the image, which has no shell to `cat` it with:

```
docker create --name structurizr-themes structurizr/structurizr version
docker cp structurizr-themes:/usr/local/structurizr-themes/<theme>/theme.json theme.json
docker rm structurizr-themes
```

Delete `theme.json` afterwards. When you could not check a tag, say in the hand-off which
icons are unverified.

## 3. Serverless functions (AWS Lambda and kin)

Each function is a **container** (see c4-classification); many functions read well through
an archetype. Managed API Gateway in front of them is an `infrastructureNode` with a `-/>`
reroute (§1), not a container. Model the local emulator as its own environment:

```
model {
    archetypes {
        lambda = container {
            technology "AWS Lambda - Python"
            tags "Lambda"
        }
    }
    ss = softwareSystem "Orders" {
        createOrder = lambda "Create Order" "Validates and stores a new order."
        orders = container "Orders Table" "Order records." "Amazon DynamoDB" {
            tags "Database"
        }
        createOrder -> orders "Writes orders to" "DynamoDB API/HTTPS"
    }

    dev = deploymentEnvironment "Development" {
        deploymentNode "Developer Laptop" {
            deploymentNode "LocalStack" {
                deploymentNode "Lambda Service" {
                    instanceOf ss.createOrder
                }
                deploymentNode "DynamoDB Service" {
                    instanceOf ss.orders
                }
            }
        }
    }
    live = deploymentEnvironment "Live" {
        aws = deploymentNode "Amazon Web Services" {
            region = deploymentNode "us-east-1" {
                deploymentNode "AWS Lambda" {
                    instanceOf ss.createOrder
                }
                deploymentNode "Amazon DynamoDB" {
                    instanceOf ss.orders
                }
            }
        }
    }
}
```

## 4. Multiple environments

One `deploymentEnvironment` per environment, one deployment view each
(`deployment ss dev "Deployment-Development"`, `deployment ss live "Deployment-Live"`).

Same container deployed as several isolated stacks? Use `deploymentGroup` so instances
only wire within their copy — per instance, or once per node:

```
production = deploymentEnvironment "Production" {
    inst1 = deploymentGroup "Instance 1"
    inst2 = deploymentGroup "Instance 2"
    deploymentNode "Server 1" {
        containerInstance api inst1
        containerInstance db inst1
    }
    deploymentNode "Server 2" {
        deploymentGroup inst2
        containerInstance api
        containerInstance db
    }
}
```

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
