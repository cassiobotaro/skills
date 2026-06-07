# 3. Version the public API by URL path

Date: 2026-06-07

## Status

Accepted

## Context

The public API needs an explicit versioning scheme so we can evolve it without breaking existing integrations. The two options on the table are encoding the version in the URL path (`/v1`, `/v2`) and encoding it in a request header.

Our SDK clients already assume a versioned path. We also route requests through a gateway, where the version is needed to direct traffic. The version must be easy to see when reading logs and when reproducing a request with curl.

## Decision

We will version the public API by URL path, exposing each major version under its own prefix (`/v1`, `/v2`), instead of carrying the version in a request header.

## Consequences

The scheme matches what our SDK clients already expect, so they integrate without changes.

The gateway can route by version directly from the path, with no header inspection.

The version is visible in plain sight in logs and in curl commands, which makes requests easier to read and reproduce.

URLs proliferate as versions accumulate. To contain this, we will keep at most two versions active at the same time and retire older ones.
