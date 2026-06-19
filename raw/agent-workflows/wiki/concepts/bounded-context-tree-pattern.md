---
title: Bounded Context Tree Pattern
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: agent-workflows
tags: [architecture, workflow, ai, knowledge-management]
sources:
  - /root/.hermes/knowledge/concepts/bounded-context-tree-pattern.md
  - Knowledge/concepts/bounded-context-tree-pattern.md
confidence: high
---

# Bounded Context Tree Pattern

## Definition

A **bounded context tree** organizes project knowledge as a self-contained domain with its own language, decisions, and artifacts.

```text
Root = bounded context / project hub
Branch = major concern inside the context
Leaf = specific artifact, decision, PRD, ADR, report, or source note
```

This adapts Domain-Driven Design for personal and agent-readable knowledge management.

## Current synthesis

Use this pattern for serious multi-artifact project knowledge. A strong context tree has:

- one `Index.md` or hub at the root that defines scope, current status, source-of-truth order, and branch map;
- branches for stable concerns such as strategy, domain model, architecture, product, research, decisions, and implementation artifacts;
- leaves that hold focused evidence or decisions, not transcript dumps;
- explicit cross-context links only when a real boundary is crossed;
- one primary parent branch for each durable note.

The goal is language isolation. Each project or domain owns its vocabulary. Agents should not import terms, priorities, or constraints from one bounded context into another unless a cross-link explains why.

## Application

Use this pattern when:

- a project has multiple PRDs, ADRs, decisions, source inventories, prototypes, or research notes;
- a brainstorm is becoming a committed project;
- raw transcripts need to be distilled into a project hub and leaf artifacts;
- an agent needs a map before editing Obsidian or a local knowledge namespace;
- MOC/navigation work risks becoming a backlink hairball.

Minimal example:

```text
Projects/Example/Index.md          # root / hub
Projects/Example/01-Strategy/      # branch
Projects/Example/02-Domain/        # branch
Projects/Example/03-Architecture/  # branch
Projects/Example/Decisions/        # branch
Projects/Example/Decisions/ADR-001.md  # leaf
```

In the local Hermes KB, the same principle means concept pages should be concise reusable leaves linked through [[moc-knowledge-cortex]], not copied project logs.

## Boundaries

- Do not dump raw chat transcripts or command logs into a project hub.
- Do not let MOCs replace project hubs; MOCs route, hubs own context.
- Do not create deep folder trees before the domain has enough durable artifacts to justify them.
- Do not import stale project status into generic concept pages.
- Do not add backlinks just to make graph view look connected; add crosslinks only for useful retrieval or real domain meaning.
- Do not promote scratch/capture notes into canonical knowledge without source review.

## Related pages

- [[moc-knowledge-cortex]]
- [[matt-pocock-sdlc-rhythm]]
- [[runtime-memory-knowledge-routing]]
- [[agent-wikis]]
- [[context-overfitting]]

## Sources

- `/root/ObsidianVault/Knowledge/concepts/bounded-context-tree-pattern.md`
- `/root/ObsidianVault/Projects/README.md`
