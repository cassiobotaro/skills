# 3. Put CloudFront in front of static assets

Date: 2026-11-22

## Status

Accepted

## Context

Users in Asia were waiting three to four seconds for first paint of the web app. The app's static assets are already fingerprinted, so they can be cached indefinitely.

## Decision

We will put CloudFront in front of the web app's static assets and cache them with no expiry.

## Consequences

Pages load faster for users far from our region.

The app servers no longer serve static files.
