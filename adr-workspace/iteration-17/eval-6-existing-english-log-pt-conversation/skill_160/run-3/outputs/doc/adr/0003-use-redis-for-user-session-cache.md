# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so would put the read load of session lookups on that database. We also want session keys to expire automatically.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session reads no longer load the primary database, and session keys expire automatically.

We now have one more infrastructure component to operate.

If Redis restarts without persistence enabled, all sessions are lost. We accept this trade-off.
