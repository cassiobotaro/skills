Here's the password reset flow, ready to paste into the GitLab wiki page (GitLab renders `mermaid` blocks natively):

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant W as Web App
    participant A as Auth API
    participant P as Postgres
    participant Q as RabbitMQ
    participant N as Notification Worker
    participant SG as SendGrid

    U->>W: Submit email on forgot-password page
    W->>+A: POST /v1/password-resets
    Note over W,A: Public endpoint — no auth header<br/>Body: { "email": "..." }<br/>Rate limit: 5 requests per hour per IP
    alt more than 5 requests/hour from this IP
        A-->>W: 429 Too Many Requests
        Note over W,A: Retry-After header
        W-->>U: Ask to try again later
    else within rate limit
        A->>+P: Look up user by email
        P-->>-A: user row or no match
        A-->>W: 202 Accepted
        Note over W,A: Always 202, whether or not the user exists —<br/>prevents email enumeration
        W-->>U: Confirm "check your email"
        opt user exists
            A-)Q: publish reset_requested
            Q-)N: consume reset_requested
            N->>SG: POST /v3/mail/send
            Note over N,SG: Authorization: Bearer (API key)
            SG-)U: Password reset email
        end
    end
    deactivate A
```

Reading it by step: the user submits their email (1) and the web app posts it to the public, rate-limited endpoint (2). If that IP is over 5 requests in the hour, the API answers 429 with `Retry-After` (3–4). Otherwise the API looks the address up in Postgres (5–6) and returns 202 either way (7–8), so a caller can't tell an existing account from a missing one. Only when the user actually exists does the API publish `reset_requested` to RabbitMQ (9), the Notification worker consumes it (10) and hands the mail to SendGrid (11), which delivers it to the user (12).

Two things I deliberately did not put in the diagram, since you didn't specify them and I didn't want to invent documentation:

- **What SendGrid returns** and how the worker reacts to a failed send (retry? dead-letter?). Step 11 is drawn as a one-way call for that reason — tell me the behaviour and I'll add the reply and any retry `loop`.
- **The rest of the flow** — the emailed link, token expiry, and the actual password change endpoint. Happy to draw that as a second diagram in the same page if the wiki article should cover the whole journey.

On validation: I did **not** validate this one through the hosted Mermaid server. It carries your internal endpoints, the `Authorization` header, your queue topology and your email provider, and that server renders remotely — so I kept the text on this machine. `mermaid-cli` isn't installed here (and I didn't install anything), so the code block is unvalidated. The quickest private check is GitLab itself: drop it into the wiki page preview, which is the renderer that has to agree with it anyway. If you'd rather have the round-trip preview and consider the exposure fine, say so and I'll run it through the hosted validator — it's your content and your call.

Everything used here is safe-core Mermaid syntax, so any GitLab version will render it.
