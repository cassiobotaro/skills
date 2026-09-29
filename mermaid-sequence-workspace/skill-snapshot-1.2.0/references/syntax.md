# Mermaid sequence diagram — syntax reference

Condensed from the official Mermaid documentation (mermaid.js.org/syntax/sequenceDiagram).
Version annotations mark features that older renderers (GitHub, GitLab, self-hosted
wikis) may not support yet — see the portability table at the end.

**Sections** — jump to what the diagram needs rather than reading straight through:

Skeleton · Participants and actors · Messages · Activations · Notes · Blocks ·
**Text escaping gotchas** · Numbering · Actor menus · **Portability** (which features
older renderers reject)

## Skeleton

```
sequenceDiagram
    autonumber
    participant A as Service A
    participant B as Service B
    A->>B: Message text
    B-->>A: Reply text
```

Statements are one per line. Indentation is cosmetic. `%%` starts a comment line.

## Participants and actors

- `participant Name` — rectangle; `actor Name` — stick figure (use for humans).
- Declaration order = left-to-right column order. Undeclared names are created in
  order of first mention — declare explicitly to control layout.
- **Alias**: `participant A as Order API` — short id for the source, readable label in
  the render. Line breaks in labels need an alias: `participant A as Order<br/>API`.
- **Typed symbols (v11.12.0+)**: `participant Cache@{ "type" : "database" }` — types:
  `boundary`, `control`, `entity`, `database`, `collections`, `queue`. Combines with
  aliases: `participant DB@{ "type": "database" } as User Database` (external `as`
  wins over an inline `"alias"` field).
- **Create / destroy (v10.3.0+)**:

  ```
  create participant C as Worker
  A->>C: spawn
  destroy C
  A-xC: terminate
  ```

  Only the recipient of a message can be created; sender or recipient can be destroyed.
- **Grouping (box)**:

  ```
  box Aqua Backend services
      participant A
      participant B
  end
  ```

  Color is optional (named or `rgb()`/`rgba()`); `box transparent Aqua` when the label
  itself is a color name.

## Messages

`[Actor][Arrow][Actor]: Message text`

| Arrow | Meaning |
|---|---|
| `->` | solid line, no arrowhead |
| `-->` | dotted line, no arrowhead |
| `->>` | solid line + arrowhead — **a request** |
| `-->>` | dotted line + arrowhead — **a reply** |
| `<<->>` | solid bidirectional (v11.0.0+) |
| `<<-->>` | dotted bidirectional (v11.0.0+) |
| `-x` | solid line + cross — message never received |
| `--x` | dotted line + cross |
| `-)` | solid line + open arrow — **async / fire-and-forget** |
| `--)` | dotted line + open arrow |

Recent additions (v11.12.3+, poor portability): half-arrows (`-|\`, `-|/`, `-\\`,
`-//` and dotted/reversed variants) and central lifeline connections — append `()`
to either end of an arrow: `A->>()B`, `A()->>B`.

## Activations

Show a participant busy processing between request and reply:

- Explicit: `activate B` / `deactivate B` on their own lines.
- Shorthand: `+` activates the receiver, `-` deactivates the sender —
  `A->>+B: req` then `B-->>-A: reply`. Activations stack for the same participant.
- **Pitfall**: when the reply happens inside an `alt`/`opt` block, do not put `-` on
  the reply in *each* branch — Mermaid processes every branch, deactivates twice, and
  errors. Activate with `+` on the request and put one explicit `deactivate B` after
  the block's `end`.

## Notes

```
Note right of A: text
Note left of A: text
Note over A: text
Note over A,B: text spanning both lifelines
```

`<br/>` inside note or message text makes a line break. Place a note immediately after
the message it annotates. Notes over two participants are the natural home for the
message's technical contract (headers, payload shape, status semantics).

## Blocks

```
loop Every 30s                 alt 2xx                     opt token present
    A->>B: poll                    B-->>A: body                A->>B: enrich
end                            else 4xx/5xx               end
                                   B-->>A: error
                               end

par Notify all                 critical Connect to DB      break checkout fails
    A->>B: event               and...                          API-->>U: failure page
and                                S-->>DB: connect        end
    A->>C: event               option Timeout
end                                S-->>S: log error
                               end
```

- `alt`/`else` — mutually exclusive outcomes; label each branch with its condition.
- `opt` — a single optional sequence (an `if` without `else`).
- `loop` — repetition; the label states the loop condition/interval.
- `par`/`and` — concurrent actions; nestable.
- `critical`/`option` — an action that must happen, with conditional circumstances.
- `break` — abort the remaining flow (exceptions, early exits).
- `rect rgb(r, g, b)` / `rect rgba(...)` — background highlight box around statements.
- All blocks close with `end` and can be nested.

## Text escaping gotchas

These produce parse errors whose message points far from the actual mistake:

- **The literal word `end`** in a message/label can terminate a block early. Wrap it:
  `(end)`, `[end]`, `{end}`, or quote it.
- **Angle brackets**: placeholder text like `session=<token>` is parsed as HTML and
  breaks the diagram (validated: `Expecting 'ACTOR', got 'INVALID'`). Write `...`,
  `(token)`, or entity codes `#lt;token#gt;`. `<br/>` is the only safe tag.
- **Semicolons** end a statement even mid-text — write `#59;` for a literal `;`.
- **Entity codes**: `#<decimal>;` (e.g. `#35;` for `#`, `#9829;` for ♥) and HTML
  character names are supported in text.

## Numbering

- `autonumber` as the first statement numbers every arrow.
- `autonumber <start> <increment>` (v11.15.0+) — custom start/step, decimals allowed.

## Actor menus (rarely needed)

```
link A: Dashboard @ https://dashboard.example.com/a
links A: {"Dashboard": "https://...", "Wiki": "https://..."}
```

Adds a popup menu to the participant — useful when the Markdown host renders
interactive SVG (most don't).

## Portability

GitHub and GitLab bundle their own Mermaid versions and upgrade on their own cadence;
mermaid.live tracks the latest release. Default to the safe core; use gated features
only when the renderer is known and name the minimum version.

| Tier | Features |
|---|---|
| **Safe core** (use freely) | participants/actors, aliases, `box`, all arrows up to `-x`/`-)`, activations, notes, `<br/>`, `loop`/`alt`/`opt`/`par`/`critical`/`break`/`rect`, `autonumber`, `%%` comments, entity codes |
| v10.3.0+ | `create` / `destroy` |
| v11.0.0+ | bidirectional arrows `<<->>`, `<<-->>` |
| v11.12.0+ | typed participants `@{ "type": ... }`, inline `"alias"` |
| v11.12.3+ | half-arrows, central connections `()` |
| v11.15.0+ | `autonumber <start> <increment>` |
