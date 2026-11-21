Lazy refill is the standard way to do this. The bucket stores the time of its last update. On each `allow()` call it works out how many tokens a timer would have added since then, clamps the total to `capacity`, and spends from that. You can see it in `limiter.py:12-15`.

The result is the same as a timer, but without a timer. Here is why that matters in this codebase:

- **There is one bucket per API key, and nothing ever removes one.** In `api.py`, `buckets` grows with every distinct key. A timer design needs a timer per bucket, or one sweeper that walks all of them every tick. Both cost CPU and scheduling even for keys that have gone quiet. With lazy refill, an idle bucket costs only its memory and no CPU.
- **A timer would add concurrency problems.** The refill thread or task would write `tokens` while `allow()` reads and decrements it. That means a lock, or a race in which a refill lands between the check and the decrement. In this code, refill and spend are one synchronous step with no `await` or yield between them. In a single-threaded or single-event-loop caller, that makes it atomic without any locking.
- **Precision is better.** Refill is fractional (`elapsed * rate`, so 0.2 s at 5/s adds 1 token). A once-per-second timer would hand out tokens in 5-token steps. That gives a visibly bursty limiter, and a request at t=0.99 s would be rejected for no good reason.
- **`time.monotonic()` makes the arithmetic safe.** Wall-clock jumps from NTP or DST can't produce negative or huge `elapsed` values.

The costs of lazy refill are small:

- `tokens` is only correct as of `updated`, so don't read it from outside without refilling first.
- Every call does a little arithmetic.
- The class is not thread-safe as written. If `check()` is called from multiple threads, two calls can both pass the `tokens >= cost` test before either subtracts. This is my reading of the code, since I haven't seen the callers. Under a threaded server, `allow()` needs a lock.

Whether the original author chose this for these reasons, I can't tell from the code. These are the reasons the design is favored, and they fit this setup.

A check on the model: say a key is idle for an hour and then sends 30 requests at once, with `RATE_PER_SECOND = 5` and `BURST = 20`. How many are allowed, and why doesn't the idle hour matter beyond the first request?
