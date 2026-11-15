I recorded the rate-limiting decision as ADR 4. I did not touch the Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`. Its status is Accepted and it is dated 2026-11-15. It follows the existing log: 0003 was the highest number, and the English Nygard format matches ADRs 1 to 3.

- **Decision:** limit login attempts per account to 5 per 15 minutes inside the session service, not at the API gateway.
- **Context:** the gateway cannot see account ids. That was the only reason you gave, so I added nothing else.
- **Consequences:** the limit can be per account. The service now keeps rate-limit counters in Redis, which is the trade-off you accepted.

I did not link this to ADR 2 ("Store sessions in Redis") or amend it. This decision adds a new use of Redis and does not change that one. Tell me if you want an Amends link.

**Making ADRs show up in Structurizr:** this is a separate job. It means adding `!adrs doc/adr` to a `workspace.dsl`, which belongs to the `structurizr` skill. There is no `workspace.dsl` in this repository, so I didn't create one. The ADR files are in the plain adr-tools format that `!adrs` imports as they are. Ask me to do that step with the structurizr skill, or tell me where your workspace lives.
