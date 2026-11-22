I wrote the ADR for the timestamp decision. The repo had no decision log, so I also created one.

- `doc/adr/0001-record-architecture-decisions.md` is the standard seed record that `adr init` creates. It's what starts a new log, and I dated it today, 2026-11-22.
- `doc/adr/0002-use-iso-8601-utc-strings-for-public-api-timestamps.md` is your decision, with status `Accepted`.

The new ADR says:
- **Context:** the public API has used epoch integers, which caused repeated timezone bugs in client integrations and can't be read in logs.
- **Decision:** we will use ISO 8601 strings in UTC for all public API timestamps.
- **Consequences:** logs become readable and the timezone bugs should stop. Clients now have to parse strings, and payloads get slightly bigger.

I only used the reasons and trade-offs you gave me. I didn't add alternatives, size figures, or a migration plan. If you want a rollout or versioning note, that would be a separate decision, so let me know.
