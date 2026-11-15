# 3. Version the public API by URL path

Date: 2026-07-21

## Status

Accepted

## Context

The public REST API needs a versioning scheme so that breaking changes can be released without breaking existing integrations. Two schemes were on the table: carrying the version in the URL path (`/v1`, `/v2`) and carrying it in a version header.

Our SDK clients already expect the version to appear in the URL. The gateway can route on the path, so a version can be sent to a different backend without inspecting request headers. A version in the path is also visible in logs and in a `curl` command, which makes support and debugging conversations concrete.

## Decision

We will version the public API by URL path, with the major version as the first path segment (`/v1`, `/v2`). We will not use a version header.

## Consequences

SDK clients get the versioning scheme they already assume, and the gateway can route each version to its own backend using path rules alone.

A request's version is obvious in logs and in ad-hoc `curl` calls, without having to reconstruct the headers that were sent.

URLs proliferate: every resource path exists once per active version, in routing rules, documentation and client code. To keep that bounded we will support at most two active versions at any time, which means releasing `/v(n+1)` commits us to retiring `/v(n-1)`.
