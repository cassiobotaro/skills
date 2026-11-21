Because it makes the timer unnecessary. `allow()` works out how many tokens should have accrued since the last call (`elapsed * rate`) and adds them just before it decides. This is lazy refill, and it gives the same answer a ticking timer would. The code doesn't record the author's reasoning, so the reasons below are inferred from the code.

**Why this beats a timer for this code**

- **Cost scales with use, not with keys.** `api.py` creates one `TokenBucket` per `api_key` in a module-level dict. A per-bucket timer means a thread or scheduled task for every key you've ever seen, and each one wakes every second even if that client has gone quiet. With lazy refill, an idle bucket costs only its memory.
- **There is no shared state to race on.** A background refiller and `allow()` would both write `self.tokens`, so you'd need a lock or atomics. This class has no lock. If it is called from a single thread or an async loop, it is consistent as written.
- **Refill is exact.** The timer version adds tokens in whole-second steps. Here `elapsed` is fractional, so 5 tokens/sec is really 0.5 tokens per 100 ms. The `min(self.capacity, …)` cap gives the same burst ceiling of 20 that a timer would.
- **It uses `time.monotonic()`.** The refill math isn't affected by wall-clock adjustments such as NTP steps.

**What it costs**

- `allow()` does a bit more arithmetic on each call. That's negligible here.
- `self.tokens` is a float and is only current as of the last call. Don't read it from outside and treat it as the live count.
- If this ever runs with multiple threads, the read-modify-write in `allow()` is not atomic and will need a lock. Lazy refill doesn't fix that. It only means there is one writer instead of two.
- `buckets` in `api.py` is never pruned. That is the one place where the "idle keys cost nothing" argument is only partly true, because the objects accumulate.

**Check your understanding:** a bucket is created at t=0 with capacity 20 and drained to 0 tokens. Nobody calls it again until t=10. What does `tokens` hold just after the call at t=10 begins, and what does that call return? The answer is 20 (50 accrued, capped), so it returns `True` and leaves 19.
