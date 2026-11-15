I recorded the rate-limiting decision as an ADR. I did not wire the ADRs into Structurizr, because that part is the `structurizr` skill's work.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`. It is Accepted and dated 2026-11-15.
  - **Context:** the gateway cannot see account ids.
  - **Decision:** limit login attempts per account inside the session service, at 5 per 15 minutes.
  - **Consequences:** the per-account limit now works, and the service keeps rate-limit counters in Redis.

I only used what you told me. If you also weighed other options, or want more consequences listed, such as the counters' failure behavior when Redis is down, tell me and I'll add them.

**Structurizr**
This repo has no `workspace.dsl`, so there is nothing to wire into yet. Showing the log in your C4 documentation means adding an `!adrs doc/adr` directive to the workspace. That is the `structurizr` skill's job, so ask it to link the existing ADRs. The files in `doc/adr/` are already in the format its importer reads.
