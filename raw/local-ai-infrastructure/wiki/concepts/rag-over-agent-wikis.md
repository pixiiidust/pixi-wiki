---
title: RAG over Agent Wikis
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: local-ai-infrastructure
tags: [local-ai-infrastructure, rag, agent-wikis, retrieval, infrastructure]
sources:
  - Knowledge/concepts/rag-over-agent-wikis.md
  - Knowledge/concepts/local-retrieval-agent-infrastructure.md
confidence: medium
---

# RAG over Agent Wikis

**RAG over Agent Wikis** means using maintained compiled wiki pages as the retrieval corpus for agents, instead of retrieving directly from raw source dumps or asking the model to answer from memory.

## Infrastructure shape

The practical loop is:

```text
compiled wiki pages → chunks/sections → embeddings → retrieval/rerank → cited answer
```

For Jamie's stack, the important design choice is that the wiki compilation layer comes before the vector layer. Retrieval quality should be improved by curated pages, frontmatter, source metadata, freshness, and namespace boundaries before adding infrastructure complexity.

## Local-first implementation posture

A future local prototype can use:

- compiled `pixi-wiki` Markdown pages as the corpus;
- local embeddings such as `nomic-embed-text` or a similar sentence model;
- FAISS or Qdrant for local vector storage;
- optional reranking for quality;
- source metadata preserved for citations and freshness checks.

## Quality gates

Do not ship retrieval infrastructure because it sounds useful. Use evals:

- recall@k for known routing questions;
- citation support for factual answers;
- fallback behavior when a namespace does not cover the query;
- change-aware questions that test whether updated wiki metadata helps.

## Boundary

No MCP server, vector DB, crawler, hosted search, or runtime RAG is approved by this compiled page. This page is an infrastructure concept and future implementation home, not a build authorization.

## Source

Compiled from `Knowledge/concepts/rag-over-agent-wikis.md` and `Knowledge/concepts/local-retrieval-agent-infrastructure.md`.
