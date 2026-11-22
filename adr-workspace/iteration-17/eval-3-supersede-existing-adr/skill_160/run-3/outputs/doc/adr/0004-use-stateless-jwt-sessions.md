# 4. Use stateless JWT sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

The Redis cluster that holds user sessions has become a single point of failure in multi-region deploys. The cost of keeping it replicated is not worth what it gives us.

## Decision

We will replace server-side sessions in Redis with stateless JWT tokens, with a short expiration of 15 minutes.

## Consequences

Sessions no longer depend on the Redis cluster, so it stops being a single point of failure in multi-region deploys, and we no longer pay to keep it replicated.

We give up immediate session revocation. The short 15-minute expiration is how we limit the cost of that.
