# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so puts session reads on the main database, and expiring old sessions would need to be handled separately.

## Decision

We will use Redis as the cache for user sessions, instead of storing them in PostgreSQL.

## Consequences

Session reads no longer load the primary database, and keys expire automatically.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence, all sessions are lost. We accept this trade-off.
