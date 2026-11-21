`push` in `sync/client.ts` now sends records in batches of at most 500, one POST per batch. I haven't run or tested it, and there's no test setup in the repo.

- **Batch size:** it's a `MAX_BATCH_SIZE = 500` constant with a comment giving the reason. The API rejects bodies over 1 MB and the largest records are about 2 KB, so 500 records come to roughly 1 MB at worst.
- **Ordering:** batches go out sequentially, in order.
- **Errors:** the first failed batch throws the same `push failed: <status>` error as before. Batches already sent stay sent, so a failure partway through can leave the push partly applied. If you need a retry or resume strategy, the error doesn't say which batch failed.
- **Empty input:** an empty `records` array now makes no request. Before, it sent one POST with `[]`.

500 × 2 KB is about 1 MB, so the margin is thin if you count 1 MB as 1,048,576 bytes. It could exceed the limit if you count 1 MB as 1,000,000 bytes. It also leaves little room for JSON overhead such as field names and escaping. If your records ever reach the 2 KB maximum in bulk, a ceiling of 250 would give real headroom.
