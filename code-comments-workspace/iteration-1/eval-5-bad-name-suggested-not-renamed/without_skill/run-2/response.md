`summarize` in `reports/usage.py` now skips any row whose `bytes` value is negative. I added a short comment saying those rows are billing corrections. I didn't run it or add tests.

An account whose rows are all negative won't appear in the result at all, rather than showing up with 0. `top_accounts` builds on `summarize`, so it ignores those rows too. If you'd rather such accounts show as 0, I can change that.
