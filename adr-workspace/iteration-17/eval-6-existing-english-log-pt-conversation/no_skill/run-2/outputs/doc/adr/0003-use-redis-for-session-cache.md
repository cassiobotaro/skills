# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

Complements [2. Use PostgreSQL for persistence](0002-use-postgresql-for-persistence.md): PostgreSQL remains the primary store, but user sessions are not kept in it.

## Context

User sessions are read on nearly every request. Storing them in PostgreSQL adds read load to the main database. Sessions also need to expire, which in PostgreSQL would require our own cleanup mechanism.

## Decision

We will use Redis as the store for user sessions instead of PostgreSQL. Session keys will use Redis's built-in key expiration (TTL) to expire automatically.

## Consequences

Read load for sessions moves off the main PostgreSQL database.

Expired sessions are removed automatically by Redis, with no cleanup job to maintain.

Redis is one more infrastructure component to provision, monitor and operate.

If Redis restarts without persistence enabled, all sessions are lost and users must log in again.
