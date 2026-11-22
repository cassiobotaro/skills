# 3. Store user-uploaded files in S3

Date: 2026-11-22

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the app servers. Next quarter the app servers move into an autoscaling group, where instances are replaced without preserving their disks. Files kept on local disk would be lost whenever an instance is replaced, and would not be visible across instances.

## Decision

We will store user-uploaded files in Amazon S3 instead of on the app servers' local disk.

## Consequences

Uploaded files survive instance replacement, so app servers can be treated as disposable.

Every file read becomes a network call to S3 instead of a local disk read. We accept this added latency and the dependency on S3 availability.

Existing files on local disks will need to be migrated to S3 before the servers move into the autoscaling group.
