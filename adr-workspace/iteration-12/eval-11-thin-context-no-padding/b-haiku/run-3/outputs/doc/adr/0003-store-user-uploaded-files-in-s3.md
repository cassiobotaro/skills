# 3. Store user-uploaded files in S3

Date: 2026-11-20

## Status

Accepted

## Context

User-uploaded files are currently stored on the app servers' local disk. The app servers are going into an autoscaling group next quarter, and instances in that group are replaced without keeping their disks.

## Decision

We will move user-uploaded files from the app servers' local disk to S3.

## Consequences

Uploaded files no longer depend on the local disk of any app server, so instances in the autoscaling group can be replaced without losing them.

Every file read becomes a network call to S3. The team has accepted this downside.
