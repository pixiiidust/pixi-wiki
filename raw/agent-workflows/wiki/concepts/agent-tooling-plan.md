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

An **Agent Tooling Plan** turns a problem into an agent-as-tools route: task buckets, tools, routing rules, memory, evaluation, permissions, and the feedback loop that lets an agent act safely.

## Core premise

An agent is not magic intelligence. It is an orchestration layer over bounded tools.

The product work is:

```text
configure the right tools for the right task bucket, then give the agent reliable routing, memory, evaluation, and permissions
```

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

## Design process

1. Define the goal: what outcome should the agent optimize for?
2. Map the environment: what does the agent need to see?
3. Break the problem into task buckets: perceive, interpret, remember, plan, act, evaluate, escalate.
4. Assign tools to each bucket: each tool needs a clear input, output, and boundary.
5. Define routing rules: when should the agent use each tool?
6. Add memory: interpreted experience that changes future action, not raw storage.
7. Add evaluation: how does the agent know whether the action worked?
8. Add permissions: what can it do alone, and what needs approval?
9. Close the loop: observe the result and choose the next tool.

## Planning outputs

For a vague request, output a scaffold plus questions/gaps and route to `/grill-me` or `/grill-with-docs` instead of inventing a complete plan.

For a clear request, output a full plan with:

- goal;
- environment;
- bucket table;
- routing rules;
- memory contract;
- evaluation contract;
- permissions table;
- feedback loop;
- first implementation slice.

## Boundaries

- Tool assignment is incomplete without routing, memory, evaluation, permissions, and feedback.
- Approval gates are part of the product surface, not an afterthought.
- Memory should store interpreted experience, not raw logs.
- Evaluation must be concrete enough to distinguish “agent says done” from “the loop worked.”

## Source

Canonical source: `Knowledge/concepts/agent-tooling-plan.md`.

Reusable Hermes skill: `~/.hermes/skills/autonomous-ai-agents/agent-tooling-plan/SKILL.md`.

Related pages: [[concepts/agent-skill-routing|Agent Skill Routing]], [[../../hermes-agent/wiki/concepts/hermes-capability-routing|Hermes Capability Routing]], [[concepts/agent-capability-route-pattern|Agent Capability Route Pattern]], [[concepts/runtime-memory-knowledge-routing|Runtime Memory Knowledge Routing]], [[concepts/matt-pocock-skills-best-practices|Matt Pocock Skills Best Practices]].
