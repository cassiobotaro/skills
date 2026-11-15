I wrote the ADR, but I did not make the ADRs show up in your Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md` (Accepted, dated 2026-11-15). It follows 0003 and uses the same adr-tools format as the rest of your log.
- **Decision:** rate-limit login attempts per account (5 per 15 minutes) inside the session service, not at the API gateway.
- **Context:** the gateway cannot see account ids.
- **Consequences:** the limit is enforced per account. The trade-off you accepted is that the service now keeps rate-limit counters in Redis.

I didn't touch the existing ADRs. This decision doesn't replace or amend 0002 or 0003.

**Structurizr:** showing the log in the C4 documentation means adding an `!adrs` directive to a `workspace.dsl`, and that is the `structurizr` skill's job, not this one's. There is no `workspace.dsl` in this repository, so there was nothing to edit here. The ADR files are in the format the `!adrs` importer reads, so once the workspace is in place you can point it at `doc/adr`. Ask for that in a Structurizr request and it will wire up the import.

One thing I'd confirm: the ADR names Redis as the counter store, as you said. It doesn't say whether this is the same Redis instance that holds sessions (0002). I left that out because you didn't state it.
