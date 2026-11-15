# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account to slow down password guessing. The API gateway is the usual place for rate limiting, but it cannot see account ids, so it cannot count attempts per account.

## Decision

We will rate-limit login attempts per account inside the session service, allowing 5 attempts per 15 minutes. The service will keep the rate-limit counters in Redis.

## Consequences

Limits apply per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, in addition to the sessions it already stores there. This adds state and load to Redis.
