I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, status Accepted, dated 2026-11-15. It follows ADR 2 in the existing log.

- **Context:** uploads sit on the app servers' local disk, and next quarter's autoscaling group replaces instances without keeping their disks.
- **Decision:** we will store user-uploaded files in S3.
- **Consequences:** files survive instance replacement, and every file read becomes a network call, which is the downside you accepted.

I kept it to what you told me. If the team also weighed alternatives, such as a shared network filesystem, or has a migration plan for the files already on disk, tell me and I'll add them. I didn't want to guess at either.
