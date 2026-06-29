---
title: Shifu
created: 2026-06-27
updated: 2026-06-29
type: entity
status: implementation-chain-complete
namespace: ai-native-product-surfaces
source: Projects/Shifu/Index.md
confidence: high
---
# Shifu

Shifu is a local-first searchable video knowledge prototype: private videos stay close to the user, while the app produces timestamped, evidence-backed answers and reusable clips.

The current corpus direction uses Valorant/CS VOD-style material as an evaluation corpus, not as the full product identity.

## Product frame

```text
source video -> light indexing -> local heavy worker -> evidence-backed answer
```

Shifu should answer questions with candidate moments, keyframes, transcript/caption evidence when available, modality state, verifier decisions, and clear boundaries. It should not pretend a query was answered when evidence is missing.

## Local-first architecture

The current architecture decision is:

```text
VPS app/orchestrator
  -> upload, source registration, browser UI
  -> light MiniVSS smoke: segmentation + keyframes
  -> search/save/export surfaces
  -> verifier manifests and reports

Local NVIDIA GTX 1070 worker
  -> heavy visual embeddings
  -> transcription/caption artifacts when available
  -> structured verifier verdicts
  -> worker_artifacts/<source_id>/status.json
```

This follows the same product logic as games and creator tools: use the user's desktop GPU for heavy local media work, then make cloud GPU a later optional accelerator.

Short contract:

> Local first. Cloud when useful. Evidence always.

## Current milestone state

The implementation chain through parent issue #3 is complete: PR #26 merged, issue #21 closed, and parent #3 closed after post-merge verification on `main`.

The app can run on an actual local video today for upload/light-processing/search smoke. It includes browser/API upload, source registration, light segmentation/keyframes, search/save/export surfaces, local GTX 1070 worker status seam, verifier manifests, structured verdict import, deeper T3 verifier pools, verified-only T3 recall, baseline-vs-verified deltas, and negative/refusal reporting.

Post-merge verification on `main`: focused verifier/eval tests 18 passed; full suite 80 passed with one warning; compileall clean; `git diff --check` clean; fixture evaluator passed 5/5 while honestly reporting `Private VOD detection proof: no`, `Verified hits: 0`, and T3 verified recall `0.00` until structured verdicts are imported.

## Boundaries

- Jamie's target local GPU is **NVIDIA GTX 1070**, not RTX 3060.
- Cloud GPU rental is deferred until the local-worker seam proves useful.
- Private media, generated frames, transcripts, embeddings, worker artifacts, verifier verdicts, and private reports should not be committed.
- Fixture reports are plumbing smoke only. Real private-VOD detection proof requires private media, private hand labels, non-placeholder modality artifacts, and structured verifier verdict imports.
- Shifu can run on an actual video today for upload/light-processing/search smoke; production-grade proof is the next frontier.

## Source handles

- Project hub: `Projects/Shifu/Index.md`
- Repo: https://github.com/pixiiidust/shifu-app
- Parent issue: https://github.com/pixiiidust/shifu-app/issues/3
- Final PR: https://github.com/pixiiidust/shifu-app/pull/26
- Final child issue: https://github.com/pixiiidust/shifu-app/issues/21
- Related concepts: [[../concepts/video-retrieve-then-verify-loop|Video Retrieve-Then-Verify Loop]], [[../concepts/verified-video-answer-surfaces|Verified Video Answer Surfaces]]
