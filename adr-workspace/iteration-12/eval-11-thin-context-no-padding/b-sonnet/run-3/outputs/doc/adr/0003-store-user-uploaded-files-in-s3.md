# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files currently live on the app servers' local disk. Next quarter the app servers are going into an autoscaling group, where instances get replaced without keeping their disks.

## Decision

We will store user-uploaded files in S3 instead of on the app servers' local disk.

## Consequences

Uploaded files no longer depend on the lifetime of any single app server, so instances in the autoscaling group can be replaced freely.

Every file read becomes a network call instead of a local disk read. The team accepted this downside.
