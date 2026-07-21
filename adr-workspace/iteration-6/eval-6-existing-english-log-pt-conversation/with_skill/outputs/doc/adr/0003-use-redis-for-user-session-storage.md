# 3. Use Redis for user session storage

Date: 2026-07-21

## Status

Accepted

## Context

User sessions were going to be kept in PostgreSQL, the primary store chosen in ADR 2.
Session lookups happen on every authenticated request, so they add read load to the same
database that serves the transactional workload. Sessions also have a natural lifetime
and need to expire on their own, which PostgreSQL does not provide without an extra
cleanup mechanism.

## Decision

We will store user sessions in Redis instead of PostgreSQL, relying on Redis key
expiration to retire sessions automatically.

## Consequences

Read load is taken off the primary database: session lookups no longer compete with the
transactional workload.

Session expiration is handled by Redis key TTLs, so no cleanup job is needed.

We take on one more piece of infrastructure to operate, monitor, and keep available.

Sessions are lost if Redis restarts without persistence, which means users are logged
out.
