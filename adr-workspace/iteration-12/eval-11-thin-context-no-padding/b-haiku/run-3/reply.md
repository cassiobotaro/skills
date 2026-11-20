I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, status Accepted, dated 2026-11-20. It records the decision, the autoscaling reason, and the accepted network-call-per-read downside. I did not touch 0001 or 0002.

Questions before this is final (none block the file as written):

1. Were other options considered, such as EFS or keeping disks with a drain step? If so, a line on each and why S3 won would make the Context and Consequences stronger. I left them out because you did not mention them.
2. Are there other consequences you accepted, for example cost, latency, migration of files already on local disks, or a change to how uploads are served? I only recorded the one you gave me.
3. Does this apply to every user-uploaded file, or only some kinds? The Decision says all of them are moving.
4. Is the decision final (Accepted), or is it still awaiting sign-off (in which case it should be Proposed)?
