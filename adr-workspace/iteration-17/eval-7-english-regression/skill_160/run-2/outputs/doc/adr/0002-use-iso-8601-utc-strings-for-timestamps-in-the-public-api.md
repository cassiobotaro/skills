# 2. Use ISO 8601 UTC strings for timestamps in the public API

Date: 2026-11-22

## Status

Accepted

## Context

Our public API has represented timestamps as unix epoch integers. Epoch integers have repeatedly caused timezone bugs in client integrations, and they are unreadable when they show up in logs.

## Decision

We will represent all timestamps in our public API as ISO 8601 strings in UTC instead of unix epoch integers.

## Consequences

Timezone bugs in client integrations should no longer come from the timestamp format, and timestamps become readable in logs.

Clients now have to parse strings rather than read integers.

Payloads get slightly bigger.
