I recorded the decision as ADR 4 and did not touch the Structurizr workspace. Details on both below.

**ADR created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`, status Accepted, dated 2026-11-15.
- It records that the per-account limit (5 per 15 minutes) lives in the session service because the gateway cannot see account ids. The accepted trade-off is that the service now keeps rate-limit counters in Redis.
- It follows your existing log's format. I added no forces or alternatives beyond what you told me. I linked the Redis consequence to ADR 2 only as a pointer, not as a supersede or amend.

**Structurizr**
- This skill only writes and maintains the ADR files. It does not edit `workspace.dsl`, so I made no workspace changes.
- No workspace exists in this repository. Your ADRs are in plain adr-tools format in `doc/adr`, which Structurizr's `!adrs` importer reads unchanged, so the workspace can point at that directory (`!adrs doc/adr`). Authoring or editing the workspace is a separate task for the Structurizr tooling. I can do that next if you want.
