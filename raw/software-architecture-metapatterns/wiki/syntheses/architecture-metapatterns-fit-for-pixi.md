---
title: Architecture Metapatterns — Fit for Pixi
created: 2026-07-02
updated: 2026-07-02
type: synthesis
status: compiled
namespace: software-architecture-metapatterns
sources:
  - README.md
  - wiki/concepts/source/root/source-wiki-home.md
  - wiki/concepts/source/introduction/metapatterns.md
---

# Architecture Metapatterns — Fit for Pixi

This corpus belongs under Knowledge Systems because it is a system for organizing software architecture knowledge, not just a pile of definitions.

## Why It Fits

- It turns scattered architecture pattern names into a navigable pattern language.
- It groups aliases and near-duplicates by structure and function.
- It includes dependency, performance, applicability, relation, and evolution framing.
- It helps agents reason about architecture forces before suggesting implementation moves.

## Best Pixi Uses

- Architecture review vocabulary for Tinker/Pixoid.
- Migration planning from monolith/layers/services/pipeline/proxy/orchestrator shapes.
- Agent retrieval before recommending hexagonal architecture, service splits, BFFs, eventing, or plugin systems.
- Crosslinks to `agent-workflows` when architecture choices affect agent-built software delivery.

## Boundary

Keep the imported source corpus separate from Jamie-authored architecture decisions. Use it to support review and reasoning; do not let it override live code evidence or project constraints.
