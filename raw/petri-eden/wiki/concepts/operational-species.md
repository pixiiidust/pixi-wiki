---
title: Operational Species
created: 2026-07-24
updated: 2026-07-24
type: concept
status: active
namespace: petri-eden
sources:
  - Petri Eden native v1 delivery plan
confidence: high
---

# Operational Species

## Definition

An operational species is a reproducible grouping rule for simulated organisms based on lineage and genome similarity. It is an analysis instrument with versioned parameters, not a subjective label based on appearance and not a claim that one universal biological species definition has been solved.

## Required Contract

A usable definition needs:

- a deterministic genome-distance function;
- explicit weights for structural and parameter differences;
- a threshold or clustering rule;
- stable tie-breaking and representative selection;
- a versioned assignment policy;
- lineage continuity rules across births, mutation, extinction, and reappearance;
- provenance in saves and exports;
- tests across repeated runs and worker counts.

## Why Species Needs Lineage

Genome distance alone can create unstable labels when a population drifts around a threshold. Lineage provides temporal and causal continuity:

- who descended from whom;
- when a branch separated;
- which mutations crossed the operational threshold;
- whether a cluster persisted or only appeared for one sample;
- how extinction and reintroduction should be recorded.

## Instrument Versus Authority

The authoritative simulation owns genomes, organisms, births, deaths, and ancestry. Species assignment is a deterministic derived index over that truth. It must not secretly change reproduction, ecology, or selection unless an experiment explicitly introduces species-dependent rules.

## UI Implications

A species surface should expose:

- stable species ID and color;
- representative genome or lineage root;
- population and biomass over time;
- generation and trait distributions;
- controller complexity distributions;
- parent/child species relationships;
- threshold/version metadata;
- uncertainty or boundary cases rather than forced confidence.

## Failure Modes

- assigning species by hand-authored predator/prey guild;
- clustering only by current appearance;
- allowing hash or iteration order to change IDs;
- changing distance weights without a version bump;
- treating every mutation as a new species;
- using species count alone as evidence of meaningful evolutionary novelty;
- letting the species index feed back into selection accidentally.

## Evidence Gate

An operational-species implementation supports statements such as "this deterministic rule identified three persistent lineage clusters." It does not by itself support "three genuinely new biological species evolved" or "open-ended evolution occurred."

## Related

- [[wiki/entities/petri-eden|Petri Eden Project]]
- [[wiki/summaries/v1-system-map|V1 System Map]]
- [[wiki/summaries/evidence-and-frontier|Evidence and Frontier]]
- [[../../eval-trace/wiki/concepts/emergence-claim-ladder|Emergence Claim Ladder]]
