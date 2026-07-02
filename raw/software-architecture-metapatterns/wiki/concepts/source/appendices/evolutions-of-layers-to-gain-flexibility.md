---
title: "Evolutions of Layers to gain flexibility"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Layers to gain flexibility.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Layers%20to%20gain%20flexibility
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Layers to gain flexibility

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Layers to gain flexibility.md`.

The last group of evolutions to consider is about making the system more adaptable\. We have [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-rely-on-plugins|already discussed]] the following evolutions for [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]]:

- The behavior of the system may be modified through [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]]\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] protects the business logic from dependencies on libraries and data stores\.
- [[wiki/concepts/source/implementation-metapatterns/microkernel|*Scripts*]] allow for customization of the system’s logic on a per client basis\.



![Diagrams of Layers with plugins, Layers with scripts, and Hexagonal Architecture with a layered core.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Layers%20-%20Further%202.png)


There is also a new evolution that modifies the upper \(orchestration\) layer:

- The [[wiki/concepts/source/basic-metapatterns/layers|*orchestration layer*]] may be split into [*Backends for Frontends*](<Backends for Frontends (BFF)>) to match the needs of several kinds of clients\.


## Divide the orchestration layer into Backends for Frontends


![The application layer is split into Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Backends%20for%20Frontends.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]], [Backends for Frontends aka BFFs](<Backends for Frontends (BFF)>)\.

<ins>Goal</ins>: let each kind of client get a dedicated development team\.

<ins>Prerequisite</ins>: no high\-level logic is shared between client types\.

It is possible that your system has different kinds of users, e\.g\. buyers, sellers, and admins; or web and mobile applications\. It may be easier to support a separate integration module for each kind of client than to keep all the unrelated code together in a single integration layer\.

<ins>Pros</ins>:

- Each kind of client gets a dedicated team which may choose best fitting technologies\.
- You get rid of the single large codebase of the integration layer\.


<ins>Cons</ins>:

- There is no good way to share code between the *BFFs* \(in the [[wiki/concepts/source/extension-metapatterns/orchestrator|naive implementation]]\)\.
- There are new components to administer\.


<ins>Further steps</ins>:

- [Evolve the *BFFs*](<Backends for Frontends (BFF)#evolutions>) through adding a shared *layer* or [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]] for the common functionality\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-layers-to-improve-performance|Evolutions of Layers to improve performance]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-services-that-restructure-services|Evolutions of Services that restructure services]] \>\> |
| --- | --- | --- |
