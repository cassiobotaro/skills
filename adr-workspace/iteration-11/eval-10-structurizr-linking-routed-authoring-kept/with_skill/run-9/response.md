I recorded the decision as ADR 4. I did not wire the ADRs into Structurizr.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`

- It has status `Accepted` and today's date, 2026-11-15.
- Context: you need a per-account limit of 5 attempts per 15 minutes, and the gateway cannot see account ids.
- Decision: the session service enforces the limit, not the gateway.
- Consequences: the limit is now per account, and the service keeps rate-limit counters in Redis.
- I added nothing beyond what you told me. The log has no existing ADR on rate limiting, so nothing is superseded or amended, and I did not touch the other ADRs.

**Structurizr:** showing the ADRs in your workspace means adding an `!adrs` directive to a `workspace.dsl`, which is the `structurizr` skill's work, not this one's. There is no `workspace.dsl` in this repository, so I did not create one.

- The log is already in the format `!adrs` imports, so no change to the ADR files is needed.
- When you add the directive, point it at the log directory: `!adrs doc/adr`. Place it in the workspace or in the software system the session service belongs to.
- Ask for that as a separate step with the `structurizr` skill. It will also need to know your existing workspace or system names.
