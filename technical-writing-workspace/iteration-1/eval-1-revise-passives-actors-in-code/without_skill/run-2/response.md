I rewrote `docs/pipeline.md` so every step names what performs it. I read `gateway.py`, `worker.py`, `notifier.py`, `requeue_dead.py` and `alerts.yaml` to get the actors right. I didn't run anything.

- **Actors:** the page now names the gateway, the queue, the worker and the notifier. Each step is in the active voice and says which component does it. The old passives ("a job is enqueued", "the link is expired") hid this.
- **Numbered steps:** Request and Processing are now numbered lists in code order.
- **Details from the code:**
  - The gateway answers `422` when `account_id` is missing and `413` when `rows` is above 100,000.
  - The file is encrypted with Fernet and uploaded as `<account_id>/<delivery_tag>.csv.enc`.
  - The download link is a presigned S3 URL, sent by SES.
- **Retries:** the old text said "retried up to three times". The code makes three attempts in total (`MAX_ATTEMPTS = 3`), and the third failure goes to `exports.dead`.
- **Operations:** I added the dead-letter alert and `scripts/requeue_dead.py`, because they belong to the same flow.
- **Email failures:** the notifier runs inside the worker's retry block. If the email fails, the job runs again and uploads a new file. I documented this because it's easy to miss.

**Backups:** I couldn't find anything in the repo that rotates bucket backups. I left the sentence as it was and added a TODO comment under that heading. Who rotates them, and where is that configured (a bucket lifecycle rule, an infrastructure job)? Once you tell me, I'll name them on the page. If nothing rotates them, remove the section.
