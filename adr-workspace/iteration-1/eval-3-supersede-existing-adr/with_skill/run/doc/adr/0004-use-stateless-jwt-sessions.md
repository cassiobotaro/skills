# 4. Use stateless JWT sessions

Date: 2026-06-04

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

Sessions are currently stored in a Redis cluster, read on every authenticated request. As the system moved to multi-region deployments, that Redis cluster became a single point of failure: an outage in the session store blocks authenticated requests across regions. Keeping the cluster replicated across regions to remove that single point of failure carries an operational and infrastructure cost that the team judges not worth what it buys.

## Decision

We will issue stateless JWT tokens for authentication instead of storing sessions in Redis. Each request is authenticated by validating the token's signature, with no server-side session lookup. Tokens carry a short expiration of 15 minutes.

## Consequences

The session path no longer depends on Redis, so the session store is removed as a single point of failure in multi-region deployments, and we no longer carry the cost of replicating that cluster across regions.

Authenticated requests are validated from the token alone, without a network round trip to a session store.

We can no longer revoke a session immediately, because a valid token stays valid until it expires. We accept this trade-off and mitigate it with the 15-minute expiration, which bounds how long a session remains active after we would have wanted to end it.
