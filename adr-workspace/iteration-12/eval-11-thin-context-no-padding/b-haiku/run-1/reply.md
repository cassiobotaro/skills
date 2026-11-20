I wrote the ADR for moving user-uploaded files to S3 as `doc/adr/0003-store-user-uploaded-files-in-s3.md` in the project's existing log (`0001` and `0002` were already there, so `0003` is the next number). It is marked Accepted, dated 2026-11-20, and has no supersede or amend links, so no existing ADR was edited.

The record contains only what you gave me: the autoscaling replacement that drops instance disks as the reason, the decision to move to S3, and the network-call-per-read downside. I did not add other consequences or alternatives.

Questions for you, since I could not ask before writing:
1. Were other options considered, such as a shared network volume or a different storage service? If so, I can add them to Context, and the reasons for rejecting them.
2. Will the files already on the app servers' disks be migrated to S3? That is a consequence of this decision and it is not recorded yet.
3. Are there other costs or trade-offs the team accepted, such as S3 request costs, latency, or the change in how uploads are written? I can add them to Consequences if you tell me.
