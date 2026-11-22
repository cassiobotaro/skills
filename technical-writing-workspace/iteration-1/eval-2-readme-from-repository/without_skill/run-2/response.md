I wrote `README.md` at the repo root. I did not run any of the commands in it.

It covers:
- what the service does and the path a request takes (gateway, queue, worker, S3, email);
- requirements, setup, the four environment variables (`QUEUE_URL`, `EXPORT_BUCKET`, `EXPORT_KEY`, `MAIL_FROM`), and the `make` targets;
- an example request and its status codes: 202, 422 for a missing `account_id`, and 413 above 100,000 rows;
- the dead-letter queue, the paging alert, and how to use `scripts/requeue_dead.py`.

A few things I noticed while reading the code, which the README only partly reflects:
- **No tests:** the repo has no tests, so `make test` will find nothing to run. I listed it anyway because the Makefile has the target.
- **Queues are not created:** the code never declares the `exports` and `exports.dead` queues, so the broker needs them created beforehand. The README says so.
- **Backups:** `docs/pipeline.md` says bucket backups rotate weekly, but nothing in the repo does that, so I left it out.
- **Requeued jobs:** `requeue_dead.py` drops the `x-attempts` header, so requeued jobs get three fresh attempts. The README states this.
- **Email recipient:** the email goes to `<account_id>@accounts.example.com`, which looks like a placeholder domain. Confirm it's what you want.
