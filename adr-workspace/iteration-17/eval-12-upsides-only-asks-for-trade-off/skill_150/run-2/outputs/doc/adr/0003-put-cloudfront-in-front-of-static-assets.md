# 3. Put CloudFront in front of static assets

Date: 2026-11-22

## Status

Accepted

## Context

Users in Asia were waiting three to four seconds for first paint of the web app. The app's static assets are already fingerprinted, so they can be cached indefinitely. The app servers currently serve those static files themselves.

## Decision

We will put CloudFront in front of the web app's static assets and cache them with a long lifetime.

## Consequences

Pages should load faster for users far from our region, which addresses the slow first paint in Asia.

The app servers stop serving static files.

No trade-offs or alternatives were discussed when this decision was made, so none are recorded here. If costs or problems turn up later, they belong in a new ADR.
