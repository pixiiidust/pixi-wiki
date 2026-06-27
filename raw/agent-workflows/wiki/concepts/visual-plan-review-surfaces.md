---
title: Visual Plan Review Surfaces
created: 2026-06-26
updated: 2026-06-27
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/visual-plan-review-surfaces.md
confidence: high
---

# Visual Plan Review Surfaces

A visual plan review surface turns a PRD, implementation plan, or planned multi-file change into a local interactive MDX artifact that Jamie can inspect before code changes begin.

For Jamie's current workflow, the default is **local/private self-use**: local MDX files and local verification, not hosted publishing, share links, or comment workflows.

## Default artifact shape

```text
.agent-native/plans/<slug>/
  plan.mdx
  canvas.mdx        # only when UI/product visuals help
  prototype.mdx     # only when interaction matters
```

The `visual-plan` Hermes skill from BuilderIO's Agent-Native skills turns normal agent plans into a richer review medium: structured plan sections, file maps, diagrams, wireframes, annotated code, open questions, and optional prototype surfaces.

## Routing rules

- Load `visual-plan` when Jamie asks to turn a PRD, implementation plan, issue plan, or architecture/UI plan into a review surface.
- Use local/private mode by default. Hosted Agent-Native Plan auth, share links, and comments are optional, not prerequisites.
- Keep durable truth in source-controlled Markdown, Obsidian project hubs, GitHub issues/PRDs, and handoffs. The visual surface is a review artifact, not the only source of truth.
- For UI/product work, include canvas wireframes or prototype surfaces only when they help review actual states or flows.
- For backend/architecture/data work, skip decorative UI and use document-local diagrams, file maps, annotated code, API/schema blocks, risks, and verification steps.
- Do not start implementation until the review surface has been generated and Jamie has approved the direction, unless the task is trivial or Jamie explicitly skips the gate.

## Where it fits

Visual-plan is an approval surface between planning and implementation:

- after `/to-prd` when the PRD needs a richer review surface before issue slicing;
- after an implementation plan when the plan touches multiple files, architecture, UX states, or open questions;
- before `/to-issues` when the plan needs human review before creating execution slices;
- before `/implement` when an existing plan needs visual inspection rather than more chat discussion.

It complements [[matt-pocock-sdlc-rhythm]]: `/prototype` tests experiential unknowns, `/grill-with-docs` aligns language and decisions, `/to-prd` captures requirements, and `visual-plan` makes approved or near-approved plans inspectable.

## Boundaries

- Not for trivial one-line fixes or changes whose diff is easier to review than a plan.
- Not a substitute for live repo inspection, tests, GitHub issues, PRDs, or handoffs.
- Not authorization to publish, deploy, share, or use hosted comment workflows.
- Not a place to store secrets, private customer data, or final project truth outside source-controlled plan files.

## Related pages

- [[matt-pocock-sdlc-rhythm]]
- [[agent-skill-routing]]
- [[../../ai-native-product-surfaces/wiki/concepts/agent-output-decision-artifacts|Agent Output Decision Artifacts]]
- [[../../ai-native-product-surfaces/wiki/concepts/interaction-mode-routing|Interaction Mode Routing]]
- [[../../ai-native-product-surfaces/wiki/concepts/material-loop-and-glass-interfaces|Material Loop and Glass Interfaces]]
