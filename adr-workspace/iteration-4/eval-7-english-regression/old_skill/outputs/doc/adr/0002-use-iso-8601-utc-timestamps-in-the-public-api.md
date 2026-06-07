# 2. Use ISO 8601 UTC timestamps in the public API

Date: 2026-06-07

## Status

Accepted

## Context

Our public API currently represents every timestamp as a Unix epoch integer. An epoch integer carries no timezone or offset information of its own, and reading one requires a conversion step. In practice this has caused repeated timezone bugs in client integrations, where the integer was interpreted against the wrong zone or assumed to be in seconds versus milliseconds. The same values are also unreadable when they appear in our logs: a developer scanning a log line sees a bare number and cannot tell at a glance what moment it refers to.

## Decision

We will represent all timestamps in our public API as ISO 8601 strings in UTC (for example, `2026-06-07T14:30:00Z`) instead of Unix epoch integers.

## Consequences

Timestamps become unambiguous: the format names UTC explicitly, so clients no longer have to guess a timezone or a unit, which removes the class of timezone bugs we have been seeing in client integrations.

Logs become readable. A timestamp in a log line is now a human-legible date and time rather than a bare integer, so developers can interpret it directly.

Clients now have to parse strings rather than read an integer directly. This is a trade-off we accepted; ISO 8601 parsing is widely supported, but it is an extra step compared to consuming a number.

Payloads get slightly bigger, since an ISO 8601 string is longer than the integer it replaces. We accepted this increase as worth the gain in clarity and correctness.
