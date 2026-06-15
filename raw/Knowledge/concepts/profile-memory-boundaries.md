---
title: Profile Memory Boundaries
created: 2026-06-11
updated: 2026-06-13
type: concept
description: Boundary model for routing durable knowledge between USER.md, Hermes memory, local knowledge, Obsidian/GitHub project truth, and skills.
status: active
domain: agent-systems
tags: [agent-systems, governance, workflow]
sources: [discord-thread]
confidence: high
---

# Profile Memory Boundaries

## Definition

A boundary model for deciding where Jamie/Hermes knowledge belongs: universal user operating contract, profile memory, local Hermes knowledge, Obsidian project truth, or skills.

## Boundary model

- **`USER.md`** — universal, person-level operating contract for how agents work with Jamie. It can point agents toward durable knowledge layers, but should not hold project/business/domain-specific north stars.
- **Profile `MEMORY.md`** — compact profile-specific facts and runtime lessons.
- **Local Hermes knowledge** — `~/.hermes/knowledge/`, the agent-facing compiled knowledge layer.
  - `concepts/` for reusable frameworks, lenses, and distinctions.
  - `entities/` for people, tools, projects, roadmaps, and durable initiatives.
- **Obsidian/GitHub** — human-facing and project-facing source of truth for project notes, strategy, decisions, PRs, issues, and long-form documentation.
- **Skills** — reusable procedures/workflows an agent should load and execute.

## Classification rule

Before saving knowledge, classify it:

| Content type | Home |
|---|---|
| Universal behavior preference | `USER.md` |
| Reusable framework/lens/distinction | Local Hermes `knowledge/concepts/` and optionally Obsidian `Knowledge/concepts/` |
| Project, roadmap, north star, initiative, domain strategy | Project/entity note, backed by Obsidian/GitHub truth |
| Repeatable procedure | Skill |
| Temporary task progress, PR/issue status, command logs | GitHub/Obsidian project notes/session logs, not memory |

## Current milestone

On 2026-06-11, Jamie clarified that the AI business north star is a **project/roadmap**, not a durable concept. Pixoid corrected the taxonomy: `USER.md` became a universal operating contract pointing agents to durable knowledge layers; the Zerg AI Democratization Roadmap remained a project; the AI-native framing material remained a reusable concept/skill.

## Related pages

- [[ai-native-problem-framing-framework]] — reusable AI-native system-framing concept.
- [[verb-first-product-positioning]] — reusable product copy lens.
- [[matt-pocock-sdlc-rhythm]] — workflow gates before product/SDLC work.
