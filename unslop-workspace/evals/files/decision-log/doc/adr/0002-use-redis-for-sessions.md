# 2. Use Redis for sessions

Date: 2026-03-02

## Status

Accepted

## Context

It is important to note that session reads were a crucial source of load on PostgreSQL — robust caching was needed.

## Decision

We will store user sessions in Redis.

## Consequences

Sessions are lost when Redis restarts, which we accept. This showcases our commitment to performance.
