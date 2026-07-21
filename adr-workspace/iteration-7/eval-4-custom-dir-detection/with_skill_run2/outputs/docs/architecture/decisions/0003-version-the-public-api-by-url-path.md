# 3. Version the public API by URL path

Date: 2026-07-21

## Status

Accepted

## Context

The public API needs a versioning scheme so that we can ship breaking changes without breaking existing integrations. Two options were on the table: carrying the version in the URL path (`/v1`, `/v2`) and carrying it in a version header.

Our SDK clients already expect the version to appear in the URL. The gateway can route on the URL path, which makes a version a routing concern rather than an application concern. A version in the path is also visible in logs and in a `curl` command, without having to inspect request headers.

## Decision

We will version the public API by URL path, exposing each major version under its own prefix (`/v1`, `/v2`). We will not use a version header.

## Consequences

SDK clients get the shape they already expect, and the gateway can route traffic per version.

Requests are easier to read in logs and to reproduce by hand, because the version is part of the URL itself.

URLs proliferate: every version adds a parallel set of paths to document, monitor and operate. To bound that cost we will keep at most two versions active at the same time, which means each new version obliges us to plan the retirement of the oldest one.
