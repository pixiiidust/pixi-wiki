---
title: Agent Capability Route Pattern
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: agent-workflows
tags: [architecture, agent-systems, workflow, governance]
sources:
  - /root/.hermes/knowledge/concepts/agent-capability-route-pattern.md
  - Knowledge/concepts/agent-capability-route-pattern.md
confidence: high
---

# Agent Capability Route Pattern

## Definition

An **agent capability route** is an explicit, bounded path from approved work into a Hermes agent capability. It defines how work enters, which profile may execute it, what that profile may do, what artifact it must return, and how Pixoid verifies the result before it becomes durable truth.

Short form:

```text
approved trigger → profile seam → bounded execution → artifact → verification → handoff/closure
```

## Current synthesis

A route is not just “ask an agent.” It is a small operating contract with these parts:

| Component | Question it answers |
|---|---|
| Trigger | How does work enter the route: approved issue, explicit handoff, scheduled job, or manual CLI command? |
| Profile seam | Which Hermes profile is requested, and how is the actual executing profile verified? |
| Authorization | What approval is required before execution, merge, posting, deployment, or live side effects? |
| Execution bounds | What scope, tools, context budget, max slices, and stop conditions apply? |
| Artifact contract | What must the route produce: PR, report, vault note, issue comment, handoff, or launch prompt? |
| Verification gate | What real evidence proves the artifact worked or stayed in bounds? |
| Observability | What event, issue comment, report, or handoff records requested profile, actual profile, status, and proof? |

The profile seam is the identity-critical part. Named crew work should run through peer Hermes profiles when a real route exists; child subagents can help with analysis, but they are not proof that Tinker, Quill, Boba, or another named peer profile executed work. See [[peer-profiles-vs-child-processes]] and [[hermes-soul-md-wiring]].

## Application

Use this pattern when a future agent needs to decide whether work may be delegated, run AFK, launched under a profile, or closed from existing evidence.

A healthy route should state:

1. the source of truth for the task, usually a GitHub issue, PRD, or handoff;
2. the requested profile or capability;
3. the allowed side effects;
4. the forbidden side effects;
5. verification commands or review checks;
6. the required durable artifact;
7. who may close or merge.

For issue-driven work, route execution usually pairs with [[issue-driven-afk-workflow]] and [[smart-zone-context-discipline]]. For broader autonomy, map the route to [[workspace-autonomy-levels]].

## Boundaries

- A route recommendation is not an automatic trigger.
- Documentation Hygiene recommendations do not automatically invoke Quill, Boba, Tinker, or any worker route.
- `delegate_task` children are useful for local read-only synthesis or review, but they are not named peer-profile execution evidence.
- Do not claim a route is live unless runtime proof shows the requested profile and actual profile match.
- Do not mutate profiles, gateways, providers, cron, webhooks, secrets, MCP, RAG, or deployment state unless the route explicitly authorizes that action.
- Do not merge, deploy, post live messages, or expose secrets without the route’s approval policy and current user scope supporting it.
- Keep transient issue numbers, PR numbers, commit SHAs, and milestone state out of generic concept pages.

## Related pages

- [[peer-profiles-vs-child-processes]]
- [[hermes-soul-md-wiring]]
- [[profile-memory-boundaries]]
- [[workspace-autonomy-levels]]
- [[issue-driven-afk-workflow]]
- [[smart-zone-context-discipline]]
- [[runtime-memory-knowledge-routing]]
- [[context-overfitting]]

## Sources

- `/root/ObsidianVault/Knowledge/concepts/agent-capability-route-pattern.md`
- `/root/ObsidianVault/Projects/Pixoid Agent Capability Routes/Index.md`
