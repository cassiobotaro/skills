# 4. Use stateless JWT for sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

ADR 2 stored sessions in Redis. In multi-region deployments the Redis cluster became a single point of failure, and the cost of keeping it replicated across regions is not justified.

## Decision

We will authenticate requests with stateless JSON Web Tokens (JWT) instead of server-side sessions in Redis. Tokens expire after 15 minutes.

## Consequences

The login path no longer depends on Redis, which removes the single point of failure in multi-region deployments and the cost of replicating the cluster.

Sessions cannot be revoked immediately. A compromised or logged-out token remains valid until it expires, at most 15 minutes. We accept this trade-off and rely on the short expiration to limit exposure.

"Log out everywhere" is no longer a single DELETE; it takes effect only as tokens expire.

The 30-day sliding session is gone. Clients must renew tokens every 15 minutes, so a renewal mechanism is needed (not decided here).

Signing keys must be distributed to all regions and rotated safely.
