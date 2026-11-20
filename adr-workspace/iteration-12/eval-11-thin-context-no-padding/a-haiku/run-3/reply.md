I wrote the ADR for moving user-uploaded files to S3: `doc/adr/0003-store-user-uploaded-files-in-s3.md`, status Accepted. It records the reason (the app servers join an autoscaling group next quarter and replaced instances lose their disks) and the downside you accepted (every file read is a network call).

The record is short because that is what you gave me. Before you rely on it, please answer these, since the ADR does not cover them and I did not want to invent them:

1. Did you consider alternatives, such as a shared network filesystem (EFS) or keeping the files on a volume that survives instance replacement? If so, what made S3 win? Context and Decision are silent on this.
2. Are there other consequences the team accepted, for example migrating the files already on the servers, S3 cost, upload or read latency, or the IAM and access changes? I have only recorded the network-call downside.
3. Is the decision final, or does it still need sign-off? I recorded it as Accepted because you said "we're moving". If it still needs agreement, I can change it to Proposed.

If you answer these, I will add the answers to Context and Consequences. If the answers change the decision itself, the record becomes a new ADR and this one stays as it is.
