# 2. Use ISO 8601 UTC timestamps in the public API

Date: 2026-06-07

## Status

Accepted

## Context

Our public API represents every timestamp as a unix epoch integer. This format carries no timezone information, which has repeatedly led client integrations to interpret values in the wrong timezone. Those bugs surface late, in client code we do not control, and are slow to diagnose.

Epoch integers are also opaque to a human reader. When a timestamp appears in a log line or an error report, it has to be converted before anyone can tell what moment it refers to, which slows down debugging and support.

## Decision

We will represent all timestamps in the public API as ISO 8601 strings in UTC (for example, `2026-06-07T14:30:00Z`) instead of unix epoch integers.

## Consequences

Timezone handling becomes unambiguous: every timestamp carries an explicit UTC offset, removing the class of timezone-interpretation bugs that epoch integers caused in client integrations.

Timestamps become directly readable in logs and error reports, so they can be understood without a conversion step.

Clients can no longer treat a timestamp as a plain integer; they now have to parse an ISO 8601 string into their own date/time type. This is the trade-off we accepted.

Payloads grow slightly, because an ISO 8601 string is longer than the equivalent epoch integer.
