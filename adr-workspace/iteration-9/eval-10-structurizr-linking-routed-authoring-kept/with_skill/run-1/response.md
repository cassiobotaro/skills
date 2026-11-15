I recorded the rate-limiting decision as an ADR, but I did not touch the Structurizr workspace.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md` has status Accepted and today's date, 2026-11-15. It follows the existing log (ADR 3 was the last one, in `doc/adr/`). It records the decision (5 attempts per 15 minutes per account, in the session service rather than the gateway), the reason (the gateway cannot see account ids) and the trade-off you accepted (rate-limit counters now live in Redis).

I took everything in the ADR from your message and the existing ADRs. I added no alternatives or metrics. The only addition is a pointer to ADR 2, since Redis already holds sessions. I linked it in the prose, not as Amends or Supersedes, because ADR 2 still stands unchanged. If you know of other consequences, such as behavior when Redis is down or the counter expiry mechanism, tell me and I'll add them.

**Structurizr**
Showing the ADRs in your Structurizr workspace means adding an `!adrs` directive to `workspace.dsl`. That is the `structurizr` skill's job, not this one's, and I didn't write or edit a workspace file. This repository has no `workspace.dsl` yet. When you run the `structurizr` skill, point it at `doc/adr`. The ADR files are already in the format its importer expects.
