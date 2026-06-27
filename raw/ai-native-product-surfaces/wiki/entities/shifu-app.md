---
title: Shifu
created: 2026-06-27
updated: 2026-06-27
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

Shifu should answer questions with candidate moments, keyframes, transcript/caption evidence when available, modality state, and clear boundaries. It should not pretend a query was answered when evidence is missing.

## Local-first architecture

The current architecture decision is:

```text
VPS app/orchestrator
  -> upload, source registration, browser UI
  -> light MiniVSS smoke: segmentation + keyframes
  -> search/save/export surfaces

Local NVIDIA GTX 1070 worker
  -> heavy visual embeddings
  -> transcription
  -> later VLM/caption passes
  -> worker_artifacts/<source_id>/status.json
```

This follows the same product logic as games and creator tools: use the user’s desktop GPU for heavy local media work, then make cloud GPU a later optional accelerator.

Short contract:

> Local first. Cloud when useful. Evidence always.

## Current milestone state

### Upload and VPS light smoke

Issue #14 is closed via PR #16.

The app now supports browser/API upload, stores private source files under `SHIFU_DATA_DIR/sources`, validates upload size/type, avoids blocking the async UI route during file writes, and exposes `/api/sources/mini-vss/status` for cheap dependency smoke.

### Local worker artifact seam

Issue #15 is implemented in PR #17 and open for review/merge.

The PR adds:

- `shifu-local-worker` / `python -m shifu_app.local_worker`;
- deterministic local-worker status at `SHIFU_DATA_DIR/worker_artifacts/<source_id>/status.json`;
- heavy modality states: `ready`, `disabled`, `pending-local-worker`, `failed`, `unsupported-on-vps`;
- `/api/sources/{source_id}/worker-status`;
- process-response merging of imported local-worker modality states;
- a placeholder visual vector artifact for seam testing when GPU/OpenCLIP deps are unavailable.

Verification before the shutdown handoff:

```text
focused tests: 18 passed
full suite: 54 passed
compileall clean
git diff --check clean
CLI worker smoke passed
live API worker-import smoke passed
```

## Boundaries

- Jamie’s target local GPU is **NVIDIA GTX 1070**, not RTX 3060.
- Cloud GPU rental is deferred until the local-worker seam proves useful.
- Private media, generated frames, transcripts, embeddings, and model artifacts should not be committed.
- The worker status artifact is the first import boundary; real embeddings/transcription quality comes after the seam is verified.

## Source handles

- Project hub: `Projects/Shifu/Index.md`
- Repo: https://github.com/pixiiidust/shifu-app
- Parent issue: https://github.com/pixiiidust/shifu-app/issues/3
- PR #17: https://github.com/pixiiidust/shifu-app/pull/17
- Related concepts: [[../concepts/video-retrieve-then-verify-loop|Video Retrieve-Then-Verify Loop]], [[../concepts/verified-video-answer-surfaces|Verified Video Answer Surfaces]]
