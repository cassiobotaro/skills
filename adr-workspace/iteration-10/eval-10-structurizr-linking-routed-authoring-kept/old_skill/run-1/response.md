I recorded the decision as ADR 4 and did not touch the Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md` (status Accepted, dated 2026-11-15). It follows the existing log's format and numbering (the log already had 0001-0003). It records:
- the decision: 5 login attempts per account per 15 minutes, enforced in the session service instead of at the API gateway
- the reason: the gateway cannot see account ids
- the accepted trade-off: the service now keeps rate-limit counters in Redis

I added nothing beyond what you told me. No existing ADR was edited, because this decision does not supersede or amend any of them.

**Not done: showing the ADRs in your Structurizr workspace.** I did not do this. Wiring `!adrs` into a `workspace.dsl` is the `structurizr` skill's job, not this skill's. There is also no `workspace.dsl` in this repository, so there was nothing to edit. The ADR files are in standard adr-tools format, so the `!adrs doc/adr` directive can import them as they are. To get that done, ask for it again with the `structurizr` skill, or share the workspace file.
