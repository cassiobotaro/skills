`summarize` in `reports/usage.py` now skips any row whose `bytes` value is negative, so billing corrections no longer count as usage. I added a short comment explaining why. I haven't run it or added a test.

An account whose rows are all negative now doesn't appear in the result at all, instead of showing up with 0. `top_accounts` uses `summarize`, so it gets the same filtering. If you'd rather those accounts show up with 0, I can change that.
