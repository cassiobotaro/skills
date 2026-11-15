I wrote the ADR, but I did not touch the Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`

- It is ADR 4, status Accepted, dated 2026-11-15, and follows the format of your existing ADRs 1-3.
- Context: the gateway cannot see account ids, so it cannot enforce a per-account limit.
- Decision: the session service limits login attempts to 5 per 15 minutes per account and keeps the counters in Redis.
- Consequences: the per-account limit is now possible, and the service now keeps rate-limit counters in Redis. The ADR does not list any other consequences, because you didn't give me any.
- It supersedes and amends nothing. ADR 2 (sessions in Redis) is related, but this decision doesn't replace it, so I left it unchanged.

**Structurizr:** showing the ADRs in the workspace means adding an `!adrs` directive to your `workspace.dsl`. That is the `structurizr` skill's work, not this one's, so I didn't start it here. The ADR files are in the plain adr-tools format that `!adrs doc/adr` imports as they are. I found no `workspace.dsl` in this repository, so I can't tell whether you want a new workspace or an edit to an existing one. Ask me to do the Structurizr step next, and tell me where the workspace lives.
