# 2. Use ISO 8601 UTC strings for public API timestamps

Date: 2026-11-22

## Status

Accepted

## Context

Our public API has represented timestamps as unix epoch integers. Client integrations have repeatedly run into timezone bugs when handling those values. Epoch integers are also unreadable in logs.

## Decision

We will represent all timestamps in our public API as ISO 8601 strings in UTC, instead of unix epoch integers.

## Consequences

Timestamps become readable in logs, and the timezone bugs that clients hit with epoch integers should no longer occur, since every value is explicitly in UTC.

Clients now have to parse strings into their own date-time types rather than consuming integers directly.

Payloads get slightly bigger, because an ISO 8601 string takes more bytes than an integer.
