I wrote `README.md` at the repo root. I haven't run any of the commands in it.

It covers:
- What the service does and how a request moves through it: the gateway queues the job, the worker builds, encrypts and uploads the CSV, and the notifier emails a 24-hour link.
- Requirements, setup, and the four environment variables (`QUEUE_URL`, `EXPORT_BUCKET`, `EXPORT_KEY`, `MAIL_FROM`).
- How to run the gateway and worker, an example `curl` request, and the status codes: 202 queued, 422 missing `account_id`, 413 more than 100,000 rows.
- How to run the tests, and the dead-letter alert and the `requeue_dead.py` script.
- A short map of the directories.

Some things to check:
- **Queues:** the code never declares the `exports` and `exports.dead` queues, so the README tells the reader to create them first. Correct that if your broker setup creates them elsewhere.
- **Retry counts:** requeued messages go out without the `x-attempts` header. The README says they get three fresh attempts, which follows from reading `requeue_dead.py` and `worker.py`.
- **Backups:** `docs/pipeline.md` says bucket backups rotate weekly, but nothing in the repo does that, so I left it out.
- **CSV contents:** `build_csv` only produces placeholder rows, and the README doesn't describe the CSV format.
