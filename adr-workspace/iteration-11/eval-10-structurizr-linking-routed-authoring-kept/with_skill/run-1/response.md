I wrote the ADR, but I did not touch the Structurizr workspace.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`. Status is Accepted, dated 2026-11-15. It is numbered 4 because the log already had 0001 to 0003.
  - **Context:** the gateway cannot see account ids, so it cannot apply a per-account limit.
  - **Decision:** rate-limit login attempts per account inside the session service, at 5 per 15 minutes, instead of at the gateway.
  - **Consequences:** the per-account limit becomes possible. The trade-off you accepted is that the service now keeps rate-limit counters in Redis.

I used only the reasons and trade-off you gave me. If you also considered other alternatives, or want to note that this adds to the Redis dependency from ADR 2, tell me. A new ADR would be the place to record that, since I don't edit accepted ADRs.

**Structurizr**
Showing the ADRs in your workspace means adding an `!adrs` directive to your `workspace.dsl`. That is the `structurizr` skill's job, not this one's, and there is no workspace file in this repository for me to edit. The ADR files are in standard adr-tools format, so `!adrs doc/adr` will import them unchanged. Ask the `structurizr` skill to add it, which also covers validating the workspace. Or point me at the `workspace.dsl` once it exists.
