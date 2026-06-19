---
title: External Hermes Wikis Import Review
created: 2026-06-18
updated: 2026-06-19
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


---

## 2026-06-19 re-run after namespace population updates

### Live Pixi Wiki state that changes routing

The namespace set is now materially populated, so the external Hermes sources should be routed more narrowly than the first review:

- `hermes-agent` already contains source-priority, session-trace, eval/trace setup, AgentWikis seed, and this import review. It remains the primary home for Hermes commands, config, providers, memory, profiles, gateway, cron, skills, and subagent mechanics.
- `agent-workflows` is now a real workflow namespace with route-pattern, SOUL.md, memory-boundary, peer-profile, Ponytail, and crew operating model pages. It should receive crosslinks for governance decisions, not duplicate Hermes mechanics.
- `local-ai-infrastructure` now has local retrieval and RAG-over-AgentWikis pages. It is the right primary home for local/offline model stack tradeoffs, with Hermes setup notes linked back to `hermes-agent`.
- `eval-trace` now has context-overfitting, workflow-quality evaluation, and Eval Trace entity pages. It should crosslink auxiliary-model/evidence-gate footguns, not own general Hermes setup.
- `pixi-vault` now has Pixi Wiki and compiler-model pages. It owns the reusable import methodology and source/output repo boundary, not Hermes operations.
- Newly populated `ai-native-product-surfaces`, `curated-tuning-datasets`, and `rl-sim-labs` do not materially change this import route. They are useful only if a specific Hermes tool becomes part of a product demo, dataset pipeline, or RL experiment workflow.

### Source inspection notes

- Hermes Guide `/wiki/` is still mostly landing/marketing HTML. Its reusable signal remains `/directory`, now observed as a 156+ tool directory across Dev Workflow, Integrations, Personal Assistant, Meta & Ecosystem, Business Ops, Enterprise, Content Creation, Cost Optimization, Creative, Research, Messaging, Trading & Markets, and Privacy/Self-Hosted.
- AgentWikis Hermes still exposes about 105 documents through `llms.txt` / raw markdown. It has useful topic maps for auxiliary models, deployment backends, cron troubleshooting, profiles, subagents, memory, local models, release notes, providers, platforms, and ecosystem pages.
- Any command/config/runtime claim from either external source still requires official Hermes docs or local installed source verification before use.

### Candidate imports by priority

#### Import now

No new full imports recommended from the re-run. The high-reuse material is already represented as source-priority, curated seed, eval/trace setup, and this routing review. Importing more now would mostly duplicate official docs or AgentWikis pages without a live operating need.

#### Crosslink only

- `Subagents & Delegation` — crosslink from `agent-workflows` route-governance pages to the Hermes mechanics in `hermes-agent`; do not duplicate the API mechanics in workflow pages.
- `Profiles & Multi-Instance` — crosslink from `profile-memory-boundaries`, `peer-profiles-vs-child-processes`, and `hermes-soul-md-wiring` to a future Hermes mechanics page if Jamie asks for one.
- `Local Models & Airplane Mode` — crosslink from `local-ai-infrastructure`; import only if local/offline Hermes operation becomes an active slice.
- `Auxiliary Models` — crosslink from `eval-trace` for evidence gates and context-overfit diagnostics; import only a Hermes concept if troubleshooting side-task routing.
- `Hermes Guide Directory` and AgentWikis ecosystem pages — keep as a source pointer for future triage; do not create 156 entity pages.

#### Import on demand

- `Memory Providers Compared` — synthesize only when choosing or troubleshooting Honcho/Mem0/Holographic/Hindsight/etc.; primary `hermes-agent`, crosslink `agent-workflows` and `local-ai-infrastructure`.
- `Deployment Backends Compared` — synthesize only when making a VPS/WSL/local/Docker/Modal/Daytona choice; primary `hermes-agent`, crosslink `local-ai-infrastructure` and `agent-workflows`.
- `Hermes Cron Troubleshooting` — create only when a real cron job fails or crew cron behavior needs a durable checklist; primary `hermes-agent`, crosslink `agent-workflows`.
- `Hermes Auxiliary Model Routing` — create only when side-task routing/compression/vision/web-extract behavior affects work quality; primary `hermes-agent`, crosslink `eval-trace`.
- `Hermes Ecosystem Directory Triage` — create only when Jamie asks to evaluate external Hermes tools; primary `hermes-agent`, crosslink `pixi-vault` for import method and `agent-workflows` for route/governance patterns.

#### Skip

- Wholesale AgentWikis mirror.
- Hermes Guide landing/marketing pages.
- Video transcripts unless a specific workflow becomes durable.
- Release/version pages unless debugging historical behavior.
- Provider/platform pages unless Jamie is configuring that provider/platform.
- Onchain/trading/game/novelty ecosystem tools unless a matching project is opened.
- Entity pages for every memory provider, backend, community project, or directory listing.

### Updated routing table

| Candidate | Primary namespace | Crosslink namespaces | Page type | Action | Rationale |
|---|---|---|---|---|---|
| External Hermes import methodology | `pixi-vault` | `hermes-agent`, `agent-workflows` | synthesis / source pointer | Crosslink only | Reusable import/routing logic belongs to compiler/source methodology, while this page remains the Hermes-specific assessment. |
| Hermes commands/config/providers/profiles/gateway/cron/skills | `hermes-agent` | `agent-workflows`, `eval-trace` | concept or synthesis | Import on demand | Durable only when verified against official docs/local source and tied to Jamie/Pixoid operations. |
| Subagents & delegation mechanics | `hermes-agent` | `agent-workflows` | concept / decision table | Crosslink now; import on demand | Hermes owns tool mechanics; Agent Workflows owns when to delegate/spawn/schedule. |
| Profile/peer/worker boundaries | `hermes-agent` | `agent-workflows` | concept | Crosslink now; import on demand | Existing workflow pages already cover route boundaries; import mechanics only if configuring profiles. |
| Memory providers comparison | `hermes-agent` | `agent-workflows`, `local-ai-infrastructure` | synthesis | Import on demand | High-reuse for provider choice, but stale/risky without official/local verification. |
| Deployment backends comparison | `hermes-agent` | `local-ai-infrastructure`, `agent-workflows` | synthesis | Import on demand | Backend tradeoffs are reusable when choosing local/VPS/Docker/remote execution; no active decision in this review. |
| Local Models / Airplane Mode | `local-ai-infrastructure` | `hermes-agent`, `agent-workflows` | concept / source pointer | Crosslink only now | Local/offline tradeoffs belong to local infrastructure; Hermes Agent should hold only verified setup mechanics. |
| Auxiliary models / side-task routing | `hermes-agent` | `eval-trace`, `agent-workflows` | concept | Import on demand | Useful for evidence-gate and side-task failures, but should be verified against docs/source before trusted. |
| Cron troubleshooting checklist | `hermes-agent` | `agent-workflows` | concept/checklist | Import on demand | Likely reusable for crew cron, but best created from a real failure or official-doc check. |
| Hermes ecosystem directory triage | `hermes-agent` | `pixi-vault`, `agent-workflows`, `local-ai-infrastructure` | summary | Import on demand | Directory is broad and noisy; only a curated shortlist beats future web search. |
| Product/demo uses of Hermes tools | `ai-native-product-surfaces` | `hermes-agent`, `agent-workflows` | source pointer | Defer | New namespace exists, but no candidate source is product-surface-specific yet. |
| Dataset/fine-tuning uses of Hermes tools | `curated-tuning-datasets` | `local-ai-infrastructure`, `hermes-agent` | source pointer | Defer | No external Hermes content is dataset-corpus-specific except possible future source collection tooling. |
| RL/simulation workflow uses of Hermes tools | `rl-sim-labs` | `eval-trace`, `local-ai-infrastructure`, `hermes-agent` | source pointer | Defer | No external Hermes content is RL-sim-specific unless a tool is adopted for Critical Ranger operations. |

### Practical verdict

Keep the review as the durable artifact. Do not import new pages until Jamie asks for one of the on-demand operating questions. The populated namespaces make crosslinks more precise, but they do not justify a broader mirror.
