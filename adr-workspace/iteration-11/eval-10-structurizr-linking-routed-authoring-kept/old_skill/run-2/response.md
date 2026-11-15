I recorded the decision as an ADR. I did not touch the Structurizr workspace.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`. It has status Accepted and today's date, 2026-11-15. The context is that the gateway cannot see account ids. The decision is the per-account limit of 5 attempts per 15 minutes, enforced in the session service. The consequences are the per-account limit becoming possible and the Redis-held counters you accepted as the trade-off. I added nothing beyond what you told me.

**Structurizr**
Showing the ADRs in your workspace means adding an `!adrs doc/adr` directive to `workspace.dsl`. That is the `structurizr` skill's job, not this skill's, so I left it alone. The ADR files are in the standard adr-tools format, so that directive can import them as they are. There is no `workspace.dsl` in this directory, so I would need the workspace to make that change. Ask for it again with the `structurizr` skill and it will wire the directive in.
