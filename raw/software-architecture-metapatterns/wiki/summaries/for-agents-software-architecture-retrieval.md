---
title: For Agents — Software Architecture Retrieval
created: 2026-07-02
updated: 2026-07-02
type: summary
status: compiled
namespace: software-architecture-metapatterns
sources:
  - README.md
  - wiki/concepts/source/
---

# For Agents — Software Architecture Retrieval

Use this namespace as a software-architecture reasoning source, not as a menu of fashionable shapes.

## Retrieval Loop

1. Clarify the design target: product surface, service, module, workflow, data system, integration boundary, or whole codebase.
2. Identify the current forces: latency, throughput, dependency churn, deployment boundaries, data ownership, team ownership, extensibility, testability, and migration risk.
3. Retrieve 3–8 relevant pages from `software-architecture-metapatterns` by pattern name, alias, force, or evolution path.
4. Compare candidates by:
   - structural shape
   - communication style
   - dependency direction
   - where business logic lives
   - performance tradeoff
   - operational/team cost
   - possible next evolution
5. Produce a recommendation with citations to source pages and a small verification checklist.

## Output Shape

```text
Design target:
Observed forces:
Relevant metapatterns:
- Metapattern/source page: reason selected
Recommendation:
- preferred shape and why
Avoid:
- shapes that are overkill or mismatched
Evolution path:
- safe next step, rollback, and later split point
Verification checklist:
- concrete checks tied to dependency, performance, and ownership assumptions
License note:
- source is attributed external reference material; preserve provenance
```

## Useful Starting Queries

- `monolith layers services migration`
- `hexagonal architecture dependency inversion adapters`
- `orchestrator choreography saga event mediator`
- `pipeline throughput latency batch stream`
- `proxy gateway backend for frontend adapter`
- `polyglot persistence data ownership shared repository`

## Pixi/Jamie Use

- For codebase review: use this namespace to name the current shape before proposing changes.
- For product prototypes: prefer simple monolith/layers unless forces justify distribution.
- For agent work: cite the metapattern pages that shaped the plan so Pixoid can review the reasoning.
- For migration: retrieve the relevant evolution pages before recommending a split.
