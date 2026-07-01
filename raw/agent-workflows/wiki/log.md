---
title: Agent Workflows — Activity Log
created: 2026-06-16
updated: 2026-07-01
type: log
status: compiled
namespace: agent-workflows
---

# Agent Workflows — Activity Log

> Append-only namespace log.

## 2026-07-01 create | Agent workflow system summary

- Added compiled summary `wiki/summaries/agent-workflow-system-summary.md` as a compact public summary of Jamie's agent workflow system: skills, tools, scheduling, delegation, Discord/GitHub control surfaces, verification, and durable knowledge routing.
- Cross-linked Hermes Mission Control, Pixoid Crew Operating Model, Agent Skill Routing, Multi-Agent Multiplayer Boundaries, Agent Capability Route Pattern, Agent Tooling Plan, Markdown-First Agent Memory, Knowledge Pack Routing, and Hermes Capability Routing.
- Kept the page focused on the agent workflow system itself and removed job-application-defensive framing.

## 2026-07-01 create | Reader-Centered Outreach Asks

- Added compiled concept `wiki/concepts/reader-centered-outreach-asks.md` from the canonical Knowledge page and Jamie's supplied article about asking strangers for help.
- Captured the cold outreach drafting contract for future agents: recipient mind first, proof of work over status, tiny context, specific low-friction bounded ask, easy no, and never lie.
- Updated namespace README and index source roots for public Pixi Wiki rebuild/deploy.

## 2026-06-30 update | Agent Tooling Plan skill v1.0.1

- Mirrored the tightened `agent-tooling-plan` skill into compiled namespace source.
- Added live-state-first planning, max-five grill questions, adjacent skill routing, a concrete email-triage mini-example, and the smallest proving loop guardrail.

## 2026-06-30 create | Agent Tooling Plan

- Added compiled concept `wiki/concepts/agent-tooling-plan.md` from Jamie's Agent-as-tools Product Playbook and the reusable Hermes skill.
- Captured the vague-vs-clear request split: vague requests produce a scaffold plus `/grill-me` or `/grill-with-docs` questions; clear requests produce a full task-bucket/tool/routing/memory/evaluation/permissions/feedback-loop plan.
- Updated namespace README and index source roots for public Pixi Wiki rebuild/deploy.

## 2026-06-29 update | Discord worker mention allowlist

- Recorded that Boba/Quill/Tinker worker gateways share Pixoid's approved Discord room allowlist but remain bounded by direct mentions in top-level channels.
- Captured the paired safety rule: `discord.channel_allow_bots: none` blocks bot/status chatter in top-level shared channels, while `allow_bots: mentions` keeps thread handoffs possible.

## 2026-06-29 update | Discord council-mode hardening shipped

- Updated compiled `agent-workflows` source pages after `pixiiidust/pixi-wiki` tracker #33–#41 closed for Discord council-mode hardening.
- Captured the shipped coordinator-first contract: `@Crew`/crew aliases route to Pixoid, direct worker mentions stay specialist-only, bounded huddles close on all-replied-or-timeout, and Pixoid returns one final answer.
- Added the live-loop lesson: prompt-level silence is insufficient; closed huddle worker/bot chatter must be suppressed at the adapter/gateway layer, reply pings must not reopen the loop without explicit textual mention/approved trigger, and top-level shared channels can use `discord.channel_allow_bots: none` while huddle threads preserve worker handoffs.
- This update is intended for public `pixi-wiki` rebuild/deploy.

## 2026-06-29 create/update | Multi-agent multiplayer boundaries

- Added compiled concept `wiki/concepts/multi-agent-multiplayer-boundaries.md` from the canonical Knowledge page and the Discord crew-edge-case analysis.
- Captured the four-mode contract: coordinator mode, specialist mode, workbench council, and explicit direct multiplayer test mode.
- Preserved edge cases for trigger parsing, turn-taking, identity proof, context/memory, authority, shared resources, handoffs, verification, UX, safety, and eval traces.
- No public `pixi-wiki` deploy was pushed.

## 2026-06-29 update | Discord crew routing coordinator mode

- Updated Hermes Mission Control and Pixoid Crew Operating Model with the settled Discord contract: `@Crew`/crew aliases wake Pixoid as coordinator, direct worker mentions wake individual profiles, and visible crew discussion belongs in topic-specific `#agent-workbench` threads.
- Captured the live failure mode: assigning the shared `Crew` role to every bot makes Boba/Quill/Tinker/Pixoid independently inspect and reply, causing duplicated work and noisy threads.
- Recorded the role-mention/human-mention adapter lesson without treating it as sufficient for true multiplayer; the remaining open thread is a coordinator-mediated council protocol.

## 2026-06-27 update | Agent Output Decision Artifacts crosslink

- Added cross-namespace routing to `ai-native-product-surfaces/wiki/concepts/agent-output-decision-artifacts.md` from the workflow index and Visual Plan Review Surfaces page.
- Preserved `agent-workflows` as the workflow layer while keeping the primary concept home under `ai-native-product-surfaces`.

## 2026-06-27 create | Compound Engineering skill layer

- Added compiled concept `wiki/concepts/compound-engineering-skill-layer.md` from the canonical Knowledge page and the installed EveryInc `compound-engineering-plugin`.
- Captured `ce-*` and `lfg` routing, how CE compares with Jamie's Pocock/product/review/vault skills, the Discord invocation caveat for `/ce-*` shorthand, and the approval boundaries around autopilot use.
- Updated namespace README and index source roots.
- No public `pixi-wiki` deploy was pushed.

## 2026-06-26 update | Hermes capability routing crosslink

- Added cross-namespace routing to `hermes-agent/wiki/concepts/hermes-capability-routing.md` so crew workflow readers can choose the right Hermes surface before turning work into skills, subagents, cron, profile/kanban routes, or publishing steps.
- Updated namespace README and index source roots.
- No Daily Notes were copied or compiled, and no public `pixi-wiki` deploy was pushed.

## 2026-06-26 create | High agency work levels

- Added compiled concept `wiki/concepts/high-agency-work-levels.md` from Jamie's Level 4+ agency framework and the patched `agent-workflow-os` skill.
- Captured the operating rule: Pixoid defaults to Level 4, moves to Level 5 only when safe/scoped/approved, and uses Level 6 for repeated failure classes.
- Updated namespace README and index source roots.

## 2026-06-26 create/update | Visual plan review surfaces

- Added compiled concept `wiki/concepts/visual-plan-review-surfaces.md` from the canonical Knowledge page and the local `visual-plan` Hermes skill.
- Updated `agent-skill-routing` and `matt-pocock-sdlc-rhythm` routing so PRDs and implementation plans can become local/private MDX review surfaces before code.
- Preserved the boundary that hosted share/comment links and public `pixi-wiki` deploys require explicit opt-in.

## 2026-06-24 create/update | Creative ideation routing

- Added compiled concept `wiki/concepts/creative-ideation-routing.md` from the canonical Knowledge page and the `creative-ideation` Hermes skill.
- Updated `agent-skill-routing` so open-ended inspiration, brainstorming, project ideas, and option generation route through `creative-ideation` by default.
- Updated namespace README and index source roots.
- No Daily Notes were copied or compiled, and no public `pixi-wiki` deploy was pushed.

## 2026-06-23 create | Agent skill routing contract

- Added compiled concept `wiki/concepts/agent-skill-routing.md` from the canonical Knowledge page and the new `jamie-skill-router` Hermes skill.
- Captured the rule that Pixoid chooses the skill stack by default and passes active skill constraints into delegated subagent context.
- Added edge cases for explicit user-invoked modes, ambiguous routing, unavailable tools, public deploy approval, and context overload.
- Updated namespace README and index source roots.

## 2026-06-16 create | Namespace scaffold initialized

- Created README, CLAUDE instructions, raw folder, index/log, and typed wiki folders.
- Source routing comes from `Wiki Compiler Maps/Namespace Wiki Compiler Map.md`.
- No Daily Notes were copied or compiled.

## 2026-06-16 update | Pilot compiled namespace page

- Added pilot entity `wiki/entities/hermes-mission-control.md` and crosslink to Eval Trace context-overfitting concept.
- Source pages remained in `Knowledge/` and `Projects/`.
- No Daily Notes were copied or compiled.

## 2026-06-16 update | Compile agent-workflows content pack v1

- Added compiled concept pages for profile memory boundaries, runtime memory knowledge routing, self-improving agent systems, and peer profiles vs child processes.
- Added synthesis `wiki/syntheses/pixoid-crew-operating-model.md`.
- Updated namespace index.
- Source pages remain in `Knowledge/` and `Projects/`.
- No Daily Notes were copied or compiled.

## 2026-06-16 update | Add KPR and clean publishing gate content

- Promoted `agent-workflows` from scaffold to active namespace overview.
- Added concept pages for `knowledge-pack-routing`, `agent-entrypoint-mesh`, and `static-retrieval-evals`.
- Added synthesis `wiki/syntheses/markdown-first-agent-memory.md`.
- Expanded `Hermes Mission Control` as a compiled entity page with crew role boundaries and source routing.
- Updated namespace index and source roots.
- Final public publish remains gated by the clean `pixi-wiki` rebuild.
- No Daily Notes were copied or compiled.

## 2026-06-18 update | Add Ponytail minimal-code discipline concept

- Added compiled concept `wiki/concepts/ponytail-minimal-code-discipline.md` from the canonical Knowledge page and Hermes skill.
- Updated namespace README and index source roots.
- No Daily Notes were copied or compiled.

## 2026-06-18 update | Crosslink external Hermes import routing

- Added cross-namespace pointer to the Hermes Agent external wiki import review so workflow-specific candidates route through Agent Workflows instead of duplicating Hermes setup content.
- No Daily Notes were copied or compiled.
## 2026-06-18 update | Publish local Hermes KB workflow concepts

- Added compiled concept pages for `agent-capability-route-pattern`, `hermes-soul-md-wiring`, `matt-pocock-sdlc-rhythm`, and `bounded-context-tree-pattern`.
- Refreshed `peer-profiles-vs-child-processes` from the verified local Hermes KB closure synthesis.
- Updated namespace index so the public Pixi Wiki can expose the closed tracker concepts.
- Preserved no-auto-trigger and no profile/cron/gateway/MCP/RAG/deploy authorization boundaries.

## 2026-06-19 create | Matt Pocock skills best practices

- Added compiled concept `wiki/concepts/matt-pocock-skills-best-practices.md` from the canonical Knowledge page and upstream `mattpocock/skills` README.
- Cross-linked `matt-pocock-sdlc-rhythm` so the generalized SDLC rhythm points back to the source-backed best-practices pattern.
- Updated namespace README and index source roots.
- No Daily Notes were copied or compiled.

## 2026-06-23 update | Interaction Mode Routing crosslink

- Added cross-namespace routing to `ai-native-product-surfaces/wiki/concepts/interaction-mode-routing.md`.
- Updated `wiki/entities/hermes-mission-control.md` with the Pixoid Review Surface pattern.
- Updated namespace README and index source roots.
- No Daily Notes were copied or compiled.
