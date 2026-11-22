# 4. Use stateless JWT sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

ADR 2 stores user sessions in Redis, which makes the Redis cluster a hard dependency of the login path. In multi-region deployments the cluster has become a single point of failure, and the cost of keeping it replicated is not worth what it provides.

## Decision

We will replace server-side sessions in Redis with stateless JWT tokens. Tokens will expire after 15 minutes.

## Consequences

The login path no longer depends on Redis, which removes the single point of failure in multi-region deployments and the cost of replicating the cluster for sessions.

Sessions cannot be revoked immediately. A token stays valid until it expires, so the 15-minute expiration is the upper bound on how long a revoked or compromised session keeps working. The team accepts this trade-off.

Logging a user out everywhere is no longer a single DELETE operation, as it was under ADR 2.
