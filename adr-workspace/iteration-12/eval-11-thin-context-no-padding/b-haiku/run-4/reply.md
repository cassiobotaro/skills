I wrote ADR 0003, "Store user-uploaded files in S3", as Accepted, in doc/adr/ next to the existing 0001 and 0002. It records the move from app-server local disk to S3, the autoscaling reason, and the accepted cost of a network call on every file read.

The record is short because I only wrote what you told me. Three questions before you rely on it:

1. Were other options considered, such as EFS or keeping the disks? If so, a line on each and why they were rejected would strengthen the Context.
2. Are there other consequences you accepted or expect, such as migrating the files already on the app servers, access control on S3 objects, or S3 cost? Consequences must list all of them, so I added nothing you did not state.
3. Is the decision final (Accepted), or still waiting for sign-off (Proposed)? I used Accepted because you wrote "we're moving".
