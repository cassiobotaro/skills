I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, with status Accepted and today's date, 2026-11-22. It follows the existing log (0001 and 0002), so it is number 3. I didn't edit any other file.

- **Context:** uploads sit on the app servers' local disk today, and next quarter the servers move into an autoscaling group where instances are replaced without keeping their disks.
- **Decision:** "We will store user-uploaded files in S3 instead of on the app servers' local disk."
- **Consequences:** files no longer depend on any single server's life. Every file read becomes a network call, which the team accepted in return for being able to replace instances freely.

You didn't mention any alternatives you considered, so the record doesn't list any. If you want, tell me what else was on the table, such as a shared network filesystem. I can mention it in the Context, but I'd need the actual reasons it was passed over.
