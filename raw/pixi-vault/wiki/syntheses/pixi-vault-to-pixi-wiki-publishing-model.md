---
title: Pixi Vault to Pixi Wiki Publishing Model
created: 2026-06-16
updated: 2026-06-16
type: synthesis
status: compiled
namespace: pixi-vault
tags: [pixi-vault, pixi-wiki, publishing, agentwikis]
sources:
  - Projects/Hermes Mission Control/PRD - Pixi Vault Namespace Compiler.md
  - Wiki Compiler Maps/Namespace Wiki Compiler Map.md
confidence: high
---

# Pixi Vault to Pixi Wiki Publishing Model

`pixi-vault` is the private source repository. `pixi-wiki` is the public generated mirror. The boundary is intentional: authoring truth and public output are separate artifacts.

## Source side

```text
pixi-vault/
├── Knowledge/              # reusable concept authoring
├── Projects/               # project/application source truth
├── Wiki Compiler Maps/     # routing contracts
└── wikis/<slug>/           # compiled namespace source
```

The `wikis/<slug>/` layer is compiled/curated source inside the vault. It is reviewable in Git and Obsidian, but agents should edit `Knowledge/`, `Projects/`, or Wiki Compiler Maps first unless intentionally patching compiled output.

## Public side

```text
pixi-wiki/
├── llms.txt
├── llms-full.txt
├── index.json
├── raw/<slug>/...
└── wiki/<slug>/...
```

`llms.txt` is the compact agent registry. `llms-full.txt` is the full concatenated corpus. `index.json` is the machine-readable registry. `raw/<slug>/` preserves Markdown, and `wiki/<slug>/` exposes human-readable HTML.

Human pages render Markdown with breadcrumbs, visible frontmatter metadata, raw Markdown links, report-a-mistake links, namespace sidebars, and previous/next navigation. The goal is not only publication; the site should make the compiled knowledge navigable enough for people and structured enough for agents.

## Publication workflow

1. Update canonical source in `Knowledge/`, `Projects/`, or Wiki Compiler Maps.
2. Compile/curate into `wikis/<slug>/`.
3. Run namespace linting against `pixi-vault/wikis`.
4. Run the `pixi-wiki` generator.
5. Run public-output tests.
6. Push both repos as needed.
7. Verify live GitHub Pages URLs with HTTP 200 checks.

## Clean rebuild policy

Old root flat pages in `pixi-wiki` are removed from the canonical public contract. The clean mirror should have only root registry files plus `/raw/<slug>/...` and `/wiki/<slug>/...` namespace trees.

No old `concept-*.html`, `projects-*.html`, `knowledge.html`, `projects.html`, `maps-of-content.html`, `root.html`, `agent/`, or `legacy/` surface should reappear without a deliberate compatibility policy and regression coverage.

## Cross-namespace relationships

- [Agent Workflows](../../../agent-workflows/README.md) documents crew workflows affected by source-truth boundaries, Knowledge Pack Routing, and markdown-first agent memory.
- [Eval Trace](../../../eval-trace/README.md) evaluates whether agents overfit stale context or skip live verification.
- [Local AI Infrastructure](../../../local-ai-infrastructure/README.md) will matter when RAG or local models consume compiled wiki pages.

## Source

Compiled from `Projects/Hermes Mission Control/PRD - Pixi Vault Namespace Compiler.md` and `Wiki Compiler Maps/Namespace Wiki Compiler Map.md`.
