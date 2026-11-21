# Ledger sync

Ledger sync moves data from the billing database to the warehouse and reconciles the two. It is more than a copy job. The new version is faster than the old one.

## Usage

Run the sync by hand:

```bash
# It is important to note that this command leverages the robust --full flag
ledger-sync run --full --since 2026-01-01
```

The job writes to the `ledger_snapshots` table. As the billing team put it in the incident review: "the sync is a crucial, robust safety net — not just a script".
