# iteration-7 — do 1.4.0 follow the official DSL patterns? (baseline for 1.5.0)

**Question.** `docs.structurizr.com/dsl/patterns/` lists 11 patterns (API gateway, load balancer,
firewall, Docker, Kubernetes, AWS EKS/Fargate/App Runner/Lambda, microservice, hardware system).
Four new evals (6–9 in `evals/evals.json`) exercise all of them except App Runner, against the
1.4.0 skill (`../skill-snapshot-1.4.0`, Docker-only validation). Static check first: a workspace
stitched from every DSL snippet in `references/` validates clean.

**Method.** One `with_skill` run per eval, foreground subagents, project root = the run's
`outputs/`. Grader re-ran `structurizr/structurizr validate` on every generated file (all exit 0).
Grading in `eval-*/with_skill/grading.json`; `run-1/` mirrors it for `aggregate_benchmark`.

## Result — 21/24 (88%), mean 65k tokens

| Eval | Passed | Miss |
|---|---|---|
| 6 EKS + ALB + WAF | 5/6 | EKS and the cluster merged into one node, Docker-container layer skipped (official: AWS → EKS → cluster → pod → container) |
| 7 Lambda + LocalStack | 5/6 | Flutter app modeled as an external system, flagged as an assumption; ownership was ambiguous — the rule is to ask |
| 8 factory cameras + robots | 5/6 | Hardware modeled as external `softwareSystem` + tag; official pattern is a custom `element` archetype. The reply named that option and still chose wrong — the skill has no rule |
| 9 microservices + custom BFF | 6/6 | — |

What held in every run: gateway/LB/firewall as `infrastructureNode`, `-/>` rerouting (second reroute
reusing the hop), microservice = `group` of containers, Docker/K8s/Fargate only in the deployment
model, custom-built gateway with logic = container, nothing invented (open points asked).

**Decisions taken for 1.5.0.** Add hardware-system guidance (classification row + pattern), Lambda /
EKS / App Runner / simplified Docker-K8s shapes, and the cookbook gotchas; relax eval 7's ownership
assertion to accept "asked".
