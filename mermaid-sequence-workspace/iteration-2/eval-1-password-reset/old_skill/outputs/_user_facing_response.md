Here is the password reset flow as a Mermaid sequence diagram. It covers the happy path (email enumeration-safe 202 + async email delivery) and the rate-limit case (429). Paste it straight into your GitLab wiki — GitLab renders ` ```mermaid ` blocks natively.

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant W as Web App
    participant A as Auth API
    participant D as Postgres
    participant Q as RabbitMQ
    participant N as Notification Worker
    participant S as SendGrid

    U->>W: Submit email on forgot-password page
    W->>+A: POST /v1/password-resets
    Note over W,A: Public endpoint (no auth header)<br/>Content-Type: application/json<br/>{ "email": "..." }<br/>Rate limit: 5 requests / hour / IP

    alt within rate limit
        A->>+D: Look up user by email
        D-->>-A: user row or not found
        Note over A: Always returns 202 regardless of result<br/>(prevents email enumeration)
        A-->>W: 202 Accepted
        W-->>U: "Check your email" confirmation

        opt user exists
            A-)Q: publish reset_requested event
            Note over A,Q: Routing: reset_requested<br/>payload: { "user_id": "...", "email": "..." }
            Q-)N: deliver reset_requested event
            N->>+S: POST /v3/mail/send
            Note over N,S: Authorization: Bearer (SendGrid API key)<br/>Content-Type: application/json<br/>{ "to": "...", "template": "password_reset", "reset_link": "..." }
            S-->>-N: 202 Accepted
        end
    else rate limit exceeded (> 5 / hour / IP)
        A-->>W: 429 Too Many Requests
        Note over W,A: Retry-After: (seconds until reset)
        W-->>U: "Too many requests, try again later"
    end
    deactivate A
```

Walking through it: the user submits their email (1) and the Web App calls the public, rate-limited `POST /v1/password-resets` (2). Inside the rate limit, the Auth API looks the user up in Postgres (4–5) and **always** answers `202 Accepted` (7) so attackers can't enumerate emails (8 confirms to the user). Only if the user actually exists does the Auth API fire-and-forget a `reset_requested` event onto RabbitMQ (9), which the Notification Worker consumes (11) and turns into a `POST /v3/mail/send` to SendGrid with a `Bearer` token (12). If the caller is over 5 requests/hour/IP, the Auth API short-circuits with `429 Too Many Requests` plus a `Retry-After` header (15). The `-)` arrows mark the RabbitMQ hops as async; everything else is request/reply.

A note on validation: I could **not** validate this diagram in the current environment — the Mermaid MCP server returned a transport error and the local mermaid-cli has no headless Chrome available to render, so I did not install anything to force it through. The syntax here sticks to Mermaid's portable core (participants/actors, `alt`/`opt`, notes, activations, `-)` async arrows), all of which GitLab's bundled Mermaid supports. To preview or tweak it before publishing, paste the block into <https://mermaid.live>.
