I recorded the decision as ADR 4, but I did not touch a Structurizr workspace. That part is for the `structurizr` skill.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`

The status is Accepted and the date is 2026-11-15. It follows ADRs 1-3, which were already in `doc/adr/`.
- **Context:** the per-account limit is 5 attempts per 15 minutes, and the gateway cannot see account ids.
- **Decision:** the session service enforces the limit instead of the gateway.
- **Consequences:** the limit can be keyed on account id. The trade-off you named is that the service now keeps rate-limit counters in Redis. I added nothing beyond what you told me.

**Structurizr:** showing the ADRs in your workspace means adding an `!adrs` directive to `workspace.dsl`. I left that edit to the `structurizr` skill, and this repository has no `workspace.dsl` yet. The ADR files are in the standard adr-tools format, so that directive can import `doc/adr` as it is. I can do that part in a follow-up request.
