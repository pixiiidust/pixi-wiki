---
title: "Analytics"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/Analytics.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/Analytics
source_license_note: "See namespace README; preserve attribution and source links."
---

# Analytics

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/Analytics.md`.

This part is dedicated to analyzing the architectural [[wiki/concepts/source/introduction/metapatterns|metapatterns]], for if this book’s taxonomy of patterns is a step forward from the state of the art, it should bear fruits for us to pick.

I had no time to research every idea collected while the book was being written and its individual chapters published for feedback. A few of those pending topics, which may make additional chapters in the future, are listed below:

- Some architectural patterns (*CQRS*, *Cache*, *Microservices*, etc.) appear under multiple metapatterns. Each individual case makes a story of its own, teaching about both the needs of software systems and uses of metapatterns.
- There are different ways to split a component into subcomponents: [*Layers of Services*](<Service-Oriented Architecture (SOA)>) differ from [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]]. This should be investigated.
- An architectural quality may depend on the structure of the system. For example, a client request may be split into three subrequests to be processed sequentially or in parallel, depending on the [[wiki/concepts/source/introduction/system-topologies|topology]] (e.g. [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrated Services*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Replicas*]]), thus it is topology which defines latency. We can even draw formulas like:
  - L = L1 \+ L2 \+ L3 for *Pipeline*,
  - L = MAX(L1, L2, L3) for *Orchestrated Services* which run in parallel,
  - L = MIN(L1, L2, L3) for *Replicas* with [*Request Hedging*](https://grpc.io/docs/guides/request-hedging/).


Other smaller topics that I was able to look into made the following chapters:

- [[wiki/concepts/source/analytics/comparison-of-architectural-patterns|Comparison]] of the ways different architectures [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|share functionality or data]], [[wiki/concepts/source/analytics/pipelines-in-architectural-patterns|build pipelines]], and use [[wiki/concepts/source/analytics/dependency-inversion-in-architectural-patterns|dependency inversion]] and [[wiki/concepts/source/analytics/indirection-in-commands-and-queries|indirection]].
- [[wiki/concepts/source/analytics/ambiguous-patterns|Ambiguous patterns]] whose meaning differs from author to author.
- [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|Evolution of the software architecture]] during a product’s life cycle.
- [[wiki/concepts/source/analytics/real-world-inspirations-for-architectural-patterns|Real-world examples]] that inspire metapatterns.
- [[wiki/concepts/source/analytics/the-heart-of-software-architecture|Cohesion and decoupling]] as the main architectural drivers: their [[wiki/concepts/source/analytics/cohesers-and-decouplers|influence on forces]], [[wiki/concepts/source/analytics/deconstructing-patterns|interplay in patterns]] and, finally, a short guide on [[wiki/concepts/source/analytics/choose-your-own-architecture|choosing an architecture]] suitable for your project.


## Contents:

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
