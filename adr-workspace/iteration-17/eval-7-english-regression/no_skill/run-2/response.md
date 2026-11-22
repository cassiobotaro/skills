I wrote the ADR at `docs/adr/0001-iso-8601-utc-timestamps-in-public-api.md`. It has the status (Accepted), the date (2026-11-22), the context, the decision and the consequences. The repo was empty, so I picked `docs/adr/` and numbered it 0001. Rename or move it if you use a different convention.

- **Context:** your two reasons. Epoch integers caused repeated timezone bugs in client integrations, and they are unreadable in logs.
- **Decision:** all public API timestamps are ISO 8601 strings in UTC with a `Z` suffix, for example `2026-11-22T14:30:00Z`.
- **Consequences:** the two trade-offs you named. Clients have to parse strings, and payloads get slightly bigger.

I added a few things you didn't say, so check them:
- The decision covers request and response bodies, query parameters and webhooks.
- It lists that existing epoch-based integrations will need to migrate.
- It says to always emit UTC with `Z`.
- The note about epoch values being ambiguous between seconds and milliseconds is my addition.
- The size figure of "about 20 bytes instead of 10 digits" is my estimate.

I left the timestamp precision (seconds or fractional seconds) and the migration and versioning plan out of scope. The ADR says to cover them in a follow-up. I haven't committed anything.
