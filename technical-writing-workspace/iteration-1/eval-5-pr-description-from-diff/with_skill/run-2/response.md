**PR description**

```markdown
## importer: reject uploads above 1 MiB and parse the body in chunks (OPS-412)

`upload` in `importer/handler.py` now returns `413` when the `content-length` header exceeds `MAX_BODY_BYTES` (1,048,576 bytes). Before, it read the whole body with `request.body()` before parsing, so a huge CSV could exhaust memory and the OOM killer stopped the prod workers.

For bodies within the limit, the handler now reads `request.stream()` and passes each chunk to `parse_csv_chunk`. Before, it passed the full body to `parse_csv`.

Ticket: OPS-412

### How to verify

Run the new test:

    pytest tests/test_handler.py::test_upload_rejects_body_above_limit

It posts 1,048,577 bytes to `/upload` and expects `413`.

### Look closely at

- **Missing `content-length`.** The handler reads a missing header as `0`, so a request without the header (for example, chunked transfer encoding) skips the size check. The size limit does not cover those requests.
- **Rows still accumulate.** `rows.extend(...)` collects every parsed row, and `store(rows)` receives the full list. Memory for the parsed rows still grows with the body size. The 1 MiB limit is what bounds it.
- **Chunk boundaries.** A chunk from `request.stream()` can end in the middle of a CSV row. I did not check how `parse_csv_chunk` handles that.

### Not in this PR

- No test covers the streaming path or a request without `content-length`.
- No enforcement of the limit while streaming.
```

**Assumed reader:** the reviewer, who hasn't seen the branch.

**Open questions for you:**
- Does `parse_csv_chunk` handle a row split across two chunks? The diff doesn't include it. If it does, delete the "Chunk boundaries" bullet. If it doesn't, that is a bug in this change.
- Do your clients or proxy always send `content-length`? If not, the first review point is a real gap, and you may want to count bytes while streaming.
- Is the `pytest` command right? I took it from the test's style (`async def`, `client` fixture). I did not run it or check the repo's test setup.

I wrote the "Look closely at" and "Not in this PR" sections from the diff alone. Trim them if the follow-up work is already planned elsewhere.
