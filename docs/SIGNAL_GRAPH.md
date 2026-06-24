# Pixi Wiki Signal Graph

The signal graph is a local analysis sidecar for orienting around Pixi Wiki's generated Markdown corpus.

It is not canonical truth. Canonical truth remains the maintained Pixi Wiki outputs:

- `raw/`
- `llms.txt`
- `llms-full.txt`
- `index.json`
- the Pixi Wiki MCP server

## What it builds

Run:

```bash
python scripts/build_signal_graph.py raw graphify-out
```

This writes:

```text
graphify-out/
├── graph.json
└── SIGNAL_MARKDOWN_GRAPH_SUMMARY.json
```

If Graphify is installed, generate the interactive report and HTML:

```bash
graphify cluster-only . --graph graphify-out/graph.json --no-label
```

That adds/updates:

```text
graphify-out/
├── GRAPH_REPORT.md
└── graph.html
```

## Why this exists

Vanilla corpus graphs over Pixi Wiki can over-weight generic metadata and headings like `status: compiled`, `type: concept`, `Rules`, `Source`, and `Boundaries`.

`build_signal_graph.py` keeps the useful structure and filters most of that glue:

- namespace → document edges;
- document → document links from wikilinks and local Markdown links;
- document → source-class edges for `Knowledge/`, `Projects/`, Hermes skills/knowledge, Wiki Compiler Maps, and GitHub sources;
- meaningful tags;
- meaningful section headings.

Use it for:

- map-before-edit orientation;
- finding concept bridges across namespaces;
- I-know-kungfu / Knowledge Pack fit-checks;
- deciding which Pixi Wiki MCP documents to read next.

Do not use it for:

- replacing Pixi Wiki MCP retrieval;
- publishing public knowledge;
- storing memory;
- making generated graph output canonical.

## Artifact policy

`graphify-out/` is generated and ignored by Git. Rebuild it on demand.

If you need to share a snapshot, zip the generated folder or serve it temporarily over a private tunnel/Tailscale route.

## Current limitations

This is deterministic extraction only. It does not call an LLM and does not infer deep semantic relationships that are not already expressed as links, tags, headings, or sources.

Graphify may deduplicate same-labeled nodes during `cluster-only`, so its report node count can be lower than the script's JSON summary. Treat that as a visualization/reporting normalization, not a source change.
