# Canonical ADR examples

All examples below are adr-tools-exact. Note the blank-line discipline: exactly one
blank line between every element.

## The seed ADR (`adr init` equivalent)

Create this verbatim as `0001-record-architecture-decisions.md` when initializing a
fresh log — substitute only the date:

```markdown
# 1. Record architecture decisions

Date: 2026-06-04

## Status

Accepted

## Context

We need to record the architectural decisions made on this project.

## Decision

We will use Architecture Decision Records, as [described by Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).

## Consequences

See Michael Nygard's article, linked above. For a lightweight ADR toolset, see Nat Pryce's [adr-tools](https://github.com/npryce/adr-tools).
```

## A model well-written ADR

From adr-tools' own decision log. Notice: neutral Context that names the forces (and
even an open constraint), a concrete Decision, and Consequences that include work the
decision creates — written as short standalone paragraphs, not fragments:

```markdown
# 8. Use ISO 8601 Format for Dates

Date: 2017-02-21

## Status

Accepted

## Context

`adr-tools` seeks to communicate the history of architectural decisions of a
project.  An important component of the history is the time at which a decision
was made.

To communicate effectively, `adr-tools` should present information as
unambiguously as possible.  That means that culture-neutral data formats should
be preferred over culture-specific formats.

Existing `adr-tools` deployments format dates as `dd/mm/yyyy` by default.  That
formatting is common formatting in the United Kingdom (where the `adr-tools`
project was originally written), but is easily confused with the `mm/dd/yyyy`
format preferred in the United States.

## Decision

`adr-tools` will use the ISO 8601 format for dates:  `yyyy-mm-dd`

## Consequences

Dates are displayed in a standard, culture-neutral format.

The UK-style and ISO 8601 formats can be distinguished by their separator
character.  The UK-style dates used a slash (`/`), while the ISO dates use a
hyphen (`-`).

Prior to this decision, `adr-tools` was deployed using the UK format for dates.
After adopting the ISO 8601 format, existing deployments of `adr-tools` must do
one of the following:

 * Accept mixed formatting of dates within their documentation library.
 * Update existing documents to use ISO 8601 dates by running `adr upgrade-repository`
```

## A complete supersede pair

`0002-store-sessions-in-redis.md` **before** being superseded:

```markdown
# 2. Store sessions in Redis

Date: 2025-11-18

## Status

Accepted

## Context

...
```

The new ADR, `0004-use-stateless-jwt-sessions.md` — keeps `Accepted`, gains
`Supersedes`:

```markdown
# 4. Use stateless JWT sessions

Date: 2026-06-04

## Status

Accepted

Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)

## Context

...
```

`0002-store-sessions-in-redis.md` **after** — the status word is gone; the link line IS
the status now. Everything below `## Context` is byte-for-byte untouched:

```markdown
# 2. Store sessions in Redis

Date: 2025-11-18

## Status

Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)

## Context

...
```

## An amend pair (Status sections only)

Both ADRs keep their status word — only supersession removes it. From adr-tools' own
log (ADRs 5 and 9):

```markdown
## Status

Accepted

Amended by [9. Help scripts](0009-help-scripts.md)
```

```markdown
## Status

Accepted

Amends [5. Help comments](0005-help-comments.md)
```

## Slug derivation examples

| Title as typed | Filename |
|---|---|
| Use ISO 8601 Format for Dates | `0008-use-iso-8601-format-for-dates.md` |
| Something About Node.JS | `0001-something-about-node-js.md` |
| Slash/Slash/Slash/ | `0002-slash-slash-slash.md` |
| -Bar- | `0003-bar.md` |

Rule: lowercase the title, collapse every run of non-alphanumeric characters into a
single hyphen, strip leading and trailing hyphens. The H1 keeps the title exactly as
given (with its original capitalization) — only the filename is slugged.
