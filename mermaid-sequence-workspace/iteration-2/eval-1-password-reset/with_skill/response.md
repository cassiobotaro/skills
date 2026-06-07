Here's the password reset flow as a Mermaid sequence diagram. It renders natively in your GitLab wiki — paste it into a page as-is. It covers the happy path, the email-enumeration protection (always 202), and the rate-limit case (429 + `Retry-After`), with notes carrying the endpoints, headers, and payloads you described.

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant W as Web App
    participant A as Auth API
    participant P as Postgres
    participant Q as RabbitMQ
    participant N as Notification Worker
    participant S as SendGrid

    U->>W: Submit email on forgot-password page
    W->>+A: POST /v1/password-resets
    Note over W,A: Public endpoint (no auth header)<br/>Content-Type: application/json<br/>{ "email": "..." }<br/>Rate limit: 5 requests / hour / IP

    alt Over rate limit (more than 5 req/hour/IP)
        A-->>W: 429 Too Many Requests
        Note over W,A: Retry-After: (seconds until reset)
        W-->>U: Show "try again later"
    else Within rate limit
        A->>+P: SELECT user by email
        P-->>-A: user row or none
        A-->>W: 202 Accepted
        Note over W,A: Always 202 regardless of whether the user exists<br/>(prevents email enumeration)
        W-->>U: Show "check your email"

        opt User exists
            A-)Q: publish reset_requested event
            Note over A,Q: Event: reset_requested<br/>{ "user_id": "...", "email": "..." }
            Q-)N: deliver reset_requested event
            N->>+S: POST /v3/mail/send
            Note over N,S: Authorization: Bearer (SendGrid API key)<br/>Content-Type: application/json<br/>reset email with reset link/token
            S-->>-N: 202 Accepted
        end
    end
    deactivate A
```

Reading the flow by step number: the user submits their email (1) and the web app POSTs it to the public, rate-limited `/v1/password-resets` endpoint (2). If that IP is over 5 requests/hour, the API returns `429` with a `Retry-After` header (3) and the user is told to try later (4). Otherwise the API looks the user up in Postgres (5–6) and always returns `202 Accepted` (7) — identical whether or not the account exists, so attackers can't enumerate emails — and the user is told to check their inbox (8). Only when the user actually exists does the API publish a `reset_requested` event to RabbitMQ (9); the Notification worker consumes it (10) and sends the reset email via SendGrid's `POST /v3/mail/send` using a `Bearer` token (11–12).

A note on validation: I could not validate the render here. The connected Mermaid MCP server returned a transport error, and the local mermaid-cli can't render in this environment (no headless Chrome). The code uses only portable, safe-core Mermaid syntax, so GitLab will render it natively; if you'd like a preview before publishing, paste it into <https://mermaid.live>.

I left two things implicit because you didn't specify them, and they're easy to add if you want them in the diagram: what happens if the SendGrid call fails (non-202), and any failure path for the RabbitMQ publish/consume. Say the word and I'll add those branches.
