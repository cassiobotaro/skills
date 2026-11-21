`push` in `sync/client.ts` now sends records in batches of at most 500 per request. I haven't run or tested it, and there were no existing tests to run.

- A `MAX_BATCH_SIZE = 500` constant sets the limit. A comment above it gives the reason: the API rejects bodies over 1 MB, and records are about 2 KB at most.
- `push` slices the records into chunks and sends them one after another. Each chunk goes through a new private `pushBatch` method, which holds the original fetch and error handling.
- Batches are sent in order. If one fails, `push` throws the same `push failed: <status>` error and does not send the remaining batches. Batches sent before the failure are not rolled back, so a retry would resend them.
- An empty array now makes no request at all. Before, it sent one request with an empty body.

At 2 KB per record, 500 records come to about 1 MB. That is right at the API's limit rather than comfortably under it, so a batch of the largest records could still be rejected. If that matters, a ceiling of about 250 would leave some headroom.
