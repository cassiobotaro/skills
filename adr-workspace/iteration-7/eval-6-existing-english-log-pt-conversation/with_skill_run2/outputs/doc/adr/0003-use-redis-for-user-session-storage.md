# 3. Use Redis for user session storage

Date: 2026-07-21

## Status

Accepted

## Context

User sessions were kept in PostgreSQL, the service's primary persistence layer. Every
request that resolves a session turns into a read against the main database, and expired
sessions have to be cleaned up by the application.

## Decision

We will store user sessions in Redis instead of PostgreSQL, relying on Redis key
expiration to retire sessions automatically.

## Consequences

Read load on the main PostgreSQL database drops, since session lookups no longer reach it.

Session expiry is handled by Redis itself through key TTLs, so we no longer need
application-side cleanup of expired sessions.

We take on one more piece of infrastructure to run, monitor and upgrade.

Sessions are lost if Redis restarts without persistence enabled, which logs every user
out.
