There's no comment or doc in the repo that records the author's reasoning. What follows is what the code shows plus the usual trade-offs.

**What `allow()` does:** it refills lazily. On each call it works out `elapsed * rate`, adds that to the bucket, caps it at `capacity`, and then spends `cost`. The bucket's state is just `(tokens, updated)`, and it only changes when someone asks for a token.

**Why that beats a timer here:**

- **One bucket per API key, and no cleanup.** `api.py` creates a bucket the first time it sees a key and keeps it in the module-level `buckets` dict. A timer design needs a timer, thread or task for each bucket, or one sweeper that walks every bucket. An idle key would still cost you wakeups. With lazy refill, an idle bucket costs only its memory.
- **It's more precise.** The refill is continuous, so 0.2s of elapsed time adds exactly 1 token at rate 5. A once-per-second timer would hand out tokens in lumps of 5. Callers could be rejected right before a tick, and a burst could land right after one.
- **No concurrency to manage.** A timer mutating `tokens` while `allow()` reads it is a race, so you'd need a lock or an event loop. The lazy version has no background writer, so the state changes only inside `allow()`. If you call `allow()` from threads, though, you still need a lock around it. The read-modify-write isn't atomic, and nothing in this code adds one.
- **It's deterministic and easy to test.** The behavior depends only on the clock values seen at each call. You can test it by patching `time.monotonic`, with no sleeping and no timer threads to flake.
- **It uses `time.monotonic()`.** That avoids wall-clock jumps from NTP or DST corrections skewing the refill.

**When a timer would be the better choice:** if something has to react to refills, such as waking queued waiters when tokens become available, you need a scheduler. A plain accept/reject limiter like this one doesn't.

**Two things to watch in this code:**

1. `buckets` grows without bound, since keys are never evicted. This is the one cost of the lazy design. You can fix it by evicting buckets that have been idle long enough to be full again, because a full bucket is the same as a brand-new one.
2. `allow()` isn't thread-safe, as noted above. That's fine if you run single-threaded or on asyncio, and a problem under a threaded server.

If you want the actual history behind the choice, `git log` or `git blame` on `limiter.py` is the place to look. I haven't checked either.
