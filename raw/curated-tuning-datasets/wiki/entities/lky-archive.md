---
title: LKY Archive
created: 2026-06-16
updated: 2026-06-16
type: entity
status: stub
namespace: curated-tuning-datasets
tags: [curated-tuning-datasets, lky-archive, provenance, dataset-readiness]
sources:
  - Projects/LKY Archive/Index.md
  - Projects/LKY Archive/Source Inventory.md
confidence: medium
---

# LKY Archive

The **LKY Archive** is a proposed curated-source inventory for Lee Kuan Yew-related material. Its current role is to define a provenance and dataset-readiness contract, not to scrape or train on data.

## Current boundary

- Inventory contract only.
- No scraping or downloading.
- No LoRA/fine-tuning.
- No claim that any source is training-safe.
- Rights/provenance review comes before dataset construction.

## Dataset-readiness ladder

```text
inventory-only → retrieval-ready → quote-ready → fine-tuning-candidate → rejected
```

A source should not move beyond `inventory-only` without provenance, source class, rights/risk notes, and format availability.

## Cross-namespace links

- `local-ai-infrastructure` — future local tuning/retrieval workflows may depend on curated datasets.
- `eval-trace` — dataset-quality and provenance gates may later need evaluation traces.

## Source

Compiled from `Projects/LKY Archive/Index.md` and `Projects/LKY Archive/Source Inventory.md`.
