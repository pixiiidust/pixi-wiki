---
title: Agentic Harness Engineering
created: 2026-07-09
updated: 2026-07-09
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/agentic-harness-engineering.md
confidence: high
---

# Agentic Harness Engineering

Agentic harness engineering treats an AI agent as a deployable software harness, not a giant prompt. The harness makes identity, actions, tool authority, channel routes, sandbox execution, durable state, background work, and eval gates inspectable before the agent runs.

## Reference pattern from Eve

Vercel's Eve framework is a useful reference shape because it authors agents as files under `agent/`:

```text
instructions.md  -> identity and standing contract
agent.ts         -> model and runtime config
tools/           -> typed model-callable actions
skills/          -> on-demand procedures
channels/        -> HTTP, Slack, Discord, GitHub, Linear, and custom entrypoints
connections/     -> MCP/OpenAPI external tool surfaces with brokered auth
subagents/       -> specialist child agents
schedules/       -> cron/background runs
sandbox/         -> isolated /workspace for shell and file work
evals/           -> route-level behavioral checks
```

The transferable lesson is not the exact folder names. The pattern is that each capability has a visible slot and a runtime boundary.

## Harness checklist

A real agentic harness should answer these questions without relying on chat history:

| Question | Harness surface |
|---|---|
| Who is this agent? | instructions / profile / identity file |
| What actions can it take? | typed tools and connection manifests |
| Where can users reach it? | channels and route auth |
| What is unsafe/untrusted execution? | sandbox backend, workspace, and network policy |
| What needs human approval? | HITL and approval policies |
| What persists across turns? | durable session state and knowledge/memory routing |
| How does work split? | subagents and delegation caps |
| What runs on a clock? | schedules / cron |
| How is behavior verified? | evals, stream events, route checks, and live proof |

## Jamie-system application

- **Hermes Mission Control:** keep profile routes, Discord channel contracts, skills, cron, MCP, memories, vault truth, and verification as explicit harness surfaces.
- **Pixi Wiki:** treat namespace source, compiler maps, generated routes, `llms.txt`, MCP tests, and live Pages checks as the publishing harness, not just generated pages.
- **Crew workflows:** use peer-profile vs child-process boundaries before claiming named-agent execution.
- **Product prototypes:** start with identity, tool/data boundary, channel, sandbox, approval path, durable state, and eval smoke test before promising autonomy.

## Boundaries

- A visible file tree is not sufficient; auth, approval, idempotency, network policy, and verification still matter.
- Secrets belong in trusted runtime tools or connection auth, not in model context or sandbox files.
- Long procedures should be load-on-demand skills/playbooks, not permanent prompt bulk.
- Subagents are not an approval boundary by themselves.

## Source

Canonical source: `Knowledge/concepts/agentic-harness-engineering.md`.

External references reviewed: `https://eve.dev/docs/introduction` and `https://github.com/vercel/eve`.

## Related pages

- [[agent-tooling-plan|Agent Tooling Plan]]
- [[agent-skill-routing|Agent Skill Routing]]
- [[../../hermes-agent/wiki/concepts/hermes-capability-routing|Hermes Capability Routing]]
- [[runtime-memory-knowledge-routing|Runtime Memory Knowledge Routing]]
- [[self-improving-agent-systems|Self-Improving Agent Systems]]
- [[peer-profiles-vs-child-processes|Peer Profiles vs Child Processes]]
