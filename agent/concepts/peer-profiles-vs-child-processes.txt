---
title: Peer Profiles vs Child Processes
created: 2026-06-13
updated: 2026-06-13
type: concept
description: Architecture decision for when Jamie's crew agents run as peer Hermes profiles versus child/subagent processes.
status: active
domain: agent-systems
tags: [agent-systems, governance, workflow]
sources: [Projects/Hermes Mission Control/Index.md, Projects/Pixoid Agent Capability Routes/Index.md]
confidence: high
---

# Peer Profiles vs Child Processes

## Decision

Jamie’s named crew agents are **peer Hermes profiles by default**, not Pixoid-owned child processes.

- **Pixoid/default** — human-facing control plane, orchestrator, reviewer, and reporting surface.
- **Tinker** — builder profile for bounded repo work.
- **Quill** — scribe/vault profile for bounded source-of-truth updates.
- **Boba** — explorer/research profile for public-web/source checks.
- **Pika** — parked/future profile; no active crew route.

Pixoid may use `delegate_task` for local analysis or to simulate a named viewpoint when no live peer route is being invoked, but that is a fallback/subagent analysis path — not proof that a named peer profile executed work.

## Why peer profiles

Peer profiles preserve identity, memory boundaries, profile-specific tools, route evidence, and auditability. They also match Jamie’s operating model: Jamie hears from Pixoid, while workers execute bounded tasks behind explicit route contracts.

## When child/subagent execution is acceptable

Use a child/subagent when:

- the work is local analysis, review, or drafting inside the current session;
- no external side effect needs to be attributed to a named peer profile;
- the result will be verified by Pixoid before being treated as source of truth;
- the task does not require profile-specific credentials, gateway identity, or persistent route logs.

When simulating Quill/Boba/Tinker viewpoints through a child, say so explicitly and do not call it a live peer execution.

## When a real peer route is required

Use a real peer route when:

- the issue or route contract requires `requested_profile` / `actual_profile` evidence;
- the work depends on profile-specific tools, memory, or delivery identity;
- the result must be audited as Tinker/Quill/Boba work;
- the work mutates a repo/vault/project source of truth under that profile’s route.

## Circuit-breaker policy

Unapproved route recursion is forbidden.

Pause and require Pixoid/Jamie review if any route attempts:

- Tinker → Quill/Boba direct trigger;
- Boba → Quill/Tinker direct trigger;
- Quill → Tinker/Boba direct trigger;
- A → B → A loops within a short window;
- profile-wide AFK autonomy without an explicit route contract;
- automatic continuation after a Smart Zone/checkpoint stop;
- dynamic webhook or supervisor activation without an approved deployment slice.

Implementation of a technical loop detector should be a separate issue. Until then, this policy is enforced through route contracts, Pixoid review, issue labels, and final consistency audits.

## Related pages

- [[agent-capability-route-pattern]]
- [[self-improving-agent-systems]]
- [[Projects/Hermes Mission Control/Index]]
- [[Projects/Pixoid Agent Capability Routes/Index]]
