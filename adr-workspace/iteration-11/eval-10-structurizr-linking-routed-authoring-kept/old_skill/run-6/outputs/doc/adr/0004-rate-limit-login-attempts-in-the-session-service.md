# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account. The API gateway is the other place where the limit could be enforced, but it cannot see account ids, so it has no way to count attempts per account.

## Decision

We will rate-limit login attempts per account inside the session service, allowing 5 attempts per 15 minutes. We will not enforce this limit at the API gateway.

## Consequences

The limit can be applied per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, so it holds more state than before and depends on Redis for this check as well as for sessions.
