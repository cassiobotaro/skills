I wrote ADR 3, `doc/adr/0003-store-user-uploaded-files-in-s3.md`, with status Accepted. It records the move of user-uploaded files from the application servers' local disk to S3, the reason (the autoscaling group replaces instances without keeping their disks), and the accepted downside (every file read becomes a network call).

The record is short because you gave me the decision, the reason and the trade-off, and nothing else. Before you rely on it, four questions:

1. Were other options on the table, such as a shared network file system (EFS) or keeping the local disk and syncing it? If so, I can add them to Context with the reason each was rejected.
2. What happens to the files already on the app servers' disks? A migration plan is a consequence the ADR should name, but I have not guessed at one.
3. Are there other consequences you accepted, for example S3 cost, how the app gets access to the bucket (IAM or presigned URLs), or behaviour when S3 is unreachable? Consequences should list all of them, so I left these out rather than invent them.
4. Should a later decision touch this one, for example a CDN in front of S3? If so it would be a new ADR that supersedes or amends 0003.

Once you answer, I will update the Consequences and Context sections of 0003 if the answers add anything. Because the ADR is Accepted, I would add those details by editing the body, which the skill normally forbids. If you prefer that the ADR stays exactly as written, I can record the extra facts in a new ADR instead.
