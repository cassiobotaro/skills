# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account to slow down repeated guessing. The API gateway is the obvious place to apply a rate limit, but it cannot see account ids, so it cannot count attempts per account.

## Decision

We will rate-limit login attempts per account inside the session service, allowing 5 attempts per 15 minutes, instead of at the API gateway.

## Consequences

The limit is applied per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, in addition to the sessions it already stores there (see [2. Store sessions in Redis](0002-store-sessions-in-redis.md)). This adds state to maintain and more data in Redis.
