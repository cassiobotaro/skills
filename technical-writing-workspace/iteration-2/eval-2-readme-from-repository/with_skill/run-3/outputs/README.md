# exporter

`exporter` turns an export request into an encrypted CSV file and emails the requester a
download link that expires after 24 hours. It has two processes: a FastAPI gateway that
accepts requests, and a worker that builds the file, uploads it to S3, and sends the email
through SES. The two communicate through RabbitMQ.

This README covers running the two processes locally and requeueing failed exports. For
what happens to a request from end to end, read [docs/pipeline.md](docs/pipeline.md).

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A RabbitMQ server that has the queues `exports` and `exports.dead`. The code does not
  declare them.
- An S3 bucket and an SES sender address that the worker can reach with AWS credentials

## Run it

1. Install the dependencies:

   ```bash
   make setup
   ```

2. Set the environment variables. The gateway reads `QUEUE_URL`. The worker reads all four.

   | Variable | Holds |
   |---|---|
   | `QUEUE_URL` | The RabbitMQ connection URL |
   | `EXPORT_KEY` | The Fernet key that encrypts each CSV file |
   | `EXPORT_BUCKET` | The S3 bucket that stores the encrypted files |
   | `MAIL_FROM` | The SES sender address of the download email |

3. Start the gateway on port 8080:

   ```bash
   make run-gateway
   ```

4. In a second terminal, start the worker:

   ```bash
   make run-worker
   ```

5. In a third terminal, request an export:

   ```bash
   curl -X POST localhost:8080/exports \
     -H 'Content-Type: application/json' \
     -d '{"account_id": "acme", "rows": 10}'
   ```

   The gateway answers `202` with `{"status": "queued"}`. When the worker finishes, an
   email with the download link goes to `acme@accounts.example.com`.

The gateway answers `422` when `account_id` is missing and `413` when `rows` is above
100,000.

## Requeue failed exports

The worker retries a failed job up to three times, then moves it to `exports.dead`. After
you fix the cause, move the messages back to `exports` with `scripts/requeue_dead.py`.
Set `QUEUE_URL` first.

To count the messages without moving them:

```bash
uv run python scripts/requeue_dead.py --dry-run
```

To move at most 50 messages (the default limit is 100):

```bash
uv run python scripts/requeue_dead.py --limit 50
```

The script prints `moved <n> message(s)`, or `would move <n> message(s)` with `--dry-run`.

The Prometheus rule `ExportsDeadLetterHigh` in [deploy/alerts.yaml](deploy/alerts.yaml)
pages when `exports.dead` holds more than 10 messages for 5 minutes.

## Test

```bash
make test
```

This runs `pytest -q`.
