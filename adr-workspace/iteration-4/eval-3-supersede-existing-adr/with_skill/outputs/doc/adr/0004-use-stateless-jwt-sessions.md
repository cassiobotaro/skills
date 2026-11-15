# 4. Use stateless JWT sessions

Date: 2026-06-07

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

Sessions are currently stored in Redis (ADR 2). As we moved to multi-region deploys, the Redis cluster became a single point of failure: when it is unavailable, no authenticated request can be served in any region. Keeping Redis replicated across regions to remove that single point of failure carries a cost that does not justify the benefit it provides for session storage.

## Decision

We will use stateless JWT tokens for sessions instead of server-side sessions in Redis. The token itself carries the session state, so authenticating a request no longer requires a lookup against a shared store.

## Consequences

The login path no longer depends on Redis being available, which removes the single point of failure across multi-region deploys, and we no longer pay the cost of replicating Redis across regions for session storage.

Sessions can no longer be revoked immediately: because the token is self-contained, there is no server-side record to delete to log a user out everywhere. We accept this trade-off and mitigate it with a short token expiration of 15 minutes.
