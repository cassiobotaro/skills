# ADR 0001: Replace Redis

- Status: Proposed
- Date: 2026-06-04
- Deciders: TODO (add the people who own this decision)

## Context

`session-api` currently relies on Redis as a backing store (see `docker-compose.yml`,
which runs `redis:7`). For this service, Redis most likely holds session data.

We want to replace Redis. This ADR records that intent. However, the key details of
the decision have not yet been provided, so they are marked as **TODO** below and
must be filled in before this ADR can move from *Proposed* to *Accepted*. Approving
this ADR without those details would mean committing to a change whose motivation and
target are undefined.

### Open questions that must be answered

1. **Why are we replacing Redis?** What problem are we solving (cost, operational
   burden, scaling limits, licensing, durability, vendor consolidation, team
   familiarity, something else)?
2. **What are we replacing it with?** (e.g. a managed cache, an in-process store,
   PostgreSQL, Memcached, DynamoDB, Valkey, a different managed Redis-compatible
   service, etc.)
3. **What data does Redis currently hold**, and what are the durability /
   consistency / latency requirements for that data?
4. **What is the migration / cutover plan**, and is downtime acceptable?

## Decision

We will replace Redis in `session-api`.

> **TODO:** State the chosen replacement and the rationale. This ADR is intentionally
> incomplete until the replacement technology and the driving reason are decided.

## Considered options

> **TODO:** List the alternatives that were evaluated and why the chosen option won.
> At minimum, document:
>
> - Keeping Redis (the status quo / "do nothing" baseline) and why it was rejected.
> - The selected replacement.
> - At least one other candidate that was considered and not selected.

## Consequences

### Positive

> **TODO:** What gets better once Redis is replaced (depends on the chosen option).

### Negative / risks

- Migration effort and risk of data loss during cutover for any data currently in Redis.
- Code that depends on Redis-specific features (TTL/expiry, pub/sub, atomic ops,
  Lua scripting, data structures) may need to be reworked if the replacement does
  not offer equivalents.
- `docker-compose.yml` and any deployment/IaC, client libraries, and configuration
  will need to be updated.

### Neutral / follow-up

- Update `docker-compose.yml` to remove the `redis` service and add the replacement.
- Update application configuration and connection code.
- Update local-development and CI setup, plus documentation.

## Notes

This ADR was drafted from a deliberately vague request ("we are going to replace
Redis") with no replacement target or rationale specified. The placeholders above are
intentional and should be completed by the deciders rather than guessed at.
