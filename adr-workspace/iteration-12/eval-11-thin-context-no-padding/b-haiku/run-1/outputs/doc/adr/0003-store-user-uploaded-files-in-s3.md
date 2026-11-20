# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently stored on the app servers' local disk. The app servers are going into an autoscaling group next quarter, and instances in that group are replaced without keeping their disks, so files kept on instance disks would be lost when an instance is replaced.

## Decision

We will move user-uploaded files from the app servers' local disk to Amazon S3.

## Consequences

Every read of a user-uploaded file becomes a network call. We accepted this downside.
