# 4. Use stateless JWT sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

ADR 2 stores user sessions in Redis. In multi-region deployments, the Redis cluster has become a single point of failure. Keeping it replicated has a cost that the team considers not worth paying.

## Decision

We will replace server-side sessions in Redis with stateless JWT tokens. Tokens will expire after 15 minutes.

## Consequences

Redis is no longer a runtime dependency of the login path, which removes the single point of failure in multi-region deployments and the cost of keeping the cluster replicated.

We can no longer revoke a session immediately. A token stays valid until it expires, so a revoked or compromised session can remain usable for up to 15 minutes. The team accepts this trade-off, and the short expiration is what limits it.

Logging a user out everywhere is no longer a single DELETE operation, as it was under ADR 2.
