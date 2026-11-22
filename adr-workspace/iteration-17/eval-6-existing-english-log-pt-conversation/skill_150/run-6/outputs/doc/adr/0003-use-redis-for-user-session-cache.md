# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions need a store. The alternative considered was keeping them in PostgreSQL, the primary database (see ADR 2). We want to take session read load off that database, and we want session keys to expire automatically.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session read load moves off the primary PostgreSQL database.

Session keys expire automatically, without a separate cleanup mechanism.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence, all sessions are lost. We accept this trade-off.
