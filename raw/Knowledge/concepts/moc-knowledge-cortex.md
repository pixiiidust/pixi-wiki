---
title: MOC Knowledge Cortex
created: 2026-06-12
updated: 2026-06-13
type: concept
description: Model of the MOC layer as the routing brain of the vault, keeping durable notes reachable through clear domain branches.
status: active
domain: knowledge-systems
tags: [architecture, agent-systems, governance]
sources: [local-hermes-knowledge]
confidence: high
---

# MOC Knowledge Cortex

## Definition

The Map of Content (MOC) layer is the **cortex / routing brain** of the Obsidian knowledge base. It is not the memory itself; it routes Jamie and agent crews to the correct source of truth.

## Core model

A healthy vault graph should look like a DDD-style domain tree, not a dense backlink hairball:

```
Vault Cortex / MOC Layer
├── Projects MOC
│   ├── active bounded contexts
│   ├── parked contexts
│   └── historical contexts
├── Knowledge MOC
│   ├── concepts
│   ├── entities
│   ├── comparisons / queries
│   └── raw sources as evidence leaves
├── Agent Operations MOC
│   ├── Pixoid control plane
│   ├── Quill scribe / vault ops
│   ├── Tinker build routes
│   └── Boba research / monitoring
├── Portfolio / Showcase branch
├── Daily Notes branch
├── Templates branch
└── Attachments / Evidence branch
```

Each durable note should have one primary parent branch. Crosslinks are allowed only when they encode real domain meaning.

## Source-of-truth distinction

- **MOCs** route to the right place.
- **Project hubs** own project state, boundaries, decisions, next slices, and source handles.
- **Knowledge pages** own reusable concepts/entities/queries.
- **GitHub issues/PRs/repos** own live execution state and verification handles.
- **Daily notes** are chronological breadcrumbs, not canonical project state.
- **Raw sources / attachments** are evidence leaves; reachable through their parent concept/project/index.

## Quill vault-update dispatch contract

A formal maintenance procedure exists for the "dispatch Quill to update the vault" operation. It covers source-packet definition, direct-vs-issue-slice choice, dirty-state guarding, layer classification, source-of-truth update order, stop conditions, prune classification, and index/log obligations.

> **The full, detailed dispatch procedure lives in local Hermes knowledge** (`~/.hermes/knowledge/concepts/moc-knowledge-cortex.md`) and the Obsidian skill reference (`~/.hermes/skills/note-taking/obsidian/references/dispatch-quill-vault-update.md`). The procedure is agent-facing and maintained there — this page only serves as a navigational pointer.

## Graph hygiene standard

Graph health is not "every note connected to everything." It is:

- module roots are reachable from the MOC layer;
- every durable note has a primary parent branch;
- evidence leaves are linked from the concept/project they support;
- isolated raw/template/attachment notes are acceptable only when a parent README/index links them into the branch;
- MOCs stay compact and navigational.

## Related pages

- [[profile-memory-boundaries]]
- [[self-improving-agent-systems]]