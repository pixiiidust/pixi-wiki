---
title: LKY Dataset Readiness Map
created: 2026-06-16
updated: 2026-07-10
type: synthesis
status: compiled
namespace: curated-tuning-datasets
tags: [curated-tuning-datasets, lky-brain, dataset-readiness, provenance, dataset-recipe]
sources:
  - Projects/LKY Archive/Index.md
  - Projects/LKY Archive/Source Inventory.md
  - https://github.com/pixiiidust/lky-brain
confidence: high
---

# LKY Dataset Readiness Map

The LKY work remains primarily a `curated-tuning-datasets` case study even though training is now complete. This namespace owns the source/provenance, transformation, recipe, and readiness contract; training runtime belongs in `local-ai-infrastructure`, and evaluation design belongs in `eval-trace`.

## Current readiness by artifact

| Artifact | Current state | Boundary |
|---|---|---|
| NAS record manifest | retrieval-ready metadata | 1,328 unique pointers; verify source drift |
| Local hydrated corpus | research/training use demonstrated | not redistributed; NAS terms still apply |
| Synthetic-question recipe | publicly published recipe | question joins need stronger passage-hash validation |
| Qwen3-14B adapter | public research artifact | persona/rights/factuality caveats remain |
| Style-transfer evaluation | directional evidence | n=24, 10 documents, one judge, stochastic generation |
| Commercial use | not established | requires separate rights and risk review |

## Updated readiness ladder

```text
source-inventory
→ locally hydrated corpus
→ recipe publication
→ hash-verified reproducibility
→ repeated evaluation
→ redistribution/commercial review
```

These are separate axes. Completing training does not automatically make the source bodies redistribution-safe, the recipe drift-proof, or the adapter commercially cleared.

## What worked

- Source metadata and transcript bodies stayed separate.
- Low-confidence OCR/translation/duplicate/ceremonial material was flagged before assembly.
- Interviews were held out by whole document.
- Synthetic questions were published without transcript bodies.
- Intermediate checkpoints were preserved and evaluated rather than selecting only the lowest train loss.

## Remaining gates

1. Add source and normalized-passage hashes to the recipe.
2. Pin the pipeline commit/schema and fail closed on chunk drift.
3. Record holdout IDs and generated dataset summaries as reproducibility artifacts.
4. Repeat evaluation with fixed/repeated seeds and document-clustered uncertainty.
5. Keep NAS rights/terms and model-weight publication risk as explicit review lanes.
6. Add tests/CI, a root code license, and a machine-readable run manifest tying commit, source/dataset hashes, executed config, checkpoint, generation, and eval artifacts together.
7. Pin the version-sensitive training stack and generate report conclusions from result data rather than hardcoded percentages.

## Cross-namespace ownership

- `curated-tuning-datasets` — manifest, provenance, cleaning, recipe, readiness.
- `local-ai-infrastructure` — successful Unsloth/WSL2/16GB QLoRA path and runtime landmines.
- `eval-trace` — trait rubric, paired candidates, uncertainty, and claim strength.
