import time

MAX_ENTRIES = 1024


class TTLCache:
    def __init__(self, ttl_s, clock=time.monotonic):
        self._ttl_s = ttl_s
        self._clock = clock
        self._entries = {}

    def get(self, key, default=None):
        entry = self._entries.get(key)
        if entry is None:
            return default
        value, stored_at = entry
        if self._clock() - stored_at > self._ttl_s:
            del self._entries[key]
            return default
        return value

    def put(self, key, value):
        if key not in self._entries and len(self._entries) >= MAX_ENTRIES:
            oldest = min(self._entries, key=lambda k: self._entries[k][1])
            del self._entries[oldest]
        self._entries[key] = (value, self._clock())
