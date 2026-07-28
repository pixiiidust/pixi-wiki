---
title: Executable Agent Worlds
created: 2026-07-28
updated: 2026-07-28
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/executable-agent-worlds.md
confidence: medium
---

# Executable Agent Worlds

An executable agent world repurposes sufficiently understood software as an environment, body, institution, or cognitive tool for AI agents.

The strong version is not “agents play old games.” The software's mechanics must causally constrain what agents know, can do, can spend, can delegate, and must endure.

## System boundary

```text
software understanding
  -> runtime adapter
  -> agent organization
  -> event/evaluation layer
```

- **Understanding:** source inspection or reverse engineering locates state, functions, structures, and interception points.
- **Adapter:** exposes structured observations, validates actions, submits commands, snapshots state, and records events.
- **Agents:** deliberate at appropriate roles and time scales; deterministic controllers handle fast loops.
- **Evaluation:** seeds, baselines, traces, and replays keep claims inspectable.

Ghidra MCP fits the understanding layer. It can help discover and annotate a binary, but a separate runtime adapter is still required.

## Causality test

> If the software mechanics disappeared, would the agents face meaningfully different information, authority, resource, timing, and consequence constraints?

If no, the software is probably a dashboard skin. If yes, it may be a genuine agent environment or institutional substrate.

## Creative branches

- Software as an agent body.
- Mechanics as an organizational operating system.
- Agents inhabiting functions and defending local invariants.
- Executable archaeology of undocumented programs.
- Cross-world transfer of agent institutions.
- Time-layered societies spanning reflex to constitutional agents.
- Legacy software used as planning, design, database, simulation, music, or debugging prosthetics.

## Example, not commitment

Dune II makes the idea easy to picture: fog, spice, production, command, unit roles, and combat impose concrete constraints. Agents could inhabit units or command layers through a bounded adapter.

That does not make original-binary hooking the best first experiment. An open-source reimplementation or a purpose-built simulation may answer the research question more cleanly.

## Advantages

- Reuses rich mechanics instead of building every environment from zero.
- Makes coordination, memory, hierarchy, and adaptation observable.
- Creates real consequences beyond prompt-only role-play.
- May expose organizational behaviors a designer would not specify directly.

## Limits and evidence gates

- Reverse engineering is brittle, expensive, software-specific, and legally sensitive.
- LLMs are too slow for every tick; separate deliberation from low-level control.
- Require fixed binaries, hashes, snapshots, seeds, logs, clean state, and simpler baselines.
- Do not let animation imply unverified progress.
- Use the [[../../eval-trace/wiki/concepts/emergence-claim-ladder|Emergence Claim Ladder]] before claiming transfer or emergence.

## Related pages

- [[agentic-harness-engineering|Agentic Harness Engineering]]
- [[multi-agent-multiplayer-boundaries|Multi-Agent Multiplayer Boundaries]]
- [[effective-state-load|Effective State Load]]
- [[creative-ideation-routing|Creative Ideation Routing]]
