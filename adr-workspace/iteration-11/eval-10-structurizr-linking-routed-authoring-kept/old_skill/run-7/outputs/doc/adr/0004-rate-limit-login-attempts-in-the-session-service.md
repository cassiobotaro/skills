# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account. The API gateway cannot see account ids, so it cannot count attempts per account.

## Decision

We will rate-limit login attempts per account inside the session service, at 5 attempts per 15 minutes, instead of at the API gateway.

## Consequences

The limit is enforced per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, which adds state and a dependency to the service that it did not need for this purpose before.
