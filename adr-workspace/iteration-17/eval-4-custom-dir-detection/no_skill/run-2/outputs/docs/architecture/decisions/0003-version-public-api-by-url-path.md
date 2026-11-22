# 3. Version public API by URL path

Date: 2026-11-22

## Status

Accepted

Builds on [2. Expose public API as REST](0002-expose-public-api-as-rest.md)

## Context

The public API needs a versioning scheme so we can ship breaking changes without breaking existing partners. The two options we considered were putting the version in the URL path (`/v1`, `/v2`) or in a request header.

Our SDK clients already expect the version in the URL. We also want to route traffic by version at the gateway, and we want the version to be obvious in logs and in `curl` commands.

## Decision

We will version the public API by URL path prefix (`/v1/...`, `/v2/...`). We will not use a version header.

We will keep at most two versions active at the same time.

## Consequences

Matches what our SDK clients already expect.

The gateway can route by version using the path alone.

The version shows up directly in access logs and in `curl` commands, which makes debugging and support easier.

URLs proliferate: every new major version adds a new set of paths.

Supporting at most two active versions means we must deprecate and retire the older version before a third one can be released. We will need a deprecation process and timeline for partners.
