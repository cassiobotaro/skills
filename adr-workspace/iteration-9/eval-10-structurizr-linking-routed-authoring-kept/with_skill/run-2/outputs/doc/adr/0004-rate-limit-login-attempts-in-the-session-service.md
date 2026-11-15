# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account to slow down repeated guessing. The API gateway is the usual place for rate limiting, but it cannot see account ids, so it cannot enforce a limit per account.

## Decision

We will rate-limit login attempts per account inside the session service, allowing 5 attempts per 15 minutes, instead of at the API gateway.

## Consequences

The limit is enforced per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, adding write load and more state to a store that is already a hard runtime dependency of the login path.
