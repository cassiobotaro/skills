# 3. Version the public API by URL

Date: 2026-06-07

## Status

Accepted

## Context

Our public API needs an explicit versioning strategy so we can evolve it without breaking existing integrations. The two candidates on the table were carrying the version in the URL path (`/v1`, `/v2`) and carrying it in a request header.

Our SDK clients already expect the version to live in the URL path. Our gateway can route requests by version when the version is part of the path. And a path-based version is visible directly in logs and in ad-hoc `curl` calls, with no need to inspect headers.

## Decision

We will version the public API in the URL path, exposing each major version under its own prefix (`/v1`, `/v2`), rather than selecting the version through a request header.

## Consequences

SDK clients work without change, since the URL is the form they already expect.

The gateway can route traffic per version using the path alone.

The active version is obvious in logs and in `curl` invocations, which makes debugging and support easier.

URLs proliferate as versions accumulate. To contain this, we will keep at most two versions active at the same time.
