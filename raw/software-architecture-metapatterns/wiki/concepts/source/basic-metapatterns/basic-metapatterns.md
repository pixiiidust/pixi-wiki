---
title: "Basic metapatterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Basic metapatterns/Basic metapatterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Basic%20metapatterns/Basic%20metapatterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Basic metapatterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Basic metapatterns/Basic metapatterns.md`.

Basic [[wiki/concepts/source/introduction/metapatterns|metapatterns]] are both common stand\-alone architectures and building blocks for more complex systems\. They include the single\-component *Monolithic Architecture* and the results of its division along each of the [[wiki/concepts/source/introduction/metapatterns|coordinate axes]], namely *abstractness*, *subdomain*, and *sharding*:

### [[wiki/concepts/source/basic-metapatterns/monolith|Monolith]]


![A diagram of Monolith, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Monolith.png)


A [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] is a single\-component system, the simplest possible architecture\. It is easy to write but hard to evolve and maintain\.

*<ins>Includes</ins>*: Reactor, Proactor, and Half\-Sync/Half\-Async\.

### [[wiki/concepts/source/basic-metapatterns/shards|Shards]]


![A diagram of Shards, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Shards.png)


[[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] are multiple instances of a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]]\. They are scalable but usually require an external component for coordination\.

*<ins>Includes</ins>*: Shards and Amazon Cells, Replicas, Pool of Stateless Instances, and Create on Demand\.

### [[wiki/concepts/source/basic-metapatterns/layers|Layers]]


![A diagram of Layered Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Layers.png)


[[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] contain one component per level of abstraction\. The layers may vary in technologies and qualities and scale individually\.

*<ins>Includes</ins>*: Layers and Tiers\.

### [[wiki/concepts/source/basic-metapatterns/services|Services]]


![A diagram of Services, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Services.png)


[[wiki/concepts/source/basic-metapatterns/services|*Services*]] organize a system into subdomains, often resulting in parts of comparable size which can be assigned to dedicated teams\. However, a system of *Services* is hard to synchronize or debug\.

*<ins>Includes</ins>*: Service\-Based Architecture, Modular Monolith \(Modulith\), Microservices, Device Drivers, and Actors\.

### [[wiki/concepts/source/basic-metapatterns/pipeline|Pipeline]]


![A diagram of Pipeline, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Pipeline.png)


A [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] is a kind of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] with unidirectional flow\. Each service implements a single step of data processing\. The system is flexible but may grow out of control\.

*<ins>Includes</ins>*: Pipes and Filters, Choreographed Event\-Driven Architecture, and Data Mesh\.

| \<\< [[wiki/concepts/source/foundations-of-software-architecture/comparison-of-communication-styles|Comparison of communication styles]] | ^ [[wiki/concepts/source/root/home|Home]] ^ | [[wiki/concepts/source/basic-metapatterns/monolith|Monolith]] \>\> |
| --- | --- | --- |
