---
title: Pixi Vault
created: 2026-06-16
updated: 2026-07-07
type: namespace-overview
status: compiled
category: knowledge-systems
namespace: pixi-vault
confidence: medium
---

# Pixi Vault

> Namespace for the private `pixi-vault` source system and its generated `pixi-wiki` public publishing surface.

## Scope

### Covers

Vault architecture, Wiki Compiler Maps, AgentWikis compatibility, namespace compiler logic, source/output repo boundaries, and pixi-wiki publication model.

### Not Covered

General agent workflow behavior unless it changes vault/compiler architecture; project-specific implementation details unless they affect the namespace compiler.

### Current As

2026-07-07 — Pixi Wiki hardening and feature delivery recorded: CI, browser-verified deploys, human search, Updates, rendering correctness, mobile navigation, SEO, shared CSS, MCP performance, and route contract tests are now part of the public artifact.

## Canonical Source Roots

- `Projects/Hermes Mission Control/PRD - Pixi Vault Namespace Compiler.md`
- `Wiki Compiler Maps/Namespace Wiki Compiler Map.md`

## Crosslinks

- [[../agent-workflows/README|agent-workflows]]
- [[../local-ai-infrastructure/README|local-ai-infrastructure]]
- [[../eval-trace/README|eval-trace]]

## Public Output Contract

When published to `pixi-wiki`, this namespace should expose:

```text
/raw/pixi-vault/README.md
/raw/pixi-vault/wiki/index.md
/wiki/pixi-vault/README.md
/wiki/pixi-vault/wiki/index.md
```

## Maintenance

- Edit canonical source notes first.
- Use `Wiki Compiler Maps/Namespace Wiki Compiler Map.md` for routing decisions.
- Do not compile Daily Notes directly unless promoted or verified.
