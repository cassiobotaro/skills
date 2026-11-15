# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account. The API gateway cannot see account ids, so it cannot count attempts per account. The session service handles logins and knows which account each attempt targets.

## Decision

We will rate-limit login attempts per account inside the session service, at 5 attempts per 15 minutes, instead of at the API gateway. The service will keep the rate-limit counters in Redis.

## Consequences

The limit applies per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, in addition to the sessions it already stores there (see ADR 2), so it carries more state and more load on Redis.
