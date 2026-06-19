---
title: I-know-kungfu
created: 2026-06-19
updated: 2026-06-19
type: entity
status: active
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, i-know-kungfu, knowledge-packs, cookbook, local-first, agent-context]
sources:
  - Projects/I-know-kungfu/Index.md
  - https://github.com/pixiiidust/I-know-kungfu
  - https://github.com/pixiiidust/I-know-kungfu/issues/1
confidence: medium
---

# I-know-kungfu

**I-know-kungfu** is an AI-native product surface for finding useful wikis, checking local fit, serving them through agent-readable surfaces, and harmonizing overlap with an existing knowledge base.

## Product shape

The current flow is:

```text
Find useful wiki / pack
→ check local fit
→ choose serving surface
→ harmonize overlap
→ inspect scope / proof / refusal
```

The product turns docs, vaults, repos, and research folders into installable Knowledge Packs that agents can inspect, search, cite, and refuse from without building custom RAG from scratch.

## Current status

The first static Cookbook serving prototype passed Jamie's initial smell test with Variant C. The accepted direction is table/list-first and decision-first: check fit before trust, choose one serving surface, then make overlap harmonization explicit.

The repo has a pushed PRD and README. The next planned pass is domain modeling plus codebase-design refinement of `CONTEXT.md` and `docs/PRD.md`, followed potentially by another grill-with-docs session.

## Namespace role

I-know-kungfu belongs in `ai-native-product-surfaces` because it is primarily about the user-facing and agent-facing product surface for trusted context routing.

It crosslinks to:

- `agent-workflows` for agent consumption, MCP, `llms.txt`, and Knowledge Pack routing mechanics;
- `pixi-vault` for compiled wiki / namespace publishing patterns;
- `local-ai-infrastructure` for local-first serving and future retrieval infrastructure.

## Boundaries

The first slice should remain local-first and endpoint-ready. Do not treat the current project as a hosted marketplace, vector database, hosted RAG layer, payments system, public upload-moderation system, or cloud MCP service.

## Source

Compiled from `Projects/I-know-kungfu/Index.md`, the public repo README/PRD, and GitHub issue #1.
