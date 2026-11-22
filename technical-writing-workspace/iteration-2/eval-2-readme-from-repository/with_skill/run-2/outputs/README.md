# exporter

`exporter` generates CSV exports on request. A FastAPI gateway accepts an export request and queues it in RabbitMQ. A worker builds the CSV, encrypts it, uploads it to an S3 bucket, and emails the account a download link that expires after 24 hours.

This page covers running the gateway and the worker locally. For the request lifecycle, see [docs/pipeline.md](docs/pipeline.md).

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A RabbitMQ broker with the queues `exports` and `exports.dead`. The code never declares them.
- An S3 bucket and an Amazon SES sender address, for the worker

## Run it

1. Install the dependencies:

   ```bash
   make setup
   ```

2. Set the environment variables. The gateway reads `QUEUE_URL`. The worker reads all four.

   | Variable | Used for |
   |---|---|
   | `QUEUE_URL` | AMQP URL of the broker |
   | `EXPORT_KEY` | Fernet key that encrypts each CSV |
   | `EXPORT_BUCKET` | S3 bucket that receives the encrypted files |
   | `MAIL_FROM` | Sender address of the download-link email |

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
     -H 'content-type: application/json' \
     -d '{"account_id": "acme", "rows": 10}'
   ```

   The gateway answers `202` with `{"status":"queued"}`. The worker then uploads the file and emails `acme@accounts.example.com` the link.

## The API

`POST /exports` takes a JSON object:

- `account_id` (required): without it the gateway answers `422`.
- `rows`: the number of rows to export. Above 100,000 the gateway answers `413`.

## Operate it

- A job that fails is retried up to three times, then moves to `exports.dead`.
- To move dead jobs back to `exports`, run `uv run python scripts/requeue_dead.py`. Add `--dry-run` to count them without moving any, and `--limit <n>` to move at most `<n>` (default 100). The script reads `QUEUE_URL`.
- The alert `ExportsDeadLetterHigh` in [deploy/alerts.yaml](deploy/alerts.yaml) pages when `exports.dead` holds more than 10 messages for 5 minutes.

## Test

```bash
make test
```

This runs `pytest -q`.
