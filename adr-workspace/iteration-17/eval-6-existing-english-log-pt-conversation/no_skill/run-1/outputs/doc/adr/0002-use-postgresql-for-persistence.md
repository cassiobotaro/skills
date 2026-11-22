# 2. Use PostgreSQL for persistence

Date: 2026-05-12

## Status

Accepted

## Context

The service needs a relational store with strong transactional guarantees. The team has
operational experience with PostgreSQL and the platform team already runs managed
PostgreSQL clusters.

## Decision

We will use PostgreSQL as the primary persistence layer for the service.

## Consequences

Schema migrations become part of the deployment pipeline and must be reviewed.

We depend on the platform team's managed clusters for backups and failover.
