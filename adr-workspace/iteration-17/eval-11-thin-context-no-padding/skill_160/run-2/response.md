I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, status Accepted and dated 2026-11-22. It follows 0002 in the existing log, and no other file changed.

- **Context:** uploads live on the app servers' local disk, and next quarter's autoscaling group replaces instances without keeping their disks.
- **Decision:** "We will store user-uploaded files in S3 instead of on the app servers' local disk."
- **Consequences:** files no longer depend on any one server's life. The accepted cost is that every file read becomes a network call.

I kept to what you told me. The record doesn't cover migrating existing files, the access pattern, or any alternatives you considered. If any of those were part of the decision, tell me and I'll add them. If a record for the migration itself would be useful, that would be a separate ADR.
