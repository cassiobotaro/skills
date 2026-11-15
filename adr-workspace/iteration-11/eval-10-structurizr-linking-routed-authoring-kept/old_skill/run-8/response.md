I recorded the decision as ADR 4: `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`. It has status Accepted and today's date, 2026-11-15. It follows the format of the existing log (ADRs 1-3, in `doc/adr/`).

- **Context:** the gateway cannot see account ids, so it cannot limit per account.
- **Decision:** the limit of 5 attempts per 15 minutes is enforced inside the session service, not at the gateway.
- **Consequences:** the per-account limit becomes possible. The trade-off you accepted is that the service now keeps rate-limit counters in Redis. I wrote only the reasons and trade-off you gave me and added nothing else.

I did not make the ADRs show up in your Structurizr workspace. There is no `workspace.dsl` in this repository, and that wiring (the `!adrs` directive) is the `structurizr` skill's job, not this one's. The log is already in the format `!adrs doc/adr` imports, so that step can use the directory as it is. Ask for it with the `structurizr` skill, which needs to create or edit the workspace file.
