# iteration-8 — 1.5.0 (patterns + cookbook) against the four pattern evals

**Question.** Does adding the official-pattern and cookbook guidance close the iteration-7 misses
without disturbing what already worked? `with_skill` = `../skill-snapshot-1.5.0`; `old_skill` =
the iteration-7 runs of the same prompts against 1.4.0, copied in as the baseline (same eval
assertions, with eval 7's ownership assertion relaxed to accept "asked before deciding").

**What changed in 1.5.0.** Hardware/devices as a custom `element` archetype (classification row,
`modeling-patterns.md` §5, SKILL.md bullet); Lambda + LocalStack, EKS layering, App Runner,
simplified Docker/K8s variants, `properties { "Image URI" }`, infrastructure-node ellipse style
(`deployment-patterns.md`); cookbook gotchas — single implied relationship per pair,
`deploymentGroup` on a node, `containerInstance` with an identifier, filtered views hiding the base
view, image-view renderer properties, cross-system container-view expressions, `title` on dynamic
views, DSL-and-code. Three corrections surfaced by validating the new snippets in Docker: an
instance identifier needs the full bound-ancestor path; **filtered views require the base view to
have no `autoLayout`** (the shipped text said the opposite); and a custom element's second
positional argument is *metadata*, so archetype instances set `description` in the block.

## Result — 23/24 (96%) vs 21/24 (88%); tokens +1.7k mean (in the noise)

| Eval | 1.4.0 | 1.5.0 | What moved |
|---|---|---|---|
| 6 EKS + ALB + WAF | 5/6 | 6/6 | AWS → EKS → cluster → pod (×3) → Docker container → API: the collapsed layer is back |
| 7 Lambda + LocalStack | 5/6 | 5/6 | Flutter app still an external system, listed as an open point but not asked first |
| 8 factory cameras + robots | 5/6 | 6/6 | `hardwareSystem = element { metadata … tags "Hardware" }` archetype, robot shape; agent verified the metadata slot via JSON export |
| 9 microservices + BFF | 6/6 | 6/6 | Left BFF→services protocol as a question instead of assuming JSON/HTTP |

Every run re-validated clean under the grader's own `structurizr/structurizr validate`.
`benchmark.md` lists Old Skill first, so its Delta column is (old − new): read the signs inverted.

**Open.** Eval 7's ownership call is one sample per version; a per-query claim needs n ≥ 10
(see CLAUDE.md). The new classification row says "ask, don't default to external" — it did not
change this one run. Not worth a rewrite on n=1.
