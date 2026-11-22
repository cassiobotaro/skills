# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

Complements [2. Use PostgreSQL for persistence](0002-use-postgresql-for-persistence.md): PostgreSQL remains the primary store, but user sessions are not kept there.

## Context

User sessions are read on nearly every request. Storing them in PostgreSQL adds read load to the primary database, and expired sessions would need to be cleaned up by our own jobs.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL. Session keys will use Redis' native key expiration (TTL) to expire automatically.

## Consequences

Read load for sessions moves off the primary PostgreSQL database.

Sessions expire automatically through key TTLs, with no cleanup job needed.

Redis is one more infrastructure component that we must operate, monitor and secure.

If Redis restarts without persistence enabled, all sessions are lost and users must log in again. We accept this trade-off.
