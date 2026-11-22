# 2. Use ISO 8601 UTC strings for timestamps in the public API

Date: 2026-11-22

## Status

Accepted

## Context

Our public API has represented timestamps as unix epoch integers. In client integrations this has repeatedly led to timezone bugs. Epoch integers are also unreadable in logs.

## Decision

We will represent all timestamps in the public API as ISO 8601 strings in UTC instead of unix epoch integers.

## Consequences

We expect this to end the repeated timezone bugs in client integrations, and timestamps in logs can now be read directly.

Clients now have to parse strings rather than consume integers, and payloads get slightly bigger. We accepted both costs in exchange for the benefits above.
