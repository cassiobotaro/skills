I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, status Accepted, dated 2026-11-20. The log already had 0001 and 0002, so this is 0003.

It records only what you told me: uploads move from local disk to S3, the autoscaling group replaces instances without keeping their disks, and every file read becomes a network call, which the team accepted. I added nothing else, such as alternatives, latency figures or migration steps, because you didn't give them.

If you want any of these in the record, tell me and I'll add them:
1. Were other options considered, such as a shared network filesystem, and why were they rejected?
2. How will the files already on disk get to S3?
3. Is there anything planned to reduce the cost of the extra network read, such as caching or a CDN? Or is it simply accepted?
