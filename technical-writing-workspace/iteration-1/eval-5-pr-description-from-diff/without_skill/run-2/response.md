**Title:** Reject uploads over 1 MiB and parse the CSV in chunks (OPS-412)

**Problem**

Production workers were being OOM-killed when someone uploaded a very large CSV. `upload()` read the whole body with `request.body()` and then parsed it, so memory use grew with the size of the upload. Ticket: OPS-412.

**Change**

In `importer/handler.py`:

- **Size limit:** a new `MAX_BODY_BYTES` constant is set to 1 MiB (1,048,576 bytes). If the `Content-Length` header is above it, `upload()` returns `413` before reading any of the body.
- **Chunked parsing:** the body is now read with `request.stream()`. Each chunk goes through `parse_csv_chunk()` instead of one `parse_csv()` call on the full body.

In `tests/test_handler.py`, a new test posts a body of `MAX_BODY_BYTES + 1` bytes and asserts a `413`.

**Limitations to review**

- **Chunked uploads skip the limit.** The limit only checks the `Content-Length` header. A request sent with `Transfer-Encoding: chunked`, or with a wrong `Content-Length`, has no usable header, so it is never rejected. Such a request can still stream an arbitrarily large body. Closing this would mean counting bytes as they arrive in the stream loop and returning `413` once the total passes the limit. I left that out of this PR. Say if you want it added here.
- **Streaming alone does not cap memory.** `rows.extend(...)` still collects every parsed row before `store(rows)` runs. For bodies under 1 MiB this is fine. The 1 MiB cap is what protects the workers, not the streaming.
- **Malformed header:** `int(request.headers.get("content-length", 0))` raises `ValueError` if the header isn't a number, which would return a 500. A request with a bad header is unlikely but possible.
- **Chunk boundaries:** `parse_csv_chunk` has to handle rows or quoted fields that span two chunks. I haven't checked its implementation and the diff adds no test for it.
- **Behaviour change:** uploads above 1 MiB that used to succeed now get a `413`. Please confirm 1 MiB is enough for real import files, or make the limit configurable.

**Testing**

- The new unit test covers the `Content-Length` rejection path.
- Not covered: chunked uploads without a `Content-Length` header, and CSV rows split across chunks.

---

I wrote this from the diff and your context alone, so I haven't run the tests or read `parse_csv_chunk`. The limitations section reflects what the diff shows. Trim it if you'd rather fix those points before opening the PR.
