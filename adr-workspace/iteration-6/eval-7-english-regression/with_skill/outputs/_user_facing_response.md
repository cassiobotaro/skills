There was no decision log in the repository yet, so I started one in the adr-tools default location and seeded it the way `adr init` does.

Files created:

- `doc/adr/0001-record-architecture-decisions.md` — the standard seed ADR that records the decision to keep a decision log at all.
- `doc/adr/0002-use-iso-8601-utc-strings-for-timestamps-in-the-public-api.md` — your decision.

ADR 2 in full:

```markdown
# 2. Use ISO 8601 UTC strings for timestamps in the public API

Date: 2026-07-21

## Status

Accepted

## Context

The public API represents timestamps as unix epoch integers. That representation carries no
timezone information of its own, and client integrations have repeatedly shipped timezone
bugs as a result.

Epoch integers are also unreadable to a human: reading a log line or a raw payload requires
converting the number before it means anything.

## Decision

We will represent all timestamps in the public API as ISO 8601 strings in UTC, instead of
unix epoch integers.

## Consequences

Timestamps carry their timezone in the value itself, which removes the class of client-side
timezone bugs we have been seeing.

Payloads and logs become readable without conversion.

Clients now have to parse strings rather than read an integer directly.

Payloads get slightly bigger, since a timestamp string is longer than the integer it
replaces.
```

The Consequences section records both sides — the two problems this fixes and the two costs you accepted (clients parsing strings, slightly larger payloads). I did not add any migration plan, deadline, or alternative formats, since you didn't mention any; if a rollout path or a deprecation window for the integer field is part of the decision, that would be worth a follow-up ADR.
