# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so would put the read load of session lookups on the main database. We also want session keys to expire automatically.

## Decision

We will use Redis as the cache for user sessions instead of storing them in PostgreSQL. Session expiry will rely on the automatic expiration of Redis keys.

## Consequences

Session reads no longer hit the main PostgreSQL database, which reduces its read load.

Expired sessions are removed automatically by Redis through key expiration.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence enabled, all sessions are lost. We accept this trade-off.
