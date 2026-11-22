# 3. Store user-uploaded files in S3

Date: 2026-11-22

## Status

Accepted

## Context

User-uploaded files are currently kept on the local disk of the app servers. Next quarter the app servers move into an autoscaling group, where instances are replaced without keeping their disks.

## Decision

We will store user-uploaded files in S3 instead of on the app servers' local disk.

## Consequences

Uploaded files no longer depend on the life of any single app server, so instances in the autoscaling group can be replaced freely.

Every file read becomes a network call. We accepted this cost in exchange for the ability to replace instances without losing files.
