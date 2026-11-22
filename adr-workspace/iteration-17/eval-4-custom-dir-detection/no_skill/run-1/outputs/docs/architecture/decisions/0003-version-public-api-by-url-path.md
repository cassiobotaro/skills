# 3. Version public API by URL path

Date: 2026-11-22

## Status

Accepted

Builds on [2. Expose public API as REST](0002-expose-public-api-as-rest.md)

## Context

The public API needs a versioning scheme so we can ship breaking changes without breaking existing partners. The two main options were putting the version in the URL path (`/v1`, `/v2`) or in a request header.

## Decision

We will version the public API by URL path prefix (`/v1/...`, `/v2/...`) instead of using a version header.

We will keep at most two API versions active at the same time.

## Consequences

Our SDK clients already expect URL-based versioning, so this matches their conventions.

The gateway can route requests by version using the path alone.

The version is obvious in logs and in `curl` commands, which makes debugging and support easier.

URLs proliferate: every new major version adds a new set of paths to document and operate.

Because at most two versions can be active at once, we must deprecate and retire the older version before releasing a third.
