I recorded the decision as ADR 4, but I did not touch your Structurizr workspace.

**Created:** `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`

- Status is `Accepted`, dated 2026-11-15.
- Context gives the 5-per-15-minutes per-account requirement and the reason the gateway can't enforce it (it can't see account ids).
- Decision says we will enforce the limit in the session service, not at the gateway.
- Consequences records the gain (the limit can be keyed by account id) and the trade-off you accepted (the service now keeps rate-limit counters in Redis).
- I added nothing beyond what you told me. I didn't list alternatives or motives you didn't mention. If you want to record other options you considered, tell me and I'll add them in a new draft.

No existing ADRs were edited. ADR 2 (sessions in Redis) is related but not superseded, so I left it as it is.

**Structurizr:** showing the ADRs in your workspace means adding an `!adrs doc/adr` directive to your `workspace.dsl`. That is the `structurizr` skill's job, not the ADR skill's, so I didn't write it here. The ADR files use the exact adr-tools layout that `!adrs` imports unchanged. Ask the `structurizr` skill to link `doc/adr` into the workspace, either at the workspace level or on the session service's container.
