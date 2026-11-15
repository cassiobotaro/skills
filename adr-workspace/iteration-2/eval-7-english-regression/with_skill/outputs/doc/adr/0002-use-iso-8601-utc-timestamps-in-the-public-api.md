# 2. Use ISO 8601 UTC timestamps in the public API

Date: 2026-06-07

## Status

Accepted

## Context

Our public API currently represents timestamps as Unix epoch integers. This has caused repeated timezone bugs in client integrations, because an epoch integer carries no explicit zone and clients have applied their own local offset to it. The same integers are also unreadable in logs, where a human reading the output cannot tell at a glance what moment in time a value refers to.

## Decision

We will represent all timestamps in our public API as ISO 8601 strings in UTC (for example, `2026-06-07T14:30:00Z`) instead of Unix epoch integers.

## Consequences

Timestamps become unambiguous: the format carries an explicit UTC zone, which removes the class of timezone bugs that client integrations have been hitting.

Timestamps become readable in logs, so a human can see what moment a value refers to without converting an integer.

Clients now have to parse strings rather than read an integer directly, which adds a parsing step on their side.

Payloads get slightly bigger, since an ISO 8601 string takes more bytes than the equivalent epoch integer.
