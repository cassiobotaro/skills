# 3. Store user-uploaded files in S3

Date: 2026-11-22

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the app servers. Next quarter the app servers move into an autoscaling group, where instances are replaced without preserving their disks. Files kept on local disk would be lost whenever an instance is replaced, and would not be visible to the other instances.

## Decision

We will store user-uploaded files in Amazon S3 instead of on the app servers' local disk. App servers will write uploads to S3 and read them from S3.

## Consequences

Uploaded files no longer depend on the lifecycle of any single app server, so instances can be added and replaced freely.

Every file read becomes a network call to S3, with more latency than a local disk read and a new dependency on S3 availability. We accept this cost.

Existing files on local disk will have to be migrated to S3 before the app servers move into the autoscaling group.
