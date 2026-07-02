---
title: "Evolutions of an Orchestrator"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of an Orchestrator.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20an%20Orchestrator
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of an Orchestrator

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of an Orchestrator.md`.

Employing an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] has two pitfalls:

- The system becomes slower because too much communication is involved\.
- A single *Orchestrator* may be found to be too large and rigid\.


There is one way to counter the first point and more ways to solve the second one:

- Subdivide the *Orchestrator* by the system’s subdomains, forming [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]] and minimizing network communication\.
- Subdivide the *Orchestrator* by the type of client, forming [*Backends for Frontends*](<Backends for Frontends (BFF)>)\.
- Add another [[wiki/concepts/source/basic-metapatterns/layers|*layer*]] of orchestration\.
- Build a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top\-Down Hierarchy*]]\.


## Subdivide to form Layered Services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20to%20Layered%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20to%20Layered%20Services.png" alt="An orchestrator is subdivided into subdomain components which become the application layers of respective services." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/fragmented-metapatterns/layered-services|Orchestrated Three\-Layered Services]] \([[wiki/concepts/source/fragmented-metapatterns/layered-services|Layered Services]] \([[wiki/concepts/source/basic-metapatterns/services|Services]], [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\)\)\.

<ins>Goal</ins>: simplify the *Orchestrator*, let the service teams own orchestration, decouple forces for the services, and improve performance\.

<ins>Prerequisite</ins>: the high\-level \([[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestration]]\) logic is weakly coupled between the subdomains\.

If the [[wiki/concepts/source/basic-metapatterns/layers|*orchestration* logic]] mostly follows the subdomains, it may be possible to partition it accordingly\. Each service gets a part of the *Orchestrator* that mostly deals with its subdomain but may call other services when needed\. As a result, [[wiki/concepts/source/foundations-of-software-architecture/orchestration|each service orchestrates every other service]]\. Still, a large part of orchestration becomes internal to each service, meaning that fewer calls over the network are involved\.

<ins>Pros</ins>:

- You subdivide the large *Orchestrator* codebase\.
- Performance is improved\.
- The services become more independent in their quality attributes\.


<ins>Cons</ins>:

- You lose the client\-facing *orchestration team* – now each service’s team will need to face its clients\.
- Service teams become interdependent \(while having equal rights\), which may result in slow development and [suboptimal decisions](https://en.wikipedia.org/wiki/Design_by_committee)\.
- There is no way to share code between different use cases or even take a look at all of the scenarios at once\.


<ins>Further steps</ins>:

- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS Views*]] or a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]] help a service access and join data that belongs to other services, further reducing the need for interservice communication\.


## Subdivide to form Backends for Frontends

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20to%20Backends%20for%20Frontends.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20to%20Backends%20for%20Frontends.png" alt="An orchestrator is subdivided into Backends for Frontends." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [Backends for Frontends](<Backends for Frontends (BFF)>), [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]\.

<ins>Goal</ins>: simplify the *Orchestrator*, employ a team per client type, and decouple the quality attributes for clients\.

<ins>Prerequisite</ins>: clients vary in workflows and forces\.

When use cases for clients vary, it makes sense for each kind of client to have a dedicated *Orchestrator*\.

<ins>Pros</ins>:

- The smaller *Orchestrators* are independent in qualities, technologies, and teams\.
- The smaller *Orchestrators* are … well, smaller\.


<ins>Cons</ins>:

- There is no good way to [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|share code]] between the *Orchestrators*\.
- There are more system components\.


<ins>Further steps</ins>:

- You may want to add client\-specific [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] and, maybe, co\-locate them with the *Orchestrators* to avoid the extra network hop\.
- Adding another shared [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] below the ones dedicated to clients creates a place for sharing functionality among the *Orchestrators*\.
- If you are running [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] over a [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]] may help to share [[wiki/concepts/source/basic-metapatterns/layers|generic code]]\.


## Add a layer of orchestration

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20add%20Orchestrator.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20add%20Orchestrator.png" alt="An orchestrator is subdivided into a pair of simple and complex orchestrators." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]], [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: implement simple use cases quickly, while still supporting complex ones\.

<ins>Prerequisite</ins>: use cases vary in their complexity\.

You may use two or three *orchestration frameworks* \(engines\) which differ in complexity\. A simple declarative tool may be enough for the majority of user requests, and falling back to the custom\-tailored code would be needed in rare complex cases\.

<ins>Pros</ins>:

- Simple scenarios are easy to write\.
- You retain good flexibility with hand\-written code when it is needed\.


<ins>Cons</ins>:

- Requires learning multiple technologies\.
- More components mean more failures and more administration\.
- Performance of complex requests may suffer from more indirection\.


<ins>Further steps</ins>:

- Subdivide one or more of the resulting *orchestration layers* to form [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]], [*Backends for Frontends*](<Backends for Frontends (BFF)>), [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]], or [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]]\.


## Form a Hierarchy

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20to%20Hierarchy.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Orchestrator%20to%20Hierarchy.png" alt="An orchestrator is subdivided into a hierarchy." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/fragmented-metapatterns/hierarchy|Top\-Down Hierarchy]] \([[wiki/concepts/source/fragmented-metapatterns/hierarchy|Hierarchy]]\)\.

<ins>Goal</ins>: simplify the *Orchestrator* and, if possible, the services\.

<ins>Prerequisite</ins>: the domain is hierarchical\.

If an *Orchestrator* becomes too complex, some domains \(e\.g\. IIoT or telecom\) encourage the use of a tree of *Orchestrators*\. The most generic functionality is processed by its root and each additional layer takes care of one aspect of the domain\.

<ins>Pros</ins>:

- Multiple specialized teams and technologies\.
- Small codebase per team\.
- Reasonable testability\.
- Some decoupling of quality attributes\.


<ins>Cons</ins>:

- Hard to debug\.
- Poor latency in global scenarios unless several layers of the *hierarchy* are colocated\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-proxy|Evolutions of a Proxy]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-a-sandwich|Evolutions of a Sandwich]] \>\> |
| --- | --- | --- |
