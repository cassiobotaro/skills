# 4. Use stateless JWT tokens for sessions

Date: 2026-06-04

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

[ADR 2](0002-store-sessions-in-redis.md) decided to store user sessions in Redis, keyed by session token. This made Redis a hard runtime dependency of the login path.

As we moved to multi-region deployments, the Redis cluster became a single point of failure: every authenticated request depends on it, and an unavailable Redis means no authenticated request can be served. Keeping Redis replicated across regions to remove that single point of failure adds operational complexity and cost that is not justified by the benefit.

## Decision

We will use stateless JWT tokens for sessions instead of storing sessions in Redis. The token itself carries the session claims and is signed by the server, so no server-side session lookup is required.

Tokens will use a short expiration of 15 minutes.

## Consequences

The login path no longer depends on Redis at runtime, removing the multi-region single point of failure and the cost of replicating Redis across regions.

Authenticated requests are validated by verifying the token signature, with no network round-trip to a session store.

We accept the trade-off that sessions cannot be revoked immediately: a token remains valid until it expires. The short 15-minute expiration bounds the window during which a session we want to end is still usable.

Logging a user out everywhere is no longer a single DELETE operation; it relies on token expiration rather than server-side state.
