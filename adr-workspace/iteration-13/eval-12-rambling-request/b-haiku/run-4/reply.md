I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-the-background.md`, following the existing log (ADRs 0001 and 0002, English, adr-tools format). I did not change any other ADR.

Choices I made that you should check:

- **Status is Accepted**, since the sync agreed on it. If the team has not fully agreed yet, say so and I will switch it to Proposed.
- **Date is 2026-11-20**, the day I wrote it, not the day of the Thursday sync.
- **The billing module rename is not in the ADR.** It is a separate decision. Tell me if you want it recorded as its own ADR once it is decided.

Questions the ADR cannot answer:

1. What happens when a PDF job or its email fails? Is there a retry, and does the customer see anything in the meantime?
2. How long does the emailed download link stay valid, and who can open it?
3. Does the billing page show a "generating" state, or does the customer simply wait for the email?
