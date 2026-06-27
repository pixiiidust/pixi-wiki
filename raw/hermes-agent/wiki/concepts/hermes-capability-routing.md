---
title: Hermes Capability Routing
created: 2026-06-26
updated: 2026-06-26
type: concept
status: compiled
namespace: hermes-agent
source: Knowledge/concepts/hermes-capability-routing.md
confidence: high
---

# Hermes Capability Routing

Hermes capability routing is the decision lens for choosing the smallest effective Hermes Agent surface for a task: direct tool call, `execute_code`, skill, memory, session search, delegation, cron, gateway, API server, MCP, plugin, profile, kanban board, or external process.

Short form:

```text
intent → smallest surface → durability boundary → side-effect boundary → verification handle
```

## Why this exists

Hermes exposes many overlapping surfaces. The optimal route depends on task shape, durability, side effects, and verification burden, not on which feature sounds most powerful.

Use this when a request is broader than skill selection but narrower than a full route contract. Skill routing decides which procedures frame the work. Capability routing decides whether the work should be a tool call, script, skill, subagent, scheduled job, gateway/API integration, profile route, MCP/plugin extension, or knowledge/project update.

## Routing matrix

| Task shape | Default Hermes surface |
|---|---|
| One immediate read/write/check | Current-session tools |
| Mechanical multi-tool loop | `execute_code` with `hermes_tools` |
| Reusable procedure | Hermes skill |
| Stable user/environment fact | Memory/user profile |
| Past-session recall | `session_search` |
| Independent bounded analysis | `delegate_task` |
| Durable scheduled work | `cronjob` or tracked background process |
| Repeated multi-profile collaboration | Kanban/profile route |
| Messaging delivery | Gateway/platform adapter |
| External app needs OpenAI-compatible access | API server |
| Existing external service has a server | MCP |
| New reusable action | Tool or plugin |
| Cost/speed/reliability choice | Model picker, provider routing, fallback providers |

## Public wiki placement

Primary namespace: `hermes-agent`, because this is a Hermes Agent capability-selection map derived from official docs and the reusable local skill.

Relevant crosslink namespace: `agent-workflows`, because Pixoid crew routing uses the lens to decide when work should become skill work, subagent work, scheduled work, peer-profile/kanban work, vault/Pixi Wiki source work, or a public deploy candidate.

Do not split this into a new namespace; it connects existing Hermes Agent and Agent Workflows pages.

## Boundaries

- Official Hermes docs remain source of truth for commands, flags, providers, config keys, and setup details.
- Capability routing is not authorization; destructive commands, deploys, merges, secrets, profile/gateway/provider/webhook changes, and public publication still require the relevant approval boundary.
- `delegate_task` is not durable; use cron/background/kanban/profile routes for work that must survive interruption.
- Do not make memory carry procedures, project state, or public wiki content.
- Do not build custom plugins/tools until existing CLI, tools, skills, MCP, gateway, and API surfaces have been checked.

## Related pages

- [[../../agent-workflows/wiki/concepts/agent-skill-routing|Agent Skill Routing]]
- [[../../agent-workflows/wiki/concepts/agent-capability-route-pattern|Agent Capability Route Pattern]]
- [[../../agent-workflows/wiki/concepts/runtime-memory-knowledge-routing|Runtime Memory Knowledge Routing]]
- [[../../agent-workflows/wiki/concepts/profile-memory-boundaries|Profile Memory Boundaries]]
- [[concepts/source-priority|Hermes Source Priority]]

## Sources

- Official docs: `https://hermes-agent.nousresearch.com/docs`
- Canonical source: `Knowledge/concepts/hermes-capability-routing.md`
- Reusable skill: `~/.hermes/skills/autonomous-ai-agents/hermes-capability-routing/SKILL.md`
