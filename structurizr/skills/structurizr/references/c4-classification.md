# C4 classification guide — what is a system, container, component?

How to place every part of a user's architecture at the right C4 abstraction level, and
which questions to ask when you can't. Derived from c4model.com (Simon Brown, CC BY 4.0) —
see NOTICE.md.

## The hierarchy

**Person → Software System → Container → Component → Code element.**

A software system is made up of one or more containers (applications and data stores),
each of which contains one or more components, which in turn are implemented by one or
more code elements. The power of C4 is this *small, fixed* set of abstractions — do not
add levels, and do not map org constructs onto them.

## Definitions and litmus tests

### Person
Humans: actors, roles, personas, named individuals who use the system.
**Litmus:** human (or role) → person. A *software* consumer is a software system, not a person.

### Software System
The highest level: something that delivers value to its users, human or not.

**Primary litmus — ownership:** something a single team builds, owns, has responsibility
for, and can see the internal implementation details of. Usually one source repository;
the system boundary tends to match a team boundary.

**Deployment litmus:** everything inside a software system is deployed together.

**Scope of a model:** your system, plus the systems it depends on (or that depend on it).
Systems you don't own are *external*: a closed box you never open up — never give an
external system containers.

**NOT a software system:** product domains, bounded contexts, business capabilities,
squads/tribes. Those are organizational constructs, not deployable software.

### Container
An application or a data store. **The litmus test: something that needs to be *running*
for the overall system to work, or that *stores data*.**

It is a *runtime* construct — NOT (necessarily) a Docker container, and deployment
topology is a separate concern (three webapps on one Tomcat in dev, one each in prod:
still three containers; replicas/instances belong in deployment views).

Canonical container examples:
- Server-side web application (Spring, ASP.NET, Rails, Node.js)
- Client-side SPA running in the browser — a *separate* container from the API serving it
- Desktop application; mobile app (each its own container)
- Standalone console/batch/worker process; a cron job; a single shell script
- A single serverless function (Lambda, Azure Function)
- Database or schema (PostgreSQL, MongoDB, …) — yes, a database IS a container
- Blob/content store (S3, Azure Blob), CDN, file system (SAN/NAS)
- A queue or topic (see below)

**NOT a container:** JARs, DLLs, assemblies, packages, namespaces, folders, libraries —
those are packaging units.

### Component
A grouping of related functionality encapsulated behind a well-defined interface,
**running in the same process** as the rest of its container.

**Litmus:** NOT separately deployable — the container is the deployable unit. If it can be
started/deployed on its own, it's a container, not a component.

Language mapping: OOP → classes+interfaces behind a facade; JS → a module; functional → a
module of related functions; C → related files in a directory.

### Code element
Classes, interfaces, functions, etc. **Optional level — skip it** except for the most
important/complex components, and prefer IDE auto-generation over hand-maintained diagrams.

## Tricky cases

| Case | Resolution |
|---|---|
| Database | Container (data store) — even when managed/hosted elsewhere (RDS, Atlas). |
| SPA + API | Two containers: the SPA runs in the browser, the API on the server. |
| Mobile app | Its own container. |
| Serverless function | A container. Many functions → many containers (group them if noisy). |
| Worker / batch job / cron | A container — it runs. |
| Microservice | Ownership decides (see below). |
| Queue / topic | A container per queue/topic — **not** the broker as one big box. Alternative: skip the box, put "via X queue" on the relationship. Modelling queues as containers keeps them independent of deployment topology. |
| Message broker | Don't model the broker itself as a container on container views; the queues/topics are the architecturally interesting parts. The broker appears in *deployment* views as a deployment/infrastructure node. |
| Shared library | Not a container, not a component — code shared across components. Refactor into a component if it truly owns functionality. |
| CDN / blob store | Container (data store). |
| Third-party SaaS | External software system (closed box). |
| API gateway / load balancer / firewall | Deployment concept: `infrastructureNode` in a deployment environment; never on a container view. (Exception: a gateway you *built*, that does real business logic, may be a container.) |
| Bounded context / domain / squad | Not a C4 abstraction. Use `group` for visual grouping if helpful. |

### Microservices — system or container?

Depends on ownership:

- **One team owns the services** → each microservice is a *group of containers* inside one
  software system — typically an API container + its database-schema container, wrapped in
  a `group "Service name"`.
- **Separate teams own them** → promote each service to its own software system; each team
  models its internals in its own workspace and sees its neighbours as external systems.

## The question bank

Ask only the questions that decide an actual open point — 2 to 4 at a time, never the
whole list. Prefer questions the repo can't answer (ownership, intent, team boundaries).

**System boundary (system vs external system):**
1. Does a single team (yours?) build and own this, with access to its code?
2. Is it deployed together with the rest, or independently by someone else?
3. Do you own it, or do you only consume it (another team / third party)?
4. Is this actually a team/domain/capability name rather than running software?

**Container vs component:**
5. Does it need to be running as its own process for the system to work?
6. Is it deployed/started/scaled independently?
7. Or does it execute inside another application's process (→ component)?
8. Is it just a package/library (→ neither)?

**Data:**
9. Which databases/schemas, caches, blob stores, file systems are involved? Who reads and
   who writes each one?

**Messaging:**
10. Do parts communicate through queues/topics? Which ones matter enough to draw as boxes
    vs a "via" label? Point-to-point or pub/sub?

**Deployment (for deployment views):**
11. What environments exist, and what runs where (cloud provider, orchestrator, replicas,
    managed services, gateways/load balancers)?

**Flows (for dynamic views):**
12. Which use case should the diagram tell, step by step, using the relationships we
    already modelled?

## FAQ essentials

- **Can terminology change?** Yes — adapt names to the org's vocabulary, as long as
  everybody explicitly understands it (e.g. "module" instead of "component").
- **Can we add abstraction levels?** Generally no. Requests for extra levels usually mean
  an existing abstraction is being misapplied, or an organizational construct is being
  forced into the model. Treat adding levels as an advanced manoeuvre.
- **"Is a database a container or component?"-type confusion** is a terminology-precision
  problem: pin down what the thing *is* (runs? stores? deploys alone?) before classifying.

---
*Derived from the C4 model by Simon Brown ([c4model.com](https://c4model.com)),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); condensed and adapted.*
