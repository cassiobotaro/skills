# exporter

`exporter` is a service that generates CSV exports on request. A FastAPI gateway accepts
an export request and queues it on RabbitMQ. A worker builds the CSV, encrypts it, uploads
it to an S3 bucket, and emails the account a download link that expires after 24 hours.

This page covers running the service locally and where to find the rest. For the full
request flow, see [docs/pipeline.md](docs/pipeline.md).

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A RabbitMQ broker you can reach
- An S3 bucket and Amazon SES access, for the worker's upload and email steps

## Run it

1. Install the dependencies:

   ```bash
   make setup
   ```

2. Set the environment variables. The gateway needs `QUEUE_URL`. The worker needs all four.

   | Variable | Holds |
   |---|---|
   | `QUEUE_URL` | AMQP URL of the RabbitMQ broker |
   | `EXPORT_BUCKET` | Name of the S3 bucket that receives the encrypted files |
   | `EXPORT_KEY` | Fernet key that encrypts each file |
   | `MAIL_FROM` | Sender address of the download-link email |

3. Start the gateway, which listens on port 8080:

   ```bash
   make run-gateway
   ```

4. In a second terminal, start the worker:

   ```bash
   make run-worker
   ```

5. Request an export:

   ```bash
   curl -X POST localhost:8080/exports \
     -H 'content-type: application/json' \
     -d '{"account_id": "<account>", "rows": 10}'
   ```

   The gateway answers `202` with `{"status":"queued"}`. When the worker finishes, it
   emails the link to `<account>@accounts.example.com`.

The gateway rejects a request without `account_id` with `422`, and a request above
100,000 rows with `413`.

## Failed exports

The worker retries a failed job up to three times, then moves it to the `exports.dead`
queue. The `ExportsDeadLetterHigh` alert in [deploy/alerts.yaml](deploy/alerts.yaml)
pages when that queue holds more than 10 messages for 5 minutes.

To send the dead messages back to `exports`, with `QUEUE_URL` set:

```bash
uv run python scripts/requeue_dead.py --dry-run
uv run python scripts/requeue_dead.py --limit 50
```

`--dry-run` counts the messages and moves none. `--limit` caps how many move, and
defaults to 100.

## Test

```bash
make test
```
