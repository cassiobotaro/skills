I recorded the rate-limiting decision as an ADR. I did not touch the Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Status is Accepted, dated 2026-11-15, and it follows the format of ADRs 0001-0003.
- Context: the gateway cannot see account ids, so it cannot count attempts per account.
- Decision: limit login attempts per account to 5 per 15 minutes inside the session service, not at the gateway.
- Consequences: per-account limiting becomes possible. The trade-off you accepted is that the session service now keeps rate-limit counters in Redis, so it holds more state and depends on Redis for this check as well as for sessions.
- I added nothing beyond what you told me. I listed no alternatives other than the gateway, and no figures.

**Structurizr:** showing ADRs in the workspace means adding an `!adrs` directive to `workspace.dsl`. That is the `structurizr` skill's job, not this one's. This repository has no `workspace.dsl`, so I did not create one. The ADR files use the exact adr-tools format, so `!adrs doc/adr` can import them as they are, including the new one. To get that wiring, ask for the Structurizr step on its own, using the `structurizr` skill if you have it installed.
