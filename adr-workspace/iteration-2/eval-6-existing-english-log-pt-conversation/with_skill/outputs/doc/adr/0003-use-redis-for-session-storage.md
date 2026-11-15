# 3. Use Redis for session storage

Date: 2026-06-07

## Status

Accepted

## Context

User sessions are currently stored in PostgreSQL, the primary persistence layer. Every
request that reads or refreshes a session adds read load to the main database, competing
with the transactional workload it was chosen for.

Sessions are also short-lived and need to expire. Enforcing that expiry in PostgreSQL
means scheduled cleanup of stale rows, whereas a store with native key expiration would
handle it automatically.

## Decision

We will use Redis as the store for user session data, instead of keeping sessions in
PostgreSQL. Session keys will be given a time-to-live so they expire automatically.

## Consequences

Read load for session lookups moves off the primary PostgreSQL database, freeing it for
the transactional workload.

Sessions expire on their own through Redis key TTLs, removing the need for scheduled
cleanup of stale session rows.

Redis becomes an additional infrastructure component that the team has to deploy,
monitor, and operate.

If Redis restarts without persistence configured, the sessions it holds are lost and
users are signed out.
