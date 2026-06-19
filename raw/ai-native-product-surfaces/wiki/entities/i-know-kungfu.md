---
title: I-know-kungfu
created: 2026-06-19
updated: 2026-06-19
type: entity
status: active
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, i-know-kungfu, knowledge-base-wikis, cookbook, local-first, agent-context]
sources:
  - Projects/I-know-kungfu/Index.md
  - https://github.com/pixiiidust/I-know-kungfu
  - https://github.com/pixiiidust/I-know-kungfu/issues/1
confidence: medium
---

# I-know-kungfu

I-know-kungfu is an AI-native product surface for growing a user's own knowledge base by importing, adapting, and serving bounded knowledge base wikis that agents can search, cite, and refuse against.

## Product shape

The current flow is:

```text
Find useful knowledge base wiki
→ check local fit
→ choose serving entry point
→ harmonize overlap
→ inspect scope / proof / refusal
```

The product is not primarily a generic "pack" marketplace. Each imported serving unit is conceptually a wiki: source-backed pages, scope/non-scope, provenance, freshness, and agent-friendly entry points such as MCP, `llms.txt`, raw Markdown, and `index.json`.

A Knowledge Pack is the portable package/install format for a knowledge base wiki. The wiki is the thing users grow and agents use; the pack is how that wiki moves between local storage, Cookbook listings, and agent harnesses.

## Why it matters

The goal is to let users evolve their knowledge base without reinventing the wheel. In the ideal case, a user can adapt proven wikis with known quality or track record to improve their own coverage, fill gaps, and avoid duplicating or polluting what they already know.

For agents, bounded wiki entry points should be faster and more token-efficient than broad web search. Agents can search a specific source, cite exact pages, and refuse when a task falls outside the wiki's scope.

## Current status

The first static Cookbook serving prototype passed Jamie's initial smell test with Variant C. The accepted direction is table/list-first and decision-first: check fit before trust, choose one serving entry point, then make overlap harmonization explicit.

The repo now has a PRD, README, glossary, and ADR that center knowledge base wiki as the product object and demote Knowledge Pack to package/install format.

## Namespace role

I-know-kungfu belongs in `ai-native-product-surfaces` because it is primarily about the user-facing and agent-facing product surface for trusted context routing and knowledge-base growth.

It crosslinks to:

- `agent-workflows` for agent consumption, MCP, `llms.txt`, and bounded source routing mechanics;
- `pixi-vault` for compiled wiki / namespace publishing patterns;
- `local-ai-infrastructure` for local-first serving and future retrieval infrastructure.

## Boundaries

The first slice should remain local-first and endpoint-ready. Do not treat the current project as a hosted marketplace, vector database, hosted RAG layer, payments system, public upload-moderation system, or cloud MCP service.

## Source

Compiled from `Projects/I-know-kungfu/Index.md`, the public repo README/PRD, and GitHub issue #1.
