I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, with status Accepted and today's date, 2026-11-22. The log already had 0001 and 0002, so this is 0003. No existing ADR was touched.

- **Context:** uploads sit on the app servers' local disk, and the autoscaling group next quarter replaces instances without keeping their disks.
- **Decision:** we will store user-uploaded files in S3.
- **Consequences:** files no longer depend on any single instance, and every file read becomes a network call. I recorded that call as the cost you accepted.

I only used the reasons you gave. I didn't add alternatives such as EFS, or anything about migrating existing files, because you didn't mention them. If either was discussed, tell me and I'll add it, or you can cover it in a follow-up ADR.
