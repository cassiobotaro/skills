# 3. Serve static assets through CloudFront

Date: 2026-11-22

## Status

Accepted

## Context

Users in Asia were waiting three to four seconds for first paint of the web app. The app's static assets are already fingerprinted, so they can be cached indefinitely.

## Decision

We will put CloudFront in front of the web app's static assets.

## Consequences

Pages load faster for users far from our region.

The app servers no longer serve static files.
