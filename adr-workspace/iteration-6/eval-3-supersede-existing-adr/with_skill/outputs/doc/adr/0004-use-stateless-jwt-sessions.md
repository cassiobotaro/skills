# 4. Use stateless JWT sessions

Date: 2026-07-21

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

Sessions are currently stored in Redis, which makes the Redis cluster a hard runtime dependency of the login path. In multi-region deploys that cluster has become a single point of failure: when it is unavailable, no authenticated request can be served anywhere. Keeping it replicated across regions carries a cost the team does not consider justified by the benefit.

## Decision

We will use stateless JWT tokens for user sessions, with a short expiration of 15 minutes, instead of server-side sessions stored in Redis.

## Consequences

The login path no longer depends on the Redis cluster at runtime, so a Redis outage no longer takes authenticated requests down, and multi-region deploys no longer require a replicated session store.

We accept that a session can no longer be revoked immediately: a token stays valid until it expires. The 15-minute expiration bounds that window, at the cost of more frequent token renewal.
