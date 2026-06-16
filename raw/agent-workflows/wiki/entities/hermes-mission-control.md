---
title: Hermes Mission Control
created: 2026-06-16
updated: 2026-06-16
type: entity
status: compiled
namespace: agent-workflows
tags: [agent-workflows, hermes, pixoid, route-governance]
sources:
  - Projects/Hermes Mission Control/Index.md
  - Projects/Hermes Mission Control/kpr-pixoid-routing-rule.md
  - Projects/Hermes Mission Control/PRD - Knowledge Pack Routing.md
confidence: medium
---

# Hermes Mission Control

**Hermes Mission Control** is Jamie's agent-ops coordination hub for the Pixoid crew: Pixoid, Quill, Tinker, and Boba.

Its primary namespace is `agent-workflows` because the durable knowledge is not the public wiki itself. The durable knowledge is how agents coordinate work: route governance, persona boundaries, issue-backed execution, handoffs, review gates, and durable truth routing.

## Crew roles

- **Pixoid:** orchestrator, reviewer, route owner, final verifier.
- **Tinker:** builder for bounded implementation slices.
- **Quill:** scribe for vault/docs updates and compiled knowledge pages.
- **Boba:** explorer/researcher for external signal and reality checks.

## What it controls

- Crew role boundaries and operating surfaces.
- GitHub issue/PR coordination as durable work truth.
- Obsidian/Git as knowledge and project truth.
- Discord as notification surface, not durable truth.
- Cron output as context, not canonical project state.
- Verification gates before tracker closure.

## Routing significance

Hermes Mission Control feeds `pixi-vault` when compiler/publication rules are affected, and it feeds `eval-trace` when route quality or workflow evidence needs evaluation.

The project should not become a standalone namespace unless it grows an independent audience, source corpus, document types, and freshness lifecycle beyond the broader `agent-workflows` domain.

## Cross-namespace links

- `pixi-vault` — source/output repo boundaries and namespace compiler rules.
- `eval-trace` — route-quality checks and failure-mode evaluation, including [context overfitting](../../../eval-trace/wiki/concepts/context-overfitting.md).

## Related pages

- [[../concepts/knowledge-pack-routing|Knowledge Pack Routing]]
- [[../concepts/agent-entrypoint-mesh|Agent Entrypoint Mesh]]
- [[../syntheses/pixoid-crew-operating-model|Pixoid Crew Operating Model]]

## Source

Compiled from `Projects/Hermes Mission Control/Index.md` and related KPR operating docs.
