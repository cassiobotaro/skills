# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account. The limit is 5 attempts per 15 minutes. The API gateway is the other place where the limit could be enforced, but the gateway cannot see account ids, so it cannot count attempts per account.

## Decision

We will enforce the login rate limit of 5 attempts per account in a 15-minute window inside the session service, not at the API gateway. The session service will keep the rate-limit counters in Redis.

## Consequences

The limit is applied per account, which the gateway could not do because it has no access to account ids.

The session service now stores rate-limit counters in Redis, in addition to sessions. Redis carries more load and more responsibility on the login path.
