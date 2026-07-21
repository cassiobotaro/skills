# 4. Use stateless JWT sessions

Date: 2026-07-21

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

Sessions are currently stored in Redis, which makes the Redis cluster a hard runtime dependency of the login path. In multi-region deploys that cluster became a single point of failure: when it is unavailable, no authenticated request can be served anywhere. Keeping it replicated across regions costs more than the team judges the benefit to be worth.

## Decision

We will use stateless JWT tokens for sessions, with a short expiration of 15 minutes, instead of server-side sessions stored in Redis.

## Consequences

Authenticating a request no longer requires a lookup in a shared store, so the login path no longer depends on the Redis cluster being available in every region.

Replicating a Redis cluster across regions is no longer necessary for sessions, removing that operational cost.

We can no longer revoke a session immediately: a token stays valid until it expires. We accept this trade-off and bound it with the 15-minute expiration, so a revoked session survives at most that long.
