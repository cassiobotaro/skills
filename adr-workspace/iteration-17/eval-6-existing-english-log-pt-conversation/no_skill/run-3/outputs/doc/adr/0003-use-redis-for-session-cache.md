# 3. Use Redis for user session cache

Date: 2026-11-22

## Status

Accepted

## Context

User sessions are read on nearly every request. Storing them in PostgreSQL (the primary
persistence layer, see [ADR 2](0002-use-postgresql-for-persistence.md)) puts constant read
load on the main database. Sessions also need to expire, which in PostgreSQL would require
a cleanup job.

## Decision

We will store user sessions in Redis instead of PostgreSQL, relying on key TTLs for
automatic expiration. PostgreSQL remains the primary persistence layer for all other data.

## Consequences

Read load for sessions is removed from the main PostgreSQL database.

Expired sessions are removed automatically by Redis, with no cleanup job.

Redis is one more infrastructure component to operate, monitor and secure.

If Redis restarts without persistence enabled, all sessions are lost and users must log in
again.
