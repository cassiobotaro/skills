I wrote the ADR for the timestamp decision and marked it `Accepted`, since you said the decision was made. The repo had no decision log, so I also created one.

- `doc/adr/0001-record-architecture-decisions.md` is the standard seed ADR that starts a log. It's the same text `adr init` produces.
- `doc/adr/0002-use-iso-8601-utc-strings-for-public-api-timestamps.md` is your decision.
  - **Context:** epoch integers caused repeated timezone bugs in client integrations and are unreadable in logs.
  - **Decision:** all public API timestamps will be ISO 8601 strings in UTC.
  - **Consequences:** logs become readable and the timezone bugs should go away. Clients now have to parse strings, and payloads get slightly bigger.

I didn't add any alternatives, metrics or migration details you didn't mention. If there is a migration plan for existing clients, such as versioning or a deprecation window for the epoch fields, tell me. That would be a separate ADR, and I can also add it to this one.
