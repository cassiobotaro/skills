# 2. Expose public API as REST

Date: 2025-08-04

## Status

Accepted

## Context

Partners integrate with our platform from many languages and frameworks. The integration teams we surveyed are most familiar with plain HTTP APIs.

## Decision

We will expose the public API as a REST API over HTTPS, with JSON request and response bodies.

## Consequences

Partners can integrate with standard HTTP clients and no special tooling.

We take on the work of documenting resources, status codes and pagination conventions ourselves.
