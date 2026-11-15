I wrote the ADR, but I did not wire the log into your Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Status: Accepted. Date: 2026-11-15.
- Context: the gateway cannot see account ids, so it cannot limit per account.
- Decision: rate-limit login attempts per account (5 per 15 minutes) inside the session service, not at the gateway.
- Consequences: the limit is enforced per account. The trade-off you accepted is that the session service now keeps rate-limit counters in Redis.

I did not edit ADRs 0001-0003. Nothing supersedes them.

**Structurizr:** showing the ADRs in the C4 documentation means adding an `!adrs` directive to your `workspace.dsl`. That is the `structurizr` skill's job, not this one's, so I left the workspace alone. The files are in plain adr-tools format, so `!adrs doc/adr` can import them as they are. Ask for the Structurizr step next, or invoke that skill.
