---
title: Video Retrieve-Then-Verify Loop
created: 2026-06-27
updated: 2026-06-27
type: concept
status: compiled
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, video-ai, retrieval, verification, product-framing]
sources:
  - Knowledge/concepts/video-retrieve-then-verify-loop.md
  - Knowledge/raw/articles/tonbistudio-mini-vss.md
  - Knowledge/raw/articles/nvidia-vss-docs.md
confidence: high
---

# Video Retrieve-Then-Verify Loop

The **Video Retrieve-Then-Verify Loop** is the reusable pattern for answering natural-language questions over video:

```text
ingest video -> segment -> caption/transcribe/embed -> retrieve candidates -> verify with visual/audio evidence -> return timestamped answer
```

Retrieval maximizes candidate recall. Verification filters false positives, cites evidence, sets confidence, and refines the answer.

## Why it matters

NVIDIA VSS shows the industrial version: video IO/storage, agent routing, model endpoints, search, summarization, alert verification, stream handling, and telemetry.

Tonbi's `mini-vss` shows the desk-scale version: segment one video, embed frames/captions/transcripts, fuse retrieval, then judge candidates with evidence. Its reported "fast break" test moved from 0.20 precision@5 on retrieval alone to 1.00 verified precision with 75% recall. The verifier also found a full-court press the human label pass had missed.

The product lesson: **video search quality is candidate recall plus evidence-bearing verification, not just vector ranking.**

## Design rules

1. Segment is the product unit; frames are evidence inside a segment.
2. Visual, caption, transcript, object, and metadata signals propose candidates.
3. Fusion should preserve recall before optimizing rank aesthetics.
4. A verifier should output match/no-match, confidence, evidence, and refined timestamp.
5. "Find every X" is a recall claim and needs deeper candidate pools.
6. A trustworthy no-result state can be better than noisy ranked guesses.

## Query tiers

| Tier | Example | Answer path |
|---|---|---|
| Appearance | "player shooting", "forklift in aisle" | visual embeddings / detections |
| Event | "made layup", "person enters restricted zone" | captions, transcript, object/action signals |
| Tactical / semantic | "fast break", "unsafe loading pattern" | retrieval pool + verifier over clip context |

## Product implication

For Jamie's app exploration, do not start with "video search app" as the promise. Start with one painful video-review job where verified timestamped answers save obvious scrubbing time.

Strong first-user candidates include coaches, creators, course/community operators, and small teams reviewing support, sales, training, or operations footage.

## Related pages

- [[verified-video-answer-surfaces|Verified Video Answer Surfaces]]
- [[ai-native-problem-framing-framework|AI-Native Problem Framing Framework]]
- [[world-model-control-surfaces|World Model Control Surfaces]]
- [[../../local-ai-infrastructure/wiki/concepts/rag-over-agent-wikis|RAG over Agent Wikis]]

## Source

Compiled from `Knowledge/concepts/video-retrieve-then-verify-loop.md`, Tonbi `mini-vss`, and NVIDIA VSS docs.
