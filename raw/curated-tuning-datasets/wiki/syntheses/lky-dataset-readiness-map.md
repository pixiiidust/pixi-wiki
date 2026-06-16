---
title: LKY Dataset Readiness Map
created: 2026-06-16
updated: 2026-06-16
type: synthesis
status: compiled
namespace: curated-tuning-datasets
tags: [curated-tuning-datasets, lky-archive, dataset-readiness, provenance]
sources:
  - Projects/LKY Archive/Index.md
  - Projects/LKY Archive/Source Inventory.md
confidence: medium
---

# LKY Dataset Readiness Map

The **LKY Archive** belongs in `curated-tuning-datasets` as a source-provenance and readiness problem, not as a training-method project.

## Current readiness level

```text
inventory-only
```

The project currently defines source-selection and provenance expectations. It does not authorize scraping, downloading, fine-tuning, LoRA training, or claims that any material is training-safe.

## Readiness ladder

```text
inventory-only → retrieval-ready → quote-ready → fine-tuning-candidate → rejected
```

A source should only move upward when provenance, rights/risk notes, transcript/audio/video availability, and format quality are recorded.

## What this namespace owns

`curated-tuning-datasets` owns:

- source inventory structure;
- provenance and source-class notes;
- corpus readiness criteria;
- copyright/risk flags;
- separation between retrieval-readiness and fine-tuning-readiness.

Training methods, model selection, and local training infrastructure should link out to `local-ai-infrastructure` unless they directly impose dataset requirements.

## Source

Compiled from `Projects/LKY Archive/Index.md` and `Projects/LKY Archive/Source Inventory.md`.
