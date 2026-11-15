No decision log existed yet, so I initialized one the way `adr init` would and recorded your decision in it. Two files were created:

- `doc/adr/0001-record-architecture-decisions.md` — the standard seed ADR that records *why* this project keeps ADRs (Michael Nygard format). Every fresh log starts with this one.
- `doc/adr/0002-use-iso-8601-utc-timestamps-in-the-public-api.md` — your decision.

ADR 2, **Use ISO 8601 UTC timestamps in the public API** (Accepted, dated 2026-06-07):

- **Context** — the public API currently uses Unix epoch integers, which carry no timezone or unit information; this has caused repeated timezone bugs in client integrations and the bare numbers are unreadable in our logs.
- **Decision** — we will represent all API timestamps as ISO 8601 strings in UTC (e.g. `2026-06-07T14:30:00Z`) instead of epoch integers.
- **Consequences** — timestamps become unambiguous and logs become human-readable; against that, the two trade-offs you accepted: clients must now parse strings rather than read an integer, and payloads get slightly bigger.

These are plain adr-tools-format files, so your existing tooling works on them unchanged — `adr list`, `adr generate toc`, `adr generate graph`, and Structurizr's `!adrs doc/adr` importer.
