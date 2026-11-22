# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, the primary database. Doing so adds read load to that database, and expired sessions would need to be removed by some other mechanism.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session reads no longer hit the primary database, which reduces its read load.

Redis expires keys automatically, so session expiration does not need separate cleanup logic.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence enabled, all sessions are lost.
