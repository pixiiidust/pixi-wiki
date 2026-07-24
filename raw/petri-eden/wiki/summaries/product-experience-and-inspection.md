---
title: Petri Eden Product Experience and Inspection
created: 2026-07-24
updated: 2026-07-24
type: summary
status: active
namespace: petri-eden
sources:
  - Petri Eden UI design and native v1 plan
confidence: high
---

# Petri Eden Product Experience and Inspection

## Product Loop

```text
design species -> seed world -> watch -> select -> inspect
              -> intervene -> save/branch -> compare
```

The world is the primary artifact. Charts and panels explain it rather than replacing it.

## Stable Desktop Frame

### World canvas

The largest surface shows organisms, plants, carcasses, materials, terrain cues, selection, and activity. It should remain legible at overview scale and useful when tracking one organism or lineage.

### Top bar

Persistent run controls and identity:

- seed and run identity;
- tick/time and current speed policy;
- pause/resume and exact step;
- save/export access when implemented;
- normal, degraded, faulted, or terminal state.

### Right rail

Progressive measurement:

- population and biomass;
- material transfer and birth/death causes;
- generation, traits, and controller complexity;
- integrity and performance diagnostics.

The rail shows raw measurements and trends. It must not collapse the ecosystem into a hidden health score.

### Bottom drawer

Contextual investigation:

- selected organism phenotype;
- lineage and operational species;
- ordered perception inputs;
- neural nodes, connections, and action outputs;
- causal events and timelines;
- charts and technical diagnostics.

### Species Design Studio

A constrained pre-run or intervention surface for creating a species while preserving experiment metadata. It should not become an unrestricted behavior-tree editor or visual programming environment in v1.

## Inspection Contract

A useful inspection path answers progressively deeper questions:

1. **What changed?** Population, biomass, material flow, births, deaths.
2. **Where did it happen?** World location, selected organism, local neighborhood.
3. **Which lineage changed?** Parent/descendant history and species branch.
4. **What did the organism sense?** Ordered spatial/perception channels.
5. **What did the controller output?** Neural activation and action evidence.
6. **What can be reproduced?** Seed, config, version, command history, save/branch identity.

## Progressive Disclosure

The interface should support three modes without separate products:

- **watch**: the world and basic trends;
- **investigate**: select organisms, lineages, and events;
- **audit**: exact metadata, diagnostics, digests, saves, exports, and comparison.

## Accessibility and State Completeness

The v1 plan reserves explicit work for keyboard access, onboarding, empty/loading/degraded/faulted states, window behavior, DPI, and visual certification. Those are later planned epics as of 2026-07-24, not current implementation claims.

## Product Risks

- dashboards dominate the world and turn exploration into spreadsheet reading;
- attractive motion becomes mistaken for scientific evidence;
- speed controls change the logical experiment;
- selection state is not stable across snapshot refreshes;
- charts omit denominators or retention/downsampling rules;
- normal ecological collapse is presented as a software error;
- controller diagrams imply intelligence without behavioral evidence.

## Related

- [[wiki/entities/petri-eden|Petri Eden Project]]
- [[wiki/summaries/v1-system-map|V1 System Map]]
- [[wiki/summaries/evidence-and-frontier|Evidence and Frontier]]
- [[wiki/concepts/operational-species|Operational Species]]
