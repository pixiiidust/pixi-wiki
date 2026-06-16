---
title: Local Retrieval-Augmented Agent Infrastructure
created: 2026-06-15
updated: 2026-06-15
type: concept
description: Applied architecture lessons from Krill's dual-RTX 5090 local agent stack — hardware setup, retrieval pipeline (Qdrant + Ollama + MCP), agent workflow governance, and relevance to Jamie's PC build decisions.
status: active
domain: agent-systems
tags: [agent-systems, ai, architecture, workflow]
sources: [raw/articles/releasing-the-kraken-krill-blog.md]
confidence: high
---

# Local Retrieval-Augmented Agent Infrastructure

> Synthesised from [[raw/articles/releasing-the-kraken-krill-blog|Releasing The Kraken (Krill Blog, 2026-06-15)]]. Directly applicable to [[Projects/New PC Build Architecture/Index|New PC Build Architecture]].

---

## Hardware Lessons for a 5090 Build

| Lesson | Implication for Jamie's Build |
|---|---|
| **Dual 5090 allows tensor-splitting 80B MoE models** — Krill runs `qwen3-coder-next` (80B MoE, ~3B active/token) at ~136 tok/s across 2×5090s. | Single 5090 is still excellent for 7B–32B full-VRAM. Dual 5090 is only needed for MoE 70B+ at speed. Jamie's build with **one 5090 first, add second later if needed** is validated. |
| **CUDA 12.8 + `cu128` is mandatory for Blackwell (`sm_120`).** Half the prebuilt wheels silently fell back to CPU. | Verify torch and all inference libs are `cu128`-built. Ollama + Docker + NVIDIA container toolkit must use CUDA 12.8. |
| **125 GiB RAM, ~7.4 TB NVMe** — not extreme. 32 logical cores. | Jamie's 128GB RAM + 4–8TB NVMe plan is well-aligned and sufficient. |
| **Ollama bound to LAN** — clean local serving without cloud exposure. | Same pattern fits Jamie's Tailscale/LiteLLM routing layer between nodes. |

---

## Retrieval Pipeline (The Corpus / Second Brain)

Krill's proven local RAG stack:

```
Ingest → Clean → Chunk → Embed (nomic-embed-text, 768d)
→ Store (Qdrant) → Retrieve (top-40 semantic)
→ Rerank (bge-reranker-v2-m3, cross-encoder, top-8)
→ Serve (local Ollama + MCP)
```

**Key details:**
- **Embedding model:** `nomic-embed-text` (768-dim) — lightweight, effective, runs on Ollama.
- **Reranker:** `bge-reranker-v2-m3` — cross-encoder, pinned to one GPU in dual-5090 setups.
- **Vector store:** Qdrant — proven, local, Docker-based.
- **MCP server** (`Corpus MCP`) wraps retrieval so agents access memory locally with no data sent to API providers.

**Applicability to Jamie's setup:** This is the exact architecture pattern for a local RAG system. The helper NVIDIA desktop (4090/3090) or 5090 PC can host the retrieval pipeline. Qdrant in Docker + Ollama + a lightweight MCP server is a realistic first-pass stack.

> See also: [[hermes-soul-md-wiring]] for agent identity patterns that pair with local MCP servers.

---

## Guardrails (Sensitivity Doors)

| Layer | Guard | Relevance |
|---|---|---|
| **Ingest** | Secrets neutralised → `[REDACTED]` markers | Apply to any local corpus ingest pipeline. |
| **Retrieval** | Two doors: work door (withholds personal/financial) vs personal door (full fidelity, output forbidden from artifacts) | Critical for Jamie's mixed-use setup — separate work/personal retrieval contexts. |
| **Egress** | Pre-commit scanner blocks secrets but passes non-secret PII | Pre-commit hooks for any agent-generated content. |

---

## Agent Workflow Governance

| Rule | Why It Matters |
|---|---|
| **No agent can merge its own work.** No single agent owns more than one link in the chain. | Prevents any single agent from having unchecked write authority. Relevant to Jamie's Hermes crew (Pixoid dispatches, Quill writes, Ben decides). |
| **Three-agent chain:** Ghost tests → Blue fixes → Kraken analyses/oversees → Ben decides/merges. | Well-bounded separation of concerns. The test/fix/oversight/decide quad is a repeatable pattern. |
| **Lesson feedback loop:** Every fix writes to `docs/lessons/`. CI rejects PRs without one. Blue reads lessons before next fix. | Jamie's Knowledge wiki `log.md` and `concepts/` serve a similar compounding-memory function. Formalising a lesson-required gate could strengthen the agent crew. |
| **No auto-promotion of voice adapters** — Ben reads the eval report before any QLoRA weights ship. | Human-in-the-loop for model changes. Relevant whenever Jamie incorporates adapters. |

---

## Local Models Reference

| Model | Role | Notes for Jamie |
|---|---|---|
| `qwen3-coder-next` (80B MoE) | Coding, nightly judge | Requires dual 5090 for full speed; single 5090 can run smaller quants with offload. |
| `qwen3.6:35b` | Reasoning/planning | ~165 tok/s on dual 5090; comfortable on single 5090 32GB. Good candidate for Jamie's daily inference model. |
| `qwen2.5vl:7b` | Vision (captioning, OCR) | Lightweight vision model — good for photo/document ingest pipeline on helper node. |
| `nomic-embed-text` | Embeddings (768d) | Standard for local RAG; runs on CPU or GPU trivially. |
| `bge-reranker-v2-m3` | Cross-encoder reranker | Pins to one GPU; improves retrieval quality significantly over raw cosine similarity. |
| QLoRA voice adapter (Qwen2.5-14B) | Writing style | Weekly retrain on human's writing samples. Fact vs voice separation is a key insight. |

> Frontier Claude is used **only** for interactive/visual design judgment. **Everything touching the private corpus stays local.**

---

## Open Questions for Jamie's Setup

1. Should Jamie's retrieval pipeline use the same stack (nomic-embed-text → Qdrant top-40 → bge-reranker top-8 via Ollama + MCP) or a lighter path?
2. Two-door guardrail (work vs personal) — does Jamie need separate retrieval contexts for Pixoid work vs personal notes?
3. Should the Hermes crew adopt a "no agent merges own work" rule more explicitly?
4. Weekly QLoRA voice adapter — is Jamie's writing corpus large enough / stable enough to justify this?
5. Once Jamie's 5090 build is live, could it host a Corpus MCP for the whole LAN, serving the Mac Studio / DGX Spark (if added later)?

---

## Related

- [[Projects/New PC Build Architecture/Index|New PC Build Architecture]] — the project this concept directly informs
- [[self-improving-agent-systems]] — compounding agent loops, related to the lesson feedback pattern
- [[moc-knowledge-cortex]] — MOC layer as routing brain, related to the MCP server pattern
- [[agent-wikis]] — maintained knowledge surfaces for agents, related to the Corpus pattern
- [[projects-hermes-mission-control|Hermes Mission Control]] — agent crew architecture where governance patterns apply