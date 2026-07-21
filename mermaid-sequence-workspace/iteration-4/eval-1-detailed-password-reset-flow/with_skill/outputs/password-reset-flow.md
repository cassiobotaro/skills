# Password reset flow

How a password reset is requested and delivered, from the forgot-password page to the
outgoing email. Covers the happy path, the always-202 anti-enumeration behaviour, and
the rate-limited case.

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
    Note over W,A: Public endpoint, no auth header<br/>Body: { "email": "..." }<br/>Rate limit: 5 requests per hour per IP

    alt within rate limit
        A->>+DB: Look up user by email
        DB-->>-A: User row, or no match
        A-->>W: 202 Accepted
        Note over W,A: Always 202, whether or not the user exists<br/>(prevents email enumeration)

        opt user exists
            A-)MQ: publish reset_requested
            MQ-)N: deliver reset_requested
            N->>SG: POST /v3/mail/send
            Note over N,SG: Authorization: Bearer (API key)
        end
    else more than 5 requests per hour from this IP
        A-->>W: 429 Too Many Requests
        Note over W,A: Retry-After header
    end
    deactivate A
```

## Reading it

Steps 1–2: the user submits their email and the web app posts it to the public,
unauthenticated `POST /v1/password-resets`. Steps 3–5 (within the rate limit): the Auth
API looks the address up in Postgres and answers `202 Accepted` regardless of the
result, so the response cannot be used to enumerate registered emails. Steps 6–8 run
only when the user actually exists: the Auth API publishes `reset_requested` to
RabbitMQ, the Notification worker consumes it and sends the email through SendGrid.
Step 9 is the rate-limited case — the 6th request within an hour from the same IP gets
`429` with `Retry-After`.
