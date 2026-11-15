I recorded the rate-limiting decision as an ADR. I did not wire the ADRs into Structurizr.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Title: "4. Rate-limit login attempts in the session service", status Accepted, dated 2026-11-15.
- Context: the limit is 5 attempts per 15 minutes per account, and the gateway cannot see account ids.
- Decision: enforce the limit inside the session service rather than at the gateway.
- Consequences: the limit works per account, and the service now keeps rate-limit counters in Redis. That is the trade-off you accepted.

I added no other ADRs and changed no existing ones. I did not state any alternatives beyond the gateway, since you didn't give me any.

**Structurizr:** I did not touch this. Showing the ADRs in your workspace means adding an `!adrs` directive to `workspace.dsl`. That is the `structurizr` skill's job, and this repository has no `workspace.dsl` yet. The log in `doc/adr` is in the plain adr-tools format that `!adrs doc/adr` imports as it is. Ask for the Structurizr wiring as a separate step, using the `structurizr` skill, and it can add the directive and validate the workspace.
