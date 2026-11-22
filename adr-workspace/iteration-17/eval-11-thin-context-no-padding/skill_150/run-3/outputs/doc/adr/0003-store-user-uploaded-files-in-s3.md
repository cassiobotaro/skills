# 3. Store user-uploaded files in S3

Date: 2026-11-22

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the app servers. Next quarter the app servers will move into an autoscaling group, where instances are replaced without keeping their disks. Files kept on an instance's local disk would be lost when that instance is replaced.

## Decision

We will store user-uploaded files in S3 instead of on the app servers' local disk.

## Consequences

Uploaded files no longer depend on the lifetime of any app server instance, so instances can be replaced freely in the autoscaling group.

Every file read becomes a network call to S3 instead of a local disk read. The team accepted this cost.

Files that are currently on the app servers' local disks will need to be moved to S3 before those instances are replaced.
