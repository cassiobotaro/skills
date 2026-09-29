# Diagrams in a design doc

Two diagram types earn their place in most design docs: a **C4 container diagram** for
the architecture — the executable processes, the data stores, and how they communicate —
and **sequence diagrams** for flows with temporal order (API call chains, pipelines,
batch processes). A diagram never stands on its own: follow each one with prose that
names the components and explains how they interact, since the reader needs to know what
the boxes mean, not merely that they exist.

## Author the C4 architecture diagram as Structurizr DSL

The DSL is the C4 model written as text: it makes every box declare what it is and every
arrow say what flows along it — the discipline the architecture section needs. When the
repository keeps a `workspace.dsl`, evolve the model there so the doc and the source of
truth move together; otherwise write a self-contained snippet that lives in the doc. When
the `structurizr` skill is available, hand your draft to it — it classifies elements at
the right C4 level, writes idiomatic DSL, validates the result, and sharpens what you
wrote, so defer to it rather than restating its conventions here.

Write **sequence diagrams as Mermaid**, through the `mermaid-sequence` skill when it is
available and inline otherwise. A fenced ```` ```mermaid ```` block renders straight on
GitHub, GitLab, and most wikis, so a flow diagram is already its own picture and needs no
extra step.

## A diagram is not a licence to invent

Notation asks questions the author never answered. Structurizr's `container` takes a
technology slot, a relationship takes a technology on the arrow, and a sequence message
wants a protocol — so a doc that says only "the worker reads from the queue and writes the
file" leaves three blanks that the syntax invites you to fill. Filling them is inventing:
`"PostgreSQL"` under a box the author called "notifications database", `AMQP` on an arrow
they only said carried events, `HTTPS` between two services they never described talking
over the network. It reads as fact, it is load-bearing (a reviewer will argue about the
database you chose for them), and it is the easiest place in the whole skill to violate
*record, don't invent* — precisely because the DSL, not the user, asked for it.

So when the source doesn't establish a technology, leave the slot out. Structurizr's
technology arguments are optional; a `container "Notifications database"` with no
technology is valid DSL and honest documentation. Then raise the blank where the author
will see it — an open question, or a line in the reply — because "which database is this?"
is exactly the question a design doc exists to force. This binds hardest when you are
*reviewing* someone else's document: the diagram you add must contain only what their
text already said.

## Embed the diagram: rendered image first, source folded beneath

Structurizr DSL doesn't render by itself inside Markdown, so lead with the **rendered
image** and tuck the **source** into a `<details>` block — the reader sees the picture,
and whoever edits the model finds the source one click away:

````markdown
![Container diagram — Report export service](diagrams/architecture.svg)

<details>
<summary>Diagram source (Structurizr DSL)</summary>

```
workspace {
    ...
}
```

</details>
````

The image line holds the space the diagram occupies, and it is always a Markdown image
reference — never a second diagram drawn by hand. Render it when you can and the path
points at a real file; when you can't, leave the reference as a placeholder marking
exactly where the rendered image belongs for the manual pass. The folded DSL is the
single source of truth for the architecture, so resist pasting an inline Mermaid copy of
the same view alongside it: that leaves two diagrams to keep in step, and they drift.

## Render the C4 diagram to an image when the tooling is there

The image in that slot is a real **PNG or SVG** rendered from the Structurizr DSL — not a
Mermaid block. Turning a C4 model into an image is the `structurizr` skill's domain, so
when that skill (or its tooling) is available, lean on it: the Structurizr CLI/Docker
`export` produces the picture (a static PNG/SVG, or PlantUML/DOT that a PlantUML renderer
turns into PNG/SVG), and the Structurizr Lite UI exports the same. Save the result under
the doc's `diagrams/` folder so the image reference resolves to the file you generated.

Rendering and validation are both best-effort. Validate the DSL when the tooling is there
and fix what it reports; but when an exporter, renderer, or validator is missing or
erroring, don't retry and don't hold the document hostage to it — keep the `![…](…)`
placeholder (a one-line "render this in the manual pass" note beside it is fine), embed
the folded DSL, and move on. The line never to write is a *validation* disclaimer that
implies the design itself wasn't checked: the diagrams get the same manual review as the
prose around them, so they don't need one.
