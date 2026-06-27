---
title: Hermes Agent — Activity Log
created: 2026-06-18
updated: 2026-06-26
type: log
status: compiled
namespace: hermes-agent
---

# Hermes Agent — Activity Log

## 2026-06-26

- Added `wiki/concepts/hermes-capability-routing.md` as the primary Hermes capability-selection concept from the official docs review and reusable local skill.
- Updated namespace README and index to route capability questions to `hermes-agent`; `agent-workflows` carries a cross-namespace pointer for Pixoid crew routing.
- Preserved the public deploy boundary: source updated here, generated public `pixi-wiki` requires verified rebuild and explicit deploy/push approval.

## 2026-06-18

- Seeded `hermes-agent` namespace as a slim operating reference, not a wholesale AgentWikis mirror.
- Added source-priority policy: official docs and local installed source outrank AgentWikis; AgentWikis is a discovery map.
- Added setup notes for native session traces, batch trajectories, Langfuse traces, and NeMo Relay ATOF/ATIF exports from official Hermes docs/local source.
- Reviewed Hermes Guide and AgentWikis Hermes for import candidates; added `wiki/summaries/external-hermes-wikis-import-review.md` with a slim import queue and skip rules.

## 2026-06-19

- Re-ran the external Hermes wiki import assessment after namespace population updates.
- Confirmed no wholesale import and no new immediate import pages; updated `wiki/summaries/external-hermes-wikis-import-review.md` with current namespace routing, crosslink-only/default defer decisions, and source-priority caveats.
