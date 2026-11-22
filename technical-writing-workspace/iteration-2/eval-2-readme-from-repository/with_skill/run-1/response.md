I wrote `README.md` at the repo root. I didn't run any commands. I took every command, port, variable and number from the Makefile, `pyproject.toml`, the code, `deploy/alerts.yaml` and `docs/pipeline.md`.

**Assumed reader:** an engineer who runs or operates the service. The README covers local setup, the failed-export path and the tests, and links to `docs/pipeline.md` for the detail.

**Left out because the repo doesn't say:**
- **License and contributing:** there is no license file and no contribution guide.
- **Where to ask for help:** the repo names no channel.
- **Backups:** `docs/pipeline.md` says the bucket backups rotate weekly, but nothing in the repo does that, so the README doesn't mention it.

**Questions for you:**
- **Broker:** is RabbitMQ the broker? I inferred it from `pika` and the `rabbitmq_queue_messages` metric.
- **Fernet key:** how should a reader generate `EXPORT_KEY`? The repo doesn't say, so the README only calls it "a Fernet key".
- **Email address:** is `<account_id>@accounts.example.com` a placeholder domain? The code hardcodes it.
