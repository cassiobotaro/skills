# 2. Use ISO 8601 UTC strings for timestamps in the public API

Date: 2026-11-22

## Status

Accepted

## Context

Timestamps in our public API are currently unix epoch integers. Client integrations have repeatedly run into timezone bugs when handling them. Epoch integers are also unreadable in logs.

## Decision

We will represent all timestamps in the public API as ISO 8601 strings in UTC instead of unix epoch integers.

## Consequences

The timezone bugs that epoch integers caused in client integrations should stop, and timestamps become readable in logs.

Clients now have to parse strings rather than consume integers, which is extra work for every integration.

Payloads get slightly bigger, because an ISO 8601 string is longer than an epoch integer.
