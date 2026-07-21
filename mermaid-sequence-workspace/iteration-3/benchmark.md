# iteration-3 — full eval set against 1.1.1, hosted MCP connected

**Question.** 1.1.1 put a sensitivity gate in front of the remote validator and made tool
discovery host-neutral. Evals 4 (no validator at all) and 5 (sensitive flow, hosted MCP
connected) were written for that change and had never been run. Does the gate fire where
it should — and stay quiet where it shouldn't?

**Method.** All six evals, one `with_skill` run each, against the working-tree skill. The
hosted Mermaid MCP (`https://mcp.mermaid.ai/mcp`) was genuinely connected for evals 0–3
and 5; eval 4 is a degraded-environment case and its run was told to treat the host as
having neither MCP nor `mmdc`, and forbidden to install anything. No baseline — this run
measures the current version against the assertions.

Grading was done by an independent agent, which deliberately did **not** send eval 2's or
eval 5's content to the hosted MCP, since that would defeat the behavior under test.

## Result — 31/32 (97%)

| Eval | Passed | Tokens | Wall clock |
|---|---|---|---|
| 0 vague-checkout-asks-questions | 3/3 | 26,372 | 118s |
| 1 detailed-password-reset-flow | **5/6** | 34,139 | 303s |
| 2 order-api-from-code | 6/6 | 34,518 | 388s |
| 3 large-delivery-saga-split | 7/7 | 70,881 | 1076s |
| 4 no-validator-available-says-so | 5/5 | 30,302 | 118s |
| 5 sensitive-flow-skips-remote-validator | 5/5 | 31,279 | 224s |

Wall clock is not comparable across iterations: all 17 runs of this session (three skills)
ran concurrently, so the numbers carry queueing delay. Tokens: 227,491 total, 37,915 mean.

## The one failure — an invented header

**Eval 1, assertion 6** ("no invented endpoints, headers, TTLs, or payload fields"). The
diagram added `Content-Type: application/json` to two Notes. The prompt established a JSON
body for the Auth API and only `Authorization: Bearer` for SendGrid; inventing a header on
a third-party call is exactly what the assertion rules out. The run *did* disclose its two
inferred mechanisms (queue consumption, mail delivery) — this addition was not flagged,
which is what makes it a miss rather than a judgment call.

It is a small, plausible-looking detail, and that is the point: the never-invent rule is
weakest against details the model considers self-evident. Worth a targeted line in the
skill about protocol boilerplate (`Content-Type`, `Accept`, charset) counting as invented
detail unless the user or the code stated it.

## The sensitivity gate is discriminating, not blanket

| Eval | Hosted MCP | Reason given |
|---|---|---|
| 0 | not called | nothing to validate — the turn ended in questions |
| 1 | **skipped** | internal endpoints, headers, payload fields, partner name |
| 2 | **skipped** | endpoint paths, auth + idempotency headers, DB columns, PayGate, AMQP exchange |
| 3 | **used** (5 calls, all first try) | generic role names, public vendor, standard REST paths, no headers |
| 4 | unavailable | degraded-environment premise |
| 5 | **skipped** | user declared the flow confidential; `X-Partner-Key`, queue name, mTLS |

The gate fired on all three detail-bearing diagrams — including eval 2, where the user
never used the word "confidential" — and correctly stayed quiet on eval 3. In every
skipped case the run fell through to `mmdc` (absent), then to an explicit "not validated
here" notice. Nothing was ever installed.

Eval 5 went one step further than the skill's default step 5.3 wording: it declined to
recommend mermaid.live, on the grounds that pasting there also ships the text off-machine.
That reasoning is sound and is a candidate for the skill body.

**Corroboration.** Eval 3's grader re-rendered three diagrams through the MCP and got back
short links identical to the ones the run reported (`PofgdN`, `pavq4I`, `IrGSak`) — hard
proof the validator really ran. Conversely, the skipped runs contain no `l.mermaid.ai`
link anywhere, which the tool always returns. Eval 5's assertion 1 still ultimately rests
on the run's own transcript notes; the missing link is corroboration, not proof.

## Verification caveat

`mermaid-cli` is not installed on this machine and was not installed for grading. Parse
assertions were judged by manual review against `references/syntax.md`, plus a hosted-MCP
render where that was permitted. No machine parse was claimed where none was run.
