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
