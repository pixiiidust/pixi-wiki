---
title: "Source Wiki Home"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Home.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Home
source_license_note: "See namespace README; preserve attribution and source links."
---

# Source Wiki Home

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Home.md`.

# Architectural Patterns Wiki

This site has multiple goals:

1. #### Become a wiki of architectural patterns

   There are many patterns here. I invested over a year in collecting architectural patterns and styles that relate to the structure of a system.

   You will find here [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] and [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] but not [*Test-Driven Development*](https://herbertograca.com/2018/08/27/distillation-of-tdd-where-did-it-all-go-wrong/) (which is a methodology pattern) or [*Dead Letter Channel*](https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html) (a communication pattern).

2. #### Show that patterns make a hierarchy

   There are way too many patterns. Thus some of them are similar, as there are only so many different things a human mind can invent. This wiki groups patterns according to their structure and function, and describes specific features, use cases, benefits and drawbacks for each group of patterns as a whole to outline the big picture and avoid repetition.

   For example, [[wiki/concepts/source/extension-metapatterns/orchestrator|*Scatter-Gather* and *MapReduce*]] are almost identical (*Scatter-Gather* lacks the Reduce step) while their relation to [[wiki/concepts/source/extension-metapatterns/orchestrator|*Saga*]] is more remote but still traceable (each of the three patterns coordinates components of a system).

3. #### Provide an intuitive way to study patterns

   Having patterns arranged into a hierarchy greatly reduces the amount of information one must remember to learn a new pattern as it differs from others in its group in minor details.

   Also, if we can enumerate patterns and see how they relate to each other, then we can [[wiki/concepts/source/analytics/comparison-of-architectural-patterns|compare them]] and even spot empty spaces in our knowledge - which is how I discovered [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]].

Places to start:

* [[wiki/concepts/source/appendices/index-of-patterns|Index of patterns]]
* [[wiki/concepts/source/introduction/about-this-book|Diagrams and notation]]
* [[wiki/concepts/source/introduction/metapatterns|The underlying theory]]

You can download this as a book from [GitHub](https://github.com/denyspoltorak/metapatterns) or [Leanpub](https://leanpub.com/metapatterns) (which also features a few testimonials and a detailed table of contents). The work is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Any help with the content, including adding new patterns or correcting the ones already described, is appreciated.

## Table of Contents:

### [[wiki/concepts/source/introduction/introduction|Introduction]]

- [[wiki/concepts/source/introduction/about-this-book|About this book]]
- [[wiki/concepts/source/introduction/metapatterns|Metapatterns]]
- [[wiki/concepts/source/introduction/system-topologies|System topologies]]

### [[wiki/concepts/source/foundations-of-software-architecture/foundations-of-software-architecture|Foundations of software architecture]]

- [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|Modules and complexity]]
- [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|Forces, asynchronicity, and distribution]]
- [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|Four kinds of software]]
- [[wiki/concepts/source/foundations-of-software-architecture/arranging-communication|Arranging communication]]
  - [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|Programming and architectural paradigms]]
  - [[wiki/concepts/source/foundations-of-software-architecture/orchestration|Orchestration]]
  - [[wiki/concepts/source/foundations-of-software-architecture/choreography|Choreography]]
  - [[wiki/concepts/source/foundations-of-software-architecture/shared-data|Shared data]]
  - [[wiki/concepts/source/foundations-of-software-architecture/comparison-of-communication-styles|Comparison of communication styles]]

### [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic metapatterns]]

- [[wiki/concepts/source/basic-metapatterns/monolith|Monolith]]
- [[wiki/concepts/source/basic-metapatterns/shards|Shards]]
- [[wiki/concepts/source/basic-metapatterns/layers|Layers]]
- [[wiki/concepts/source/basic-metapatterns/services|Services]]
- [[wiki/concepts/source/basic-metapatterns/pipeline|Pipeline]]

### [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|Extension metapatterns]]

- [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]]
- [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]
- [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]
- [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]
- [[wiki/concepts/source/extension-metapatterns/sandwich|Sandwich]]

### [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Fragmented metapatterns]]

- [[wiki/concepts/source/fragmented-metapatterns/layered-services|Layered Services]]
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]]
- [Backends for Frontends (BFF)](<Backends for Frontends (BFF)>)
- [Service-Oriented Architecture (SOA)](<Service-Oriented Architecture (SOA)>)
- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|Hierarchy]]

### [[wiki/concepts/source/implementation-metapatterns/implementation-metapatterns|Implementation metapatterns]]

- [[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]]
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal Architecture]]
- [[wiki/concepts/source/implementation-metapatterns/microkernel|Microkernel]]
- [[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]]

### [[wiki/concepts/source/analytics/analytics|Analytics]]

- [[wiki/concepts/source/analytics/comparison-of-architectural-patterns|Comparison of architectural patterns]]
  - [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|Sharing functionality or data among services]]
  - [[wiki/concepts/source/analytics/pipelines-in-architectural-patterns|Pipelines in architectural patterns]]
  - [[wiki/concepts/source/analytics/dependency-inversion-in-architectural-patterns|Dependency inversion in architectural patterns]]
  - [[wiki/concepts/source/analytics/indirection-in-commands-and-queries|Indirection in commands and queries]]
- [[wiki/concepts/source/analytics/ambiguous-patterns|Ambiguous patterns]]
- [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|Architecture and product life cycle]]
- [[wiki/concepts/source/analytics/real-world-inspirations-for-architectural-patterns|Real-world inspirations for architectural patterns]]
- [[wiki/concepts/source/analytics/the-heart-of-software-architecture|The heart of software architecture]]
  - [[wiki/concepts/source/analytics/cohesers-and-decouplers|Cohesers and decouplers]]
  - [[wiki/concepts/source/analytics/deconstructing-patterns|Deconstructing patterns]]
  - [[wiki/concepts/source/analytics/choose-your-own-architecture|Choose your own architecture]]

### [[wiki/concepts/source/appendices/appendices|Appendices]]

- [[wiki/concepts/source/appendices/acknowledgements|Acknowledgements]]
- [[wiki/concepts/source/appendices/books-referenced|Books referenced]]
- [[wiki/concepts/source/appendices/copyright|Copyright]]
- [[wiki/concepts/source/appendices/disclaimer|Disclaimer]]
- [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-lead-to-shards|Evolutions of a Monolith that lead to Shards]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-result-in-layers|Evolutions of a Monolith that result in Layers]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-make-services|Evolutions of a Monolith that make Services]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-rely-on-plugins|Evolutions of a Monolith that rely on Plugins]]
  - [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-data|Evolutions of Shards that share data]]
  - [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-logic|Evolutions of Shards that share logic]]
  - [[wiki/concepts/source/appendices/evolutions-of-layers-that-make-more-layers|Evolutions of Layers that make more layers]]
  - [[wiki/concepts/source/appendices/evolutions-of-layers-that-help-large-projects|Evolutions of Layers that help large projects]]
  - [[wiki/concepts/source/appendices/evolutions-of-layers-to-improve-performance|Evolutions of Layers to improve performance]]
  - [[wiki/concepts/source/appendices/evolutions-of-layers-to-gain-flexibility|Evolutions of Layers to gain flexibility]]
  - [[wiki/concepts/source/appendices/evolutions-of-services-that-restructure-services|Evolutions of Services that restructure services]]
  - [[wiki/concepts/source/appendices/evolutions-of-services-that-add-layers|Evolutions of Services that add layers]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-pipeline|Evolutions of a Pipeline]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-middleware|Evolutions of a Middleware]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-shared-repository|Evolutions of a Shared Repository]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-proxy|Evolutions of a Proxy]]
  - [[wiki/concepts/source/appendices/evolutions-of-an-orchestrator|Evolutions of an Orchestrator]]
  - [[wiki/concepts/source/appendices/evolutions-of-a-sandwich|Evolutions of a Sandwich]]
- [[wiki/concepts/source/appendices/format-of-a-metapattern|Format of a metapattern]]
- [[wiki/concepts/source/appendices/glossary|Glossary]]
- [[wiki/concepts/source/appendices/history-of-changes|History of changes]]
- [[wiki/concepts/source/appendices/index-of-patterns|Index of patterns]]

| \<\< [[wiki/concepts/source/appendices/index-of-patterns|Index of patterns]] |  | [[wiki/concepts/source/introduction/introduction|Introduction]] \>\> |
| --- | --- | --- |
