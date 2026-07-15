---
title: LKY Brain / LKY Archive
created: 2026-06-16
updated: 2026-07-15
type: entity
status: active
namespace: curated-tuning-datasets
tags: [curated-tuning-datasets, lky-brain, provenance, dataset-recipe, qlora]
sources:
  - Projects/LKY Archive/Index.md
  - Projects/LKY Archive/Source Inventory.md
  - Projects/LKY Avatar/Index.md
  - https://github.com/pixiiidust/lky-brain
  - https://huggingface.co/datasets/sjsim/lky-reasoning-recipe
confidence: high
---

# LKY Brain / LKY Archive

`lky-brain` is a completed public case study that turns a National Archives of Singapore source manifest into a locally hydrated chat corpus, a Qwen3-14B QLoRA adapter, and a post-hoc reasoning-style evaluation.

## What changed from the original inventory stub

The project is no longer inventory-only:

- 1,328 unique NAS records are cataloged in the committed manifest;
- local extraction/cleaning, turn parsing, corpus filtering, speech chunking, and question backfill ran end to end;
- the assembled training set contains 4,441 rows / about 4.0M tokens;
- a Qwen3-14B QLoRA adapter trained for three epochs on one 16GB consumer GPU;
- the epoch-2 checkpoint and a source-pointer dataset recipe are public;
- a small n=24 held-out evaluation shows a directional shift in judged behavior.

## Dataset design

- **Stream A:** 1,142 interview/press-conference windows, with loss on LKY assistant turns only.
- **Stream B:** 2,895 speech passages paired with synthetic interviewer questions.
- **Generic retention:** 404 Dolly instruction rows.
- **Eval:** 66 windows from 10 whole held-out interviews; the published comparison uses 24 selected rows.
- **Temporal control:** LKY samples carry a dated role/persona prompt. Generic rows use a generic assistant prompt.

## Publication boundary

The public dataset is a **recipe**, not a transcript mirror. It publishes project-authored synthetic questions, NAS metadata pointers, hydration code, and documentation. Transcript bodies remain local and subject to NAS terms.

This reduces source-body redistribution. It does not prove that fetched transcripts or trained model weights are commercial-clean or unrestricted. Apache-2.0 labels cover project-owned code/recipe contributions, not automatically the source archive.

## Evidence boundary

The evaluation supports a provisional behavioral-shift claim, not factual fidelity or general reasoning improvement. Epoch 2 is a sensible checkpoint preference because it preserved more reframing and bounded uncertainty than epoch 3, but the current sample is too small and clustered to establish definitive overfitting.

## Applied downstream relationship

The separate LKY Avatar product now consumes the published epoch-2 adapter through a merged Q4_K_M llama.cpp serving path and pairs it with a tuned voice and animated portrait. That downstream milestone does not turn this corpus-and-adapter entity into a factual knowledge base. Live product use surfaced invented biography, dates, offices, and events, which confirms that style transfer and fact grounding must remain separate evidence lanes.

Use `Projects/LKY Avatar/Index.md` for interaction, voice, portrait, hosting, and factual-grounding status. Keep this page focused on corpus provenance, dataset design, publication boundaries, and the adapter result.

## Related pages

- [[concepts/dataset-recipe-publication|Dataset Recipe Publication]]
- [[syntheses/lky-dataset-readiness-map|LKY Dataset Readiness Map]]
- Cross-namespace: `local-ai-infrastructure/wiki/summaries/lky-brain-consumer-gpu-qlora.md`
- Cross-namespace: `eval-trace/wiki/concepts/style-transfer-evaluation.md`
