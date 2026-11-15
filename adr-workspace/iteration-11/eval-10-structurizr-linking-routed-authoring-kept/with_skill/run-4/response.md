I recorded the decision as ADR 4. I did not touch your Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`
- Status: Accepted. Date: 2026-11-15.
- Context: the 5-per-15-minutes per-account requirement, and the gateway's inability to see account ids.
- Decision: enforce the limit inside the session service instead of at the gateway.
- Consequences: the limit can be keyed by account id. The trade-off you named is that the session service now keeps rate-limit counters in Redis. I added nothing beyond what you told me.

I changed no existing ADR (0001 to 0003).

**Structurizr:** showing the ADRs in your workspace means adding an `!adrs` directive to `workspace.dsl`. That is the `structurizr` skill's job, not this one's, so I left it alone. The log is in standard adr-tools format, so `!adrs` can import `doc/adr` unchanged. Ask the `structurizr` skill to link `doc/adr` into the workspace, and it can also validate the result.
