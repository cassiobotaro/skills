# 3. Version the public API by URL path

Date: 2026-11-22

## Status

Accepted

## Context

The public API needs a versioning scheme. The two options considered were putting the version in the URL path (`/v1`, `/v2`) or sending it in a version header.

Our SDK clients already expect the version in the URL. A path-based version can be used to route requests by version at the gateway, and it is visible in logs and in `curl` commands.

## Decision

We will version the public API by URL path (`/v1`, `/v2`) instead of by a version header. We will keep at most two versions active at the same time.

## Consequences

Clients that use our SDKs get the versioning style they already expect.

The gateway can route traffic by version, and the version of any request is obvious in logs and `curl` commands.

URLs proliferate: every new major version adds a new set of paths.

We commit to maintaining at most two active versions at once, so retiring the older version has to be planned whenever a new one is released.
