`summarize` in `reports/usage.py` now skips any row whose `bytes` value is negative. I didn't run it or any tests.

I added a one-line comment above the check saying these rows are billing corrections kept in the same table, so they don't count as usage. That reason comes from your message.

- **Corrections-only accounts:** an account whose rows are all negative no longer appears in the result at all, instead of showing up with a total of 0. `top_accounts` is affected the same way. If you want such accounts listed with 0, the fix is to add the key without adding the bytes.
- **Suggested rename, not done:** the existing comment `# d maps account id to total bytes used` only exists to explain the name `d`. Renaming it to `bytes_by_account` would let you delete that comment. I left it alone because it is existing code outside this change.
