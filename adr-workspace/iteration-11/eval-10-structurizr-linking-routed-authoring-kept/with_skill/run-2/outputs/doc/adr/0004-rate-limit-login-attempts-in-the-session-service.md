# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts must be rate-limited per account, at 5 attempts per 15 minutes. The API gateway cannot see account ids, so it cannot apply a limit per account.

## Decision

We will enforce the per-account login rate limit (5 attempts per 15 minutes) inside the session service instead of at the API gateway.

## Consequences

The limit can be keyed by account id, which the gateway cannot do.

The session service now keeps rate-limit counters in Redis, which is an additional use of Redis beyond session storage.
