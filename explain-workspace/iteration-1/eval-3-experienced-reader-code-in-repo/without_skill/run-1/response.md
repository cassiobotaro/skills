The code doesn't record why it was written this way, so I'm inferring the reasoning from what's in `limiter.py` and `api.py`. There are no comments, docs or commit history for this. This is the standard lazy-refill pattern, and the design supports these reasons:

**1. There is one bucket per API key, and it's created on demand.**
`api.py` keeps a `buckets` dict and creates a `TokenBucket` the first time a key shows up. A timer design would need a timer, or a shared sweeper loop, for every live bucket. Each of those would wake up every second even for keys that have gone idle. With lazy refill, an idle bucket costs only memory and no CPU.

**2. The lazy refill gives the same result as a timer.**
Tokens are `min(capacity, tokens + elapsed * rate)`. Computing that at the moment of the call gives exactly what a timer would have accumulated, because the bucket's state only matters when someone asks.

**3. It refills continuously, not once a second.**
A timer that adds `rate` tokens every second makes the limit bursty at second boundaries. A client could use up the bucket just before a tick and then again just after. Computing `elapsed * rate` with fractional tokens gives a smooth refill. The `tokens` field is a float for that reason.

**4. It uses no threads and has no timer lifecycle.**
There's no background thread, event loop task, or shutdown handling, and no drift or missed ticks if the process stalls. `time.monotonic()` is also immune to wall-clock changes, which a timer based on wall time is not.

**5. It is easy to test.**
You can test it deterministically by patching `time.monotonic`. A timer would need real sleeps or a fake scheduler.

**Things to watch in this code**
- **Thread safety:** `allow()` does a read-modify-write on `tokens` and `updated` with no lock. If `check()` is called from multiple threads, you can get races: two callers could both see enough tokens, or lose an update. A timer design wouldn't fix that, but you'd need a lock either way.
- **Unbounded `buckets` dict:** with lazy refill nothing ever evicts idle keys. If key cardinality is high, you'll need an eviction policy such as TTL, LRU, or dropping buckets that are full again. This is the one real cost of not having a background process. A cheap sweeper for eviction is reasonable, and it's a different job from refilling.
- **Per-process state:** the buckets live in memory, so with multiple workers or hosts each one enforces its own limit. If you need a global limit, this would move to something like Redis, where lazy refill is still the usual approach (store `tokens` and `updated`, and refill in a Lua script).

If the original author left a rationale somewhere (a PR description or design doc), that would be the authoritative answer, and I haven't seen one.
