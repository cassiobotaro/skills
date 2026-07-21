# 4. Use stateless JWT sessions

Date: 2026-07-21

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

Sessions are currently stored in Redis, which makes the Redis cluster a hard runtime dependency of the login path. With deployments spread across multiple regions, that cluster has become a single point of failure: when it is unreachable during a deploy, no authenticated request can be served in the affected region.

Keeping Redis replicated across regions would address the availability problem, but the cost of operating that replication does not pay for itself.

## Decision

We will use stateless JWT tokens for user sessions, with a short expiration of 15 minutes. Session state is no longer stored server-side, so an authenticated request is validated from the token itself.

## Consequences

The login path no longer depends on the Redis cluster being reachable, so a multi-region deploy cannot take authentication down with it, and we stop paying to keep Redis replicated across regions.

We give up immediate session revocation: a token stays valid until it expires, so a logout or a forced sign-out is not effective right away. The 15-minute expiration is the trade-off we accept to bound that window.
