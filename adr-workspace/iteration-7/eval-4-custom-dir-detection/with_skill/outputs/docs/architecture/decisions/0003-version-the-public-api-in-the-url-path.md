# 3. Version the public API in the URL path

Date: 2026-07-21

## Status

Accepted

## Context

The public API needs a versioning scheme so that we can ship breaking changes without
breaking existing integrations. Two options were on the table: carrying the version in
the URL path, or carrying it in a version header.

Our SDK clients already expect the version to appear in the URL. The gateway can route
on the version when it is part of the path. A version that is visible in the URL is also
visible in logs and in a `curl` command, without inspecting request headers.

## Decision

We will version the public API in the URL path — `/v1`, `/v2` — rather than through a
version header.

## Consequences

SDK clients get the shape they already expect, and the gateway can route traffic per
version.

Requests are easier to read in logs and to reproduce with `curl`, because the version is
part of the address.

URLs proliferate: every resource exists once per active version. To keep that bounded, we
will support at most two active versions at any one time, which means retiring an old
version is a recurring piece of work rather than a one-off.
