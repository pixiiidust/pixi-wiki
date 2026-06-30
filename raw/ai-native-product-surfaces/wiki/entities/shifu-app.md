---
title: Shifu
created: 2026-06-27
updated: 2026-06-30
type: entity
status: pivot-thesis-under-review
namespace: ai-native-product-surfaces
source: Projects/Shifu/Index.md
confidence: high
---
# Shifu

Shifu is a local-first video knowledge/workbench prototype: private videos stay close to the user while the app helps users find, verify, save, compare, export, and reuse timestamped moments.

The current corpus direction uses Valorant/CS VOD-style material as an evaluation corpus, not as the full product identity. The gameplay thesis is under review because generic visual embeddings are weak at precise tactical state.

## Product frame

```text
source video -> light indexing -> local heavy worker -> evidence/workflow surface
```

Shifu should expose candidate moments, keyframes, transcript/caption/structured evidence when available, modality state, verifier decisions, manual tags, and clear boundaries. It should not pretend a query was answered when evidence is missing; AI assists only where it earns trust.

## Local-first architecture

The current architecture decision is:

```text
VPS app/orchestrator
  -> upload, source registration, browser UI
  -> light MiniVSS smoke: segmentation + keyframes
  -> search/save/export surfaces
  -> verifier manifests and reports

Local desktop GPU worker
  -> heavy visual embeddings
  -> transcription/caption artifacts when available
  -> structured verifier verdicts
  -> worker_artifacts/<source_id>/status.json
```

This follows the same product logic as games and creator tools: use the user's desktop GPU for heavy local media work, then make cloud GPU a later optional accelerator.

Short contract:

> Local first. Cloud when useful. Evidence always.

## Current milestone state

The implementation chain through parent issue #3 is complete: PR #26 merged, issue #21 closed, parent #3 closed after post-merge verification on `main`, and PR #27 added the Windows/D: local-video guide.

The app can run on an actual local video today for upload/light-processing/search smoke. It includes browser/API upload, source registration, light segmentation/keyframes, search/save/export surfaces, local worker status seam, verifier manifests, structured verdict import, deeper T3 verifier pools, verified-only T3 recall, baseline-vs-verified deltas, and negative/refusal reporting.

The product thesis is now under review. Jamie's private Valorant/CS `mini-vss` smoke showed the GTX 1070 CUDA/OpenCLIP path and LanceDB visual index can work technically, but manual inspection found the visual-only `post plant throw` hits wrong. Transcript/commentary looked more useful, and the full Tonbi loop still needs a clean reproduction with captions/transcripts/fusion/deeper pools/verifier before judging `mini-vss` itself.

Post-merge verification on `main`: focused verifier/eval tests 18 passed; full suite 80 passed with one warning; compileall clean; `git diff --check` clean; fixture evaluator passed 5/5 while honestly reporting `Private VOD detection proof: no`, `Verified hits: 0`, and T3 verified recall `0.00` until structured verdicts are imported.

## Boundaries

- Jamie's previous local proof target was **NVIDIA GTX 1070**; next heavy experiments are expected after the repaired 5070 Ti desktop is available.
- Cloud GPU rental is deferred until the local-worker seam proves useful.
- Private media, generated frames, transcripts, embeddings, worker artifacts, verifier verdicts, and private reports should not be committed.
- Fixture reports are plumbing smoke only. Real private-VOD detection proof requires private media, private hand labels, non-placeholder modality artifacts, and structured verifier verdict imports.
- Shifu can run on an actual video today for upload/light-processing/search smoke; production-grade proof is not established.
- Visual embeddings are low-trust recall for tactical gameplay until structured signals and verifier evidence support them.
- Do not judge Tonbi `mini-vss` from OpenCLIP visual-only output; its intended loop includes captions/transcripts, fused retrieval, candidate pools, and verification.

## Source handles

- Project hub: `Projects/Shifu/Index.md`
- Repo: https://github.com/pixiiidust/shifu-app
- Parent issue: https://github.com/pixiiidust/shifu-app/issues/3
- Final PR: https://github.com/pixiiidust/shifu-app/pull/26
- Final child issue: https://github.com/pixiiidust/shifu-app/issues/21
- Windows/D: guide PR: https://github.com/pixiiidust/shifu-app/pull/27
- Related concepts: [[../concepts/video-retrieve-then-verify-loop|Video Retrieve-Then-Verify Loop]], [[../concepts/verified-video-answer-surfaces|Verified Video Answer Surfaces]]
