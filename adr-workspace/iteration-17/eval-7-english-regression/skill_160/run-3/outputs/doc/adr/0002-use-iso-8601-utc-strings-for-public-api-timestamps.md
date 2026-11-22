# 2. Use ISO 8601 UTC strings for public API timestamps

Date: 2026-11-22

## Status

Accepted

## Context

Our public API has represented timestamps as unix epoch integers. Epoch integers have repeatedly caused timezone bugs in client integrations, and they are unreadable in logs.

## Decision

We will represent all timestamps in our public API as ISO 8601 strings in UTC instead of unix epoch integers.

## Consequences

Timezone bugs in client integrations should become less likely, and timestamps in logs become readable.

Clients now have to parse strings instead of receiving integers.

Payloads get slightly bigger.
