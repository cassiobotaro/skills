# Password reset flow

How a password reset request travels from the forgot-password page to the reset email.
The `alt` block covers the two outcomes of the rate limiter; the `opt` block is the part
that only happens when the email actually belongs to a user — the response the caller
sees is the same either way.

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant W as Web App
    participant A as Auth API
    participant DB as Postgres
    participant MQ as RabbitMQ
    participant N as Notification Worker
    participant SG as SendGrid

    U->>W: Submit email on forgot-password page
    W->>+A: POST /v1/password-resets
    Note over W,A: Public endpoint — no Authorization header<br/>Content-Type: application/json<br/>{ "email": "..." }

    alt more than 5 requests per hour per IP
        A-->>W: 429 Too Many Requests
        Note over W,A: Retry-After: seconds until the window resets
        W-->>U: Show rate-limit message
    else within the rate limit
        A->>+DB: Look up user by email
        DB-->>-A: user row, or no match
        A-->>W: 202 Accepted
        Note over W,A: Always 202, whether or not the user exists<br/>(no email enumeration)
        W-->>U: Show "check your inbox" confirmation

        opt user exists
            A-)MQ: publish reset_requested
            MQ-)N: deliver reset_requested
            N->>+SG: POST /v3/mail/send
            Note over N,SG: Authorization: Bearer (SendGrid API key)<br/>Content-Type: application/json
            SG-->>-N: accepted
            SG-)U: Password reset email
        end
    end
    deactivate A
```
