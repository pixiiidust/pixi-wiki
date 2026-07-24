---
title: "Software Architecture Metapatterns"
created: 2026-07-02
updated: 2026-07-24
type: namespace-overview
status: active
category: knowledge-systems
namespace: software-architecture-metapatterns
confidence: medium
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_license_note: "Repository root is CC BY-NC-SA 4.0; book/source directory and wiki indicate CC BY 4.0. Preserve attribution and no-endorsement guardrails."
---

# Software Architecture Metapatterns

> Software-architecture pattern-language reference for agents, compiled from Denys Poltorak's *Architectural Metapatterns: The Pattern Language of Software Architecture* GitHub wiki.

## Scope

### Covers

The `software-architecture-metapatterns` namespace covers software architecture metapatterns: system topologies, layers, services, pipelines, proxies, orchestrators, plugins, hexagonal architecture, service-oriented architecture, polyglot persistence, pattern aliases, architectural forces, dependencies, performance tradeoffs, architecture evolution paths, and clearly labeled applied syntheses derived from project evidence.

### Not Covered

This namespace does not cover every design pattern or programming idiom, prescribe architecture by fashion, replace project-specific code review, or establish commercial-clean training-data clearance. It is a reference and reasoning aid for architecture review, migration planning, and agent retrieval.

### Current As

2026-07-24 — The namespace remains classified under Knowledge Systems, preserves the imported public architecture corpus, and now includes an applied authoritative-simulation-boundary synthesis linked reciprocally to Petri Eden.

## Canonical Source Roots

- Source repository: `https://github.com/denyspoltorak/metapatterns`
- Source wiki: `https://github.com/denyspoltorak/metapatterns/wiki`
- Source website: `https://metapatterns.io/`
- Latest release inspected: `https://github.com/denyspoltorak/metapatterns/releases/tag/v1.2`

## Provenance and License Guardrail

The repository root license is **Creative Commons Attribution-NonCommercial-ShareAlike 4.0**. The book/source directory and wiki copyright page indicate **Creative Commons Attribution 4.0**. This namespace keeps the ambiguity visible and follows a conservative public-use stance: preserve attribution, source links, license notes, and no-endorsement boundaries.

Use this corpus for reference, critique, education, architecture review, and non-misleading agent retrieval. Do not present it as unrestricted commercial training data or as Jamie/Pixi-authored source material.

## Agent Use Contract

- Start with [[wiki/summaries/for-agents-software-architecture-retrieval|For Agents — Software Architecture Retrieval]].
- Retrieve a bounded set of 3–8 relevant metapattern/source pages before recommending an architecture.
- Compare patterns by structure, dependency direction, communication style, performance, team ownership, and likely evolution path.
- Cite metapattern names and source pages in the recommendation so a human can inspect the reasoning.
- Prefer "what forces are present?" over "what architecture is trendy?" Tiny systems do not need distributed cosplay.

## Applied Syntheses

- [[wiki/syntheses/authoritative-simulation-boundary|Authoritative Simulation Boundary]] — One mutation authority, ordered commands, immutable snapshots, deterministic parallel work, and explicit fault boundaries.
- Cross-namespace case: [[../../petri-eden/wiki/summaries/v1-system-map|Petri Eden V1 System Map]].

## Public Output Contract

When published to `pixi-wiki`, this namespace should expose:

```text
/raw/software-architecture-metapatterns/README.md
/raw/software-architecture-metapatterns/wiki/index.md
/wiki/software-architecture-metapatterns/README.md.html
/wiki/software-architecture-metapatterns/wiki/index.md.html
/wiki/software-architecture-metapatterns/llms.txt
```
