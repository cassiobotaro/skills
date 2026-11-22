I wrote `README.md` at the repository root. I ran none of its commands. Every command, variable name, port, status code and limit comes from the `Makefile`, `pyproject.toml`, the code under `exporter/`, `scripts/requeue_dead.py` and `deploy/alerts.yaml`.

**Reader I assumed:** a developer or operator who has just found the repo and needs to run it, call it and handle failed exports. Tell me if you meant a different reader.

**Open questions, marked as `TODO` comments at the end of the README:**
- **License:** there is no `LICENSE` file. Which license applies?
- **Support:** where should people ask for help (channel, issue tracker or on-call contact)?
- **RabbitMQ and AWS setup:** the repo has no compose file or setup instructions, so the README lists them as prerequisites and doesn't say how to provision them. Is there a standard local setup I should link to?

**Things I noticed in the code:**
- **Download email recipient:** `notifier.py` sends the email to `<account_id>@accounts.example.com`. That looks like a placeholder domain. The README repeats it as written, so correct it if the domain is wrong.
- **Failed jobs are acknowledged:** `worker.py` acknowledges the original message even after a failed attempt. It republishes the job to `exports`, or to `exports.dead` on the third failure.
- **`docs/pipeline.md` is passive:** it says "the payload is validated" and "a job is enqueued" without naming who does it, and it doesn't mention that oversized requests get a `413`. I left it alone, since you asked only for the README. I can rewrite it with the actors from the code.
