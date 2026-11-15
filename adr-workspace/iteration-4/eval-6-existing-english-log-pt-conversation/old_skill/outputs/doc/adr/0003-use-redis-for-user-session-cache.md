# 3. Use Redis for user session cache

Date: 2026-06-07

## Status

Accepted

## Context

User sessions are currently stored in PostgreSQL, which is also the primary persistence
layer for the service. Every request that reads or refreshes a session adds read load to
the main database, competing with the transactional workload it was chosen to serve.
Sessions are also short-lived and need to expire, but PostgreSQL has no built-in
key-expiration mechanism, so expiry has to be handled in application code or by periodic
cleanup jobs.

## Decision

We will use Redis to store the user session cache, instead of keeping sessions in
PostgreSQL. Session reads and writes will go to Redis, and session keys will rely on
Redis's native time-to-live for automatic expiration.

## Consequences

Read load is taken off the primary PostgreSQL database, leaving more of its capacity for
the transactional workload.

Session expiration is handled automatically by Redis key TTLs, so no separate cleanup
job is needed.

We now operate an additional infrastructure component, with its own deployment,
monitoring, and failure modes to manage.

Sessions are lost if Redis restarts without persistence enabled, which means a restart
can log users out.
