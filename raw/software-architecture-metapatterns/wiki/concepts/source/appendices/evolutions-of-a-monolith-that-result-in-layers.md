---
title: "Evolutions of a Monolith that result in Layers"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Monolith that result in Layers.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Monolith%20that%20result%20in%20Layers
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Monolith that result in Layers

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Monolith that result in Layers.md`.

Another drawback of [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] is its … er … monolithism\. The entire application exposes a single set of qualities and all its parts \(if they ever emerge\) are deployed together\. However, life awards flexibility: parts of a system may benefit from being written in varying languages and styles, and deployed with different frequency and amount of testing, sometimes to specific hardware or end users’ devices\. They may need to [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|vary in security and scalability]] as well\. Enter [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] – the subdivision by the *level of abstractness*:

- Most *Monoliths* can be divided into three or four [[wiki/concepts/source/basic-metapatterns/layers|*layers*]]\.
- It is common to see the database separated from the main application\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] \(e\.g\. [[wiki/concepts/source/extension-metapatterns/proxy|*Firewall*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Cache*]], and [[wiki/concepts/source/extension-metapatterns/proxy|*Reverse Proxy*]]\) are common additions to the system\.
- An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] adds a layer of indirection to simplify the system’s API for its clients\.


## Divide into Layers


![A monolith is split into application, domain and database layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Layers.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: let parts of the system vary in qualities, improve the structure of the code\.

<ins>Prerequisite</ins>: there is a natural way to separate the high\-level logic from the low level implementation details and dependencies\.

Most systems apply *layering* by default as it grants a lot of flexibility at very little cost\. [[wiki/concepts/source/basic-metapatterns/layers|Common sets of layers]] are: [[wiki/concepts/source/basic-metapatterns/layers|UI]], [[wiki/concepts/source/basic-metapatterns/layers|tasks]] \(orchestration\), [[wiki/concepts/source/basic-metapatterns/layers|domain]] \(detailed business rules\) and infrastructure \(database and libraries\) or [[wiki/concepts/source/basic-metapatterns/layers|frontend, backend and data]]\.

<ins>Pros</ins>:

- It is a natural way to specialize and decouple two or three development teams\.
- The layers may vary in virtually any quality:
  - They are deployed and scaled independently\.
  - They may run on different hardware, including client devices\.
  - They may vary in programming language, paradigm, and release cycle\.
- Most changes are isolated to a single layer\.
- Layering opens a way to many evolutions of the system\.
- The code [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|becomes easier to read]]\.


<ins>Cons</ins>:

- Dividing an existing application into *Layers* may take some effort\.
- There is a small performance penalty\.


## Use a database


![The data of a monolithic system is moved to a database, leaving the business logic stateless.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20add%20Database.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]], [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Database]] \([[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]\)\.

<ins>Goal</ins>: avoid implementing a database\.

<ins>Prerequisite</ins>: the system needs to query \(and maybe also edit\) a large amount of data\.

A database is non\-trivial to implement\. While ordinary files are good for small volumes of data, as your needs grow so needs to grow your technology\. Deploy a database\.

<ins>Pros</ins>:

- A well\-known database is sure to be more reliable than any in\-house implementation\.
- Many databases provide heavily optimized algorithms for querying data\.
- You can choose specific hardware to deploy the database to\.
- Your \(now stateless\) application will be easy to scale\.


<ins>Cons</ins>:

- Databases are complex and require fine\-tuning\.
- You cannot adapt the database engine to your evolving needs\.
- Most databases do not scale\.
- You are stepping right into [vendor lock\-in](https://en.wikipedia.org/wiki/Vendor_lock-in)\.


<ins>Further steps</ins>:

- Deploy multiple [[wiki/concepts/source/basic-metapatterns/shards|*instances*]] of your application behind a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]]\.
- Continue the transition to [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] by separating the high\-level and low\-level business logic\.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] improves performance of the data layer\.
- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]] handles read and write requests in separate services\.
- [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]] has low latency and allows for dynamic scalability of the whole system, including the data layer\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] will allow you to switch to another database in the future\.


## Add a Proxy


![A part of generic functionality of a monolith is moved to a proxy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20add%20Proxy.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]], [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]\.

<ins>Goal</ins>: avoid implementing generic functionality\.

<ins>Prerequisite</ins>: Your system serves clients \(as opposed to [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|controlling hardware]]\)\.

A *Proxy* is placed between your system and its clients to provide generic functionality that otherwise would have to be implemented by the system\. The kinds of *Proxy* to use with [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] are: [[wiki/concepts/source/extension-metapatterns/proxy|*Firewall*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Cache*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Reverse Proxy*]], and [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]]\. Multiple *Proxies* can be deployed\.

<ins>Pros</ins>:

- You save some time \(and money\) on development\.
- A well\-known *Proxy* is likely to be more secure and reliable than an in\-house implementation\.
- You can choose the hardware to deploy the *Proxy* to\.


<ins>Cons</ins>:

- Latency degrades, except for [[wiki/concepts/source/extension-metapatterns/proxy|*Response Cache*]] where it depends on frequency of identical requests\.
- The *Proxy* may fail, which increases the chance of total failure of your system\.
- Beware of [vendor lock\-in](https://en.wikipedia.org/wiki/Vendor_lock-in)\.


<ins>Further steps</ins>:

- Another kind of *Proxy* may be added\.
- Some systems employ a *Proxy* per client, leading to [*Backends for Frontends*](<Backends for Frontends (BFF)>)\.


## Add an Orchestrator


![An orchestrator is added to a monolithic system, allowing for higher-level client requests.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20add%20Orchestrator.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]], [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]\.

<ins>Goal</ins>: provide a high\-level public API with improved developer experience and performance\.

<ins>Prerequisite</ins>: the API of your system is fine\-grained and there are common [[wiki/concepts/source/basic-metapatterns/layers|use cases]] which repeat certain sequences of calls to your API\.

A well\-designed *Orchestrator* should provide a high\-level API which is intuitive, easy to use, and coarse\-grained to minimize the number of interactions between the system and its clients\. An old way to access the original system’s API may still be maintained for uncommon use cases or legacy client applications \([[wiki/concepts/source/extension-metapatterns/orchestrator|*open* orchestration]]\)\. As a matter of fact, you program the common application logic on behalf of your clients\.

<ins>Pros</ins>:

- Client applications become easier to write\.
- Latency improves\.


<ins>Cons</ins>:

- You get yet another moving part to design, test, deploy, and observe; and lots of design meetings between the development teams for a bonus\.
- The new coarse\-grained interface will likely be less powerful than the original one\.


<ins>Further steps</ins>:

- [*Backends for Frontends*](<Backends for Frontends (BFF)>) use an *Orchestrator* per client type\.


## Further steps

Applying one of the evolutions discussed above does not prevent you from following another one of them, or even the same one for a second time:

- A layer can sometimes be split into two layers\.
- A database can be added\.
- Multiple kinds of *Proxies* are OK\.
- If you don’t have an *orchestration layer* yet, you may add one\.


Those were evolutions from *Layers* to [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]\.

Another set of evolutions stems from splitting one or more *layers* into [[wiki/concepts/source/basic-metapatterns/services|*Services*]]:

- Splitting a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] and/or [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] yields [*Backends for Frontends*](<Backends for Frontends (BFF)>) where requests from each kind of client are processed by a dedicated component\.
- Splitting the layer with the main business logic results in [[wiki/concepts/source/basic-metapatterns/services|*Services*]], possibly augmented with layers of [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]], [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] and/or [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\. If all the other layers beside the business logic layer remain monolithic, it is a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]]\.
- Splitting the [[wiki/concepts/source/basic-metapatterns/layers|*database layer*]] leads to [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] with specialized storages\.
- If all the layers share the domain dimension and are split along it, [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]] \(or its subtype [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]]\) emerge\.
- If each layer is split along its own domain, the system follows [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) that is built around component reuse\.
- Finally, some domains support [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] – a tree\-like architecture where each layer takes a share of the system’s functionality\.



![Diagrams of Backends for Frontends over Layers, Service-Oriented Architecture, Sandwich, Layered Services, Hierarchy, and Layers with Polyglot Persistence.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Layers%20-%20Further%201.png)


In addition,

- Distributed systems usually allow for the [[wiki/concepts/source/basic-metapatterns/shards|scaling]] of one or more layers\.
- A layer may employ [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] for better customizability\.
- The UI and infrastructure layers may be split and abstracted according to the rules of [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] \(or its subtype [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Separated Presentation*]]\)\.
- The system can often be extended with [[wiki/concepts/source/implementation-metapatterns/microkernel|*Scripts*]], resulting in a kind of [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]]\.



![Diagrams of Layers with plugins, Layers with scripts, and Hexagonal Architecture with a layered core.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Layers%20-%20Further%202.png)


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-lead-to-shards|Evolutions of a Monolith that lead to Shards]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-make-services|Evolutions of a Monolith that make Services]] \>\> |
| --- | --- | --- |
