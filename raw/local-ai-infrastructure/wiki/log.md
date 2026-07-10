---
title: Local AI Infrastructure — Activity Log
created: 2026-06-16
updated: 2026-07-10
type: log
status: active
namespace: local-ai-infrastructure
---

# Local AI Infrastructure — Activity Log

> Append-only namespace log.

## 2026-06-16 create | Namespace scaffold initialized

- Created README, CLAUDE instructions, raw folder, index/log, and typed wiki folders.
- Source routing comes from `Wiki Compiler Maps/Namespace Wiki Compiler Map.md`.
- No Daily Notes were copied or compiled.

## 2026-06-16 update | Add first local-AI infrastructure compiled concepts

- Added `wiki/concepts/local-retrieval-agent-infrastructure.md`.
- Added `wiki/concepts/rag-over-agent-wikis.md`.
- Updated `wiki/index.md` from scaffold to active content index.
- Preserved the boundary that this is not approval to build MCP/vector/search runtime infrastructure.
- No Daily Notes were copied or compiled.

## 2026-06-16 update | Link Pixi Wiki to RAG-over-wiki posture

- Updated `wiki/concepts/rag-over-agent-wikis.md` to name `pixi-wiki` as the current public corpus candidate.
- Preserved the eval-first boundary: use the compiled wiki as the first retrieval/eval surface before adding vector DB or runtime RAG infrastructure.
- No Daily Notes were copied or compiled.

## 2026-06-18 update | Crosslink Hermes local-stack routing

- Added cross-namespace pointer to the Hermes Agent external wiki import review for Local Stack / Airplane Mode and deployment-backend routing.
- No Daily Notes were copied or compiled.
## 2026-06-18 update | Refresh local retrieval infrastructure boundary

- Refreshed `wiki/concepts/local-retrieval-agent-infrastructure.md` from the verified local Hermes KB closure synthesis.
- Preserved the explicit no-install/no-MCP/no-RAG-build/no-provider/no-deploy authorization boundary.

## 2026-06-19 ingest | Tonbi VPS agent web app workflow

- Added `raw/transcripts/tonbi-vps-agent-web-app-workflow-2026.md` from Jamie-supplied transcript of Tonbi AI video.
- Added `wiki/concepts/vps-agent-web-app-pattern.md` as a local-infrastructure concept for small-VPS + resident-agent web app operation.
- Updated `wiki/index.md` with the new concept and source handles.
- Routed workflow/human-gate material by crosslink to `agent-workflows`; kept primary namespace as `local-ai-infrastructure` because the reusable decision is VPS/local deployment topology.

## 2026-07-10 add | LKY Brain consumer-GPU QLoRA case study

- Added `wiki/summaries/lky-brain-consumer-gpu-qlora.md` from the verified public repo and training report.
- Distinguished the successful Unsloth script from the retained but unexecuted Axolotl portability config.
- Captured WSL2 + Blackwell failure isolation, non-packed training, plain-Transformers inference, checkpoint preservation, and environment-specific boundaries.
- Crosslinked source/provenance to `curated-tuning-datasets` and evidence quality to `eval-trace`.

## 2026-07-10 refresh | LKY Brain public-use and portability milestone

- Refreshed the consumer-GPU QLoRA summary from repo commit `da490f6`.
- Recorded checkout-relative launchers, the documented 4-bit PEFT quick-test path, and the vLLM OpenAI-compatible serving path.
- Preserved the boundary between the executed training run and newly documented but not review-executed inference/serving examples.
- Confirmed that dataset, training, and evaluation numbers did not change in this prose/portability refresh.
