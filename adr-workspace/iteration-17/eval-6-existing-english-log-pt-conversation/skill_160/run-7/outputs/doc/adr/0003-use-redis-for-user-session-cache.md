# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so would put the read load of session lookups on that main database, and expiring old sessions would need to be handled separately.

## Decision

We will use Redis as the cache for user sessions, instead of storing them in PostgreSQL.

## Consequences

Session reads no longer hit the main PostgreSQL database, and session keys expire automatically.

Redis is one more infrastructure component that we have to operate.

Sessions are lost if Redis restarts without persistence enabled. We accept this trade-off.
