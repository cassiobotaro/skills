I wrote the ADR, and it is marked `Accepted`. The repo had no decision log, so I also created a standard first ADR.

- `doc/adr/0001-record-architecture-decisions.md` is the usual first record that says the project keeps ADRs. I added it so the new record is `0002` and the log is compatible with adr-tools.
- `doc/adr/0002-use-iso-8601-utc-strings-for-timestamps-in-the-public-api.md` is your decision.

The ADR 0002 text uses only what you told me:
- **Context:** epoch integers caused repeated timezone bugs in client integrations, and they are unreadable in logs.
- **Decision:** we will represent all public API timestamps as ISO 8601 strings in UTC instead of unix epoch integers.
- **Consequences:** the two benefits, plus the trade-off you accepted. Clients now have to parse strings, and payloads get slightly bigger.

I didn't add alternatives you didn't mention, such as other date formats. I also didn't add a migration plan for existing clients. If either was part of the decision, tell me and I'll add it before the record gets referenced.

Both files are dated 2026-11-22. I didn't commit anything.
