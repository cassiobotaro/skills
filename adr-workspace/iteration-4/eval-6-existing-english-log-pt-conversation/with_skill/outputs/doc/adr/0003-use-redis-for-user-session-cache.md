# 3. Use Redis for user session cache

Date: 2026-06-07

## Status

Accepted

## Context

User sessions are currently stored in PostgreSQL, the primary persistence layer for the
service. Reading and writing session state on every request adds read load to the main
database, and expiring stale sessions requires explicit cleanup because the relational
store has no built-in notion of key expiry.

## Decision

We will store user session state in Redis instead of in PostgreSQL, using Redis key
expiration to age out sessions automatically.

## Consequences

Read load on the primary PostgreSQL database is reduced, since session lookups no longer
hit it.

Sessions expire automatically through Redis key TTLs, removing the need for explicit
cleanup of stale session rows.

We now operate an additional infrastructure component, which the platform team must
provision, monitor, and maintain.

Sessions are lost if Redis restarts without persistence configured, which can log users
out unexpectedly.
