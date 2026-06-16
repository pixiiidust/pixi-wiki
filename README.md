# Pixi Wiki

Public, repo-local copy of selected Pixiedust agent wiki surfaces.

- Human site: https://pixiiidust.github.io/pixi-wiki/
- Agent index: https://pixiiidust.github.io/pixi-wiki/llms.txt
- Machine registry: https://pixiiidust.github.io/pixi-wiki/index.json
- Full corpus: https://pixiiidust.github.io/pixi-wiki/llms-full.txt
- Raw root pack: https://pixiiidust.github.io/pixi-wiki/raw/llms.txt

## Agent entrypoints

Use this order:

1. Read `llms.txt` for the public routing map.
2. Use `index.json` when you need structured document metadata.
3. Follow `raw_text_path` to `.txt` concept files for convenient model ingestion.
4. Treat concept `.txt` files as durable synthesis, then verify project/runtime facts against packs, GitHub, or live tools.

## Raw layout

```text
raw/llms.txt                         # root pack
raw/Knowledge/llms.txt               # Knowledge domain pack
raw/Knowledge/concepts/*.txt         # agent-friendly concept text mirrors
raw/Knowledge/concepts/*.md          # Markdown source mirrors
raw/Projects/**/llms.txt             # project packs
raw/Maps of Content/llms.txt         # MOC pack
```

Source of truth remains the private Obsidian/Hermes knowledge packs unless separately published. This repo is a public derived surface for browsing and agent entry.
