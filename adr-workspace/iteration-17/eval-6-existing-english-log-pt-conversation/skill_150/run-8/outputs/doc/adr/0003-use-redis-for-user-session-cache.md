# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so adds read load to that database, and expiring sessions would have to be handled by us rather than by the store.

## Decision

We will use Redis as the cache for user sessions instead of storing them in PostgreSQL.

## Consequences

Session reads no longer hit the primary PostgreSQL database, which takes that load off it.

Session keys expire automatically, so we do not need to build our own expiration for them.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence enabled, all sessions are lost. We accept this trade-off.
