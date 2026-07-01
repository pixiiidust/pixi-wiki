---
title: Unreal MCP Worldbuilding Adapter — Deferred Design Space
created: 2026-07-01
updated: 2026-07-01
type: synthesis
status: deferred
namespace: pattern-language
sources:
  - README.md
  - wiki/summaries/for-agents-spatial-pattern-retrieval.md
  - https://github.com/pixiiidust/pixi-wiki/issues/48
---

# Unreal MCP Worldbuilding Adapter — Deferred Design Space

The first `pattern-language` release publishes the knowledge namespace only. The Unreal MCP adapter is a later design/build slice after live retrieval and search are verified.

## Adapter Question

How should a Hermes agent translate selected spatial patterns into Unreal actions while keeping the design explainable and verifiable?

## Candidate Input Contract

```yaml
design_target: walkable village square
selected_patterns:
  - Activity Nodes (30)
  - Promenade (31)
  - Small Public Squares (61)
  - Accessible Green (60)
  - Intimacy Gradient (127)
constraints:
  - paths should converge at activity anchors
  - square should remain human-scaled
  - public/private transitions should be legible
verification:
  - each selected pattern has at least one scene-level check
```

## Candidate Unreal-Level Actions

- Create or select a terrain/zone boundary.
- Place path network and intersections.
- Place activity nodes at path convergence points.
- Zone public, semi-public, and private gradients.
- Place plazas, greens, thresholds, and view/rest points.
- Add labels or metadata tying generated objects back to pattern IDs.
- Run a verifier that checks the scene graph against selected pattern constraints.

## Open Design Questions

- What schema maps a pattern to one or more Unreal MCP actions?
- Should the adapter act directly or produce a design brief for a separate builder agent?
- How many patterns should one generation pass apply before becoming incoherent?
- Which scene graph facts are needed for verification: distances, visibility, adjacency, path connectivity, scale, object tags?
- How should license/provenance notes appear in generated scene metadata or reports?

## Deferral Rule

Do not start adapter implementation until `pattern-language` is live, searchable, and verified through Pixi Wiki raw/HTML/llms/MCP surfaces.
