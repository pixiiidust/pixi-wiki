---
title: Shifu
created: 2026-06-27
updated: 2026-06-28
type: entity
status: active-pr-review
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

### Upload and VPS light smoke

Issue #14 is closed via PR #16.

The app supports browser/API upload, stores private source files under `SHIFU_DATA_DIR/sources`, validates upload size/type, avoids blocking the async UI route during file writes, and exposes `/api/sources/mini-vss/status` for cheap dependency smoke.

### Local worker artifact seam

The local GTX 1070 worker seam adds `shifu-local-worker`, deterministic worker status at `SHIFU_DATA_DIR/worker_artifacts/<source_id>/status.json`, heavy modality states, `/api/sources/{source_id}/worker-status`, and process-response merging of imported modality states.

The worker status artifact is the first import boundary; real embeddings/transcription quality comes after the seam is verified on Jamie's local machine.

### Verifier report gate

Issue #21 is implemented in PR #26 and open for merge approval.

PR #26 adds verifier manifests, structured verdict import, deeper T3 verifier pools, verified-only T3 recall, baseline-vs-verified deltas, negative/refusal reporting, fixture/private proof-scope labels, and an actual-video guide at `docs/guide.md`.

Review follow-up tightened the truth boundary: fallback `LIKELY` evidence is audit-only and no longer inflates verified hits or verified T3 recall. Fixture evaluation can pass baseline retrieval while still showing `Private VOD detection proof: no`, `Verified hits: 0`, and T3 verified recall `0.00` until structured verdicts are imported.

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
- Current PR: https://github.com/pixiiidust/shifu-app/pull/26
- Final child issue: https://github.com/pixiiidust/shifu-app/issues/21
- Related concepts: [[../concepts/video-retrieve-then-verify-loop|Video Retrieve-Then-Verify Loop]], [[../concepts/verified-video-answer-surfaces|Verified Video Answer Surfaces]]
