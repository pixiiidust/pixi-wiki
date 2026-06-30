---
title: Agent Tooling Plan
created: 2026-06-30
updated: 2026-06-30
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/agent-tooling-plan.md
confidence: high
---

# Agent Tooling Plan

An **Agent Tooling Plan** turns a problem into an agent-as-tools route: live-state checks, task buckets, tools, routing rules, memory, evaluation, permissions, and the smallest proving loop that lets an agent act safely.

## Core premise

An agent is not magic intelligence. It is an orchestration layer over bounded tools.

The product work is:

```text
configure the right tools for the right task bucket, then give the agent reliable routing, memory, evaluation, permissions, and a proving loop
```

## Start with live state

Before assigning tools, inspect named docs, repos, APIs, channels, files, dashboards, or existing workflows. If a source is unavailable, mark the relevant plan row as an assumption.

Route upstream to AI-native problem framing when the product/problem is fuzzy. Route downstream to Hermes capability routing when the work shape is clear and the question is which Hermes surface should execute it.

## Agent loop

```text
Goal → choose tool → run tool → observe result → interpret → choose next tool → repeat
```

## Tool buckets

| Bucket | Purpose | Example tools |
|---|---|---|
| Perception | See the environment | Browser, files, APIs, sensors, logs |
| Interpretation | Turn signals into meaning | LLM, classifier, parser, summarizer |
| Memory | Apply interpreted past experience | Retrieval, compression, preference memory |
| Planning | Decide possible next steps | Decomposer, simulator, option ranker |
| Action | Change the environment | Email, code editor, deploy, browser click |
| Evaluation | Judge result quality | Tests, metrics, scoring, human review |
| Escalation | Hand off when uncertain | Approval gate, human decision, exception flow |

## Planning outputs

For a vague request, output a scaffold plus questions/gaps and route to `/grill-me` or `/grill-with-docs` instead of inventing a complete plan. Ask at most five questions, and only when each answer changes tool choice, routing, evaluation, permissions, memory, or the proving loop.

For a clear request, output a full plan with:

- goal;
- environment;
- inspected sources and assumptions;
- bucket table;
- routing rules;
- memory contract;
- evaluation contract;
- permissions table;
- feedback loop;
- smallest proving loop.

## Smallest proving loop

The proving loop is the smallest buildable/testable route that demonstrates:

```text
perception → action or simulated action → evaluation → next routing decision
```

For high-risk domains, the first loop can be read-only or simulated. Do not call the system autonomous until observe, evaluate, and escalate are all defined.

## Mini-example

Request: “Plan an email triage agent.”

- **Goal:** reduce inbox review time without losing important messages.
- **Perception:** Gmail/API inbox search, labels, message metadata, sender history.
- **Interpretation:** classify urgency, topic, action needed, and confidence.
- **Memory:** user preferences for VIP senders, recurring newsletters, prior corrections.
- **Planning:** choose archive, label, draft reply, summarize, or escalate.
- **Action:** apply labels, draft replies, archive low-risk messages.
- **Evaluation:** sample 20 decisions, check false archives, compare user corrections, measure time saved.
- **Escalation:** ask before sending replies, deleting, unsubscribing, or handling low-confidence/VIP messages.
- **Smallest proving loop:** read 25 recent emails → classify only → user reviews labels → update routing before enabling actions.

## Boundaries

- Tool assignment is incomplete without routing, memory, evaluation, permissions, feedback, and a proving loop.
- Approval gates are part of the product surface, not an afterthought.
- Memory should store interpreted experience, not raw logs.
- Evaluation must be concrete enough to distinguish “agent says done” from “the loop worked.”
- Do not produce a pretty table that cannot be executed or evaluated.

## Source

Canonical source: `Knowledge/concepts/agent-tooling-plan.md`.

Reusable Hermes skill: `~/.hermes/skills/autonomous-ai-agents/agent-tooling-plan/SKILL.md`.

Related pages: [[concepts/agent-skill-routing|Agent Skill Routing]], [[../../hermes-agent/wiki/concepts/hermes-capability-routing|Hermes Capability Routing]], [[concepts/agent-capability-route-pattern|Agent Capability Route Pattern]], [[concepts/runtime-memory-knowledge-routing|Runtime Memory Knowledge Routing]], [[concepts/matt-pocock-skills-best-practices|Matt Pocock Skills Best Practices]].
