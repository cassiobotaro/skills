# 3. Version the public API by URL

Date: 2026-06-04

## Status

Accepted

## Context

Our public API (see [2. Expose public API as REST](0002-expose-public-api-as-rest.md)) will evolve over time, and we need a strategy for introducing breaking changes without disrupting existing integrations. The two options we considered were embedding the version in the URL path (`/v1`, `/v2`) and carrying the version in a request header.

Our SDK clients already expect URL-based versioning, the gateway can route by version when it is part of the path, and a version in the URL stays obvious in logs and in ad-hoc `curl` requests.

## Decision

We will version the public API by URL path (`/v1`, `/v2`, ...) rather than by a version header.

## Consequences

SDK clients get the versioning scheme they already expect, with no extra configuration.

The gateway can route requests to the right backend by inspecting the version segment of the URL.

The active version is visible in logs and in `curl` invocations, which makes debugging and support easier.

URLs will proliferate as new versions are added. To keep this manageable, we will support at most two active versions at the same time, retiring the oldest when a third would otherwise be introduced.
