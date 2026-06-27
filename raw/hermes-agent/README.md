---
title: Hermes Agent
created: 2026-06-18
updated: 2026-06-26
type: namespace-overview
status: compiled
category: agent-infrastructure
namespace: hermes-agent
confidence: medium
---

# Hermes Agent

> Curated Hermes Agent operating reference for Jamie/Pixoid: setup, configuration, MCP, profiles, tracing, evals, observability, and workflow-specific usage.

## Scope

### Covers

Hermes Agent setup and configuration, MCP integration, profiles, skills, memory, cron, gateway operations, subagents/delegation, session traces, trajectory capture, batch evals, Langfuse traces, NeMo Relay ATOF/ATIF exports, capability-routing decisions, and Jamie-specific operating reference for Pixoid.

### Not Covered

General AI-agent theory, unrelated community projects, old video transcripts unless they explain a workflow Jamie uses, stale release history not needed for current operation, and web rumors not verified against official Hermes docs or local installed source.

### Current As

2026-06-26 — added Hermes Capability Routing as the primary capability-selection concept: choose the smallest effective Hermes surface, preserve approval boundaries, and verify the route.

## Source Priority

1. Official Hermes docs: `https://hermes-agent.nousresearch.com/docs`
2. Local installed Hermes source: `/usr/local/lib/hermes-agent`
3. AgentWikis Hermes: `https://agentwikis.com/wiki/hermes/llms.txt`
4. Web search for freshness checks only

## Canonical Source Roots

- Official docs mirrored in local install: `/usr/local/lib/hermes-agent/website/docs/`
- Canonical capability-routing concept: `Knowledge/concepts/hermes-capability-routing.md`
- Local source/plugin docs: `/usr/local/lib/hermes-agent/`
- AgentWikis Hermes raw pages: `https://agentwikis.com/raw/hermes/...`

## Crosslinks

- [[../agent-workflows/README|agent-workflows]]
- [[../eval-trace/README|eval-trace]]
- [[../pixi-vault/README|pixi-vault]]
- [[../local-ai-infrastructure/README|local-ai-infrastructure]]

## Maintenance

- Verify commands against official docs or live `hermes --help` before using them.
- Prefer MCP retrieval over web search for stable Hermes reference questions.
- Use web search only when checking latest releases, GitHub issues, or current external state.
- Keep this namespace slim: add operational pages, not a full AgentWikis mirror.
