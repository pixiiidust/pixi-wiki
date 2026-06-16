---
title: Peer Profiles vs Child Processes
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, crew, governance, routing]
sources:
  - Knowledge/concepts/peer-profiles-vs-child-processes.md
confidence: high
---

# Peer Profiles vs Child Processes

Jamie's named crew agents are **peer Hermes profiles by default**, not Pixoid-owned child processes.

## Decision

- Pixoid/default is the human-facing control plane, orchestrator, reviewer, and reporting surface.
- Tinker is the builder profile for bounded repo work.
- Quill is the scribe/vault profile for bounded source-of-truth updates.
- Boba is the explorer/research profile for public-web and source checks.

Pixoid may use `delegate_task` for local analysis or to simulate a viewpoint, but that is not proof that a named peer profile executed work.

## When child execution is acceptable

Use child/subagent execution for local analysis, review, or drafting when Pixoid will verify the result and no external side effect needs to be attributed to a named peer profile.

## When a real peer route is required

Use a real peer route when issue or route contracts require requested/actual profile evidence, profile-specific tools, profile memory, delivery identity, or auditable worker execution.

## Circuit breaker

Unapproved route recursion is forbidden. Pause if routes attempt direct worker-to-worker triggering, A→B→A loops, profile-wide autonomy, or dynamic supervisors without an approved deployment slice.

## Source

Compiled from `Knowledge/concepts/peer-profiles-vs-child-processes.md`.
