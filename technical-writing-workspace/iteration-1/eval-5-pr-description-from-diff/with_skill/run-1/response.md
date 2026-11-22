**Title:** Reject uploads above 1 MiB with 413 (OPS-412)

`upload` in `importer/handler.py` now returns `413` when the `Content-Length` header is above `MAX_BODY_BYTES` (1,048,576 bytes). It also reads the body as a stream and parses it chunk by chunk. Before, it called `request.body()`, which loads the whole upload into memory. Prod workers were getting OOM-killed when someone uploaded a huge CSV (OPS-412).

**How to verify**

```
pytest tests/test_handler.py::test_upload_rejects_body_above_limit
```

The new test posts 1,048,577 bytes to `/upload` and expects `413`.

**What to look at closely**

- **The limit depends on the `Content-Length` header.** When a request has no header, such as a chunked upload, the handler reads `0`, skips the check, and streams the whole body. That upload is not capped. A fix would count the bytes inside the `request.stream()` loop and return `413` once the total passes the limit. I left this out of this PR. Tell me if you want it added here.
- **A non-numeric `Content-Length` makes `int(...)` raise `ValueError`.** The handler does not catch it.
- **The handler still collects every row in `rows` and passes the full list to `store`.** Streaming does not lower peak memory by itself. The 1 MiB limit is what bounds it.
- **`parse_csv_chunk` receives raw chunks.** I could not see its implementation in this diff, so check how it handles a row that spans two chunks.

**Not in this change**

- The limit is a constant. There is no config setting for it.
- The only test covers the oversize case. No test covers the streaming path or a missing header.

Ticket: OPS-412

---

I wrote this for a reviewer who has not seen the branch.

Open questions:
- Is the 1 MiB limit the value ops chose for OPS-412? The diff does not say.
- Should the missing-header case be fixed in this PR?
- Does `parse_csv_chunk` keep state across chunks? The diff does not show it.

I did not run the test or any other command, and I did not look at the code outside the diff.
