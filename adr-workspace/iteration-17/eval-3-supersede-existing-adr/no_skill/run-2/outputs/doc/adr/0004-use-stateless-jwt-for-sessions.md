# 4. Use stateless JWT for sessions

Date: 2026-11-22

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

ADR 2 stored sessions in Redis, making it a hard runtime dependency of the login path. In multi-region deploys the Redis cluster has become a single point of failure, and the cost of keeping it replicated across regions is not justified.

## Decision

We will replace server-side sessions in Redis with stateless JSON Web Tokens (JWT). Tokens are signed, validated locally by each API instance, and expire after 15 minutes.

## Consequences

Authenticated requests no longer depend on Redis, removing the single point of failure on the login path and the cost of cross-region replication.

Sessions cannot be revoked immediately. A logged-out or compromised session remains valid until its token expires, up to 15 minutes. We accept this trade-off.

The short expiration means clients must obtain new tokens frequently, so a renewal mechanism needs to be defined.

Signing keys must be distributed to all API instances and rotated safely.
