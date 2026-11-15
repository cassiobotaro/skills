# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account, at 5 attempts per 15 minutes. The API gateway cannot see account ids, so it cannot apply a limit per account.

## Decision

We will rate-limit login attempts per account, at 5 per 15 minutes, inside the session service instead of at the API gateway.

## Consequences

The limit is enforced per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, so it holds more state in Redis than before.
