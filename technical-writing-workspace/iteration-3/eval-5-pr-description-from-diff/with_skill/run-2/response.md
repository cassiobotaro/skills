**Title:** Reject uploads above 1 MiB with 413 (OPS-412)

**Description**

`upload` in `importer/handler.py` now returns `413` when the `Content-Length` header is above `MAX_BODY_BYTES` (1,048,576 bytes), and it reads the body in chunks. Before, it called `request.body()` and held the whole body in memory. A huge CSV upload got prod workers OOM-killed (OPS-412).

**Changes**

- `upload` compares `Content-Length` to `MAX_BODY_BYTES` before it reads anything. Above the limit, it returns `413`.
- `upload` iterates `request.stream()` and passes each chunk to `parse_csv_chunk`. It no longer calls `parse_csv` on the full body.
- `test_upload_rejects_body_above_limit` posts `1_048_576 + 1` bytes and expects `413`.

**Verify**

Run `pytest tests/test_handler.py::test_upload_rejects_body_above_limit`. It should pass. I haven't run it.

**Look closely at**

- **Requests without `Content-Length`:** The header defaults to `0`, so a request that omits it, such as chunked transfer encoding, passes the check. The limit only holds for clients that send the header.
- **`rows` still grows without a bound:** `upload` still collects every parsed row in `rows` before it calls `store`. Streaming lowers the peak from "raw body plus parsed rows" to "parsed rows". For an upload that skips the header check, memory still scales with file size.
- **Chunk boundaries:** `parse_csv_chunk` receives arbitrary network chunks. Check that it handles a row split across two chunks, because the diff doesn't show its implementation.

**Not in this change**

- A limit enforced while streaming, for requests without `Content-Length`.
- Writing rows to `store` in batches instead of accumulating them.
- Making the limit configurable.

---

Notes for you:

- I wrote this for a reviewer on the importer service. They haven't seen the branch, and they read the description before they open the diff.
- The "Look closely at" items come from reading the diff alone. If the service has a body-size limit at the proxy or framework layer, or if `parse_csv_chunk` already buffers partial rows, drop or adjust those bullets. I didn't see either.
- I didn't know whether OPS-412 should link to your tracker. Add the URL if you want it.
- The "Not in this change" list is my reading of what the diff leaves out. Remove any item you plan to include.
- I didn't run the test, so the "should pass" line is untested.
