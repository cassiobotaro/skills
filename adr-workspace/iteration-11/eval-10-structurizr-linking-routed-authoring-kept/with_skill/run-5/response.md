I recorded the decision as an ADR, but I did not change your Structurizr workspace.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`, status Accepted, dated 2026-11-15.
  - Context: login attempts need a per-account limit, and the gateway cannot see account ids.
  - Decision: limit logins to 5 per 15 minutes per account inside the session service, not at the gateway.
  - Consequences: the limit is enforced per account, and the session service now keeps rate-limit counters in Redis.

I wrote only the reasons and the trade-off you gave me. I didn't add alternatives or motives you didn't mention. If you want the ADR to name rejected alternatives, tell me and I'll add them.

**Structurizr**
Showing the ADRs in your workspace means adding an `!adrs` directive to `workspace.dsl`. That is the structurizr skill's job, not the ADR skill's, so I left it alone. The ADR files use the adr-tools format that `!adrs doc/adr` imports unchanged, so the structurizr skill can wire it up from here. Ask for that as a follow-up, or invoke the structurizr skill directly.
