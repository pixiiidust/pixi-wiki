---
title: "Choose your own architecture"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/The heart of software architecture/Choose your own architecture.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/The%20heart%20of%20software%20architecture/Choose%20your%20own%20architecture
source_license_note: "See namespace README; preserve attribution and source links."
---

# Choose your own architecture

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/The heart of software architecture/Choose your own architecture.md`.

Now that we’ve seen patterns decomposed into decoupling and cohesion, we can try reconstructing architecture based on your project’s needs\.

## Project size

The project’s expected size is among the main determinants of the project’s architecture as both overgrown components and excessive fragmentation handicap development and maintenance\. A moderate number of components of moderate size is the desired zone of comfort\.

Therefore, a one day task will likely be [[wiki/concepts/source/basic-metapatterns/monolith|*monolithic*]], a man\-month of work needs [[wiki/concepts/source/basic-metapatterns/layers|*layering*]], while anything larger than that calls for at least partial separation into *subdomain* [[wiki/concepts/source/basic-metapatterns/services|*modules*]] or [[wiki/concepts/source/basic-metapatterns/services|*services*]]\. Very large projects may require further subdivision into [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) or [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Size-1.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Size-1.png" alt="Diagrams of Monolith, Layers, Services, Service-Oriented Architecture, and Cell-Based Architecture." loading="lazy" width=100%/>
</a>
</div>

Any inherent decoupling within your domain is another factor to consider in the initial design\. For example, the layer with [[wiki/concepts/source/basic-metapatterns/layers|*domain* logic]] is very likely to comprise independent subdomains which naturally make modules or services at next to no development or runtime cost \(see [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]]\)\. Likewise, [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top\-Down Hierarchy*]] is a good fit for a hierarchical domain\. A domain that builds around stepwise processing of data or events may be modeled as a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], which is a very flexible architectural style\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Size-2.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Size-2.png" alt="Diagrams of Sandwich, Top-Down Hierarchy, and Pipeline." loading="lazy" width=100%/>
</a>
</div>

The number of teams you start the project with is also important\. For the teams to be as efficient as possible you want them to be almost independent\. As every team gets ownership of one or two components, you must assure that the architecture has enough modules or services for the teams to specialize, because anything shared will likely become a bottleneck\. For example, you can hardly employ more than 3 teams with a [[wiki/concepts/source/basic-metapatterns/layers|*layered architecture*]] as there are only so many layers in any system\. Thus, having a large number of teams strongly hints at [[wiki/concepts/source/basic-metapatterns/services|*Services*]], [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], [*SOA*](<Service-Oriented Architecture (SOA)>), or [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]\.

If not all the teams are available from day one, it is still preferable to initially set up component boundaries for the prospective number of teams because subdividing an already implemented component is a terrible experience\. However, it may be [easier and safer](https://martinfowler.com/bliki/MonolithFirst.html) for now to leave all the components running within a single process \(as [[wiki/concepts/source/basic-metapatterns/services|*modules*]]\) to avoid the overhead of going distributed and have less trouble moving pieces of code around as needed \(as new requirements often make a joke of your original design\)\. You should be able to turn *modules* into [[wiki/concepts/source/basic-metapatterns/services|*services*]] through moderate effort once that becomes an imperative\.

## Domain features

We have already seen above that hierarchical or pipelined domains enable the use of corresponding architectures\. There is more to it\.

Sometimes you expect to have many complex use cases which cannot be matched to your subdomains because every scenario involves multiple components, thus spreading over the entire system\. You would usually collect the global use cases into a dedicated component – an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\. And if the *Orchestrator* grows out of control, it is [[wiki/concepts/source/extension-metapatterns/orchestrator|subdivided]] into layers or services\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Features-1.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Features-1.png" alt="Diagrams of Services with: a monolithic orchestrator, Backends for Frontends, an orchestrator per use case, a hierarchical orchestrator and a layered orchestrator." loading="lazy" width=100%/>
</a>
</div>

Other systems are built around data\. You cannot split it into private databases because almost every service needs access to the whole, which necessitates a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]], or the highly performant [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Features-2.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Features-2.png" alt="Diagrams of Services with a shared database and Space-Based Architecture." loading="lazy" width=100%/>
</a>
</div>

Once you go distributed, you will likely employ a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] to centralize the communication between your services\. And you will have various [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]], such as a [[wiki/concepts/source/extension-metapatterns/proxy|*Firewall*]], a [[wiki/concepts/source/extension-metapatterns/proxy|*Reverse Proxy*]], and a [[wiki/concepts/source/extension-metapatterns/proxy|*Response Cache*]]\. You may even deploy a *Proxy* per kind of client if the clients vary in their protocols, resulting in [*Backends for Frontends*](<Backends for Frontends (BFF)>) \(*BFF*\)\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Features-3.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Features-3.png" alt="Diagrams of Services with a middleware, Services with a proxy, and Backends for Frontends." loading="lazy" width=100%/>
</a>
</div>

## Runtime performance

Moreover, there are non\-functional requirements, such as performance and fault tolerance\.

High throughput is achieved by [[wiki/concepts/source/basic-metapatterns/shards|*sharding*]] or [[wiki/concepts/source/basic-metapatterns/shards|*replicating*]] your business logic or even your data\. Sharding also helps process huge datasets while replication improves fault tolerance\. [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]] replicates the entire dataset in memory for faster access\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-1.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-1.png" alt="Diagrams of stateless instances with a load balancer and a shared database, shards behind a sharding proxy, and replicas behind a load balancer." loading="lazy" width=100%/>
</a>
</div>

Alternatively, you may use several specialized databases \([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\) or redesign a highly loaded part of your system as a self\-scaling [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-2.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-2.png" alt="Diagrams of Services with Polyglot Persistence and a Cell with a scaled pipeline." loading="lazy" width=100%/>
</a>
</div>

Scalability under uneven load is achieved through [[wiki/concepts/source/basic-metapatterns/services|*Function as a Service*]] \(*Nanoservices*\), [[wiki/concepts/source/implementation-metapatterns/mesh|*Service\-Mesh*]]\-based [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] and, to a greater extent, [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-3.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-3.png" alt="Diagrams of scaled single-layer Nanoservices, Microservices, and processing units of Space-Based Architecture." loading="lazy" width=100%/>
</a>
</div>

Fault tolerance requires you to have [[wiki/concepts/source/basic-metapatterns/shards|*replicas*]] of every component, including databases, ideally over multiple data centers\. If you are not that rich, be content with [[wiki/concepts/source/basic-metapatterns/services|*Actors*]] or [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-4.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-4.png" alt="Diagrams of whole-system replicas of Services with an API Gateway, actors running in a distributed framework, and a peer-to-peer mesh." loading="lazy" width=100%/>
</a>
</div>

Low latency makes you place simplified first response logic close to your input, leading to:

- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Presenter*]] or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Controller*]] pattern families for user interaction\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] with [[wiki/concepts/source/basic-metapatterns/layers|*strategy injection*]] for single hardware input\.
- A [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] for distributed [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control*]] systems such as [IIoT](https://en.wikipedia.org/wiki/Industrial_internet_of_things)\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-5.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Performance-5.png" alt="Shortcuts in the control flow of Model-View-Presenter, Model-View-Controller, Layers optimized through business logic injection, and Top-Down Hierarchy in a control system." loading="lazy" width=100%/>
</a>
</div>

## Flexibility

If your product needs customization, you go for [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]]\.

If it is to survive for a decade, you need [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] to be able to swap vendors\.

If you mediate between resource or service providers and consumers, you build a [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Flexibility-1.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Flexibility-1.png" alt="Diagrams of Plugins, Hexagonal Architecture, and Microkernel." loading="lazy" width=100%/>
</a>
</div>

When your teams develop services and you want them to be [[wiki/concepts/source/analytics/indirection-in-commands-and-queries|less interdependent]], you insert an [[wiki/concepts/source/extension-metapatterns/proxy|*Anticorruption Layer*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Open Host Service*]], or [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS View*]] between them\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Flexibility-2.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Heart/Flexibility-2.png" alt="Diagrams of Anticorruption Layer, Open Host Service, and CQRS View." loading="lazy" width=100%/>
</a>
</div>

When you have built a large system and really need that thorough data analytics, consider implementing a [[wiki/concepts/source/basic-metapatterns/pipeline|*Data Mesh*]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Data%20Mesh.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Data%20Mesh.png" alt="Data Mesh builds an extra graph of services that stream and process analytical data." loading="lazy" width=100%/>
</a>
</div>

## Every domain is unique

No one\-size\-fits\-all\. Embedded projects or single\-player games don’t have databases and run in a single process\. High Frequency Trading bypasses the OS kernel to save microseconds\. *Middleware* and distributed databases care about quorum and leader election\. Huge\-scale data processing must account for [bit flips](https://en.wikipedia.org/wiki/Soft_error)\. A medical device should never crash\. Banks store their history forever for external audits\.

There is no universal architecture\. No silver bullet pattern\. Patterns are mere tools\. Know your tools and choose wisely\.

## So it goes

Software architecture lies lifeless in my hands, devoid of its magical colors, *like the dead iguana*\.

| \<\< [[wiki/concepts/source/analytics/deconstructing-patterns|Deconstructing patterns]] | ^ [[wiki/concepts/source/analytics/the-heart-of-software-architecture|The heart of software architecture]] ^ | [[wiki/concepts/source/appendices/appendices|Appendices]] \>\> |
| --- | --- | --- |
