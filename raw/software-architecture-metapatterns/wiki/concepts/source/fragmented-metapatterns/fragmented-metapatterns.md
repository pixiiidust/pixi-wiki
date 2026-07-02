---
title: "Fragmented metapatterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Fragmented metapatterns/Fragmented metapatterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Fragmented%20metapatterns/Fragmented%20metapatterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Fragmented metapatterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Fragmented metapatterns/Fragmented metapatterns.md`.

There are several [[wiki/concepts/source/introduction/system-topologies|topologies]] with no system-wide layers. Some of them incorporate two or three orthogonal domains which vary in abstractness to the extent that a service (limited to a subdomain) of one domain acts as a layer for another domain.

### [[wiki/concepts/source/fragmented-metapatterns/layered-services|Layered Services]]


![A diagram of Layered Services, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Layered%20Services.png)


[[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]] is an umbrella metapattern which highlights implementation details of [[wiki/concepts/source/basic-metapatterns/services|*Services*]], [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], or [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]].

*<ins>Includes</ins>*: Orchestrated Three-Layered Services, Choreographed Two-Layered Services, and Command Query Responsibility Segregation (CQRS).

### [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]]


![A diagram of Services with Polyglot Persistence, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Polyglot%20Persistence.png)


[[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] is about using multiple data stores which differ in roles or technologies. Each of the upper-level components may have access to any data store. Each data store is a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]].

*<ins>Includes</ins>*: specialized data stores, private and shared databases, data file, and Content Delivery Network (CDN); read-only replicas, Reporting Database, CQRS View Database, Memory Image, Query Service, search index, historical data, and Cache-Aside.

### [Backends for Frontends](<Backends for Frontends (BFF)>)


![A diagram of Services with Backends for Frontends, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Backends%20for%20Frontends.png)


[*Backends for Frontends*](<Backends for Frontends (BFF)>) feature a service (*BFF*) for each kind of the system’s client. A *BFF* may be a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], or both. Each *BFF* communicates with all the components below it. The pattern looks like multiple *Proxies* or *Orchestrators* deployed in parallel.

*<ins>Includes</ins>*: Layered Microservice Architecture.

### [Service-Oriented Architecture](<Service-Oriented Architecture (SOA)>)


![A diagram of Service-Oriented Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Service-Oriented%20Architecture.png)


[*SOA*](<Service-Oriented Architecture (SOA)>) comprises three or four layers of services, with each layer making a domain. The upper layer contains [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]] which are often client-specific, just like [*BFF*](<Backends for Frontends (BFF)>)*s*. The second layer incorporates business rules and is divided into business subdomains. The lower layer(s) are libraries and utilities, grouped by functionality and technologies. Any component may use (orchestrate) anything below it.

*<ins>Includes</ins>*: distributed monolith, enterprise SOA, and Domain-Oriented Microservice Architecture (DOMA).

### [[wiki/concepts/source/fragmented-metapatterns/hierarchy|Hierarchy]]


![A diagram of Hierarchy, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Hierarchy.png)


Some domains allow for [[wiki/concepts/source/fragmented-metapatterns/hierarchy|hierarchical composition]] where the functionality is spread over a tree of components.

*<ins>Includes</ins>*: Orchestrator of Orchestrators, Presentation-Abstraction-Control (PAC) and Hierarchical Model-View-Controller (HMVC), Bus of Buses, and the WSO2 version of Cell-Based (Microservice) Architecture (Services of Services).
