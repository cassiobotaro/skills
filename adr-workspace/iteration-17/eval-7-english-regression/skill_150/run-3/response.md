I wrote the ADR, `0002`, with status Accepted and today's date, 2026-11-22. The repo had no decision log, so I also created a seed ADR, `0001`, to start one.

- `doc/adr/0001-record-architecture-decisions.md` is the standard "we will use ADRs" record that `adr init` creates.
- `doc/adr/0002-use-iso-8601-utc-strings-for-timestamps-in-the-public-api.md` is your decision.

ADR 0002 contains only what you told me:
- **Context:** the public API's timestamps are epoch integers, they caused repeated timezone bugs in client integrations, and they are unreadable in logs.
- **Decision:** "We will represent all timestamps in the public API as ISO 8601 strings in UTC instead of unix epoch integers."
- **Consequences:** the timezone bugs should stop and logs become readable. Clients now have to parse strings, and payloads get slightly bigger.

I didn't add alternatives you didn't mention, such as a different string format or keeping both representations. If you considered any, tell me and I'll add them. The same goes for a migration plan for existing clients. I left that out because you didn't describe one.
