**Title:** Reject uploads above 1 MiB with 413 and parse the body in chunks (OPS-412)

**Description**

`upload` in `importer/handler.py` now returns `413` when the `Content-Length` header is above `MAX_BODY_BYTES` (1,048,576 bytes). Before, it read the whole body into memory with `request.body()`. Production workers were getting OOM-killed when someone uploaded a huge CSV (OPS-412).

For requests under the limit, the handler now reads the body with `request.stream()` and passes each chunk to `parse_csv_chunk`, instead of passing the full body to `parse_csv`.

**How to verify**

Run the new test:

```
pytest tests/test_handler.py::test_upload_rejects_body_above_limit
```

It posts `1_048_576 + 1` bytes to `/upload` and expects `413`.

**What to look at closely**

- **The limit checks the header, not the bytes read.** A request with no `Content-Length` header (for example, chunked transfer encoding) counts as 0 and passes the check. The streaming loop has no byte counter, so it does not stop such a request. If you want a hard cap, the loop needs to count bytes as it reads. I left that out of this PR.
- **A non-numeric `Content-Length` raises `ValueError` in `int(...)`.** The diff does not handle it.
- **`rows` still holds every parsed row.** Memory is now bounded by the 1 MiB limit when the header is honest. Streaming does not reduce it further.
- **`parse_csv_chunk` is not in this diff.** I could not check how it handles a row that spans two chunks.
- **Behavior change for users:** uploads above 1 MiB that used to work now fail with `413`.

**Not in this PR:** a byte cap on the stream, and streaming rows into `store` instead of collecting them.

---

**Questions for you (I couldn't answer these from the diff):**
- Is the 1 MiB limit agreed with whoever owns the uploads? Is anyone uploading larger legitimate files today?
- Does `parse_csv_chunk` handle rows split across chunks? If it does, delete that bullet. If you don't know, leave it so the reviewer checks.
- Is a missing `Content-Length` possible in production, for example behind a proxy that uses chunked encoding? If so, that bullet is the main gap, and you may want to fix it before merging.

**Assumed reader:** a reviewer on your team who knows the importer but hasn't seen this branch. The repository has no PR template, so I used the standard order: what and why, verification, review focus, exclusions. I did not run the test.
