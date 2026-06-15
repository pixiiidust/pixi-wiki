---
title: Agent Wikis
created: 2026-06-15
updated: 2026-06-15
type: concept
description: Agent-native knowledge surfaces that give agents maintained, scoped, source-backed maps before they act.
status: active
domain: knowledge-systems
tags: [agent-systems, architecture, governance, workflow]
sources:
  - https://agentwikis.com/
  - https://agentwikis.com/why-wikis
  - Projects/Hermes Mission Control/PRD - Knowledge Pack Routing.md
  - Projects/Hermes Mission Control/Knowledge Pack Contract V1.md
confidence: high
---

# Agent Wikis

## Definition

**Agent Wikis** are maintained, scoped, source-backed knowledge surfaces designed for agents. They give agents a trustworthy map before work begins: what the domain covers, what it does not cover, which sources are canonical, how fresh the knowledge is, and what to do when the map is stale or out of scope.

Short form:

```text
Agent Wiki = maintained, scoped, source-backed knowledge surface for agents.
```

## Current synthesis

The important pattern is not “make a private clone of AgentWikis.” The reusable idea is that agents need **maintained knowledge before retrieval**, not just raw search over a pile of files.

Agent Wikis differ from adjacent surfaces:

| Surface | Primary user | Job |
|---|---|---|
| MOCs / project indexes | Humans | Navigate the vault and project context. |
| Knowledge packs / `llms.txt` | Agents | Route to canonical sources with scope, freshness, provenance, and fallback rules. |
| Raw RAG / search | Agents or humans | Retrieve matching text, often without maintained context or trust boundaries. |
| Static HTML wiki | Humans + agents | Browse/read the same maintained corpus in a rendered surface. |

The useful trust semantics to preserve are:

- explicit scope and not-covered boundaries;
- provenance/source links;
- freshness and current-as metadata;
- confidence posture;
- fallback rules for stale or out-of-scope questions;
- raw Markdown as the durable primitive;
- optional rendered HTML as a human surface.

## Pixiedust implementation

In Pixiedust, the first implementation is **Knowledge Pack Routing**:

- root vault `llms.txt`;
- project `llms.txt` files;
- strict frontmatter and required sections;
- source-of-truth hierarchy;
- freshness/fallback metadata;
- Quill maintenance;
- Pixoid review and routing policy;
- Boba source inventory and Tinker implementation facts when needed.

This means:

```text
Concept: Agent Wikis / agent-native knowledge surfaces
Implementation: Knowledge Pack Routing
Artifact type: llms.txt / knowledge pack
Human surface: MOCs now; static HTML in V2
```

## Why it matters

Without this concept, future agents may reduce KPR to “some `llms.txt` files.” The real operating lesson is stronger:

> Agents should load maintained domain maps before acting.

That keeps agents from confusing stale chat context, project notes, GitHub issues, and public web material. It also gives Jamie a reusable vocabulary for future projects that need agent-readable competence without immediately building a crawler, vector store, MCP server, or hosted wiki platform.

## Applications

- **Vault routing:** root and project packs tell agents where to start and when to verify live state.
- **Project onboarding:** a new agent can load one scoped pack before touching issues, PRDs, or code.
- **Portfolio/project knowledge:** public-facing or semi-public knowledge can eventually render from the same Markdown corpus.
- **Crew coordination:** Pixoid routes, Quill maintains narrative and provenance, Boba inventories public sources, and Tinker contributes build facts.

## Boundaries / do not confuse

- Do not treat Agent Wikis as the canonical source of project truth. They route to canonical sources.
- Do not replace human MOCs with `llms.txt`; keep human navigation and agent retrieval contracts separate.
- Do not jump from the concept to V2 runtime work. Static HTML, freshness reports, `index.json`, MCP, and search are later layers with their own gates.
- Do not copy the whole AgentWikis platform when the current need is a vault-native routing contract.

## Related pages

- [[moc-knowledge-cortex]]
- [[agent-capability-route-pattern]]
- [[self-improving-agent-systems]]
- [[profile-memory-boundaries]]
- [[Projects/Hermes Mission Control/PRD - Knowledge Pack Routing|PRD - Knowledge Pack Routing]]
- [[Projects/Hermes Mission Control/Knowledge Pack Contract V1|Knowledge Pack Contract V1]]
- [[Projects/Hermes Mission Control/PRD - Knowledge Pack Routing V2|PRD - Knowledge Pack Routing V2]]
