---
title: Local Retrieval Agent Infrastructure
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: local-ai-infrastructure
tags: [agent-systems, ai, architecture, workflow, knowledge-management]
sources:
  - /root/.hermes/knowledge/concepts/local-retrieval-agent-infrastructure.md
  - Knowledge/concepts/local-retrieval-agent-infrastructure.md
confidence: medium
---

# Local Retrieval Agent Infrastructure

## Definition

**Local retrieval agent infrastructure** is the reference pattern for giving agents private, source-grounded retrieval over local knowledge without sending the private corpus to hosted systems.

Reference pipeline:

```text
ingest → clean → chunk → embed → Qdrant/vector store → retrieve → rerank → MCP/agent access
```

The pattern is useful as architecture vocabulary. It is not an implementation approval.

## Current synthesis

The vault source describes a local RAG stack inspired by Krill-style infrastructure:

1. ingest documents from approved local sources;
2. clean and neutralize sensitive or irrelevant material;
3. chunk by stable sections with metadata;
4. embed chunks with a local embedding model;
5. store vectors in Qdrant or a similar vector database;
6. retrieve a broad candidate set;
7. rerank to a small evidence packet;
8. expose results to an agent through MCP or another controlled local interface.

For Jamie’s current agent workflow, the governance lesson matters more than the stack: improve explicit routing first, then only add retrieval infrastructure if static wiki/index/llms routing fails an important question set. See [[agent-wikis]], [[rag-over-agent-wikis]], and [[runtime-memory-knowledge-routing]].

## Application

Use this page to reason about:

- when a markdown/`llms.txt` knowledge pack is enough;
- when a static retrieval eval should be written before infrastructure;
- how private-corpus retrieval should preserve provenance and freshness;
- why compiled/synthesized wiki pages are usually a better retrieval corpus than raw transcripts;
- how hardware/local-model lessons differ from agent workflow governance.

Hardware/local-model lessons answer “can this run locally?” Workflow-governance lessons answer “should this be routed, verified, and maintained this way?” Keep those questions separate.

## Boundaries

This concept does **not** authorize:

- installing Qdrant, Ollama, MCP servers, vector databases, rerankers, or embedding services;
- changing providers, gateways, profile config, cron jobs, webhooks, secrets, or deployment routing;
- building or deploying RAG infrastructure;
- generating or publishing public wiki output;
- creating automatic memory pruning, model fine-tuning, profile creation, or provider changes;
- treating raw transcripts or scratch notes as equivalent to compiled wiki pages;
- replacing explicit routing with embeddings.

If retrieval is needed, start with a separate approved issue that defines eval questions, privacy boundaries, corpus scope, verification, and rollback.

## Related pages

- [[agent-wikis]]
- [[rag-over-agent-wikis]]
- [[runtime-memory-knowledge-routing]]
- [[self-improving-agent-systems]]
- [[moc-knowledge-cortex]]
- [[bounded-context-tree-pattern]]

## Sources

- `/root/ObsidianVault/Knowledge/concepts/local-retrieval-agent-infrastructure.md`
- `/root/ObsidianVault/Knowledge/concepts/agent-wikis.md`
- `/root/ObsidianVault/Knowledge/concepts/rag-over-agent-wikis.md`
