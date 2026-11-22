# Exporting diagrams

Read this when the user asks for exported diagrams, or when another skill needs a rendered
image of a view. The image is `structurizr/structurizr`, the one that validates; run the
commands from the directory that holds the DSL file. `-u` keeps the files the container
writes owned by the user, and `STRUCTURIZR_THEMES` lets bundled theme names resolve.

## Text formats

Export to `diagrams/` in a text format (`plantuml`, `plantuml/c4plantuml`, `mermaid`,
`websequencediagrams`, `json`, `theme`, `static`) with the regular image:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.json -format <format> -output diagrams
```

This reads `workspace.json` (where saved layout lives), so preview with the UI at least
once first — or export straight from the DSL with `-workspace workspace.dsl` (autolayout
only). `dot`, `d2`, and `ilograph` are not formats this CLI knows.

## PNG and SVG

Only the `-playwright` variant of the image can render them; the regular one answers
`Exporting to PNG/SVG is not supported in this build`. The variant is published per
version (`structurizr/structurizr:<version>-playwright`, no floating tag), bundles the
same themes, and is a far larger pull (~2 GB). Match the version of the regular image
already in use (`docker run --rm structurizr/structurizr version`):

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr:<version>-playwright export \
    -workspace workspace.json -format svg -output diagrams
```

Writes one `<view key>.svg` (or `.png`) plus a `<view key>-key.svg` legend per view;
`-mode dark` renders the dark theme. The same `-workspace workspace.dsl` note applies.
When the variant isn't pulled and can't be, don't pull it on the user's behalf unless
asked — hand over this command instead, as with validation.
