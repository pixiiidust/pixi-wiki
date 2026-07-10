---
title: Local AI Infrastructure
created: 2026-06-16
updated: 2026-07-10
type: namespace-overview
status: active
category: infrastructure
namespace: local-ai-infrastructure
confidence: high
---

# Local AI Infrastructure

> Active namespace for local-first models, retrieval, fine-tuning, deployment, and hardware/software constraints.

## Scope

### Covers

Local-first AI setup, local LLMs, LoRA/fine-tuning infrastructure, RAG over compiled wikis, deterministic local workflow offload, and hardware/software constraints.

### Not Covered

Cloud-only infrastructure unless it affects local-first migration; product UX unless tied to local model constraints.

### Current As

2026-07-10 — active. Includes local retrieval/RAG concepts, VPS app operation, and the LKY Brain consumer-GPU QLoRA case study.

## Canonical Source Roots

- `Knowledge/concepts/local-retrieval-agent-infrastructure.md`
- `Knowledge/concepts/rag-over-agent-wikis.md`
- `Projects/LKY Archive/Index.md`

## Crosslinks

- [[../pixi-vault/README|pixi-vault]]
- [[../curated-tuning-datasets/README|curated-tuning-datasets]]
- [[../rl-sim-labs/README|rl-sim-labs]]

## Public Output Contract

When published to `pixi-wiki`, this namespace should expose:

```text
/raw/local-ai-infrastructure/README.md
/raw/local-ai-infrastructure/wiki/index.md
/wiki/local-ai-infrastructure/README.md
/wiki/local-ai-infrastructure/wiki/index.md
```

## Maintenance

- Edit canonical source notes first.
- Use `Wiki Compiler Maps/Namespace Wiki Compiler Map.md` for routing decisions.
- Do not compile Daily Notes directly unless promoted or verified.
