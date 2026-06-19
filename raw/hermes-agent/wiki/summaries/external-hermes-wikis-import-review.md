---
title: External Hermes Wikis Import Review
created: 2026-06-18
updated: 2026-06-18
type: summary
status: compiled
namespace: hermes-agent
tags: [hermes-agent, curation, import-review, agentwikis, hermesguide]
sources:
  - https://hermesguide.xyz/wiki/
  - https://hermesguide.xyz/directory
  - https://agentwikis.com/wiki/hermes/README.md
  - https://agentwikis.com/wiki/hermes/llms.txt
  - https://agentwikis.com/raw/hermes/wiki/index.md
confidence: medium
---

# External Hermes Wikis Import Review

Reviewed `hermesguide.xyz` and AgentWikis Hermes for content worth importing into Jamie/Pixoid's Hermes Agent namespace.

## Verdict

Do **not** mirror either source. Keep this namespace slim and operational.

Import only content that is:

- hard to rediscover with one web search;
- likely to help Jamie operate Hermes, profiles, gateway, cron, memory, evals, or subagents;
- stable enough to be useful after a week;
- cross-checked against official Hermes docs or local installed source before commands/config are trusted.

## Hermes Guide / hermesguide.xyz

### Useful signal

`https://hermesguide.xyz/wiki/` is currently a landing/marketing route, not a deep wiki. The useful page is the ecosystem directory at `https://hermesguide.xyz/directory`, which lists 156+ community tools grouped by Dev Workflow, Integrations, Personal Assistant, Meta & Ecosystem, Business Ops, Enterprise, Content Creation, Cost Optimization, Creative, Research, Messaging, Trading & Markets, and Privacy/Self-Hosted.

### Worth importing

Import as **one summary**, not 156 entity pages:

- `Hermes Ecosystem Directory Triage` — curated shortlist of tools Jamie might actually evaluate.
- Include categories, short descriptions, and triage status: `watch`, `maybe`, `skip`, `needs verification`.
- Verify each selected tool against its primary repo before creating an entity page.

Possible shortlist for Jamie:

- Hermes Desktop / Scarf / Hermes Workspace / Hermes Console — front-end/control-plane options for sessions, memory, cron, project dashboards, and SSH-first operation.
- Hermes Memory UI / Herm / Autograph / Obsidian memory keep-alive — memory observability or Obsidian-linked memory workflows.
- Hermes Labyrinth / Hermescheck / Hermes progress tail / H-Ops — observability, health checks, progress visibility, and Kanban operations.
- Hermes Google Workspace / Microsoft Graph API skill / Nextcloud / Apple Calendar assistant — productivity integrations matching Jamie's assistant workflows.
- Hermes-Web-Search-Plus / video research ingest / Obsidian-Video-Notes — research ingestion helpers.
- Hermes-Multitenancy / Shellward / Hermes-Aegis / HermesClaw — security and multi-tenant routing ideas, only if Jamie works on gateway/profile isolation.
- Agent-Team-Orchestrator / Maestro / mission-control-like tools — compare against Jamie's existing crew/mission-control model; avoid importing unless they add a concrete pattern.

### Skip

- Broad creative/game/trading novelty tools unless Jamie opens a matching project.
- Most named forks with no current need.
- Pricing/model benchmark pages from Hermes Guide; freshness decays fast and web search is better.
- Landing pages that duplicate official docs.

## AgentWikis Hermes

AgentWikis has roughly 105 Hermes documents. It is a useful discovery map, but it is secondary to official docs and local source.

### Already covered locally

The current `hermes-agent` namespace already has:

- [[../concepts/source-priority|Hermes Source Priority]]
- [[../concepts/session-trace-store|Hermes Session Trace Store]]
- [[../concepts/evals-and-traces-setup|Hermes Evals and Traces Setup]]
- [[agentwikis-hermes-curated-seed|AgentWikis Hermes Curated Seed]]

### Highest-value imports

Create or expand these only when verified against official docs/local source:

1. `Memory Providers Compared` — high leverage because provider choice is hard to rediscover by search and crosses Honcho, Holographic, Hindsight, Mem0, OpenViking, ByteRover, RetainDB, Supermemory, and Memori. This should be a concept or synthesis, not separate entity pages for every provider unless Jamie evaluates them.
2. `Deployment Backends Compared` — useful for local vs Docker vs SSH/VPS vs Modal vs Daytona vs Singularity decisions. Jamie already uses VPS/WSL/local distinctions, so this would reduce repeated setup reasoning.
3. `Cron Troubleshooting Checklist` — worth a compact operational concept: timing, delivery, permissions, skill loading. This is likely to be reused for crew cron and gateway jobs.
4. `Auxiliary Models` — import the footguns: side-task routing, `auto` fallback, compression config split, approval/vision/web_extract/curator/task slots. This is web-search-resistant operational detail.
5. `Profiles & Multi-Instance` — import as Jamie-specific operating notes: profile isolation, gateway token boundaries, profile-scoped cron/memory paths, when to clone vs separate profile.
6. `Subagents & Delegation` — import only the operational decision table: `delegate_task` vs background process vs cron vs full spawned Hermes instance.
7. `Local Stack / Airplane Mode` — import only if Jamie actively works on local/offline Hermes; otherwise keep as a deferred pointer under local-ai-infrastructure.

### Medium priority / import on demand

- `Skills Catalog — 644-Skill Map` — useful as a pointer, but likely stale; prefer live `hermes skills browse/search` when available.
- `Awesome Hermes Agent — Ecosystem Inventory` — overlaps Hermes Guide directory; keep as source for the same ecosystem triage summary.
- Release summaries — only import when debugging historical behavior.
- Provider pages — import only selected providers Jamie actually uses or evaluates.
- Platform pages — import only Discord/Telegram/Email/Home Assistant/Google Workspace/Slack if actively configured.

### Skip by default

- Video transcript summaries unless they contain a workflow Jamie wants to preserve.
- OpenClaw comparison pages unless doing migration/positioning work.
- Onchain/trading workflow pages.
- One-page entity stubs for every community project.
- Old version pages as standalone entities.

## Suggested import queue

1. Create `wiki/syntheses/memory-providers-compared.md` from AgentWikis + official docs. Crosslink to agent-workflows memory-routing pages.
2. Create `wiki/syntheses/hermes-deployment-backends-compared.md` from AgentWikis + local source/docs. Include Jamie-specific VPS/WSL/Puffer notes only if they are stable and already authorized for this namespace.
3. Create `wiki/concepts/hermes-cron-troubleshooting.md` as a compact four-category checklist.
4. Create `wiki/concepts/hermes-auxiliary-model-routing.md` for side-task model routing and compression footguns.
5. Create `wiki/summaries/hermes-ecosystem-directory-triage.md` from Hermes Guide + AgentWikis ecosystem pages, with selected tools only.

## Import rule

One external source can justify a local page only if the page answers: “Would Jamie/Pixoid plausibly ask this again, and would web search be slower or noisier than retrieving the wiki page?”

If yes, import a compact synthesis. If no, leave the source as a pointer.


## Namespace routing review

Primary home stays `hermes-agent` for Hermes-specific operations and setup. Other namespaces should crosslink to this review or to future focused pages rather than duplicate the content.

| Candidate | Primary namespace | Crosslink namespaces | Decision |
|---|---|---|---|
| Memory Providers Compared | `hermes-agent` | `agent-workflows`, `local-ai-infrastructure` | Add as a Hermes synthesis if Jamie starts comparing providers; crosslink to runtime memory routing and local-first memory infrastructure. |
| Deployment Backends Compared | `hermes-agent` | `local-ai-infrastructure`, `agent-workflows` | Add as a Hermes synthesis; crosslink from local infrastructure because backend choice affects VPS/WSL/local execution. |
| Cron Troubleshooting Checklist | `hermes-agent` | `agent-workflows` | Add as a Hermes operational concept; crosslink from crew/cron workflow pages because recurring jobs are workflow infrastructure. |
| Auxiliary Models | `hermes-agent` | `eval-trace`, `agent-workflows` | Add as a Hermes concept; crosslink where eval/tracing side tasks and approval/compression behavior affect workflow quality. |
| Profiles & Multi-Instance | `hermes-agent` | `agent-workflows` | Add as a Hermes concept; crosslink from profile/memory boundary and peer-profile pages. |
| Subagents & Delegation | `hermes-agent` | `agent-workflows` | Split if needed: Hermes API/tool mechanics in `hermes-agent`; route-governance decision table in `agent-workflows`. |
| Local Stack / Airplane Mode | `local-ai-infrastructure` | `hermes-agent` | If imported, primary home should be local infrastructure; Hermes Agent should only link to setup-specific notes. |
| Ecosystem Directory Triage | `hermes-agent` | `pixi-vault`, `agent-workflows`, `local-ai-infrastructure` | Keep as a single triage summary first; create entity pages only for tools Jamie evaluates. |
| AgentWikis / external wiki import pattern | `pixi-vault` | `hermes-agent`, `agent-workflows` | The reusable import/routing method belongs to Pixi Vault; this page is the Hermes-specific instance. |

### Crosslink policy

- `hermes-agent` owns Hermes commands, config, providers, memory plugins, profiles, gateway, cron, skills, and subagent mechanics.
- `agent-workflows` owns Pixoid/Tinker/Quill/Boba route decisions, handoffs, governance, memory-boundary behavior, and when to delegate vs spawn vs schedule.
- `local-ai-infrastructure` owns offline/local model stacks, local retrieval, hardware constraints, and local-first deployment tradeoffs.
- `eval-trace` owns observability/evaluation failure modes and evidence gates, not general Hermes setup.
- `pixi-vault` owns the namespace-routing/import methodology and public wiki/compiler mechanics.
