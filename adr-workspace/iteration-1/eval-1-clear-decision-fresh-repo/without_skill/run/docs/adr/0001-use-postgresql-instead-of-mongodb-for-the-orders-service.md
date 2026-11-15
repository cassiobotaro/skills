# 1. Use PostgreSQL instead of MongoDB for the orders service

Date: 2026-06-04

## Status

Accepted

## Context

The orders service is responsible for the order lifecycle. The core flow,
creating an order, is not a single isolated write: it updates inventory,
payment, and the order itself, and these updates must happen together. If any
one of them fails, none of them should be persisted, otherwise we end up with
inconsistent state such as reserved stock without a paid order, or a paid order
with no stock decrement.

This requirement points to a need for ACID transactions spanning multiple
records (and potentially multiple tables) committed atomically.

Two main options were on the table:

- **MongoDB** — a document database. While modern MongoDB does support
  multi-document transactions, they are not its primary design center, and the
  team has less operational experience running and tuning them in production.
- **PostgreSQL** — a relational database with mature, first-class support for
  ACID transactions across multiple rows and tables.

Additional factors relevant to the decision:

- The team already has solid hands-on experience with PostgreSQL, which lowers
  the operational and development risk and shortens ramp-up time.
- The company already pays for and operates Amazon RDS, so adopting PostgreSQL
  adds no new managed-infrastructure cost or vendor footprint.

## Decision

We will use **PostgreSQL** (hosted on Amazon RDS) as the primary datastore for
the orders service, instead of MongoDB.

The order-creation flow that updates inventory, payment, and the order will be
wrapped in a single PostgreSQL ACID transaction so that the three writes either
all commit or all roll back together.

## Consequences

### Positive

- The multi-write order-creation flow (inventory, payment, order) gets strong
  ACID guarantees in a single atomic transaction, eliminating the partial-update
  inconsistencies that motivated this decision.
- We reuse the team's existing PostgreSQL expertise, reducing development and
  operational risk.
- We reuse the existing, already-paid-for RDS platform, so there is no new
  infrastructure cost or new technology to operate.

### Negative

- The schema becomes more rigid. Changes to the data model must be designed and
  applied deliberately rather than written ad hoc per document.
- Database migrations become an explicit deployment step. Each schema change
  requires a migration that has to be authored, reviewed, and run as part of the
  release process, adding overhead to deploys.
