# 2. Use PostgreSQL for the orders service

Date: 2026-06-04

## Status

Accepted

## Context

The orders service owns the order-creation flow, which updates inventory, payment, and the order itself as a single unit of work. Either all three changes commit together or none of them do; a partial write would leave stock reserved without a paid order, or a charge without a recorded order. This flow therefore needs ACID transactions spanning these writes.

The team already operates PostgreSQL and is comfortable with it, and the company already pays for managed PostgreSQL on Amazon RDS. The main alternative considered was MongoDB.

## Decision

We will use PostgreSQL as the datastore for the orders service, running on the existing Amazon RDS instance, rather than MongoDB.

## Consequences

The order-creation flow can wrap the inventory, payment, and order writes in a single ACID transaction, so the data stays consistent without application-level compensation logic.

We reuse the team's existing PostgreSQL experience and the RDS spend the company is already committed to, so there is no new operational tooling or vendor to adopt.

The schema becomes more rigid: the structure of the data is defined up front and enforced by the database rather than left flexible at the document level.

Schema changes turn into migrations that must run as a step of the deploy, which adds a coordination point to releases that change the data model.
