# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account, at 5 attempts per 15 minutes. The API gateway is the obvious place for rate limiting, but it cannot see account ids, so it cannot enforce a per-account limit.

## Decision

We will enforce the per-account login rate limit (5 attempts per 15 minutes) inside the session service instead of at the API gateway.

## Consequences

The limit can be applied per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, which adds write load and more state to the Redis instance it already depends on for sessions (see ADR 2).

Rate-limiting logic lives in the session service rather than at the edge, so it is applied only after a request has reached the service.
