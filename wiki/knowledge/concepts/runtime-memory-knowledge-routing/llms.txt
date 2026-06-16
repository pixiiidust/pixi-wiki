---
title: Runtime Memory Knowledge Routing
created: 2026-06-15
updated: 2026-06-15
type: concept
description: Runtime rule for combining injected memory, Honcho, local Hermes knowledge, Obsidian Knowledge, skills, GitHub/project truth, and session search without turning memory into a wiki dump.
status: active
domain: agent-systems
tags: [agent-systems, knowledge-management, governance, memory]
sources: [discord-thread]
confidence: high
---

# Runtime Memory Knowledge Routing

## Definition

Runtime memory knowledge routing is the rule for how agents combine always-injected memory, Honcho recall, local Hermes knowledge, Obsidian Knowledge packs, skills, GitHub/project truth, and session search while doing live work.

The goal is better agent evolution without turning memory into a wiki dump.

## Layer model

| Layer | Runtime role | Entrypoint |
|---|---|---|
| `USER.md` / profile memory | Tiny always-injected operating contract and stable facts | injected prompt + memory tools |
| Honcho | Recalled observations and peer-context synthesis | Honcho tools, not files |
| Local Hermes knowledge | Agent-facing reusable concepts and dossiers | `~/.hermes/knowledge/llms.txt` |
| Obsidian Knowledge | Human-facing durable concepts and source-backed synthesis | `Knowledge/llms.txt` |
| Projects / GitHub | Current source of truth for project state | `Projects/llms.txt` + GitHub live checks |
| Skills | Repeatable procedures | skill loader |
| Sessions | Conversation archaeology | `session_search`, never canonical alone |

## Rule

Memory should not get a raw `llms.txt` dump, because memory is intentionally compact, private, tool-mediated, and always injected. Instead, agents need a **memory routing contract** inside knowledge packs:

- use memory for tiny stable facts and preferences;
- use Honcho for observed peer context;
- use local Hermes knowledge for reusable agent-operational concepts;
- use Obsidian Knowledge for human-facing durable concepts;
- use GitHub/project packs for current project truth;
- use skills for repeatable procedures;
- use session search only to recover prior conversation context.

## Runtime pattern

1. Start with injected memory and user profile as hints, not proof.
2. Load the relevant `llms.txt` pack when the task touches a durable domain.
3. Verify current state live when the task depends on project/runtime facts.
4. Promote durable learning to the narrowest correct layer after the work:
   - memory only for stable tiny facts;
   - local knowledge for reusable agent-operational concepts;
   - Obsidian for human-facing knowledge/project truth;
   - skills for procedures.
5. Do not save raw outputs, issue progress, PR numbers, command logs, or stale project state to memory.

## Why not a memory `llms.txt`?

A file entrypoint for memory contents would encourage agents to treat memory as a source corpus. That is wrong. Memory is an always-on hint layer with capacity and privacy constraints. It is tool-mediated context, not a raw Markdown corpus. The correct agent-readable object is a routing contract that tells the agent **when to use memory tools** and **when not to**.

## Guardrails

- No raw memory dump and no memory `llms.txt` file.
- No automatic memory pruning from this routing pattern.
- No automatic pack rewriting.
- No cron, profile, gateway, provider, webhook, MCP, RAG, crawler, search, vector DB, or public hosting changes from this concept.
- Treat injected memory as hints; verify live state when current project/runtime facts matter.

## Related pages

- [[profile-memory-boundaries]] — storage-layer classification rule.
- [[agent-wikis]] — broader concept of maintained, scoped, source-backed agent knowledge surfaces.
- [[self-improving-agent-systems]] — promotion ladder for durable agent learning.
