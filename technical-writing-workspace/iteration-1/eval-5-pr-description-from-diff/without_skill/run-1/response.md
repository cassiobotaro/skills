**Title:** importer: reject uploads over 1 MiB and parse CSV as a stream (OPS-412)

**Problem**

Production workers were being OOM-killed when someone uploaded a very large CSV. `upload` called `await request.body()`, which buffers the whole request in memory before parsing, so one big file could exhaust a worker's memory.

**Changes**

- Add `MAX_BODY_BYTES = 1_048_576` (1 MiB). If the `Content-Length` header is larger, `upload` returns `413` before reading any of the body.
- Read the body with `request.stream()` and parse it chunk by chunk with `parse_csv_chunk`. It no longer calls `request.body()` and `parse_csv` on the full payload.
- Add `test_upload_rejects_body_above_limit`. It posts `MAX_BODY_BYTES + 1` bytes and expects a `413`.

**Review notes**

- **The size limit relies on the `Content-Length` header.** A request with no header, such as chunked transfer encoding, counts as 0 and is not rejected. A client that sends a false header is not rejected either. Nothing in this change stops those requests from streaming an unbounded body.
- **`rows` still holds every parsed row.** `rows.extend(...)` collects all rows before `store(rows)` runs. Streaming avoids holding the raw body and the parsed rows at the same time, but memory still grows with the number of rows. With the 1 MiB header check this is bounded for honest clients only.
- **`parse_csv_chunk` and chunk boundaries.** I couldn't see its implementation. A chunk can end in the middle of a row, or in the middle of a quoted field. If the function doesn't keep state between calls, rows that span two chunks will be parsed wrongly. Please check this before merging.
- **Behavior change.** Uploads over 1 MiB that used to work now fail with `413`. If legitimate imports are larger than that, the limit needs to be higher or configurable.
- **Test coverage.** The new test covers only the oversized-body rejection. Nothing tests the streaming path or a row split across chunks.

**Testing**

- Added the unit test above. I haven't run the suite.

Note: I wrote this from the diff and your context only. I didn't run the tests or look at `parse_csv_chunk`, so the review notes are things to confirm, not confirmed bugs.
