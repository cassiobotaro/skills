# 3. Version the public API by URL path

Date: 2026-11-22

## Status

Accepted

## Context

The public API needs a versioning scheme. The two options considered were a version in the URL path (`/v1`, `/v2`) and a version header. Our SDK clients already expect the version in the URL.

## Decision

We will version the public API by URL path (`/v1`, `/v2`) instead of using a version header. We will keep at most two versions active at the same time.

## Consequences

SDK clients get the versioning scheme they already expect.

The gateway can route requests by version.

The version is obvious in logs and in `curl` commands.

URLs proliferate, since each new version adds its own set of paths.

We take on the work of maintaining at most two active versions at once, so an older version has to be retired before a third one goes live.
