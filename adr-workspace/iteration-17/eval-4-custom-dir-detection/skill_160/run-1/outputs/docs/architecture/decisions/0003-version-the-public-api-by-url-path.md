# 3. Version the public API by URL path

Date: 2026-11-22

## Status

Accepted

## Context

The public API needs a versioning scheme. The two options considered were putting the version in the URL (`/v1`, `/v2`) or sending it in a version header.

## Decision

We will version the public API by URL path (`/v1`, `/v2`) instead of using a version header.

We chose this because our SDK clients already expect URL versioning, because it lets the gateway route requests by version, and because the version is obvious in logs and in `curl` commands.

## Consequences

SDK clients get the versioning style they already expect.

The gateway can route by version, and the version is visible in logs and `curl` commands without inspecting headers.

URLs proliferate as new versions are added.

We will keep at most two versions active at the same time, so older versions have to be retired to make room for new ones.
