# 3. Use Redis for the user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in PostgreSQL, our primary database. Doing so puts the read load of session lookups on that database. We also want session keys to expire automatically.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL.

## Consequences

Session reads no longer hit the primary database, and keys expire automatically.

We now have one more infrastructure component to operate.

Sessions are lost if Redis restarts without persistence. We accept this trade-off.
