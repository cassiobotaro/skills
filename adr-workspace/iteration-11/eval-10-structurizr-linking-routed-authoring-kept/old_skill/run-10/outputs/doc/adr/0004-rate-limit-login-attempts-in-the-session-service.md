# 4. Rate-limit login attempts in the session service

Date: 2026-11-15

## Status

Accepted

## Context

Login attempts need to be limited per account, at 5 attempts per 15 minutes. The API gateway cannot see account ids, so it cannot apply a per-account limit.

## Decision

We will enforce the login rate limit inside the session service, per account, at 5 attempts per 15 minutes. The API gateway will not enforce this limit.

## Consequences

The limit applies per account, which the gateway could not do.

The session service now keeps rate-limit counters in Redis, which adds state and write load to a service that already depends on Redis for sessions (ADR 2).
