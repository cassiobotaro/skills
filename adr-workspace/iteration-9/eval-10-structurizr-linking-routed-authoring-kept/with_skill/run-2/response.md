I recorded the rate-limiting decision as an ADR, and left the Structurizr part undone. That part belongs to the `structurizr` skill.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Status: Accepted. Date: 2026-11-15. It follows the existing log (0001 to 0003) and its adr-tools format.
- Context: the gateway cannot see account ids, so it cannot limit per account.
- Decision: limit login attempts per account inside the session service, 5 per 15 minutes, instead of at the gateway.
- Consequences: per-account limiting is now possible. The cost is that the service keeps rate-limit counters in Redis. That adds load and state to a store that ADR 2 already made a hard dependency of the login path.

I wrote only what you told me. I did not add alternatives or metrics you did not mention. I did not touch ADRs 1 to 3.

**Structurizr:** I did not edit a `workspace.dsl`, because adding `!adrs` to a workspace is the `structurizr` skill's job. The log is in standard adr-tools format, so Structurizr's `!adrs doc/adr` can import it as is. To wire it in, ask for that through the `structurizr` skill, or tell me if it is not installed and you want the directive written by hand. No `workspace.dsl` exists in this repository yet.
