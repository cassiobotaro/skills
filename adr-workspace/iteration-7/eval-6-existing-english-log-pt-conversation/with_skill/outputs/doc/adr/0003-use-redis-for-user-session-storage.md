# 3. Use Redis for user session storage

Date: 2026-07-21

## Status

Accepted

## Context

User sessions are currently kept in PostgreSQL, the service's primary persistence layer.
Every request that resolves a session turns into a read against that database, so session
traffic competes with the rest of the application's load on the main store. Sessions are
also short-lived data with an expiry, and PostgreSQL has no built-in expiration for rows:
expiring them requires application or job code that we have to write and operate.

## Decision

We will store user sessions in Redis instead of PostgreSQL, relying on Redis key
expiration to retire sessions automatically.

## Consequences

Read load on the main PostgreSQL database drops, since session lookups no longer reach it.

Session expiry is handled by Redis key TTLs, so we no longer need our own cleanup
mechanism for expired sessions.

We take on one more piece of infrastructure to operate, monitor, and keep available.

Sessions are lost if Redis restarts without persistence configured.
