# 2. Use ISO 8601 UTC strings for timestamps in the public API

Date: 2026-07-21

## Status

Accepted

## Context

Our public API represents timestamps as unix epoch integers. That representation carries
no timezone information of its own, and client integrations have repeatedly hit timezone
bugs as a result.

The same representation is also opaque to humans. An epoch integer in a log line cannot
be read without converting it first, which slows down anyone diagnosing a problem from
the logs.

## Decision

We will represent every timestamp in the public API as an ISO 8601 string in UTC,
replacing the unix epoch integers.

## Consequences

The timezone is now carried explicitly by the value itself, so a client no longer has to
infer it. This removes the ambiguity behind the timezone bugs seen in client
integrations.

Timestamps become readable as they appear, in logs and anywhere else a payload is
inspected by a person, without a conversion step.

Clients now have to parse strings rather than read an integer directly. We accepted this
as the cost of the change.

Payloads get slightly bigger, since an ISO 8601 string is longer than the integer it
replaces.
