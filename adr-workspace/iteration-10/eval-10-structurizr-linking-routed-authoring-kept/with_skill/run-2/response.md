I wrote the ADR, but I did not touch the Structurizr workspace.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`, status Accepted, dated 2026-11-15. It follows ADRs 0001-0003 in `doc/adr/`.
  - Context: the gateway cannot see account ids.
  - Decision: limit login attempts per account (5 per 15 minutes) inside the session service instead of at the API gateway.
  - Consequences: the limit is enforced per account, and the service now keeps rate-limit counters in Redis.

I used only what you told me. The Consequences section has one real trade-off, the Redis counters. If you accepted other costs, such as behavior when Redis is down or lockout side effects, tell me and I'll add them. ADR 0004 doesn't supersede or amend any earlier ADR, so I left the other files alone.

**Structurizr:** showing the ADRs in your workspace means adding an `!adrs` directive to `workspace.dsl`. That is the structurizr skill's job, not this skill's, and there is no `workspace.dsl` in this repository yet. The files are in standard adr-tools format, so `!adrs doc/adr` will import them unchanged. Ask for that as a separate step, or run the structurizr skill, and it will author or edit the workspace and link the log.
