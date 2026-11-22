I wrote the ADR and, because the repo had no decision log, a seed ADR before it.

- `doc/adr/0001-record-architecture-decisions.md` is the standard seed ADR that starts an adr-tools log. It uses the stock text with today's date (2026-11-22).
- `doc/adr/0002-use-iso-8601-utc-strings-for-public-api-timestamps.md` is your decision, with status `Accepted`.

ADR 0002 records only what you told me.
- **Context:** epoch integers caused repeated timezone bugs in client integrations and are unreadable in logs.
- **Decision:** all public API timestamps will be ISO 8601 strings in UTC instead of unix epoch integers.
- **Consequences:** the benefits are fewer timezone bugs and readable logs. The accepted costs are that clients have to parse strings and payloads get slightly bigger.

I didn't add alternatives, such as epoch with an explicit timezone field, or a migration plan, because you didn't mention any. If the team considered other options or has a rollout plan for existing clients, tell me and I'll add them. If you think the decision is still awaiting sign-off, I'll change the status to `Proposed`.
