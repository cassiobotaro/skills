I recorded the rate-limiting decision as an ADR. I did not touch the Structurizr workspace.

**ADR created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`, status Accepted, dated 2026-11-15. It follows ADRs 1 to 3 in your existing log.
- **Context:** the gateway cannot see account ids, so it cannot limit per account.
- **Decision:** the session service limits logins to 5 per 15 minutes per account and keeps the counters in Redis.
- **Consequences:** the limit now works per account. The cost is the trade-off you accepted: the service keeps rate-limit counters in Redis, which adds state and load on top of the sessions it already stores there (ADR 2).

I only used the reasons you gave and added no alternatives or numbers of my own. If you want the Redis counters to carry specific risks, such as behavior when Redis is down, tell me and I will add them.

**Structurizr:** I did not wire the ADRs into your workspace. That is the `structurizr` skill's job, not the ADR skill's. The ADRs are in standard adr-tools format, so a `!adrs doc/adr` directive in your `workspace.dsl` can import them as they are. Ask for that step separately, and the `structurizr` skill will make the edit and validate it.
