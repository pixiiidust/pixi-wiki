---
title: AgentWikis Hermes Curated Seed
created: 2026-06-18
updated: 2026-06-18
type: summary
status: compiled
namespace: hermes-agent
tags: [hermes-agent, agentwikis, source-ingest, curation]
sources:
  - https://agentwikis.com/wiki/hermes/README.md
  - https://agentwikis.com/wiki/hermes/llms.txt
  - https://agentwikis.com/raw/hermes/wiki/index.md
confidence: medium
---

# AgentWikis Hermes Curated Seed

AgentWikis hosts a Hermes knowledge base with roughly 105 documents covering Hermes setup, configuration, workflows, extensions, releases, memory providers, platforms, providers, and community projects.

## Useful slices for Jamie/Pixoid

Use AgentWikis as a map for:

- MCP integration
- CLI and configuration reference
- profiles and multi-instance routing
- skills and memory systems
- cron and scheduling
- subagents and delegation
- release summaries when checking feature history
- ecosystem/community inventory when exploring external references

## Skip by default

Do not import everything. Skip or quarantine:

- video transcript summaries unless a transcript explains a workflow Jamie uses;
- broad community lists unless they answer a current question;
- old release pages unless debugging historical behavior;
- pages that conflict with official docs or local installed source.

## Staleness note

The AgentWikis Hermes README still claims an older verified release in one place, while `llms.txt` and the master index report v0.16.0 current as of 2026-06-16. Treat this as a useful but secondary source.

## Import posture

AgentWikis is a discovery layer. Official Hermes docs and live local source decide commands, config, and setup steps.
