# 3. Version public API by URL path

Date: 2026-11-22

## Status

Accepted

Builds on [2. Expose public API as REST](0002-expose-public-api-as-rest.md)

## Context

The public API needs a versioning scheme so we can ship breaking changes without breaking existing partners. The two options considered were putting the version in the URL path (`/v1`, `/v2`) or in a version request header.

## Decision

We will version the public API by URL path prefix (`/v1`, `/v2`), not by a version header.

Reasons:

- It is what our SDK clients already expect.
- The gateway can route by version directly from the path.
- The version is obvious in logs and in `curl` commands.

## Consequences

Routing, logging and debugging by version are simple and visible.

URLs proliferate: each new major version adds a new set of paths.

We will keep at most two versions active at the same time, so a new version means retiring the oldest one, and we must plan deprecation and sunset for partners accordingly.
