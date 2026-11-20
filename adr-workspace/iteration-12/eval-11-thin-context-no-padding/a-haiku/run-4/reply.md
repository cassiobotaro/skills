I wrote ADR 3, `doc/adr/0003-store-user-uploaded-files-in-s3.md`, as Accepted. It records the move of user-uploaded files from the app servers' local disk to S3, the autoscaling-group reason, and the accepted cost that every file read becomes a network call.

The record is short because that is all you gave me. Before you rely on it, could you tell me:

1. Which other options did the team weigh (for example EFS or a shared volume, or keeping the disks and accepting the replacement risk)? If none were discussed, I will leave the record as it is rather than invent alternatives.
2. What are the other consequences you accept, such as migrating the files that already sit on the servers, S3 cost, access control for downloads, or latency? Consequences must list all of them, not only the one you mentioned.
3. Does this apply to every file type and every service, or only to the web app? The record currently covers user-uploaded files generally.
