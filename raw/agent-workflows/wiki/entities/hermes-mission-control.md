---
title: Hermes Mission Control
created: 2026-06-16
updated: 2026-06-16
type: entity
status: pilot
namespace: agent-workflows
tags: [agent-workflows, hermes, pixoid, route-governance]
sources:
  - Projects/Hermes Mission Control/Index.md
confidence: medium
---

# Hermes Mission Control

**Hermes Mission Control** is Jamie's agent-ops coordination hub for the Pixoid crew: Pixoid, Quill, Tinker, and Boba. Its primary namespace is `agent-workflows` because the durable concepts are route governance, persona boundaries, delivery routing, cron interpretation, and issue-driven execution.

## What it controls

- Crew role boundaries and operating surfaces.
- GitHub issue/PR coordination as durable work truth.
- Obsidian/Git as knowledge and project truth.
- Discord as notification surface, not durable truth.
- Cron output as context, not canonical project state.

## Routing significance

Hermes Mission Control is not primarily a public wiki architecture artifact. It feeds `pixi-vault` when compiler/publication rules are affected, and it feeds `eval-trace` when route quality or workflow evidence needs evaluation.

## Cross-namespace links

- `pixi-vault` — for source/output repo boundaries and namespace compiler rules.
- `eval-trace` — for route-quality checks and failure-mode evaluation, including [[../../../eval-trace/wiki/concepts/context-overfitting|context overfitting]].

## Source

Compiled from `Projects/Hermes Mission Control/Index.md`.
