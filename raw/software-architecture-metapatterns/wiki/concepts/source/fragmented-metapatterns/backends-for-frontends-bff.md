---
title: "Backends for Frontends (BFF)"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Fragmented metapatterns/Backends for Frontends (BFF).md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Fragmented%20metapatterns/Backends%20for%20Frontends%20%28BFF%29
source_license_note: "See namespace README; preserve attribution and source links."
---

# Backends for Frontends (BFF)

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Fragmented metapatterns/Backends for Frontends (BFF).md`.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Backends%20for%20Frontends.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Backends%20for%20Frontends.png" alt="A diagram for Services with Backends for Frontends, in abstractness-subdomain-sharding coordinates." loading="lazy" width=100%/>
</a>
</div>

*Hire a local guide\.* Dedicate a service for every kind of client\.

<ins>Known as:</ins> Backends for Frontends \(BFF\), [Layered Microservice Architecture](https://github.com/wso2/reference-architecture/blob/master/api-driven-microservice-architecture.md)\.

<ins>Structure:</ins> A layer of integration services over a shared layer of core services\.

<ins>Type:</ins> Extension component, derived from [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and/or [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]]\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Clients become independent in their protocols, workflows and, to an extent, qualities | No single place for cross\-cutting concerns |
| A specialized team and technology per client may be employed | More work for the DevOps team |
| The multiple *Orchestrators* are smaller and more cohesive than a universal one would be |  |

<ins>References:</ins> The [original article](https://samnewman.io/patterns/architectural/bff/), a [smaller one](https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends) from Microsoft, and an [excerpt](https://microservices.io/patterns/apigateway.html) from \[[wiki/concepts/source/appendices/books-referenced|[MP]]\]\. Here are the [reference diagrams](https://github.com/wso2/reference-architecture/blob/master/api-driven-microservice-architecture.md) from WSO2 \(notice multiple *Microgateway* \+ *Integration Microservice* pairs\)\.

If some aspect\(s\) of serving our system’s clients strongly vary by client type \(e\.g\. OLAP vs OLTP requests, user vs admin privileges, buyer vs seller vs customer support roles\), it makes sense to use a dedicated component \(the titular *Backend for Frontend* or *BFF*\) per client type to encapsulate that variation\. Protocol variations call for multiple [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]], workflow variations – for several [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]], both coming together – for [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateways*]] or *Proxy \+ Orchestrator* pairs\. It is even possible to vary the *BFF*’s programming language on a per client basis\. The drawback is that once the clients get their dedicated *BFFs* it becomes hard to share a common functionality between them, unless you are willing to add yet another new utility [[wiki/concepts/source/basic-metapatterns/services|*service*]] \(that will strongly smell of [*SOA*](<Service-Oriented Architecture (SOA)>)\) or a [[wiki/concepts/source/basic-metapatterns/layers|*layer*]] that can be used by each of them\.

### Performance

As the multiple *Orchestrators* of *BFF* don’t intercommunicate, the pattern’s performance is identical to that of an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]: it also slows down request processing in the general case but allows for several [[wiki/concepts/source/extension-metapatterns/orchestrator|specific optimizations]], including direct communication channels between the orchestrated [[wiki/concepts/source/basic-metapatterns/services|services]]\.

### Dependencies

Each *BFF* depends on all the services which it uses \(usually every service in the system\)\. The services themselves are likely to be independent, as is common in [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrated* systems]]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Dependencies/Backends%20for%20Frontends.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Dependencies/Backends%20for%20Frontends.png" alt="Each Backend for Frontend depends on every service which it calls." loading="lazy" width=91%/>
</a>
</div>

### Applicability

*Backends for Frontends* are <ins>good</ins> for:

- *Multiple client protocols\.* Deploying a [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] per protocol hides the variation from the underlying system\.
- *Multiple UIs\.* When you have one team per UI, each of them may [want to have](https://netflixtechblog.com/embracing-the-differences-inside-the-netflix-api-redesign-15fd8b3dc49d) an API which they feel comfortable with\.
- *Drastically different workflows\.* Let each client\-facing development team own a component and choose the best fitting technologies and practices\.


*Backends for Frontends* <ins>should be avoided</ins> when:

- *The clients are mostly similar\.* It is hard to share code and functionality between *BFF*s\. If the clients have much in common, the shared aspects either find their place in a shared monolithic layer \(e\.g\. multiple client protocols call for multiple [[wiki/concepts/source/extension-metapatterns/proxy|*Gateways*]] but a shared [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\) or are duplicated\. *BFF* may not be the best choice – use OOD \(conditions, factories, strategies, and inheritance\) instead to handle the clients’ differences within a single codebase\.


### Relations

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/BFF.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/BFF.png" alt="Diagrams of Backends for Frontends over a monolith, layers, shards, and services." loading="lazy" width=100%/>
</a>
</div>

*Backends for Frontends*:

- Extends [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or rarely [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], or [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]]\.
- Is derived from a client\-facing extension pattern: [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]], or [[wiki/concepts/source/extension-metapatterns/orchestrator|*Event Mediator*]]\.


## Variants

*Backends for Frontends* vary according to the kind of component that gets dedicated to each client:

- A [*Proxy*](#proxies) per client when clients differ in protocols\.
- An [*Orchestrator*](#orchestrators) or [*Event Mediator*](#event-mediators) per client for different client roles and use cases\.
- A [*Proxy \+ Orchestrator* pair](#proxy--orchestrator-pairs) or an [*API Gateway*](#api-gateways) when clients differ in both protocols and roles\.


### [[wiki/concepts/source/extension-metapatterns/proxy|Proxies]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Gateways.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Gateways.png" alt="Each gateway in the Backends for Frontends layer adapts its client's protocol and calls the services of the domain layer." loading="lazy" width=100%/>
</a>
</div>

Dedicating a [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] per client is useful when the clients differ in the mode of access to the system \(protocols / encryption / authorization\) but not in workflows\.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrators]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Orchestrators.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Orchestrators.png" alt="Each orchestrator in the Backends for Frontends layer calls the services of the domain layer." loading="lazy" width=100%/>
</a>
</div>

An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] per client makes sense if the clients use the system in completely unrelated ways, e\.g\. a shop’s customers have little to share with its administrators\.

### [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]] \+ [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]] pairs

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Gateways%20+%20Orchestrators.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Gateways%20+%20Orchestrators.png" alt="In each pair in the Backends for Frontends layer the gateway adapts its client's protocol while the orchestrator calls the services of the domain layer." loading="lazy" width=100%/>
</a>
</div>

Clients vary in both access mode \(protocol\) and workflow\. [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]] or [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] may be reused if some kinds of clients share only the protocol or [[wiki/concepts/source/basic-metapatterns/layers|*application logic*]]\.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|API Gateways]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20API%20gateways.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20API%20gateways.png" alt="Each API Gateway in the Backends for Frontends layer both adapts its client's protocol and orchestrates the services of the domain layer." loading="lazy" width=100%/>
</a>
</div>

Clients vary in access mode \(protocol\) and workflow and there is a third\-party [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]] framework which seems to fit your requirements off the shelf\.

Multiple *API Gateways* match the literal meaning of *Backends for Frontends* – each UI team \([backend, mobile, desktop](https://www.thoughtworks.com/insights/blog/bff-soundcloud); or [end\-device\-specific](https://netflixtechblog.com/embracing-the-differences-inside-the-netflix-api-redesign-15fd8b3dc49d) teams\) gets some code on the backend side to adapt the system’s API and protocols to its needs by building a new, probably higher\-level specialized API with a convenient transport\.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|Event Mediators]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Event%20mediators.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/3/BFF%20-%20Event%20mediators.png" alt="Each event mediator in the Backends for Frontends layer orchestrates the services of the domain layer." loading="lazy" width=100%/>
</a>
</div>

\[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] mentions that multiple [[wiki/concepts/source/extension-metapatterns/orchestrator|*Event Mediators*]] may be deployed in [[wiki/concepts/source/basic-metapatterns/pipeline|*Event\-Driven Architecture*]] to split the codebase and improve stability\.

## Evolutions

*BFF*\-specific evolutions aim at sharing logic between the *BFF*s:

- The *BFF*s can be merged into a single [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] if their functionality becomes mostly identical\.
- A shared *orchestration* [[wiki/concepts/source/basic-metapatterns/layers|*layer*]] with common functionality may be added for use by the *BFF*s\.
- A layer of *Integration Services* under the *BFF*s simplifies them by providing shared high\-level APIs for the resulting [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]]\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]] \(of [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]]\) are a way to share libraries among the *BFF*s\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/3/BFF.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/3/BFF.png" alt="Backends for Frontends can be merged into an Orchestrator, can share code via sidecars, or put shared functionality into a dedicated orchestration layer or into Cell gateways." loading="lazy" width=100%/>
</a>
</div>

## Summary

*Backends for Frontends* assigns a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] and/or an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] per each kind of a system’s client to encapsulate client\-specific use cases and protocols\. The drawback is that there is no good way for sharing functionality between the *BFF*s\.

| \<\< [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]] | ^ [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Fragmented metapatterns]] ^ | [Service\-Oriented Architecture \(SOA\)](<Service-Oriented Architecture (SOA)>) \>\> |
| --- | --- | --- |
