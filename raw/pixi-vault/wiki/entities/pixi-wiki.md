---
title: Pixi Wiki
created: 2026-06-16
updated: 2026-06-18
type: entity
status: active
namespace: pixi-vault
tags: [pixi-vault, pixi-wiki, agentwikis, public-wiki, rag]
sources:
  - wikis/pixi-vault/wiki/syntheses/pixi-vault-to-pixi-wiki-publishing-model.md
  - wikis/local-ai-infrastructure/wiki/concepts/rag-over-agent-wikis.md
  - https://github.com/pixiiidust/pixi-wiki
confidence: high
---

# Pixi Wiki

`pixi-wiki` publishes Jamie's notes, project docs, and research as maintained knowledge bases so humans can browse a clean wiki and agents can read, search, and cite the same Markdown corpus.

## What it does

Pixi Wiki turns each compiled knowledge base into:

- rendered HTML pages for human browsing;
- raw Markdown pages for source-backed retrieval;
- `llms.txt` files for compact agent routing and onboarding;
- `llms-full.txt` files for full-corpus agent context;
- `index.json` registries for tools, tests, and retrieval pipelines;
- a local read-only MCP server so agents can list, search, and read the same KB Markdown files.

## Why it exists

The project turns messy private knowledge work into a shareable publishing surface. Humans browse the web wiki; agents consume the raw Markdown, routing files, registry, and local MCP tools. The private vault remains the source of truth.

## Potential uses

- **RAG over compiled wiki pages:** use maintained pages as the retrieval corpus before adding vector/search infrastructure.
- **Hallucination reduction:** route agents to scoped, cited, freshness-aware pages instead of letting them answer from memory.
- **Agent onboarding:** give new sessions a compact `llms.txt` map before they read deeper pages.
- **Project memory:** preserve decisions, entities, concepts, syntheses, and publication boundaries across sessions.
- **Portfolio surface:** expose selected knowledge/project work as a coherent public system.
- **Eval target:** test whether agents retrieve from the right namespace and cite the right source.

## Namespace classification

Pixi Wiki is primarily an **entity/project artifact** inside the `pixi-vault` namespace because it is the generated public output of the vault compiler system.

Its retrieval use case cross-links to `local-ai-infrastructure`, especially [[../../../local-ai-infrastructure/wiki/concepts/rag-over-agent-wikis|RAG over Agent Wikis]]. Its workflow/use-contract side cross-links to [[../../../agent-workflows/README|Agent Workflows]].

## Current milestone

As of 2026-06-18, the public mirror has:

- compiled namespace pages for project/domain clusters;
- collapsible namespace sidebars with page lists;
- rendered Markdown pages with metadata, raw Markdown links, report-a-mistake links, and previous/next navigation;
- a repository README and GitHub About description that frame Pixi Wiki as a publishing surface for human and agent KB access;
- MCP setup docs at `docs/MCP_SERVER.md`;
- a local read-only MCP server with `list_kbs`, `list_documents`, `read_document`, `search_kb`, `search_all_kbs`, and `get_kb_summary`.

## Public handles

- Human site: https://pixiiidust.github.io/pixi-wiki/
- Repository: https://github.com/pixiiidust/pixi-wiki
- Agent registry: https://pixiiidust.github.io/pixi-wiki/llms.txt
- Full corpus: https://pixiiidust.github.io/pixi-wiki/llms-full.txt
- Machine registry: https://pixiiidust.github.io/pixi-wiki/index.json
- MCP guide: https://pixiiidust.github.io/pixi-wiki/docs/MCP_SERVER.md
