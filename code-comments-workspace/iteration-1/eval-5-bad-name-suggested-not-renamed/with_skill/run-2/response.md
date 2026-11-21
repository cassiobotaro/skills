`summarize` in `reports/usage.py` now skips any row whose `bytes` value is negative. I haven't run it or any tests.

I added a one-line comment above the check saying that negative values are billing corrections stored in the same table, not usage. That comes from your description.

- **Accounts with only corrections:** An account whose rows are all negative no longer appears in the result. Before, it would have shown up with a negative total. `top_accounts` is affected the same way. If you want such accounts listed with 0, say so.
- **Suggested rename (not applied):** The existing comment `# d maps account id to total bytes used` is only there because `d` is a poor name. Renaming it to something like `bytes_by_account` would let you delete the comment. I left it alone because it's outside this change, so it's your call.
