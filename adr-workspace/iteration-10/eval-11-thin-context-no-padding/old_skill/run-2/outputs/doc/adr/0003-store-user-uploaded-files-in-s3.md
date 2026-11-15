# 3. Store user-uploaded files in S3

Date: 2026-11-15

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the app servers. Next quarter the app servers move into an autoscaling group, where instances are replaced without keeping their disks. Files kept on local disk would be lost whenever an instance is replaced.

## Decision

We will store user-uploaded files in S3 instead of on the app servers' local disk.

## Consequences

Uploaded files no longer depend on the lifetime of any single app server, so instances in the autoscaling group can be replaced freely.

Every file read becomes a network call to S3 instead of a local disk read. We accepted this downside.
