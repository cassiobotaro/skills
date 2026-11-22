# 4. Use stateless JWT sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

ADR 2 stores user sessions in Redis. In multi-region deployments the Redis cluster has become a single point of failure, and the cost of keeping it replicated is not worth paying.

## Decision

We will replace server-side sessions in Redis with stateless JWT tokens. Tokens will expire after 15 minutes.

## Consequences

Authenticating a request no longer requires a lookup in Redis, so the cluster stops being a single point of failure for sessions in multi-region deployments, and we no longer pay to keep it replicated for this purpose.

We lose the ability to revoke a session immediately. A token stays valid until it expires, so the 15-minute expiration is the upper bound on how long a revoked or compromised session can keep working.

The "log out everywhere" operation described in ADR 2, a single DELETE, no longer exists.
