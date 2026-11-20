# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently stored on the local disk of the app servers. The app
servers are going into an autoscaling group next quarter, and instances in that group are
replaced without keeping their disks, so files kept on instance disks would not survive
the replacement.

## Decision

We will move user-uploaded files from the app servers' local disk to Amazon S3.

## Consequences

Every file read becomes a network call. We accept this downside.
