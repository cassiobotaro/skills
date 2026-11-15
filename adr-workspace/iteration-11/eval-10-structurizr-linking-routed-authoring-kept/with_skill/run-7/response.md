I recorded the decision as an ADR. I did not touch the Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`. It has status Accepted and today's date, 2026-11-15, and continues your existing log after 0003.
- **Context:** the gateway cannot see account ids, so it cannot limit per account.
- **Decision:** we will rate-limit login attempts per account inside the session service, at 5 per 15 minutes, instead of at the gateway.
- **Consequences:** per-account limiting becomes possible. The trade-off you named is that the session service now keeps rate-limit counters in Redis.

I wrote only the reasons you gave, with no extra rationale or alternatives. If you want other alternatives or consequences in the record, tell me and I'll add them. Because the Redis counters tie into ADR 2, you could also add that Redis is already a hard dependency of the login path. I left that out because you didn't say it.

**Not done, the Structurizr part:** showing the ADRs in your workspace means adding an `!adrs` directive to a `workspace.dsl`. That is the `structurizr` skill's job, not this one's, and this repository has no `workspace.dsl` yet. The files are in the adr-tools format that `!adrs doc/adr` imports as they are. Ask for the Structurizr step next and it can add the directive to your workspace, or create a workspace if you don't have one.
