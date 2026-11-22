# exporter

Asynchronous CSV exports. A FastAPI gateway accepts export requests and queues them on RabbitMQ. A worker builds the CSV, encrypts it, uploads it to S3, and emails the account a download link.

See [docs/pipeline.md](docs/pipeline.md) for the request lifecycle.

## How it works

```
POST /exports → gateway → queue "exports" → worker → S3 (encrypted CSV) → SES email with presigned link
                                               ↓ after 3 failed attempts
                                          queue "exports.dead"
```

- **Gateway** (`exporter/gateway.py`): validates the payload and publishes it to the `exports` queue. Returns `202 {"status": "queued"}`.
- **Worker** (`exporter/worker.py`): consumes `exports`, builds the CSV, encrypts it with Fernet, uploads it as `<account_id>/<delivery_tag>.csv.enc`, then calls the notifier. On failure it republishes the job with an `x-attempts` header. After 3 attempts it publishes the job to `exports.dead`.
- **Notifier** (`exporter/notifier.py`): sends the account (`<account_id>@accounts.example.com`) an email containing a presigned S3 link that expires after 24 hours.

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A RabbitMQ broker with the queues `exports` and `exports.dead` already created (the code does not declare them)
- An S3 bucket and SES, with AWS credentials available to boto3 in the usual way

## Setup

```bash
make setup
```

## Configuration

Both processes read these environment variables:

| Variable | Used by | Purpose |
|---|---|---|
| `QUEUE_URL` | gateway, worker, `scripts/requeue_dead.py` | AMQP URL of the RabbitMQ broker |
| `EXPORT_BUCKET` | worker, notifier | S3 bucket for the encrypted files |
| `EXPORT_KEY` | worker | Fernet key used to encrypt each file |
| `MAIL_FROM` | notifier | Sender address for the notification email |

AWS credentials and region are taken from the standard boto3 configuration.

## Running

```bash
make run-gateway   # uvicorn on port 8080
make run-worker    # consumes the exports queue
```

Request an export:

```bash
curl -X POST localhost:8080/exports \
  -H 'content-type: application/json' \
  -d '{"account_id": "acct-123", "rows": 500}'
```

| Status | Meaning |
|---|---|
| `202` | The job was queued |
| `422` | `account_id` is missing |
| `413` | `rows` is above 100,000 |

## Dead-letter queue

Jobs that fail three times land in `exports.dead`. The `ExportsDeadLetterHigh` alert (`deploy/alerts.yaml`) pages when more than 10 messages sit there for 5 minutes.

To move them back to `exports`:

```bash
uv run python scripts/requeue_dead.py --dry-run    # count only, move nothing
uv run python scripts/requeue_dead.py --limit 50   # move at most 50 (default 100)
```

Requeued messages are published without the `x-attempts` header, so they get three new attempts.

## Tests

```bash
make test
```
