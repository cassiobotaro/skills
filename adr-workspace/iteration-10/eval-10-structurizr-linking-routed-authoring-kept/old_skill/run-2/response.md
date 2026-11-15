I wrote the ADR. I did not touch your Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Status: Accepted. Date: 2026-11-15.
- Decision: rate-limit login attempts per account (5 per 15 minutes) inside the session service, not at the API gateway.
- Context: the gateway cannot see account ids.
- Consequences: the limit is per account, and the service now keeps rate-limit counters in Redis.

I used your existing log in `doc/adr/` and continued after 0003. I did not edit any existing ADR. ADR 0002 already makes Redis a dependency of the login path, but I did not link or amend it, because this decision does not change that one.

**Structurizr:** showing the ADRs in the workspace means adding an `!adrs doc/adr` directive to `workspace.dsl`. That belongs to the `structurizr` skill, not the ADR skill, so I did not write it here. The files in `doc/adr/` are in the format that `!adrs` imports, so that step needs no changes to the ADRs. There is no `workspace.dsl` in this repository, so ask for that step separately.
