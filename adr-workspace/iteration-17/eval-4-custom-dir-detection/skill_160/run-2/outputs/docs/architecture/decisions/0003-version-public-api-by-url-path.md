# 3. Version public API by URL path

Date: 2026-11-22

## Status

Accepted

## Context

The public API needs a versioning scheme. The two options considered were putting the version in the URL (`/v1`, `/v2`) or in a version header.

Our SDK clients already expect the version to appear in the URL. A URL-based version can also be routed on at the gateway, and it is visible in logs and in `curl` commands.

## Decision

We will version the public API by URL path (`/v1`, `/v2`) instead of using a version header.

## Consequences

SDK clients get the versioning scheme they already expect. The gateway can route requests by version. The version is obvious in logs and in `curl` invocations.

URLs proliferate, since each new version adds a new set of paths.

We will keep at most two versions active at the same time.
