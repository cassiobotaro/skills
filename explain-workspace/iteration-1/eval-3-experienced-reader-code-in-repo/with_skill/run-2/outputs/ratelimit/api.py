from ratelimit.limiter import TokenBucket

RATE_PER_SECOND = 5
BURST = 20

buckets = {}


def check(api_key):
    bucket = buckets.get(api_key)
    if bucket is None:
        bucket = buckets[api_key] = TokenBucket(RATE_PER_SECOND, BURST)
    return bucket.allow()
