# Ledger sync

In today's fast-paced world, data consistency is crucial. Ledger sync serves as a robust bridge between the billing database and the warehouse — it is not just a copy job, but a comprehensive reconciliation pipeline. Studies show that reconciliation reduces incidents. The new version is significantly faster than the old one, ensuring reliability, scalability, and peace of mind.

## Usage

Run the sync by hand:

```bash
# It is important to note that this command leverages the robust --full flag
ledger-sync run --full --since 2026-01-01
```

The job writes to the `ledger_snapshots` table. As the billing team put it in the incident review: "the sync is a crucial, robust safety net — not just a script".

In conclusion, Ledger sync showcases our commitment to data quality. Let me know if you have any questions!
