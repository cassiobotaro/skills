The poller in `worker/poller.py` now waits 45 seconds between polls instead of 10. I changed `POLL_INTERVAL_S` from `10` to `45`, and `time.sleep` already reads that constant. I haven't run it.
