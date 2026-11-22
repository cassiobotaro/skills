# 3. Store user-uploaded files in S3

Date: 2026-11-22

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the application servers.

Next quarter the application servers move into an autoscaling group. Instances in that group are replaced without their disks being kept, so any file stored on local disk would be lost whenever an instance is replaced. Local disk is also not shared between instances, so a file uploaded through one instance would not be readable through another.

## Decision

We will store user-uploaded files in Amazon S3 instead of on the application servers' local disk. The application servers will write uploads to S3 and read them from S3.

## Consequences

Uploaded files survive instance replacement, and every instance sees the same files, so the application servers can scale in and out freely.

Every file read becomes a network call to S3 instead of a local disk read. We accept the added latency and the dependency on S3 availability.

Existing files on the current servers must be migrated to S3 before the move to the autoscaling group.
