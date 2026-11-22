# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, the primary database ([2. Use PostgreSQL for persistence](0002-use-postgresql-for-persistence.md)). Doing so would put the read load of session lookups on that main database, and expiring old sessions would not happen automatically.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL. Session keys will expire automatically.

## Consequences

Session reads no longer hit the main PostgreSQL database, which reduces its read load.

Expired sessions are removed automatically through key expiration.

Redis is one more infrastructure component that the team has to operate.

If Redis restarts without persistence enabled, all sessions are lost.
