I changed `POLL_INTERVAL_S` in `worker/poller.py` from 10 to 45, so the poller now sleeps 45 seconds between polls. I didn't run anything.

I added no comment next to the constant. You didn't say why 45 seconds, and nothing in the repo explains it, so any reason I wrote would be a guess. If there's a real reason, such as a rate limit or a load target, tell me and I'll record it next to the constant.
