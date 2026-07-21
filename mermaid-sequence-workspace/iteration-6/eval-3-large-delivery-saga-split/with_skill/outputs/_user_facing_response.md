Written to `order-lifecycle.md` — one Markdown document with five ` ```mermaid ` blocks,
ready to paste into the wiki (GitHub renders them natively).

The whole lifecycle in one diagram would run past 25 messages and 12 participants, so I
split it by phase and kept participant ids/labels identical across the set:

1. **Overview** — the whole lifecycle at coarse grain, both failure branches included.
2. **Phase 1 — placing the order and paying** — Customer → app → API gateway →
   `POST /orders` → Postgres (PENDING) → `POST /payments` → Stripe. Step 11 is the
   approved path publishing `order.paid`; the `else` branch marks the order FAILED and the
   app shows the payment error.
3. **Phase 2 — the restaurant accepts or rejects** — continues from step 10 of phase 1:
   the Restaurant Service consumes `order.paid`, pushes to the tablet, and either publishes
   `order.accepted` or triggers the refund + CANCELLED branch.
4. **Phase 3 — courier assignment and delivery** — continues from step 5 of phase 2. The
   decline-and-retry is a `loop until a courier accepts` wrapping the offer; after the
   assignment the courier collects and delivers, marking PICKED_UP and DELIVERED through
   the Courier Service, which publishes each status event.
5. **Notifications** — the cross-cutting consumer: every `order.*` event turns into a push
   at the stages you listed (paid, accepted, courier assigned, picked up, delivered), plus
   the cancellation notice.

**Not validated here.** A Mermaid MCP server is connected, but it renders remotely and
these diagrams carry your internal detail — service names, `POST /orders` / `POST /payments`,
Kafka topics, Stripe as the processor — so I didn't ship them off the machine, and
mermaid-cli isn't installed locally. The safest preview is your own repo or wiki: open the
file in GitHub's Markdown preview, which renders ` ```mermaid ` blocks natively and never
leaves your org. If you'd rather trade that exposure for an instant check, say so and I'll
run it through the hosted validator — it's your content and your call.

Everything is safe-core Mermaid syntax (no version-gated features), so any GitHub/GitLab
Mermaid version will render it.

Four things I had to choose rather than read off your description — all listed under
**Open points** at the bottom of the file: who owns the refund/CANCELLED transition on a
restaurant rejection (drawn as the Order Service), the event names for the courier stages
(placeholders — `order.paid` and `order.accepted` are yours, the rest aren't), the push
transport, and the absence of headers/payload fields in the notes since none were given.
