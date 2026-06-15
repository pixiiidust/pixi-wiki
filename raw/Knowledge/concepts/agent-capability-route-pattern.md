---
title: Agent Capability Route Pattern
created: 2026-06-07
updated: 2026-06-13
type: concept
tags: [architecture, agent-systems, workflow, governance]
sources: [Projects/Pixoid Agent Capability Routes/Index.md]
confidence: high
---

# Agent Capability Route Pattern

## Definition

An explicit, bounded trigger path from approved work into a Hermes agent's capabilities, governed by route contracts, profile seams, verification gates, and observability. Each route defines:

- **Trigger** — how work enters the route (approved GitHub issue, explicit handoff)
- **Profile seam** — which agent profile executes the work (Tinker, Quill, Boba)
- **Authorization** — what approvals are needed before execution begins
- **Execution bounds** — scope limits, context budgets, Smart Zone discipline
- **Artifact contract** — what the route produces (PR, report, documentation)
- **Verification gate** — how results are checked before handoff
- **Observability** — events recorded for traceability

## Origin

The pattern was developed in the `pixoid-inbound-agents` repository (repo: `pixiiidust/pixoid-inbound-agents`) to solve a specific problem: agents with broad capability sets need explicit guardrails so they don't exceed their authorized scope, trigger unintended work, or operate without oversight.

The original v1 route proved a narrow Tinker path: approved GitHub issue or explicit approved handoff → bounded Tinker execution seam → scoped branch/commit → PR review artifact → verification → route-authorized merge → main verification → issue closure → handoff and next launch prompt. Later slices generalized the GitHub issue dispatcher route to Quill and Boba while preserving Pixoid review gates.

## Route anatomy

| Component | Description |
|-----------|-------------|
| Trigger adapter | GitHub issue dispatcher with dry-run/live modes, one-task lock, pause/resume |
| Authorization | Strict approved-trigger path; rejected triggers explicitly blocked |
| Profile seam | Runtime profile selection (`tinker`, `quill`, `boba`); requested vs actual profile logged |
| Execution bounds | Smart Zone discipline (watch at 30%, stop before 40%, checkpoint); max 3 slices without Jamie approval |
| Artifact contract | Issue-named branch → scoped commit → PR as review artifact → merge when route-approved |
| Verification | Unittest checks on main, profile mismatch/failure stop behavior, route observance |
| Observability | Route-event fields, compact final report shape, closure handoff + launch prompt |

## Preserved boundaries

- Tinker may mutate repos only from `ready-for-tinker` issues or explicit approved route handoffs
- Explicit route handoffs are approval prompts first, not silent triggers
- Tinker opens PRs as review artifacts; no direct main merge by default
- Pixoid handles review, bounded feedback, and merging for Tinker
- Tinker cannot directly command Quill or Boba
- Documentation Hygiene recommendations are metadata only; they do not auto-trigger other agents
- Smart Zone discipline is universal across all routes

## Current implementation

Pixoid Agent Capability Routes is the reference implementation. The residual GitHub issue closure chain is complete: children #63-#66 and parent issues #2/#4/#5/#6 are closed with 102 passing unittests on `main`. This means the bounded GitHub issue dispatcher route is proven for Tinker, Quill, and Boba. It does **not** mean dynamic webhooks, always-on supervisors, or broad live Discord posting are shipped.

Role names overlap with the parked EdenOS adaptation vocabulary, but the route pattern is now independently grounded in Jamie's Hermes workflow: Pixoid is the default control plane/reviewer, Tinker is builder, Quill is scribe, and Boba is explorer/researcher. Pika remains parked/future unless Jamie reopens that route.

## Related concepts

- **Route status matrix** — live-vs-future route truth in [[Projects/Hermes Mission Control/Index#Canonical live route status matrix]]
- **Smart Zone discipline** — context budget enforcement: watch at ~30%, checkpoint before 40%
- **Handoff contract** — every issue/PR closure produces a compact `/handoff` document + separate launch prompt
- **Route contract** — formal specification of trigger, authorization, execution bounds, artifact, and verification
- **Profile seam** — the runtime profile layer that enforces which agent capabilities are available on a given route

## Related pages

- [[Projects/Pixoid Agent Capability Routes/Index|Pixoid Agent Capability Routes]]
- [[Projects/EdenOS/Index|EdenOS — Multi-Agent Workflow OS]]
- [[Knowledge/concepts/matt-pocock-sdlc-rhythm|Matt Pocock SDLC Rhythm]]
- [[Knowledge/concepts/bounded-context-tree-pattern|Bounded Context Tree Pattern]]
- [[Knowledge/index|Knowledge Wiki Index]]