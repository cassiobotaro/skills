# 3. Use Redis for user session caching

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so would add session read load to that database. We also want session keys to expire automatically.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session reads no longer hit the primary database, which takes that load off PostgreSQL.

Session keys expire automatically.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence, all sessions are lost.
