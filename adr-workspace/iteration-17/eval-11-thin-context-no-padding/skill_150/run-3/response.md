I wrote ADR 3, "Store user-uploaded files in S3", with status Accepted and today's date, 2026-11-22. The file is `doc/adr/0003-store-user-uploaded-files-in-s3.md`. It follows ADRs 1 and 2 in the existing log, and I didn't edit either of them.

- **Context:** Uploads sit on the app servers' local disk today. The servers move into an autoscaling group next quarter, and instances there are replaced without keeping their disks.
- **Decision:** We will store user-uploaded files in S3.
- **Consequences:** Files no longer depend on any one instance, so instances can be replaced freely. Every file read becomes a network call, which the team accepted. Files already on local disks will need to be moved to S3 before those instances are replaced.

That last consequence is my inference from the move itself, not something you said. If the existing files are handled some other way, or you'd rather keep migration out of this record, tell me and I'll adjust it.

I didn't list alternatives such as EFS or a shared volume, since you didn't mention any. If you considered some, tell me and I can add them.
