Here's a Mermaid sequence diagram for your password reset flow. It's written for GitLab's flavored Markdown (a fenced ` ```mermaid ` block), so you can paste it straight into your wiki page. It covers both the success path and the rate-limited (429) case, with notes carrying the endpoints, headers, and payloads.

## Password reset flow

```mermaid
sequenceDiagram
    autonumber

    actor User
    participant Web as Web App<br/>(forgot-password page)
    participant Auth as Auth API
    participant DB as Postgres
    participant MQ as RabbitMQ
    participant Worker as Notification Worker
    participant SG as SendGrid

    User->>Web: Submit email on forgot-password page
    Web->>Auth: POST /v1/password-resets
    Note over Web,Auth: Public endpoint (no auth header)<br/>Body: {"email": "..."}<br/>Rate limit: 5 req/hour per IP

    alt Rate limit exceeded (> 5 req/hour per IP)
        Auth-->>Web: 429 Too Many Requests
        Note over Auth,Web: Header: Retry-After: <seconds>
        Web-->>User: Show "try again later" message
    else Within rate limit
        Auth->>DB: Look up user by email
        DB-->>Auth: User record (found or not found)

        alt User exists
            Auth->>MQ: Publish reset_requested event
            MQ-->>Worker: Deliver reset_requested event
            Worker->>SG: POST /v3/mail/send
            Note over Worker,SG: Header: Authorization: Bearer <SENDGRID_API_KEY><br/>Body: reset email (to, subject, reset link)
            SG-->>Worker: 202 Accepted
            Note right of Worker: Reset email delivered to user
        else User does not exist
            Note over Auth,DB: No event published.<br/>Same response as the "exists" case<br/>to prevent email enumeration.
        end

        Auth-->>Web: 202 Accepted
        Note over Auth,Web: Always 202 regardless of whether<br/>the user exists (anti-enumeration)
        Web-->>User: Show "if an account exists,<br/>you'll receive an email"
    end
```

## Notes on the flow

- POST /v1/password-resets (Auth API): public, unauthenticated endpoint. Request body `{"email": "..."}`. Rate-limited to 5 requests per hour per IP; exceeding the limit returns `429 Too Many Requests` with a `Retry-After` header.
- Anti-enumeration: the Auth API always returns `202 Accepted` whether or not the user exists, so attackers can't tell which emails are registered. The reset event (and therefore the email) is only produced when the user actually exists.
- RabbitMQ: on a matching user, the Auth API publishes a `reset_requested` event. The Notification Worker consumes it asynchronously, so email delivery happens off the request path.
- SendGrid: the worker calls `POST /v3/mail/send` with an `Authorization: Bearer <API key>` header to send the reset email.

### Rendering / wiki tips

- GitLab renders Mermaid from a fenced code block tagged `mermaid` (shown above) — no plugin needed.
- The `<br/>` line breaks inside notes/participant labels are supported by GitLab's Mermaid renderer; if your wiki is on an older GitLab version and a label looks off, replace `<br/>` with a space.
- `autonumber` adds the step numbers automatically; remove that line if you'd rather not number the steps.
