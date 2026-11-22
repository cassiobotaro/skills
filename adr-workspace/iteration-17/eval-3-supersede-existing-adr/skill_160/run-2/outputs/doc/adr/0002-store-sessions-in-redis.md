# 2. Store sessions in Redis

Date: 2025-11-18

## Status

Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)

## Context

The session service must share login sessions between multiple API instances. Sessions are read on every authenticated request, so lookups must be fast. We already operate a Redis instance for caching.

## Decision

We will store user sessions in Redis, keyed by session token, with a sliding expiration of 30 days.

## Consequences

Session lookups stay below one millisecond and sessions survive API restarts and deploys.

Logging a user out everywhere is a single DELETE operation.

Redis becomes a hard runtime dependency of the login path. If Redis is unavailable, no authenticated request can be served.
