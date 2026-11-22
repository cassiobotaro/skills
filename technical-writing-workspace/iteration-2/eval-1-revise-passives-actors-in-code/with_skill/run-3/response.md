I rewrote `docs/pipeline.md` so each step names the component that does it: the gateway validates, rejects and publishes, the worker generates, encrypts, uploads and retries, and the notifier sends the email. The structure and facts are unchanged, except for the retry count below.

- **Retry count corrected to match the code.** The old text said "retried up to three times". `MAX_ATTEMPTS = 3` in `exporter/worker.py` means three attempts in total, so two retries, and `deploy/alerts.yaml` also says "failed three times". The page now says "up to three attempts in total". Tell me if you meant three retries.
- **Added from the code.** The `413` status and `exports` / `exports.dead` queue names come from the gateway and worker. The link is a presigned S3 URL that S3 refuses after 24 hours.
- **Open question: backups.** Nothing in the repository rotates the bucket backups, so "Backups of the bucket are rotated weekly" stays as written, with a `TODO` comment in the file. Who or what does the rotation?

I assumed the reader is an engineer on the team who needs to debug or operate the pipeline. I didn't run anything.
