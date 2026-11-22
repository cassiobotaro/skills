# 3. Version the public API by URL path

Date: 2026-11-22

## Status

Accepted

## Context

The public API needs a versioning scheme. The two options considered were a version in the URL path (`/v1`, `/v2`) and a version header.

Our SDK clients already expect the version to appear in the URL. A path-based version also lets the gateway route requests by version, and it is visible in logs and in `curl` commands.

## Decision

We will version the public API by URL path (`/v1`, `/v2`) instead of by a version header. We will keep at most two versions active at the same time.

## Consequences

SDK clients get the versioning style they already expect.

The gateway can route traffic by version, and the version of any request is obvious in logs and `curl` output.

URLs proliferate, since each new version adds its own set of paths.

We have to retire old versions to stay within the limit of two active versions, so a new version can only ship once an older one has been shut down.
