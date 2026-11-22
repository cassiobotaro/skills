# ADR 0001: Use ISO 8601 UTC strings for timestamps in the public API

- Status: Accepted
- Date: 2026-11-22

## Context

Our public API has represented timestamps as Unix epoch integers. In practice this has caused problems:

- Client integrations repeatedly introduced timezone bugs. Examples are mixing up seconds and milliseconds and applying local-time conversions incorrectly.
- Epoch integers are unreadable in logs, support tickets and ad-hoc debugging, so people have to convert them by hand.

## Decision

All timestamps in the public API will be ISO 8601 strings in UTC, using the `Z` suffix, for example `2026-11-22T14:30:00Z`. This applies to both requests and responses. Unix epoch integers will no longer be used for timestamps in the public API.

## Consequences

### Positive

- The format is unambiguous. The UTC designator and explicit date and time fields remove the seconds/milliseconds and timezone ambiguity behind the earlier client bugs.
- Values are human-readable in logs, traces, support conversations and API explorers.
- ISO 8601 is widely supported by standard libraries and tooling.

### Negative (accepted trade-offs)

- Clients must parse strings into native date/time types instead of consuming integers directly.
- Payloads are slightly larger (about 20 bytes per timestamp versus about 10 for an epoch integer).

## Notes

Not covered by this ADR, to be decided separately:

- Migration and versioning for existing clients that rely on epoch integers.
- Precision, such as whether fractional seconds are allowed.
