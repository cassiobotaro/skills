I recorded the decision as an ADR. I did not touch the Structurizr workspace.

**Created**
- `doc/adr/0004-rate-limit-login-attempts-in-the-session-service.md`. It has status Accepted and today's date, 2026-11-15. It follows the format of your existing ADRs 0001-0003, and the rationale and trade-off are the ones you gave me. It is the only file I changed.

**Structurizr**
- Authoring or editing your Structurizr workspace is outside what I do here, and there is no `workspace.dsl` in this repository for me to edit. I did not invent one.
- The ADRs already use the plain adr-tools format, so Structurizr's `!adrs` importer can read them as they are (`!adrs doc/adr`, see https://docs.structurizr.com/server/decisions). The `!adrs` line itself has to go in your workspace DSL. The Structurizr tooling is the right place to add it.
