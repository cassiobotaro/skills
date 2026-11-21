`push` in `sync/client.ts` now sends records in batches of at most 500 per request. I haven't run or tested it.

- **Batching:** `push` loops over the records in slices of 500 and sends each slice with a new private method, `pushBatch`. `pushBatch` holds the original fetch and error handling, so a failed response still throws `push failed: <status>`.
- **Comment:** the constant `MAX_RECORDS_PER_REQUEST` carries a two-line comment. It says the API rejects bodies over 1 MB and that our largest records are about 2 KB, so batches of 500 stay under the limit. Both facts are the ones you gave me.

Two things to know about the batching:
- **Margin:** 500 records at 2 KB is about 1 MB, so the margin is thin if some records run larger than 2 KB or the JSON overhead is bigger than expected. A smaller ceiling, such as 250, would leave more room. I kept 500 as you asked.
- **Partial failure:** batches are sent one after another. If one fails, `push` throws and the earlier batches stay sent, with no retry or rollback. Callers should expect a partial push.
