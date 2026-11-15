I recorded the decision as an ADR. I did not touch the Structurizr workspace, because that part belongs to the `structurizr` skill.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`

- Status: Accepted, dated 2026-11-15. It follows the numbering of your existing log (0001 to 0003) and uses the same format.
- Decision: rate-limit login attempts per account (5 per 15 minutes) inside the session service, not at the API gateway.
- Context: only the reason you gave. The gateway cannot see account ids.
- Consequences: the limit can be keyed by account id. The accepted trade-off is that the service now keeps rate-limit counters in Redis. That adds state and load to the Redis instance it already depends on.

I did not add alternatives, metrics or other reasons you didn't give me.

**Structurizr:** showing the ADRs in your workspace means adding an `!adrs` directive to `workspace.dsl`. This skill only writes the ADR files, and the `structurizr` skill handles the workspace. There is no `workspace.dsl` in this repository, so I made no change there. The ADRs are in standard adr-tools format in `doc/adr`, so `!adrs` can import that directory as it is. Ask for the workspace change in a separate request so the `structurizr` skill picks it up. If your workspace is in another repository, tell me where it lives.
