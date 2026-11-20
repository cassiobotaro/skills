I wrote the ADR as 0003, next after the two already in `doc/adr/`. It is "Store user-uploaded files in S3", status Accepted, dated 2026-11-20.

The Context holds only your two facts. Files sit on the app servers' local disk today, and the autoscaling group next quarter replaces instances without keeping their disks. Consequences records that files survive instance replacement, and that every read becomes a network call, which you accepted. I added nothing else, such as latency figures, cost, or alternatives you didn't mention.

Two optional questions, if you want the record fuller:
1. Were other options considered (EFS or a shared volume, for example)? If so, I can add them to Context.
2. Do you plan to mitigate the extra read cost, with a CDN or caching? If so, I can record that in Consequences.

Files:
- outputs/doc/adr/0003-store-user-uploaded-files-in-s3.md
