# Before and after

Read this when a comment deserves to exist but resists being made precise or short. Each
pair shows one rule of `SKILL.md`. The examples are in several languages on purpose; the
rules do not depend on the language.

## Contents

- Comments to delete
- Comments that record a reason
- Wording

## Comments to delete

**Restates the code.**

```python
# Before
# Loop over the orders and add up the totals
revenue = sum(order.total for order in orders)

# After
revenue = sum(order.total for order in orders)
```

**Narrates the edit.** The first comment is true only on the day of the change.

```go
// Before
// Fixed: now checks for nil before dereferencing, as requested
if user != nil {

// After: only when the reader would wonder how user can be nil here
// user is nil for requests authenticated with an API key.
if user != nil {
```

**Repeats the signature.**

```typescript
// Before
/** Finds a user by email. @param email the email @returns the user */
function findUserByEmail(email: string): User | undefined

// After: says what the signature does not
/** Matches case-insensitively. Deactivated users are not returned. */
function findUserByEmail(email: string): User | undefined
```

**Props up a name.** In new code, change the name; in existing code, suggest it.

```python
# Before
t = 30  # timeout in seconds for the upstream call

# After
upstream_timeout_s = 30
```

## Comments that record a reason

**A constant, reason given by the user.** The user said the provider drops connections
that are idle for 60 seconds.

```python
# The provider closes connections idle for 60 s; stay under it.
KEEPALIVE_INTERVAL_S = 45
```

**A constant, no reason given.** The user said "use 45". Nobody said why.

```python
# Wrong: a motive nobody stated
# 45 s balances server load against freshness.
POLL_INTERVAL_S = 45

# Right
POLL_INTERVAL_S = 45
```

**A value you chose yourself.** Say how much it matters.

```python
# Arbitrary. Only has to be larger than the longest line in the input.
BUFFER_SIZE = 64 * 1024
```

**A choice the reader would question.**

```rust
// A linear scan, not a HashMap: the list has at most the 12 months of a year.
let entry = months.iter().find(|m| m.id == id);
```

**A known flaw.**

```javascript
// TODO: paginate. This loads every invoice of the account into memory.
const invoices = await api.listInvoices(accountId);
```

**A pitfall.**

```python
def normalize(records):
    """Sorts `records` in place and returns it; the caller's list is modified."""
```

## Wording

**Ambiguous pronoun.**

```
Before: Insert the row into the batch, but check if it is full first.
After:  Insert the row into the batch, but check if the batch is full first.
```

**Imprecise behavior.**

```
Before: Returns the number of lines in the file.
After:  Counts newline bytes ('\n'). A last line without a newline is not counted.
```

**An example that settles the corner case.**

```python
# Before
def strip_prefix(text, prefix):
    """Removes the prefix from the text."""

# After
def strip_prefix(text, prefix):
    """Removes `prefix` once, from the start only.

    strip_prefix("ababc", "ab") -> "abc"
    """
```

**Mechanics instead of intent.**

```
Before: Iterate through the list in reverse order.
After:  Show the most expensive items first.
```

**Opaque arguments.**

```c
/* Before */
connect(10, false);

/* After */
connect(/* timeout_s = */ 10, /* use_tls = */ false);
```

**A sentence where one word does the job.**

```
Before: Keeps the results of earlier lookups so the same key is not fetched twice.
After:  Caches lookups by key.
```
