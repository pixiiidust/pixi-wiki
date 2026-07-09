---
title: J-Space-Replay
created: 2026-07-08
updated: 2026-07-08
type: entity
status: working-demo
namespace: ai-native-product-surfaces
source: Projects/J-Space-Replay/Index.md
confidence: high
---
# J-Space-Replay

J-Space-Replay is a public working side project for replaying a vision-language model's decoded internal readouts on a video timeline while it answers a question. The public lite version lets users browse preset traces; upload/new-video generation requires local install/GPU.

The product surface is intentionally glass-box and cautious: it helps a user inspect Qwen2.5-VL logit-lens or fitted J-lens readouts, but it does **not** claim to reveal model thoughts or validate mechanistic claims about VLMs.

## Product frame

```text
short video + question
  -> one offline Qwen2.5-VL pass on a local NVIDIA GPU
  -> per-layer residual capture
  -> logit-lens-v1 or j-lens-v1 decode
  -> schema-v1 trace
  -> replay UI: answer, video, word grid, patch/box overlays, unspoken/adversarial cues
```

The UI is a technical replay dashboard: honesty banner, query/answer console, video transport, readout-strength bars, answer-token × layer workspace grid, raw top-token drilldown, lens selector, and trace library.

## What the demo shows

- **Answer precursors:** answer-token readouts can surface words such as `gravity` before the model emits them.
- **Adversarial checks:** when an answer rules something out, cells that still decode the ruled-out word pulse as a warning surface.
- **Unspoken readouts:** the UI lists words read across many cells that appear in neither prompt nor answer.
- **Computed but unsaid content:** the ball-drop example shows late-mid J-lens readouts such as `level`, `horizontal`, `move`, `off`, and `right` while the answer remains a generic gravity explanation.

## Architecture

- Backend: Python/FastAPI package `src/jsr/`.
- Model path: Qwen2.5-VL-7B-Instruct, NF4 + SDPA + fp16 stack.
- Trace pipeline: video frame sampling, prompt preparation, residual capture, lens decode, label extraction, grounding queries, validated `trace.json` schema v1.
- Frontend: React + Vite screens for upload, progress, replay, and library.
- Demo mode: no-GPU pre-baked traces for instant browsing.
- J-lens: ships as a fitting recipe, not committed weights.

## Evidence and caveats

The repo reports a verified J-lens port against component-level autograd checks, with the paper-faithful identity seed making final-layer J-lens readouts exactly equal to the logit lens. On synthetic clips, J-lens improves concept recall by about 31% and reveals a late-mid visual content band around layers 22-26.

The honest boundary is central:

- demo-quality interpretability only;
- the Anthropic workspace paper validated text models, not VLMs;
- single-token readouts only;
- adversarial/unspoken surfaces are mechanical string analysis;
- natural-video baselines and interventions are not done;
- raw-token grid remains primary because concept-label recall is still limited.

## Source handles

- Project hub: `Projects/J-Space-Replay/Index.md`
- Repo: https://github.com/pixiiidust/j-space-replay
- Lite preset library: https://pixiiidust.github.io/j-space-replay/
- Inspiration concept: [[../concepts/j-space-global-workspace|J-Space as Global Workspace]]
- Screenshot/demo: `docs/screenshot.png`, `docs/demo.mp4`
- Evidence: `reports/jlens_evidence.md`, `reports/m2_quality_gate.md`
- Related concepts: [[../concepts/video-retrieve-then-verify-loop|Video Retrieve-Then-Verify Loop]], [[../concepts/verified-video-answer-surfaces|Verified Video Answer Surfaces]], [[../concepts/material-loop-and-glass-interfaces|Material Loop and Glass Interfaces]]
