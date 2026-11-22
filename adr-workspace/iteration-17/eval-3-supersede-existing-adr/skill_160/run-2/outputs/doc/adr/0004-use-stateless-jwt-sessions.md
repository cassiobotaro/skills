# 4. Use stateless JWT sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

The Redis cluster that holds user sessions has become a single point of failure in multi-region deployments. Keeping it replicated costs more than the team considers worthwhile.

## Decision

We will replace server-side sessions in Redis with stateless JWT tokens. Tokens will expire after 15 minutes.

## Consequences

Sessions no longer depend on the Redis cluster, which removes that single point of failure from multi-region deployments, along with the cost of keeping the cluster replicated.

A session cannot be revoked immediately. An issued token stays valid until it expires, so the 15-minute expiration is the upper bound on how long a revoked session can keep working. The team accepts this trade-off.
