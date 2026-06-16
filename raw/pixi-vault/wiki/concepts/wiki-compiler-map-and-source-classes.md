---
title: Wiki Compiler Map and Source Classes
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: pixi-vault
tags: [pixi-vault, wiki-compiler-map, source-of-truth, namespace-routing]
sources:
  - Wiki Compiler Maps/Namespace Wiki Compiler Map.md
  - Projects/Hermes Mission Control/PRD - Pixi Vault Namespace Compiler.md
confidence: high
---

# Wiki Compiler Map and Source Classes

A **Wiki Compiler Map** is an internal routing artifact that maps authoring-source notes into compiled AgentWikis namespaces. It replaces the old MOC mental model when the job is source-to-namespace routing.

## Why this exists

The vault has many useful authoring surfaces: `Knowledge/`, `Projects/`, scratch chronology, generated reports, and project artifacts. Future agents need a durable contract for deciding which of those are canonical enough to compile into public/agent-facing wiki pages.

## Source classes

### Canonical

Canonical sources can directly feed compiled namespace pages after normal review. Examples include `Knowledge/concepts/*.md`, `Projects/<Project>/Index.md`, PRDs, ADRs, source inventories, verified project reports, and committed repo artifacts with stable paths.

### Supporting

Supporting sources guide routing and maintenance. Examples include Wiki Compiler Maps, taxonomy maps, verified generated reports, lint reports, and issue tracker parent/child tables. They are not usually public wiki content unless rewritten deliberately.

### Scratch

Scratch sources are volatile capture. They can help agents find context, but they do not compile directly unless Jamie/Pixoid promotes or verifies the relevant material against canonical sources.

## Namespace routing rules

- Use one primary namespace for each compiled page.
- Use crosslinks for secondary relevance.
- Duplicate only when a source is rewritten for a genuinely different namespace-specific purpose.
- Promote projects or concepts to standalone namespaces only through an explicit decision.

## Promotion rule

A source cluster can become a namespace when it has at least two of five signals: independent audience, multiple document types, raw source corpus, ongoing update lifecycle, or clear covers/not-covered scope.

## Source

Compiled from `Wiki Compiler Maps/Namespace Wiki Compiler Map.md` and `Projects/Hermes Mission Control/PRD - Pixi Vault Namespace Compiler.md`.
