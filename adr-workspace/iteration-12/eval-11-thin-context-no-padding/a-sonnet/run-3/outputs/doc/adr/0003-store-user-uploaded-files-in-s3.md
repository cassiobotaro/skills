# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files currently live on the app servers' local disk. Next quarter the app servers move into an autoscaling group, where instances are replaced without keeping their disks.

## Decision

We will store user-uploaded files in S3 instead of on the app servers' local disk.

## Consequences

Uploaded files no longer depend on any one app server's disk, so instances in the autoscaling group can be replaced without losing them.

Every file read becomes a network call. The team accepted this downside.
