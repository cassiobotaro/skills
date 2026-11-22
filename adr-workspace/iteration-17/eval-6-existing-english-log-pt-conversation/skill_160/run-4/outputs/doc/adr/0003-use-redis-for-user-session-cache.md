# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be kept in PostgreSQL, our primary database. Doing so adds read load to the main database, and session expiry would have to be handled by us rather than by the store.

## Decision

We will use Redis as the cache for user sessions, instead of storing them in PostgreSQL.

## Consequences

Session reads no longer hit the main PostgreSQL database, and session keys expire automatically.

We now have one more infrastructure component to operate.

Sessions are lost if Redis restarts without persistence enabled. We accept this trade-off.
