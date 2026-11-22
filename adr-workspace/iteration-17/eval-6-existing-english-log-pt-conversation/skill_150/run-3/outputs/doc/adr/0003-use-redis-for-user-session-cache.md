# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions could be stored in the primary PostgreSQL database. Doing so adds read load to that database, and session keys would not expire on their own.

## Decision

We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL. PostgreSQL remains the primary persistence layer, as decided in ADR 2.

## Consequences

Session reads no longer hit the primary database, which reduces its read load.

Session keys expire automatically, so we do not need to clean up expired sessions ourselves.

Redis is one more infrastructure component that we have to operate.

If Redis restarts without persistence enabled, all sessions are lost.
