I recorded the decision as ADR 4, but I did not touch the Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Status is Accepted and the date is 2026-11-15. It follows ADRs 1–3 in `doc/adr/`.
- Context: the gateway cannot see account ids, so it cannot limit per account.
- Decision: the session service enforces 5 login attempts per 15 minutes per account.
- Consequences: per-account limiting becomes possible. The cost is that the service now keeps rate-limit counters in Redis. I wrote only what you told me and did not invent any other alternatives or metrics.

**Not done: showing the ADRs in Structurizr.** Adding `!adrs` to a `workspace.dsl` is the `structurizr` skill's job, not the ADR skill's. This repository also has no `workspace.dsl` yet. The ADR files are already in the format Structurizr's `!adrs doc/adr` importer reads, so nothing in them needs to change. Ask for the Structurizr step in a follow-up so that skill can create or edit the workspace and wire the directive in.
