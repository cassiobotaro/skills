# 3. Serve static assets through CloudFront

Date: 2026-11-22

## Status

Accepted

## Context

Users in Asia were waiting three to four seconds for first paint of the web app, because static assets were served from our single region. The assets are already fingerprinted, so they can be cached indefinitely.

## Decision

We will put CloudFront in front of the web app's static assets and cache them with long-lived (immutable) cache headers.

## Consequences

Pages load faster for users far from our region.

The app servers no longer serve static files, which reduces their load.

Because assets are cached forever, every asset must keep a fingerprinted filename; changing content without changing the name would serve stale files.
