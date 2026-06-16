---
title: RAG over Agent Wikis
created: 2026-06-15
updated: 2026-06-15
type: concept
description: Foundation for using embeddings, semantic search, and retrieval-augmented generation over compiled agent wiki pages instead of raw source dumps.
status: draft
domain: knowledge-systems
tags: [agent-systems, architecture, ai, workflow, research]
sources: [Knowledge/raw/transcripts/tonbi-embeddings-semantic-search-rag.md, https://agentwikis.com/why-wikis, https://pixiiidust.github.io/pixi-wiki, https://github.com/pixiiidust/pixi-wiki]
confidence: medium
---

# RAG over Agent Wikis

## Definition

**RAG over Agent Wikis** means using a maintained wiki as the retrieval corpus for an agent, instead of asking the model to answer from memory or retrieving directly from uncompiled raw sources.

The practical loop is: embed wiki pages or sections, retrieve relevant chunks by semantic similarity, inject the retrieved evidence into the prompt, and require the answer to cite the wiki page/source metadata.

## Current synthesis

Tonbi's embeddings/RAG walkthrough is a useful implementation foundation: embeddings turn text into meaning vectors, cosine similarity retrieves nearby meanings, FAISS or another vector store makes search fast, and the LLM answers from retrieved context instead of guessing from parametric memory.

The Agent Wikis argument adds the architectural punchline: retrieval works better when the corpus is already compiled and curated. Their published comparison claims RAG over raw sources scored 63% correct with 26% hallucination, while RAG over a compiled wiki scored 89% correct with 7% hallucination under the same model/retrieval/token budget. Treat those numbers as product evidence from Agent Wikis, not universal law, but the direction is useful: **maintenance and compilation are the quality lever, not just vector search**.

For Jamie's `pixi-wiki`, this points to a two-layer design:

1. **Canonical wiki layer** — Markdown pages, frontmatter, `llms.txt`, source links, freshness/confidence metadata, and human-readable navigation.
2. **Retrieval layer** — generated embeddings/indexes over those compiled pages or sections, with source metadata preserved for citation and freshness checks.

## Implementation shape for pixi-wiki

- **Corpus:** start with compiled wiki pages, not raw transcript/source dumps. Raw sources can stay as evidence leaves, but retrieval should prefer synthesized pages.
- **Chunking:** for a small wiki, whole-page retrieval may be enough. As pages grow, index stable sections with headings, page slug, source URLs, tags, confidence, and updated date.
- **Embeddings:** use a sentence-embedding model trained for similarity, such as `all-MiniLM-L6-v2` for a small local prototype, then evaluate stronger embedding models if recall is poor.
- **Similarity:** normalize vectors and use cosine similarity / inner product search. Keep exact keyword search as a fallback for names, issue numbers, paths, and rare terms.
- **Vector store:** FAISS is enough for a local/static prototype. Chroma, LanceDB, or a hosted vector DB can be considered only when operational needs exceed local files.
- **Answer flow:** route with `llms.txt` and index metadata first, retrieve top-k wiki sections, build a compact evidence packet, answer only from retrieved evidence, and cite page/source handles.
- **Freshness:** use frontmatter `updated`, `confidence`, and source metadata to tell the agent when wiki evidence is stale or outside scope.

## Quality gates

A wiki-RAG implementation should be judged by retrieval and answer quality, not by whether a vector database exists.

Useful gates:

- **Retrieval recall@k:** does the correct page/section appear in the top-k for vague user queries?
- **Citation support:** every factual answer should cite the retrieved page/source; unsupported claims count as hallucinations.
- **Change-aware questions:** can it answer "what changed?" using updated wiki metadata better than live web search?
- **Fallback behavior:** does it say "not covered" or fall back to web/search when the wiki scope does not cover the question?
- **Maintenance loop:** can page updates refresh the index without retraining or hand-editing prompts?

## Boundaries

- Do not fine-tune for changing wiki knowledge; update the wiki and retrieval index instead.
- Do not treat raw-source RAG and wiki-RAG as equivalent. The wiki compilation step is the expected quality gain.
- Do not let embeddings replace explicit routing. `llms.txt`, indexes, tags, and MOCs still tell the agent where truth lives.
- Do not build a hosted/vector/MCP runtime for `pixi-wiki` without a separate implementation gate; this page is a foundation note, not approval to ship infrastructure.

## Related pages

- [[agent-wikis]]
- [[local-retrieval-agent-infrastructure]]
- [[moc-knowledge-cortex]]
- [[runtime-memory-knowledge-routing]]
