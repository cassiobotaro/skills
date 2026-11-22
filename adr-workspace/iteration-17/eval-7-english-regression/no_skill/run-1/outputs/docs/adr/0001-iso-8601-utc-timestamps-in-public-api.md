# 1. Use ISO 8601 UTC strings for timestamps in the public API

- Status: Accepted
- Date: 2026-11-22

## Context

Our public API has represented timestamps as Unix epoch integers. In practice
this has caused problems:

- Client integrations repeatedly introduced timezone bugs when converting
  epoch values to and from local time.
- Epoch integers are unreadable in logs, making debugging and support harder.

## Decision

All timestamps in the public API will be ISO 8601 strings in UTC, using the
`Z` suffix (e.g. `2026-11-22T14:30:00Z`), instead of Unix epoch integers.

This applies to both requests and responses.

## Consequences

### Positive

- Values are unambiguous about their timezone, removing a recurring class of
  client integration bugs.
- Timestamps are human-readable in logs, traces, and support tooling.

### Negative (accepted trade-offs)

- Clients must parse strings rather than consume integers directly.
- Payloads are slightly larger.

## Notes

Open points to settle during implementation (not decided here): migration and
versioning strategy for existing clients, and whether fractional seconds are
allowed.
