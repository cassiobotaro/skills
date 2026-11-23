**Title:** Reject uploads above 1 MiB with 413 (OPS-412)

**Description:**

`upload` in `importer/handler.py` now returns `413` when the request's `Content-Length` header is above `MAX_BODY_BYTES` (1,048,576 bytes). The handler no longer calls `request.body()`, which read the whole upload into memory. It now reads the body with `request.stream()` and passes each chunk to `parse_csv_chunk`. This fixes OPS-412, where prod workers were OOM-killed on huge CSV uploads.

**How to verify**

Run `pytest tests/test_handler.py::test_upload_rejects_body_above_limit`. The test posts `1_048_576 + 1` bytes to `/upload` and expects `413`.

**Where to look closely**

- **Chunked uploads skip the check.** The handler reads `content-length` with a default of `0`. A request without that header, such as a chunked upload, therefore passes the size check. The handler then streams the body with no size cap.
- **Parsed rows still pile up in memory.** The loop collects every parsed row in `rows` before it calls `store(rows)`. Memory is bounded only by the header check, not by the streaming.
- **A non-numeric `Content-Length` raises.** `int(...)` raises `ValueError` on a non-numeric header value. I did not find handling for that in the diff.
- **The tests cover one case.** The new test covers an oversized body that carries a `Content-Length`. Nothing covers a body just under the limit, a missing header, or a chunked request.

**Not in this PR**

- Enforcing the limit while streaming.
- Making `MAX_BODY_BYTES` configurable.

Closes OPS-412.

---

**Notes for you**

- I assumed the reader is a reviewer on the importer service who has not seen the OOM incident.
- **Unconfirmed:** whether the `1 MiB` limit is enough for real customer CSVs. The diff does not say, and the description does not claim it. Add the reason for 1 MiB if the team has one.
- **Unconfirmed:** whether production sits behind a proxy that already rejects chunked bodies or caps their size. The "chunked uploads skip the check" point is written from the handler code alone. If a proxy covers it, say so there or drop the bullet.
- I did not run the tests. The repository here contains only the diff, so I wrote the verify command from the test name in the diff.
- I did not post or commit anything.
