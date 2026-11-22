# 4. Use stateless JWT sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

Sessions are currently stored in Redis, as decided in ADR 2. In multi-region deploys the Redis cluster has become a single point of failure, and the cost of keeping it replicated is not worth what it provides.

## Decision

We will stop storing sessions in Redis and use stateless JWT tokens instead. Tokens will expire after 15 minutes.

## Consequences

The login path no longer depends on a Redis cluster, which removes the single point of failure in multi-region deploys and the cost of replicating it.

We give up immediate session revocation. A token stays valid until it expires, so the 15-minute expiration bounds how long a revoked session can keep working. The team accepts this trade-off.

Logging a user out everywhere is no longer a single DELETE operation, as it was under ADR 2.
