# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the application servers.

The application servers are going into an autoscaling group next quarter. Instances in that group are replaced without keeping their disks, so files kept on an instance's local disk would not survive the replacement.

## Decision

We will store user-uploaded files in Amazon S3 instead of on the local disk of the application servers.

## Consequences

Every read of an uploaded file becomes a network call to S3. We accepted this trade-off.

Application servers no longer hold uploaded files on local disk, so instances in the autoscaling group can be replaced without losing them.
