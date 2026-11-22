# 4. Use stateless JWT tokens for sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

ADR 2 stored sessions in Redis. In multi-region deployments the Redis cluster became a single point of failure, and the cost of keeping it replicated across regions is not justified. Because Redis is a hard dependency of the login path, its unavailability prevents any authenticated request from being served.

## Decision

We will authenticate requests with stateless, signed JWT access tokens instead of server-side sessions in Redis. Tokens will have a short expiration of 15 minutes. Services validate tokens locally by verifying the signature, with no session store lookup.

## Consequences

Redis is no longer a runtime dependency of the login path, which removes the single point of failure in multi-region deployments and the cost of replicating the cluster.

Token validation needs no network call, so it stays fast and works independently in each region.

Sessions cannot be revoked immediately. A logged-out or compromised session remains valid until its token expires, at most 15 minutes. We accept this trade-off. The "log out everywhere with a single DELETE" capability from ADR 2 no longer exists.

The 15-minute expiration means clients need a way to obtain new tokens without forcing users to log in again. This decision does not define the refresh mechanism, which must be decided separately. Signing key management and rotation must also be handled across regions.
