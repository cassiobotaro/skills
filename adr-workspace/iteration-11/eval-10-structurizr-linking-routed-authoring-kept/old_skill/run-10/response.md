I wrote the ADR. I did not wire the ADRs into your Structurizr workspace.

**ADR created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`

- It is dated 2026-11-15 and has status Accepted.
- Context: the gateway cannot see account ids, so it cannot rate-limit per account.
- Decision: the session service enforces 5 login attempts per account per 15 minutes.
- Consequences: the limit works per account, and the service now keeps rate-limit counters in Redis. I noted that Redis is already a dependency for sessions (ADR 2). I added nothing beyond what you told me.
- I left ADRs 1 to 3 untouched.

**Structurizr linking:** this skill does not edit `workspace.dsl`. That is the `structurizr` skill's job, and I could not run it here. It imports the log with an `!adrs` directive pointing at `doc/adr`. The files already use the format that importer parses, so the new ADR needs no changes. Ask for the Structurizr step in a follow-up, or run that skill, to add the directive.
