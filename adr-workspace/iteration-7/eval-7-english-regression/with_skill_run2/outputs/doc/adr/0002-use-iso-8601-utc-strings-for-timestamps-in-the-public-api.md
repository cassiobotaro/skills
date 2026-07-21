# 2. Use ISO 8601 UTC strings for timestamps in the public API

Date: 2026-07-21

## Status

Accepted

## Context

The public API represents timestamps as unix epoch integers. That representation carries no
timezone information of its own, and client integrations have repeatedly shipped timezone
bugs as a result.

Epoch integers are also unreadable to a human: a value in a log line or an error report has
to be converted before anyone can tell what moment it refers to.

## Decision

We will represent all timestamps in the public API as ISO 8601 strings in UTC, instead of
unix epoch integers.

## Consequences

Timestamps carry their timezone with them, which removes the class of client-side timezone
bugs we have been seeing, and they are directly readable in logs.

Clients now have to parse strings rather than read an integer.

Payloads get slightly bigger, since a string timestamp takes more bytes than an integer.
