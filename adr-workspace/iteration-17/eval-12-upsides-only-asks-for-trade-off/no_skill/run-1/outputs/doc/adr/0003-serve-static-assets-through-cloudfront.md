# 3. Serve static assets through CloudFront

Date: 2026-11-22

## Status

Accepted

## Context

Users in Asia were waiting three to four seconds for first paint, because static assets were served from the app servers in our home region. The web app's static assets are already fingerprinted, so they can be cached indefinitely without risk of serving stale content.

## Decision

We will put CloudFront in front of the web app's static assets and cache them with long-lived (immutable) cache headers.

## Consequences

Pages load faster for users far from our region, since assets are served from edge locations close to them.

The app servers no longer serve static files, which reduces their load.

Assets must keep fingerprinted filenames, since long-lived caching depends on it. Non-fingerprinted files would need a different caching policy or explicit invalidation.

We take on CloudFront as a new piece of infrastructure to configure and operate.
