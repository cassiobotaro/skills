# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the application servers. The application servers are going into an autoscaling group next quarter, and instances in that group get replaced without keeping their disks, so files stored on an instance's local disk would be lost when that instance is replaced.

## Decision

We will store user-uploaded files in S3 instead of on the application servers' local disk.

## Consequences

Every read of a user-uploaded file becomes a network call to S3. The team has accepted this downside.

Uploaded files no longer depend on the local disk of any application server, so instances in the autoscaling group can be replaced without losing them.
