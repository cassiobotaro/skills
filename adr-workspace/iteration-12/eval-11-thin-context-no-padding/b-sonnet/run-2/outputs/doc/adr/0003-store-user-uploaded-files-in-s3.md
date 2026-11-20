# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently stored on the app servers' local disk. Next quarter the app servers will move into an autoscaling group, where instances are replaced without keeping their disks.

## Decision

We will store user-uploaded files in S3 instead of on the app servers' local disk.

## Consequences

Uploaded files no longer depend on the life of any single app server, so instances in the autoscaling group can be replaced freely.

Every file read becomes a network call instead of a local disk read. The team has accepted this downside.
