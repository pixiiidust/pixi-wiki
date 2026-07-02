---
title: "Layered Services"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Fragmented metapatterns/Layered Services.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Fragmented%20metapatterns/Layered%20Services
source_license_note: "See namespace README; preserve attribution and source links."
---

# Layered Services

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Fragmented metapatterns/Layered Services.md`.


![A diagram for Layered Services, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Layered%20Services.png)


*Cut the cake\.* Divide each service into layers\.

<ins>Structure:</ins> Subdomain services divided into layers\.

<ins>Type:</ins> Implementation of [[wiki/concepts/source/basic-metapatterns/services|*Services*]], [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], or [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]]\.

*Layered Services* is an umbrella architecture for common implementations of systems of [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\. It does not introduce any special features as the layers are completely encapsulated by the service which they belong to\. Still, as the services may communicate at different layers, there are a couple of things to learn by exploring the subject matter\.

### Performance

*Layered Services* are similar to [[wiki/concepts/source/basic-metapatterns/services|*Services*]] performance\-wise: use cases that involve a single service are the fastest, those that need to synchronize states of multiple services are the slowest\.

Remarkable features of *Layered Services* include:

- Independent scaling of the layers inside the services\. It is common to have multiple [[wiki/concepts/source/basic-metapatterns/shards|instances]] \(with the number varying from service to service and changing dynamically under load\) of the layers that contain business logic while the corresponding [[wiki/concepts/source/basic-metapatterns/layers|data layers]] \(databases\) are limited to a single instance\.



![The use of scaled stateless services and load balancers in Layered Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Layered%20Services%20-%20sharding.png)


- The option to establish additional communication channels between the lower layers in order to drive [*CQRS*](#command-query-responsibility-segregation-cqrs) databases \([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|read/write replicas]] of the same database\) or [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS Views*]] \(cached subsets of data from other services\) \[[wiki/concepts/source/appendices/books-referenced|[MP]]\]\.



![Data streams in Three-Layered Services: from data layer to data layer, from domain layer to data layer, and between two domain-level components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Layered%20Services%20-%20channels.png)


## Variants

*Layered Services* vary in the number of [[wiki/concepts/source/basic-metapatterns/layers|layers]] and in the layer through which the [[wiki/concepts/source/basic-metapatterns/services|services]] communicate:

- In [*Orchestrated Three\-Layered Services*](#orchestrated-three-layered-services) the application layer of any service may call the same layer in other services\.
- In [*Choreographed Two\-Layered Services*](#choreographed-two-layered-services) the domain layers of services are assembled into a *Pipeline*\.
- [*Command Query Responsibility Segregation*](#command-query-responsibility-segregation-cqrs) streams changes from a transactional to an analytical database\.


## Orchestrated Three\-Layered Services


![In three-layered services the application layer of every service calls the domain layer of its service and the application layers of other services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Three-Layered%20Services.png)


Likely the most common backend architecture has [[wiki/concepts/source/basic-metapatterns/layers|three layers]]: [[wiki/concepts/source/basic-metapatterns/layers|*application*]], [[wiki/concepts/source/basic-metapatterns/layers|*domain*]], and *infrastructure* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\. The application layer [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrates*]] the domain layer\.

If such an architecture is divided into [[wiki/concepts/source/basic-metapatterns/services|services]], each of them receives a part of every layer, including application, which means that now there are as many *Orchestrators* as services\. Each *Orchestrator* implements the API of its service by integrating \(calling or messaging into\) the domain layer of its service and the APIs of other services, which makes all the *Orchestrators* interdependent:

### Dependencies

The upper \([[wiki/concepts/source/basic-metapatterns/layers|*application*]]\) layer of each service orchestrates both its middle \(*domain*\) layer and the upper layers of other services, resulting in [[wiki/concepts/source/foundations-of-software-architecture/orchestration|mutual orchestration and interdependencies]]\.


![In Layered Services only the application layers of the services are interdependent.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Mutual%20Orchestration%20-%204.png)


The good thing is that the majority of the code belongs to the domain layer which depends only on its service’s database\. The bad thing is that changes in the application of one service may affect the application layers of all of the other services\.

### Relations

*Three\-layered services*:

- Implement [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- Are derived from [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- Have multiple [[wiki/concepts/source/extension-metapatterns/orchestrator|*Integration \(sub\)Services*]] \([[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]]\)\.


### Evolutions

*Orchestrated Layered Services* may become coupled, which is resolved either by merging their layers:

- A part of or the whole [[wiki/concepts/source/basic-metapatterns/layers|*application layer*]] can be merged into a shared [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\.
- Some or all the [[wiki/concepts/source/basic-metapatterns/layers|*databases*]] can be united into a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] or shared as [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\.
- Both the *application* and *data* layers can be merged into a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]]*\.*



![Diagrams for Three-Layered Services with partially merged application layer, partially merged databases and shared databases, and a Sandwich.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Three-Layered%20Services%20-%201.png)


or by building derived datasets:

- A [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS View*]] inside a service aggregates any events from other services which its host is interested in\.
- A dedicated [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]] captures the whole system’s state by subscribing to events from all the services\.



![Diagrams for Three-Layered Services employing CQRS views and a Query Service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Three-Layered%20Services%20-%202.png)


If a service becomes too large:

- Its middle layer can be split, resulting in a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]]\.



![The domain layer of a large three-layered service is split into sub-subdomain components, resulting in a Sandwich Cell.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Three-Layered%20Services%20-%203.png)


## Choreographed Two\-Layered Services


![The domain-level components of two-layered services participate in multiple pipelines and access their service's databases.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Two-Layered%20Services.png)


If there is no [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]], there is no role for the [[wiki/concepts/source/basic-metapatterns/layers|*application* layer]]\. [[wiki/concepts/source/foundations-of-software-architecture/choreography|*Choreographed*]] systems are made up of services that implement individual steps of request processing\. The sequence of actions \(*integration logic*\) which three\-layered systems put in the [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]] now moves to the graph of *event channels* between the services\. This means that with choreography the high\-level part of the business logic \(use cases\) exists outside of the code for the system’s constituent services\.

### Dependencies

Dependencies are identical to those of a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] or [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreographed*]] [[wiki/concepts/source/basic-metapatterns/services|*Services*]] except that each service also depends on its database\.

### Relations

*Two\-layered services*:

- Implement [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.
- Are derived from [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.


### Evolutions

If *Choreographed Layered Services* become coupled:

- The *business logic* of two or more services can be merged together, resulting in [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\.
- Some databases can be united into a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] or shared as [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\.



![Diagrams for Two-Layered Services with partially merged domain layer, partially merged databases, and shared databases.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Two-Layered%20Services%20-%201.png)


[[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS Views*]] or a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]] are also an option:


![Diagrams for Two-Layered Services employing CQRS views and a Query Service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Two-Layered%20Services%20-%202.png)


An overgrown service can be:

- Split in two



![The domain layer of a large two-layered service is split in half.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Two-Layered%20Services%20-%203.png)


## [[wiki/concepts/source/extension-metapatterns/sandwich|Command Query Responsibility Segregation]] \(CQRS\)


![Write requests from a client go to the write backend and OLTP database which feeds OLAP databases. Read requests go to the scaled read backend and the scaled OLAP database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/CQRS.png)


*Command Query Responsibility Segregation* \(*CQRS*\) \[[wiki/concepts/source/appendices/books-referenced|[MP]], [[wiki/concepts/source/appendices/books-referenced|LDDD]]\] is, essentially, the division of a [[wiki/concepts/source/basic-metapatterns/layers|layered]] application or a service into two \(rarely more\) [[wiki/concepts/source/basic-metapatterns/services|services]], one of which is responsible for write access \(handling *commands*\) to the domain data while the other\(s\) deal with read access \(*queries*\), thus [[wiki/concepts/source/analytics/pipelines-in-architectural-patterns|creating]] a data [[wiki/concepts/source/basic-metapatterns/pipeline|*pipeline*]] \(see the diagram below\)\. Such an architecture makes sense when the write and read operations don’t rely on a common vision \(*model*\) of the domain, for example, writes are individual changes \([*OLTP*](https://en.wikipedia.org/wiki/Online_transaction_processing)\) that require cross\-checks and validation of input while reads show aggregated data \([*OLAP*](https://en.wikipedia.org/wiki/Online_analytical_processing)\) and may take long time to complete \(meaning that the [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|*forces*]] for the read and write paths differ\)\. If there is nothing to share in the code, why not separate the implementations?


![In CQRS data streams from the client to the write backend, then to the OLTP database, to the OLAP database, to the read backend and, finally, returns to the client.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/CQRS%20-%20pipeline%20view.png)


This separation brings in the pros and cons of [[wiki/concepts/source/basic-metapatterns/services|*Services*]]: commands and queries may differ in technologies \(including schemas or even kinds of the databases\) and forces, and even be developed by separate teams, at the expense of [consistency](https://en.wikipedia.org/wiki/Eventual_consistency) \(database replication delay\) and increasing the system’s complexity\. In addition, for read\-heavy applications the read database\(s\) is easy to scale\.

*CQRS* has the following variations:

- The database may be shared, commands and queries may use dedicated databases, or the read service may maintain a [*Memory Image*](https://martinfowler.com/bliki/MemoryImage.html) / [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Materialized View*]] fed by events from the write service \(as in other kinds of *Layered Services*\)\.
- Data [[wiki/concepts/source/basic-metapatterns/shards|replication]] may be implemented as a [[wiki/concepts/source/basic-metapatterns/pipeline|*pipeline*]] between the databases \(based on nightly snapshots or [log\-based replication](https://www.dremio.com/wiki/log-based-replication/)\) or a [direct event feed](https://martinfowler.com/bliki/EagerReadDerivation.html) from the OLTP code to the OLAP database\.



![In CQRS the OLAP databases receive data from the OLTP database or from events originating in the write backend. Alternatively, the read and write backends may share a database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/CQRS%20-%20subtypes.png)


It is noteworthy that while ordinary *Layered Services* usually communicate through their upper\-level components that drive the use cases, a *CQRS* system is held together by spreading data changes through its lowest layer\.

Examples: Martin Fowler has a [short article](https://martinfowler.com/bliki/CQRS.html) and Microsoft a [longer one](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)\.

### Dependencies

Each backend depends on its database \(its technology and schema\)\. The OLTP to OLAP data replication requires an additional dependency that comes from the way the replication is implemented:


![In CQRS each service depends on its database while the OLAP database depends on the source of its event feed.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/CQRS.png)


### Relations

*CQRS*:

- Implements [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] \(a whole *system* or a single [[wiki/concepts/source/basic-metapatterns/services|*service*]]\)\.
- Is derived from both [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.
- Is a development of [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\.


### Evolutions

- You will usually need a [[wiki/concepts/source/extension-metapatterns/proxy|*Reverse Proxy*]] or an [[wiki/concepts/source/extension-metapatterns/proxy|*API Gateway*]] to segregate commands from queries\.
- If the commands and queries become intermixed, the business logic can be merged together but the databases are left separate, resulting in [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\.
- Both read and write backends can be split into [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] or [[wiki/concepts/source/basic-metapatterns/services|*Services*]] \(yielding [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]]\)\.
- Applying [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]] may further improve performance\.
- Multiple schemas or even kinds of OLAP databases can be used simultaneously \([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\)\.



![Diagrams of CQRS behind an API Gateway, with a single backend, with multiple OLAP databases, with layered backends, Cells for backends, and Data Grid for a database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/CQRS.png)


## Summary

*Layered Services* is an umbrella pattern that conjoins:

- *Three\-Layered Services* where each service [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrates*]] other services\.
- *Two\-Layered Services* that form a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.
- *CQRS* that separates the read and write request processing paths\.


| \<\< [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Fragmented metapatterns]] | ^ [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Fragmented metapatterns]] ^ | [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]] \>\> |
| --- | --- | --- |
