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
- **LEGACY:** `!extend` and `!ref` — superseded by `!element`/`!relationship`.

## 3. Filtered, custom, and image views

```
filtered <baseKey> <include|exclude> <tags> [key] [description]
custom [key] [title] [description] { … }        // for custom `element` types only
image <*|element-id> [key] {
    <plantuml|mermaid|kroki <format>|image> <file|url>
    title <text>
}
```

Filtered views slice a base view by tag (e.g. current vs future state tagged elements).
On v6+, filtered views cannot sit on top of views whose layout you hand-tune with
auto-layout disabled — keep the base view's key stable.

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
applicable. Rarely needed — prefer plain DSL.

---
*Condensed from the Structurizr documentation
([docs.structurizr.com](https://docs.structurizr.com), MIT License, © Simon Brown);
adapted.*
