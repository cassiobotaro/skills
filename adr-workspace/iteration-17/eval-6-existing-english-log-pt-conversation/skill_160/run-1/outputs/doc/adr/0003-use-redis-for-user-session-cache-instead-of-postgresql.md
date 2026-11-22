# 3. Use Redis for the user session cache instead of PostgreSQL

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so adds read load to that database, and expired sessions would need to be removed by us rather than disappearing on their own.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session reads no longer hit the primary database, which takes load off it.

Session keys expire automatically, so we do not have to clean them up ourselves.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence enabled, sessions are lost. We accept this trade-off.
