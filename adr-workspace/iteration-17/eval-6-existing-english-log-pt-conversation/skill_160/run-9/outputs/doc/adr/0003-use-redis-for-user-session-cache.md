# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. We want to take session read load off that main database and to have session keys expire automatically.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session reads no longer load the main database, and session keys expire automatically.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence, the sessions are lost. We accept this trade-off.
