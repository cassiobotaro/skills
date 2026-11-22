# 3. Version the public API by URL path

Date: 2026-11-22

## Status

Accepted

## Context

The public API needs a versioning scheme, and the two options considered were a version in the URL (`/v1`, `/v2`) or a version header.

Our SDK clients already expect the version to appear in the URL. Our gateway can route requests by version when it is in the URL. A version in the URL is also visible in logs and in `curl` commands.

## Decision

We will version the public API by URL path (`/v1`, `/v2`) instead of by a version header. We will keep at most two versions active at the same time.

## Consequences

Clients that use our SDKs get the versioning style they already expect.

The gateway can route traffic by version, and the version of any request is obvious in logs and `curl` invocations.

URLs proliferate: each new version adds a new set of paths.

We can maintain at most two active versions at once, so a new version means retiring the oldest one.
