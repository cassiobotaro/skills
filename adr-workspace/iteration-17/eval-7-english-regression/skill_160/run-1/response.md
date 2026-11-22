I've written the ADR, and I'm doing a last check on its wording before I report back.

The repo had no decision log, so I started one. I created these files:

- `doc/adr/0001-record-architecture-decisions.md` is the standard seed ADR that `adr init` creates. I didn't write this one for your decision.
- `doc/adr/0002-use-iso-8601-utc-strings-for-timestamps-in-the-public-api.md` is your decision, with status Accepted and today's date, 2026-11-22.

The Context holds only the reasons you gave: epoch integers caused repeated timezone bugs in client integrations, and they're unreadable in logs. The Decision says we will use ISO 8601 strings in UTC for all public API timestamps. The Consequences cover the trade-off you accepted: clients have to parse strings, and payloads get slightly bigger. I didn't add any alternatives or metrics you didn't mention.

I made one wording change after the first draft. I had written a sentence about clients no longer working out timezones from a bare integer, which was my own explanation of the mechanism. I replaced it with "We expect this to end the repeated timezone bugs in client integrations."

I haven't committed anything.
