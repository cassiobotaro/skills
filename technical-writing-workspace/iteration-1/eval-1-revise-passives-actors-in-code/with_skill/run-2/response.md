I rewrote `docs/pipeline.md` in place so each step names what does it. I did not run anything.

- **Actors:** I looked each one up in the code.
  - The gateway (`exporter/gateway.py`) validates the payload, enqueues the job and returns `202`.
  - The worker (`exporter/worker.py`) picks up the job, builds the CSV, encrypts it, uploads it, requeues failures and moves a job to `exports.dead`.
  - The notifier (`exporter/notifier.py`) emails the link, and the worker calls it.
- **Fact corrected:** the old text said the job is "retried up to three times". The code makes three attempts in total, which is two retries, and the alert says "failed three times". I wrote "after three failed attempts". Check that this is the meaning you want.
- **Link expiry:** I changed "The link is expired after 24 hours" to "The link expires after 24 hours". The link is an S3 presigned URL with a 24-hour `ExpiresIn`, so it expires by itself.
- **Open question:** "Backups of the bucket are rotated weekly" is unchanged. Nothing in the repository says what rotates them, and I did not guess. What does, and where is it configured? Once you know, I can name it.

I assumed the reader is a developer or on-call engineer who is new to this service.
