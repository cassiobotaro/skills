# 3. Use gRPC for internal communication

Date: 2026-01-12

## Status

Accepted

## Context

Internal services call the session service on every authenticated request. The team wants typed contracts between services and lower serialization overhead than JSON over HTTP.

## Decision

We will expose the session service's internal API over gRPC, with contracts defined in Protocol Buffers.

## Consequences

Service contracts are explicit and versioned in .proto files.

Debugging requires gRPC-aware tooling; plain curl is no longer enough.
