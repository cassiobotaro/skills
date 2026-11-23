**Title:** Reject uploads above 1 MiB with 413 and parse the body in chunks (OPS-412)

```markdown
`upload` in `importer/handler.py` now returns `413` when the request's `Content-Length` header is above 1 MiB (`MAX_BODY_BYTES = 1_048_576`). Before, it read the whole body into memory with `request.body()`, and production workers were OOM-killed when someone uploaded a huge CSV. Fixes OPS-412.

The handler now also reads the body with `request.stream()` and calls `parse_csv_chunk` on each chunk, instead of calling `parse_csv` on the full body.

## How to verify

Run the new test:

    pytest tests/test_handler.py::test_upload_rejects_body_above_limit

It posts 1,048,577 bytes to `/upload` and expects `413`.

## Where to look

- **The limit relies on the `Content-Length` header.** A request without the header counts as 0 bytes and passes the check. A client that lies about the header passes too. The handler enforces no cap while it streams.
- **`rows` still holds every parsed row until `store(rows)` runs.** Streaming removes the second copy of the raw body. It does not bound memory for a request that skips the check.
- **A non-numeric `Content-Length` makes `int(...)` raise `ValueError`.** The diff does not handle that.
- **Chunk boundaries.** `parse_csv_chunk` is not in this diff. Check that it handles a row split across two chunks.

## Not in this change

- No cap on the streamed byte count.
- No change to `store`.
- No test for a body at exactly the limit, or for a streamed body without `Content-Length`.
```

Assumptions and open items:
- **Reader:** the reviewer who will open this diff. I wrote it for them.
- **Open question:** is 1 MiB the right limit for real import files? The diff doesn't say, and I didn't state a reason for it. Add one if you have it.
- **Open question:** does `parse_csv_chunk` handle rows split across chunks? I couldn't check, because the function isn't in the diff. The "Where to look" section tells the reviewer to check it.
- **Not run:** I didn't run the test, since the repository here is empty. The "How to verify" command assumes `pytest` and the test's path from the diff.
- **Delete if you disagree:** the first three "Where to look" bullets come straight from reading the diff. Cut any you'd rather fix in code before opening the PR.
