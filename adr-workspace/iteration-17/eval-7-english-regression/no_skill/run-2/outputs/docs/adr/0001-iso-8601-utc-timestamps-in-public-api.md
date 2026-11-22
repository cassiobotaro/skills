# ADR 0001: Use ISO 8601 UTC strings for timestamps in the public API

- **Status:** Accepted
- **Date:** 2026-11-22

## Context

Our public API has represented timestamps as Unix epoch integers. In practice this has caused problems:

- Client integrations repeatedly introduced timezone bugs. Epoch values don't say whether they are seconds or milliseconds, and clients often convert them with local-time assumptions.
- Epoch integers are unreadable in logs, support tickets and debugging sessions. Reading one requires a conversion step.

## Decision

All timestamps in the public API will be ISO 8601 strings in UTC, using the `Z` suffix, for example `2026-11-22T14:30:00Z`. This applies to request and response bodies, query parameters, and webhooks. Unix epoch integers will no longer be used for timestamps in the public API.

## Consequences

### Positive

- The format is unambiguous, and the UTC offset is explicit in the value. This removes the main source of the timezone bugs.
- Values are human-readable in logs, traces and support conversations.
- Standard libraries in most languages can parse the format.

### Negative (accepted trade-offs)

- Clients must parse strings into native date/time types instead of using integers directly.
- Payloads are slightly larger (about 20 bytes per timestamp instead of 10 digits).
- Existing integrations that use epoch values will need to migrate.

## Notes

- Always emit UTC with `Z`, never local offsets, so that string comparison and sorting stay consistent.
- The precision (seconds or fractional seconds) and the migration and versioning plan for existing clients are not covered by this ADR. Record them in a follow-up ADR or in the API changelog.
