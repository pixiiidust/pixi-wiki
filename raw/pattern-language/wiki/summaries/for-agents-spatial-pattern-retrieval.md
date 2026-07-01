---
title: For Agents — Spatial Pattern Retrieval
created: 2026-07-01
updated: 2026-07-01
type: summary
status: compiled
namespace: pattern-language
sources:
  - README.md
  - wiki/concepts/patterns/
---

# For Agents — Spatial Pattern Retrieval

Use this namespace as a spatial-design constraint source, not as generic inspirational prose.

## Retrieval Loop

1. Clarify the design target: room, building, street, neighborhood, town, world zone, or gameplay space.
2. Retrieve 5–12 relevant patterns from `pattern-language` by title, problem, solution, or related-pattern graph.
3. Prefer a mixed scale stack: one or two large-scale patterns, several layout/activity patterns, and a few detailed human-experience patterns.
4. Convert each selected pattern into constraints:
   - spatial relationship
   - adjacency or separation rule
   - scale cue
   - human activity/comfort cue
   - verification question
5. Produce a design brief that cites pattern names and numbers.
6. Verify the output against the selected patterns before calling it coherent.

## Output Shape

```text
Design target:
Selected patterns:
- Pattern Name (N): reason selected
Constraints:
- Pattern Name (N): concrete spatial/action constraint
Scene or layout moves:
- move, placement, zoning, path, view, threshold, activity node
Verification checklist:
- checkable question tied to each pattern
License note:
- source is non-commercial attribution reference material
```

## Worldbuilding and Unreal MCP Use

For Unreal-connected agents, use retrieved patterns to create a scene brief before issuing world-building actions. Examples:

- `Activity Nodes (30)` → place active anchors where paths converge.
- `Promenade (31)` → create a legible walking loop or public edge.
- `Accessible Green (60)` → keep shared green space near dwellings or activity clusters.
- `Small Public Squares (61)` → keep plazas human-scaled rather than oversized.
- `Intimacy Gradient (127)` → order spaces from public to private.
- `Light on Two Sides of Every Room (159)` → prefer room volumes with multi-directional light.
- `Window Place (180)` → create inhabitable view/rest points, not just flat walls.

Do not implement tool calls directly from this document. Treat it as the retrieval-to-constraint contract a future adapter can consume.
