I wrote `README.md` at the repo root. It is in English, like `docs/pipeline.md`.

**Assumed reader:** a developer who runs or operates the exporter. The README covers local setup, a sample request, requeueing dead-letter messages and tests. It links to `docs/pipeline.md` for the pipeline itself.

**Left out:** license, contributing and support sections, because the repo has none of them. If you want those sections, tell me what to put in them.

**Open questions:**
- The code never declares the RabbitMQ queues `exports` and `exports.dead`. I wrote that they must already exist. Check whether something else creates them, such as broker config or infrastructure code.
- The README doesn't say how to get a Fernet key for `EXPORT_KEY`, because the repo doesn't say.
- `docs/pipeline.md` has passives with no named actor: "the payload is validated", "a job is enqueued", "the link is expired", "backups are rotated". The code covers the first three, so the README doesn't repeat them. Nothing in the repo says who rotates the backups, so I left that doc alone.

**Not run:** `make setup`, the servers, the `curl` request, the tests and `requeue_dead.py`. They need RabbitMQ, AWS and uv. I took every command, variable name, port, limit and message from the Makefile, the code and the script docstring.
