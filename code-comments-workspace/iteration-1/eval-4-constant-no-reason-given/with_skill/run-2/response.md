I changed `POLL_INTERVAL_S` from 10 to 45 in `worker/poller.py`, so the poller now sleeps 45 seconds between polls. I didn't run anything.

I added no comment next to the constant. You didn't say why 45 seconds, and nothing in the repository says either. Writing a reason would mean making one up. If there's a real one, such as a rate limit or a latency budget, tell me and I'll record it next to the constant.
