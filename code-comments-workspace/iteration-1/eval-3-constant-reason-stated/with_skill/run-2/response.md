`push` in `sync/client.ts` now sends records in batches of at most 500 per request. I haven't run or tested it.

- **Batching:** batches go out one after another, each as its own POST to `/records`. If a batch fails, `push` throws the same `push failed: <status>` error as before. Batches sent before the failure stay pushed.
- **Empty input:** an empty `records` array now sends no request. Before, it sent one request with `[]`.
- **Comments:** I added two.
  - The constant `MAX_RECORDS_PER_REQUEST` has a comment giving the 1 MB request-body limit and the roughly 2 KB largest record, both from your message.
  - `push` has a comment warning that a failure partway leaves the earlier batches already pushed. Anyone calling `push` and retrying should know that.

**Margin on the 500 ceiling:** 500 records of 2 KB each come to about 1 MB, which is the API's limit. That leaves little or no room for the JSON array syntax and each record's `id` field, and none if a "KB" here means 1024 bytes. It's only safe if "about 2 KB" is an upper bound with some slack. If you want real headroom, use a lower constant such as 250, or batch by serialized size. I left it at 500 as you asked and kept this doubt out of the code comment.
