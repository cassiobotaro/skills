# 4. Use stateless JWT sessions

Date: 2026-06-07

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

Sessions are currently stored in Redis, which makes Redis a hard runtime dependency of the login path. As the system moves to multi-region deployments, the Redis cluster has become a single point of failure during deploys: a region whose Redis is unavailable cannot serve authenticated requests. Keeping Redis replicated across regions carries an operational and infrastructure cost that the team judges not to be worth the benefit it provides.

## Decision

We will store sessions as stateless JWT tokens instead of in Redis. Session state travels inside the signed token, so no shared session store is read on authenticated requests. Tokens are issued with a short expiration of 15 minutes.

## Consequences

The login path no longer depends on Redis, removing it as a single point of failure for authenticated requests and eliminating the cost of replicating the Redis cluster across regions.

Sessions can no longer be revoked immediately, because a stateless token remains valid until it expires. The team accepts this trade-off and mitigates it with the short 15-minute expiration, which bounds how long a token stays usable after a session should have ended.
