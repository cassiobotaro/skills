# Structurizr DSL — advanced features

Read this only when the task explicitly needs one of these: archetypes, workspace
extension, filtered/custom/image views, perspectives, scripts/plugins. Derived from
[docs.structurizr.com/dsl](https://docs.structurizr.com/dsl) (MIT) — see NOTICE.md.

## 1. Archetypes

Custom element/relationship types with shared defaults (modern replacement for repeated
tagging). Defined inside `model`:

```
archetypes {
    application = container {
        technology "Go"
        tag "Application"
    }
    datastore = container {
        technology "PostgreSQL"
        tag "Database"
    }
    async = -> {
        technology "RabbitMQ"
        tag "Async"
    }
}
s = softwareSystem "Shop" {
    api = application "API"
    db = datastore "Orders DB"
}
s.api --async-> s.db "Publishes events to"
```

Base types: `person`, `softwareSystem`, `container`, `component`, `deploymentNode`,
`infrastructureNode`, `group`, `element`. Archetypes can extend other archetypes.

## 2. Workspace extension and `!element`

```
workspace extends <file|url> {
    model {
        !element a {
            webapp = container "Web Application"
        }
        a.webapp -> b "Gets data from"
    }
}
```

- `!element <id> { … }` re-opens an existing element (add children, tags, relationships).
- `!elements <expression> { … }` / `!relationships <expression> { … }` apply changes in
  bulk, with `this` bound to each match. Useful e.g. for
  `!elements "element.parent==a" { this -> logging "Sends logs to" }`.
- **DEPRECATED:** `!extend` and `!ref` — superseded by `!element`/`!relationship`.

## 3. Filtered, custom, and image views

```
filtered <baseKey> <include|exclude> <tags> [key] [description]
custom [key] [title] [description] { … }        // for custom `element` types only
image <*|element-id> [key] {
    <plantuml|mermaid> <file|url|viewKey>    // viewKey: render another view of this workspace
    kroki <format> <file|url>
    image <file|url>
    title <text>
}
```

Filtered views slice a base view by tag (e.g. current vs future state tagged elements).
Two rules, both verified against the parser: the **base view must not have `autoLayout`**
(the CLI rejects it: "automatic layout enabled — this is not supported for filtered
views"), so its layout is arranged by hand in the UI and saved to `workspace.json` — keep
its key stable or that layout is orphaned; and **defining any filtered view hides the
base view from the diagram list** (by design), so to keep the full picture available add
`filtered "<baseKey>" include "Element,Relationship" "<baseKey>-all"`.

Image views from a Mermaid/PlantUML source need a renderer configured in `views`:
`properties { "mermaid.url" "https://mermaid.ink" "mermaid.format" "svg" }` (PlantUML:
`"plantuml.url"` / `"plantuml.format"`; Kroki: `"kroki.url"` / `"kroki.format"`) —
otherwise the view is an empty box. The public renderers send the diagram source to a
third party and may lack the CORS headers image views need; prefer a local instance. A
static PNG/SVG needs nothing.

## 4. Perspectives

Cross-cutting annotations on elements/relationships (Security, Ownership, Tech Debt…):

```
perspectives {
    "Technical Debt" "Legacy auth module pending rewrite" "High"
    perspective "Health" {
        url "https://example.com/health"      // dynamic: polled, value shown live
    }
}
```

Style by value: `element "Perspective:Technical Debt[value==High]" { stroke red }`.

## 5. Scripts and plugins

```
!script groovy {
    workspace.views.createDefaultViews()
}
!script <file.kts|.rb|.js|.groovy> { name value }
!plugin com.example.MyPlugin { name value }
```

Variables in scope: `workspace`, `context`, plus `element`/`relationship`/`view` where
applicable. Rarely needed — prefer plain DSL. Handy ones: `workspace.views.views.findAll {
it instanceof com.structurizr.view.ModelView }.each { it.removeElementsWithNoRelationships() }`
(drop orphans from every view); `it.addTags(it.technology)` over containers (style by
technology).

**DSL and code.** To add components extracted from code, keep the hand-written model in
DSL and append to it from a program: parse `workspace.dsl` with the Java `structurizr-dsl`
library (`com.structurizr:structurizr-dsl`), or `structurizr export -format json` and load
the JSON with any language port. The libraries are append-only — nothing already in the
DSL can be removed or edited from code.

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
