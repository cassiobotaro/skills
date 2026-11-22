I wrote `README.md` at the repo root. It covers what `exporter` is, prerequisites, running the gateway and worker, the API, operating it (retries, requeue script, alert) and testing. I assumed the reader is an engineer who will run or operate the service. I took every command, variable and number from the `Makefile`, the code, `scripts/requeue_dead.py` and `deploy/alerts.yaml`. I ran no commands, including `make test`.

**Left out because the repo doesn't state it:**
- License.
- Contribution guide.
- Where to ask for help.

**Open questions:**
- **Tests:** `make test` runs `pytest`, but the repo has no tests. Confirm the target is meant to stay.
- **Queues:** nothing declares `exports` and `exports.dead`, so I told the reader to create them in RabbitMQ first. Say if some other deployment step creates them.
- **`EXPORT_KEY`:** I only wrote "Fernet key", since the repo doesn't say how to generate or store it.
- **Source of `README.md`:** it says what the code does. Two lines in `docs/pipeline.md` are passive with no actor: "the job is picked up" (the worker, per the code) and "Backups of the bucket are rotated weekly" (nothing in the repo does this, so I left it out).
