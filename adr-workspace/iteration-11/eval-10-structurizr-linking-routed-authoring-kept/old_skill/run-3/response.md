I recorded the decision as an ADR and did not touch the Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Status: Accepted. Date: 2026-11-15.
- Context: the gateway cannot see account ids, so it cannot limit per account.
- Decision: limit login attempts per account inside the session service, at 5 per 15 minutes, with counters in Redis.
- Consequences: limits now work per account. The trade-off you named is that the session service keeps rate-limit counters in Redis.
- No existing ADR was edited. ADR 2 (sessions in Redis) is related, but this decision doesn't replace or change it.

**Structurizr:** I didn't wire the ADRs into your workspace. That is the `structurizr` skill's job, and this repository has no `workspace.dsl` yet. The ADR files are in standard adr-tools format, so Structurizr's `!adrs` directive can import `doc/adr` without changes. Ask for that step and the `structurizr` skill will add the directive to the workspace.
