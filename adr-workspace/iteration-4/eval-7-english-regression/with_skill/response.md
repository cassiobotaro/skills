I recorded your decision as an ADR. Since there was no existing decision log, I initialized one (mirroring `adr init`): I created `doc/adr/` and seeded it with the canonical "record architecture decisions" ADR, so your decision is numbered 2.

Files written:

- `doc/adr/0001-record-architecture-decisions.md` — the seed ADR that establishes the log (standard adr-tools starter).
- `doc/adr/0002-use-iso-8601-utc-timestamps-in-the-public-api.md` — your decision.

ADR 0002 captures it in the Michael Nygard format:

- **Context** (neutral): epoch integers carry no timezone information, which repeatedly caused client integrations to misinterpret values, and they are opaque in logs and error reports.
- **Decision**: we will represent all public-API timestamps as ISO 8601 strings in UTC (e.g. `2026-06-07T14:30:00Z`) instead of unix epoch integers.
- **Consequences**: unambiguous timezone handling and human-readable logs on the upside; and the trade-offs you accepted — clients now have to parse the strings, and payloads grow slightly.

The files use exact adr-tools conventions (sequential `NNNN-slug.md` numbering, the four standard sections), so `adr list` and `adr generate toc`/`graph` work on them unchanged.
