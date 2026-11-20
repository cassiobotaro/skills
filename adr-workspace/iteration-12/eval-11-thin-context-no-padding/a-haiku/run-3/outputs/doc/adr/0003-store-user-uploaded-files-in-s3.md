# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently kept on the local disk of the application servers.

The application servers are moving into an autoscaling group next quarter. Instances in that group are replaced without keeping their disks.

## Decision

We will store user-uploaded files in S3 instead of on the application servers' local disk.

## Consequences

Every file read becomes a network call to S3. The team accepted this downside.

Uploaded files no longer depend on the local disk of any single application instance, so replacing instances in the autoscaling group does not remove them.
