---
title: Dataset Recipe Publication
created: 2026-07-10
updated: 2026-07-10
type: concept
status: compiled
namespace: curated-tuning-datasets
tags: [curated-tuning-datasets, dataset-recipe, provenance, hydration, reproducibility]
sources:
  - Knowledge/concepts/dataset-recipe-publication.md
  - Projects/LKY Archive/Index.md
  - Projects/LKY Archive/Source Inventory.md
confidence: high
---

# Dataset Recipe Publication

A **dataset recipe** publishes project-owned labels or transformations, source pointers, schemas, and hydration code instead of redistributing source bodies whose terms or rights remain constrained.

## Good recipe contents

- stable source IDs and URLs;
- provenance metadata;
- project-authored questions, labels, or annotations;
- deterministic retrieval, cleaning, and assembly code;
- schema and pipeline versions;
- source and normalized-passage hashes;
- explicit rights and downstream-use boundaries.

## Hard rule

A recipe is not a legal bypass. Hydration still acquires the source under the source host's terms, and model-weight publication is a different review question from raw-text publication.

## Reproducibility rule

Do not rely only on `source_id + chunk_index`. Source files, extraction libraries, and chunking code can change while the identifier still looks valid. Bind each project-authored label/question to a normalized passage hash and fail closed when the hash drifts.

## LKY Brain example

`lky-brain` publishes about 2,895 synthetic interviewer questions and 1,328 NAS record pointers, plus hydration code, while excluding transcript bodies. That is a strong public boundary. Its next hardening step is to add source/passage hashes, pipeline versioning, and holdout manifests so the recipe is drift-detecting rather than only nominally deterministic.

## Readiness ladder

```text
inventory → recipe → hash-verified hydration → repeated eval → rights/commercial review
```

Each gate is independent; training completion does not collapse them into one status.
