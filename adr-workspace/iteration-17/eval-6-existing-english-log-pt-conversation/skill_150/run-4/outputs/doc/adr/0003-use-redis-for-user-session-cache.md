# 3. Use Redis for the user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, the primary database. Doing so puts the read load of session lookups on that database. Sessions also need to expire, and the keys should expire automatically.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session reads no longer hit the primary database, which reduces its read load.

Session keys expire automatically, so we don't have to clean them up ourselves.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence, the sessions are lost.
