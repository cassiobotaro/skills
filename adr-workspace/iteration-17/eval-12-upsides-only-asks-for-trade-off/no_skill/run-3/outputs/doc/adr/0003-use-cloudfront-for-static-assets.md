# 3. Use CloudFront for static assets

Date: 2026-11-22

## Status

Accepted

## Context

Users in Asia were waiting three to four seconds for first paint of the web app, because static assets were served from our home region by the app servers.

The static assets are already fingerprinted, so they can be cached indefinitely without the risk of serving stale content.

## Decision

We will put CloudFront in front of the web app's static assets and serve them from the CDN rather than from the app servers.

## Consequences

Pages load faster for users far from our region.

The app servers no longer serve static files, which reduces their load.

Because assets are cached forever, every change to an asset must produce a new fingerprinted filename. Assets that are not fingerprinted must not be served through this cache without a shorter cache lifetime.

We take on CloudFront as a new dependency, including its configuration and cost.
