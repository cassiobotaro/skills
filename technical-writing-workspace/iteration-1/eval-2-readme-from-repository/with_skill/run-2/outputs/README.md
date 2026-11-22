# exporter

`exporter` generates CSV exports for an account. A FastAPI gateway accepts an export request and queues it on RabbitMQ. A worker builds the CSV, encrypts it, uploads it to S3, and emails the account a download link that expires after 24 hours.

This page covers running the gateway and the worker locally, and requeuing failed exports. The [pipeline description](docs/pipeline.md) covers what happens to a request in more detail.

## Prerequisites

- Python 3.12 or later and [uv](https://docs.astral.sh/uv/)
- A RabbitMQ server with the queues `exports` and `exports.dead`. The code does not declare them. <!-- TODO: say who creates the queues (a deploy step, or you by hand), and with which settings. -->
- An S3 bucket, and AWS credentials that can write to it and send email through SES
- <!-- TODO: say which SES setup the sender address needs, and which AWS region the code uses. -->

## Run it

1. Install the dependencies:

   ```bash
   make setup
   ```

2. Set the environment variables. The gateway needs `QUEUE_URL`. The worker needs all four.

   | Variable | Used by | Holds |
   |---|---|---|
   | `QUEUE_URL` | gateway, worker, `scripts/requeue_dead.py` | AMQP URL of the RabbitMQ server |
   | `EXPORT_KEY` | worker | Fernet key that encrypts each CSV |
   | `EXPORT_BUCKET` | worker | S3 bucket that receives the encrypted files |
   | `MAIL_FROM` | worker | Sender address of the download-link email |

3. Start the gateway on port 8080:

   ```bash
   make run-gateway
   ```

4. In a second terminal, with the same variables set, start the worker:

   ```bash
   make run-worker
   ```

5. Request an export:

   ```bash
   curl -X POST localhost:8080/exports \
     -H 'content-type: application/json' \
     -d '{"account_id": "acct-1", "rows": 10}'
   ```

   The gateway answers `202` with `{"status":"queued"}`. The worker then uploads `acct-1/<delivery tag>.csv.enc` to the bucket and emails the link to `acct-1@accounts.example.com`.

## The request

`POST /exports` takes a JSON body:

- `account_id` (required). The gateway answers `422` without it.
- `rows`. The gateway answers `413` when the value is above 100,000.

## Requeue failed exports

After a job fails three times, the worker moves it to `exports.dead`. The `ExportsDeadLetterHigh` alert in `deploy/alerts.yaml` pages when that queue holds more than 10 messages for 5 minutes.

To move messages back to `exports`, run the script with `QUEUE_URL` set:

```bash
uv run python scripts/requeue_dead.py --dry-run    # count the messages, move nothing
uv run python scripts/requeue_dead.py --limit 50   # move at most 50 messages (default 100)
```

The script prints `would move N message(s)` for a dry run and `moved N message(s)` otherwise.

## Develop

Run the tests with:

```bash
make test
```

<!-- TODO: the repository has no tests yet; remove this note when it does, or say where they live. -->

## License and help

<!-- TODO: the repository has no LICENSE file and names no contact or channel. Add both. -->
