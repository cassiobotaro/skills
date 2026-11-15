# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account, at 5 attempts per 15 minutes. The API gateway is the usual place for rate limiting, but it cannot see account ids, so it cannot enforce a limit per account.

## Decision

We will enforce the per-account login rate limit (5 attempts per 15 minutes) inside the session service instead of at the API gateway.

## Consequences

The limit can be applied per account, because the session service has the account id.

The session service now keeps rate-limit counters in Redis, which adds state and load to a component that previously only stored sessions there.
