---
title: Bounded Context Tree Pattern
created: 2026-06-07
updated: 2026-06-07
type: concept
tags: [architecture, workflow, ai]
sources: [Projects/README.md]
confidence: high
---

# Bounded Context Tree Pattern

## Definition

A project organization pattern where every project in a vault or workspace is structured as a **bounded context** — a self-contained domain with its own language, decisions, and execution artifacts. Contexts are arranged as trees:

- **Root** = the bounded context (e.g., `myAbode/`, `LeJEPA/`)
- **Branches** = the major concerns within that context (strategy, architecture, product, experiments)
- **Leaves** = specific artifacts (ADRs, POC documents, status reports, conclusion write-ups)

This is inspired by Domain-Driven Design (DDD) bounded contexts but adapted for personal knowledge management: each project context owns its vocabulary, decisions stay local, and cross-context references are explicit.

## Current application

Jamie's Obsidian vault organizes all projects as bounded contexts under `Projects/`. Each context has:

- A numbered or tiered file structure that maps to the concern hierarchy
- An `Index.md` hub note describing the context and linking to all branches
- Self-contained artifacts: PRDs, ADRs, POC specs, status reports
- Explicit cross-context links when boundaries are crossed

Current bounded contexts:

- `Projects/myAbode/` — AI-native Agent CRM (product strategy exercise)
- `Projects/LeJEPA/` — Market Stress Detection experiment (concluded FAIL)
- `Projects/Planned/` — Planned.com Program Intelligence demo
- `Projects/Pixoid Agent Capability Routes/` — agent route governance
- `Projects/EdenOS/` — multi-agent workflow OS
- `Projects/Personal/` — infrastructure and setup notes

## Examples and applications

**LeJEPA tree:**
```
LeJEPA/
├── Index.md                  (hub note — experiment overview, results, architecture)
├── 01 - Experiment Overview.md (full experiment design, quickstart)
├── 02 - POC-1.md             (locked FAIL — threshold inflated by COVID volatility)
├── 03 - POC-2.md             (locked FAIL — regime filtering helped but still late)
├── 04 - POC-3.md             (locked FAIL — 0/10 seeds, failure is consistent)
└── 05 - Conclusion.md        (final write-up — structural FAIL)
```

**myAbode tree:**
```
myAbode/
├── 01 - Strategy.md          (what, why, constraints)
├── 02 - Domain/
│   └── Ubiquitous Language.md (glossary)
├── 03 - Architecture/
│   ├── ADR Index.md          (all 9 decisions)
│   └── ADR-0001 through ADR-0009
└── 04 - Product/
    ├── UI Surfaces.md        (5 surfaces identified)
    └── Command Grid.md       (selected variant)
```

## Advantages

- **Language isolation** — each context owns its jargon; no accidental cross-pollution
- **Autonomous evolution** — contexts can be updated, concluded, or archived independently
- **Narrative flow** — numbered files guide readers and agents through the context's story
- **Explicit boundaries** — cross-context references become deliberate decisions, not drift
- **Agent-friendly** — agents can navigate by tree structure and hub notes without guessing

## Open questions

- How to handle a context that spawns a child context (e.g., myAbode ADRs referencing a compliance-domain context)?
- Should the tree depth be limited? Current max is 3 levels (context → concern → artifact).

## Related pages

- [[Projects/README|Projects Bounded Context Tree]]
- [[Projects/myAbode/Index|myAbode Index]]
- [[Projects/LeJEPA/Index|LeJEPA Index]]
- [[Knowledge/concepts/matt-pocock-sdlc-rhythm|Matt Pocock SDLC Rhythm]]
- [[Knowledge/index|Knowledge Wiki Index]]