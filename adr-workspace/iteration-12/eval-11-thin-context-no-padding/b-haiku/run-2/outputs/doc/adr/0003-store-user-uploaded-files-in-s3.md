# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the application servers. Next quarter the application servers go into an autoscaling group, and instances in that group are replaced without keeping their disks, so files stored on local disk would not survive an instance replacement.

## Decision

We will move user-uploaded files from the application servers' local disk to S3.

## Consequences

Every file read becomes a network call to S3. We accepted this trade-off.

Uploaded files no longer depend on the lifetime of an individual application server, so instances in the autoscaling group can be replaced without losing them.
