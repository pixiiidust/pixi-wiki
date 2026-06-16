# Pixi Wiki

Public, repo-local copy of selected Pixiedust agent wiki surfaces.

- Human site: https://pixiiidust.github.io/pixi-wiki/
- Agent index: https://pixiiidust.github.io/pixi-wiki/llms.txt
- Machine registry: https://pixiiidust.github.io/pixi-wiki/index.json
- Full corpus: https://pixiiidust.github.io/pixi-wiki/llms-full.txt
- Raw root pack: https://pixiiidust.github.io/pixi-wiki/raw/llms.txt

## Agent entrypoints

Use this order:

1. Read `agent/llms.txt` for the canonical public routing map.
2. Use `agent/index.json` when you need structured document metadata.
3. Follow `agent_text_path` to clean `.txt` concept or pack aliases for convenient model ingestion.
4. Fall back to root `llms.txt`, root `index.json`, or `raw/` paths only for compatibility/provenance checks.
5. Treat concept `.txt` files as durable synthesis, then verify project/runtime facts against packs, GitHub, or live tools.

## Repo layer contract

This repo is organized into three consumption layers. See [docs/PRD-pixi-wiki-repo-organization.md](docs/PRD-pixi-wiki-repo-organization.md) for the full requirements and migration plan.

| Layer | Purpose | Status |
|---|---|---|
| `agent/` | Clean agent entry layer — `llms.txt`, `index.json`, `concepts/*.txt`, and `packs/*.txt` | Active — canonical start for agents |
| `raw/` | Source-shaped provenance mirror — preserves vault paths and fidelity | Active — see layout below |
| `site/` | Human/browser HTML layer | Future — introduced only with a tested backward-compat strategy |

**Root compatibility:** Existing root files (`llms.txt`, `llms-full.txt`, `index.json`, `concept-*.html`) remain available during migration. They are compatibility entrypoints, not the canonical contract. Agents should prefer `agent/` paths.

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
