# 3. Version the public API by URL path

Date: 2026-06-04

## Status

Accepted

## Context

The public API needs an explicit versioning strategy so that we can evolve it without breaking existing integrations. Two approaches are on the table: encoding the version in the URL path (`/v1`, `/v2`) or carrying it in a request header.

Our clients already consume the API through SDKs, and those SDKs assume a versioned URL path. The API sits behind a gateway, where routing decisions are made per request. The API is also exercised directly in logs, in support tickets, and through ad hoc `curl` calls during debugging.

## Decision

We will version the public API by URL path, exposing each version under its own prefix (`/v1`, `/v2`, and so on), rather than selecting the version through a request header.

## Consequences

The URL path is what our SDK clients already expect, so they keep working without adapting to a header-based scheme.

The gateway can route by version directly from the path, without inspecting headers.

The version in use is obvious everywhere the URL appears, including logs and `curl` commands, which makes debugging and support easier.

URLs proliferate as versions accumulate. To keep this under control, we will maintain at most two active versions at any one time, retiring older versions as new ones ship.
