---
title: Agent Workflow System Summary — Skills, Tools, Scheduling, Delegation
created: 2026-07-01
updated: 2026-07-01
type: summary
status: compiled
namespace: agent-workflows
tags: [agent-workflows, product-management, skills, tools, scheduling, delegation]
sources:
  - wiki/entities/hermes-mission-control.md
  - wiki/syntheses/pixoid-crew-operating-model.md
  - wiki/concepts/agent-skill-routing.md
  - wiki/concepts/multi-agent-multiplayer-boundaries.md
  - wiki/concepts/agent-capability-route-pattern.md
  - wiki/concepts/agent-tooling-plan.md
confidence: high
---

# Agent Workflow System Summary — Skills, Tools, Scheduling, Delegation

This page summarizes Jamie's hands-on agent workflow system: the way Discord, Pixi Wiki, skills, tools, scheduling, delegation, verification gates, and durable knowledge surfaces come together as a system for building.

It is not a polished product case study or a proof dossier. The system is the work: a live operating model for turning intent into routed agent work, inspected artifacts, reusable knowledge, and verified progress while building with Hermes, Pixi Wiki, Discord, GitHub, and Obsidian.

## One-screen summary

Jamie's agent workflow system turns a human request in Discord into routed, inspectable building work:

```text
human request
→ Pixoid route selection
→ skills / tools / subagents / cron / MCP-style knowledge access
→ GitHub, Obsidian, and Pixi Wiki as durable truth surfaces
→ verification before final answer, closure, merge, or deploy
```

The product lesson is simple: agents become useful when the building system makes work legible — what triggered, who/what executed, which tools were used, what artifact was produced, what became reusable, and what evidence proves it worked.

## What this summarizes

- **Skills and tools:** [Agent Skill Routing](/pixi-wiki/wiki/agent-workflows/wiki/concepts/agent-skill-routing.md.html) defines how intent maps to useful skill stacks and how constraints are carried into delegated work.
- **Runtime/capability routing:** [Hermes Capability Routing](/pixi-wiki/wiki/hermes-agent/wiki/concepts/hermes-capability-routing.md.html) maps tasks to direct tools, scripts, skills, subagents, cron, MCP/plugins, gateway routes, or durable knowledge updates.
- **Agent delegation:** [Agent Capability Route Pattern](/pixi-wiki/wiki/agent-workflows/wiki/concepts/agent-capability-route-pattern.md.html) defines trigger → profile/capability → bounded execution → artifact → verification.
- **Multi-agent coordination:** [Multi-Agent Multiplayer Boundaries](/pixi-wiki/wiki/agent-workflows/wiki/concepts/multi-agent-multiplayer-boundaries.md.html) captures coordinator mode, specialist mode, workbench huddles, direct multiplayer risks, and suppression of noisy worker chatter.
- **Control plane:** [Hermes Mission Control](/pixi-wiki/wiki/agent-workflows/wiki/entities/hermes-mission-control.md.html) documents Pixoid/Tinker/Quill/Boba roles, Discord routing, GitHub issue/PR truth, and verification gates.
- **Operating model:** [Pixoid Crew Operating Model](/pixi-wiki/wiki/agent-workflows/wiki/syntheses/pixoid-crew-operating-model.md.html) explains how work moves across route selection, source-of-truth checks, memory boundaries, and review.
- **Planning agents as tools:** [Agent Tooling Plan](/pixi-wiki/wiki/agent-workflows/wiki/concepts/agent-tooling-plan.md.html) turns vague or clear requests into task buckets, tools, routing rules, memory, evaluation, permissions, and smallest proving loops.
- **Durable knowledge for agents:** [Markdown-First Agent Memory](/pixi-wiki/wiki/agent-workflows/wiki/syntheses/markdown-first-agent-memory.md.html) and [Knowledge Pack Routing](/pixi-wiki/wiki/agent-workflows/wiki/concepts/knowledge-pack-routing.md.html) keep agent context visible, versioned, citeable, and reusable.

## Product judgment shown here

This work is not just "using agents." The product judgment is in the boundaries:

- one visible owner for the user-facing thread;
- explicit route contracts instead of unbounded agent autonomy;
- skills as reusable operating procedures, not prompt vibes;
- GitHub issues, PRs, Obsidian, and Pixi Wiki as durable truth surfaces;
- Discord as a control plane and notification layer, not the canonical source of truth;
- verification before claiming success;
- public/wiki surfaces that humans can browse and agents can retrieve.

## Implementation tradeoffs and scaling lessons

The hard parts have been product and systems tradeoffs, not just wiring tools together:

- Coordination vs agent noise — direct multiplayer feels powerful, but it can create duplicate work and noisy threads. The system now favors Pixoid as one visible coordinator, with bounded huddles only when specialist input is useful.
- Convenience vs trigger precision — role mentions, reply pings, bot-authored chatter, and thread metadata can accidentally wake the wrong agent. The routing layer needs explicit summons, channel controls, and closed-loop suppression before model invocation.
- Builder speed vs trust — agents can move fast, but outputs only become durable after verification: changed files, tests, links, GitHub state, and source-truth checks.
- Local knowledge vs shareable surfaces — Pixi Wiki keeps the same knowledge usable by humans and agents through browsable pages, raw Markdown, indexes, and local MCP-style retrieval.
- Custom workflows vs scale — the repeatable unit is a route, skill, template, or scheduled job: define the trigger, allowed actions, artifact, owner, stop condition, and verification handle so one builder workflow can become a team workflow.

A concrete implementation example is the [Discord council and bot routing hardening PR](https://github.com/NousResearch/hermes-agent/pull/55200), which came from a real product problem: `@Crew` should create coordinated progress, not wake every worker into the same user thread. That work maps directly to [Multi-Agent Multiplayer Boundaries](/pixi-wiki/wiki/agent-workflows/wiki/concepts/multi-agent-multiplayer-boundaries.md.html) and [Hermes Mission Control](/pixi-wiki/wiki/agent-workflows/wiki/entities/hermes-mission-control.md.html).

## How it maps to a Founding PM, Agents role

For an agents product, the important questions are practical:

1. How does a builder go from an idea to a working agent or skill?
2. How does the runtime know what the agent can see, call, schedule, delegate, and change?
3. How do humans inspect what happened and trust the output?
4. How does useful work become reusable templates, skills, or durable knowledge?
5. How do teams avoid agent noise, duplicate work, and unsafe side effects?

The linked pages are Jamie's working answers to those questions.
