---
title: "Service Oriented Architecture (SOA)"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Fragmented metapatterns/Service-Oriented Architecture (SOA).md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Fragmented%20metapatterns/Service-Oriented%20Architecture%20%28SOA%29
source_license_note: "See namespace README; preserve attribution and source links."
---

# Service Oriented Architecture (SOA)

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Fragmented metapatterns/Service-Oriented Architecture (SOA).md`.


![A diagram for Service-Oriented Architecture, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Service-Oriented%20Architecture.png)


*The whole is equal to the sum of the parts.* Distributed [Object-Oriented Design](https://en.wikipedia.org/wiki/Object-oriented_design).

<ins>Known as:</ins> Service-Oriented Architecture (SOA), [Segmented Architecture](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-layered-segmented.md).

<ins>Structure:</ins> Usually three layers of services where each service can access any other service in its own or lower layers.

<ins>Type:</ins> System topology, derived from [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]].

| *Benefits* | *Drawbacks* |
| --- | --- |
| Supports huge codebases | Very hard to debug |
| Multiple development teams and technologies | Hard to test as there are many dependencies |
| Forces may vary between the components | Very poor latency |
| Deployment to dedicated hardware | Very high DevOps complexity |
| Fine-grained scaling | The teams are highly interdependent |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] has a chapter on Orchestration-Driven (Enterprise) Service-Oriented Architecture. \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] mentions Distributed Monolith. There is also much (though somewhat conflicting) content over the Web.

*Service-Oriented Architecture* looks like the [application of modular or object-oriented design](https://www.uber.com/en-UA/blog/microservice-architecture/) followed by distribution of the resulting components over a network. The system usually contains three (rarely four) [[wiki/concepts/source/basic-metapatterns/layers|*layers*]] of [[wiki/concepts/source/basic-metapatterns/services|*services*]] where every service has access to all the services below it (and sometimes some within its own layer). The services stay small, but as their number grows it becomes hard for programmers to keep in mind all the API methods and contracts available for use by their component. Another issue originates from the idea of reusable components – multiple applications, written for different clients with varied workflows, require the same service to behave in (subtly) different ways, either causing its API to bloat or else impairing its usability (which means that a new customized duplicate service will likely be added to the system). On top of that, request processing is slow because there is much interservice communication. Teams are interdependent as any use case involves many services, each owned by a dedicated team. Testability is poor because there are too many moving (and being independently updated!) parts. The OOP’s foundational idea of reuse [failed in practice](https://softwareengineering.stackexchange.com/questions/7618/does-oop-fulfill-the-promise-of-code-reuse-what-alternatives-are-there-to-achie), but its child architecture, namely *SOA*, still survives in historical environments.

Even though *SOA* fell from grace and is rarely seen in modern projects, it may soon be resurrected by low-code and no-code frameworks for serverless systems (e.g. [[wiki/concepts/source/basic-metapatterns/services|*Nanoservices*]]) – it has everything ready: code reuse, granular deployment, and elastic scaling.

### Performance

*SOA* is remarkable for its poor latency which results from extensive communication between its distributed components. There is hardly any way to help that as processing a request usually involves many services from all the layers.

Nevertheless, this pattern allows for good throughput as its stateless components can be scaled individually, leaving the system’s scalability to be limited only by its databases, [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] … and funding.

### Dependencies

Each service of each layer depends on everything it uses. As a result, development of a low-level (utility) component may be paralyzed because too many services already use it, thus no changes are welcome. Hence, the team writes a new version of their utility as a new service, which defeats the very idea of component reuse which *SOA* was based on.


![Tasks depend on entities. Entities depend on utilities and libraries. The many dependencies make it hard to change almost any component.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Service-Oriented%20Architecture.png)


### Applicability

*Service-Oriented Architecture* <ins>is useful</ins> in:

- *Huge projects.* Many teams can be employed, each handling a moderate amount of code. Yet, dependencies between the teams and the combined length of the APIs in the system may [stall the development](https://goomics.net/374) anyway.
- *A system of specialized hardware devices.* If there is a lot of different hardware interacting in complex ways, the system may naturally fit the description of *SOA*. Don’t fight this kind of [Conway’s law](https://en.wikipedia.org/wiki/Conway%27s_law).


*Service-Oriented Architecture* <ins>hurts</ins>:

- *Fast-paced projects.* Any feature requires coordination of multiple teams, which is hard to achieve in practice.
- *Latency-sensitive domains*. Over-distribution means too much messaging which causes too high latency.
- *High availability systems*. Components may fail. The failure of a lower-level component is going to stall a large part of the system because every low-level component is used by many higher-level services.
- *Safety-critical systems with frequent updates*. *SOA* is hard to test comprehensively. Either all the components must be certified with a strict standard and an exhaustive test suite or any single component update requires re-testing the entire system.


### Relations

*Service-Oriented Architecture*:

- Is a stack of [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] each of which is divided into [[wiki/concepts/source/basic-metapatterns/services|*Services*]].
- Is often extended with an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Enterprise Service Bus*]] (a kind of [[wiki/concepts/source/extension-metapatterns/orchestrator|*orchestrating*]] [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]) and one or more [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Databases*]].


## Examples

This architecture was hyped at the time when enterprises were expanding by acquiring smaller companies and conjoining their IT systems. The resulting merged systems were still heterogeneous and the development experience unpleasant, which inclined popular opinion towards the then novel notion of [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]]. As nearly everybody has turned from merging existing systems to failing to apply *Microservices* in practice, the chance to find a pure greenfield *SOA* project in the wild is quite low. Known examples of this topology include:

- [*Distributed Monolith*](#distributed-monolith) with synchronous interactions.
- [*Enterprise SOA*](#enterprise-soa) that features a notorious *Enterprise Service Bus*.
- [*Domain-Oriented Microservice Architecture*](#domain-oriented-microservice-architecture-doma) built of *Cells*.
- [*Automotive SOA*](#misapplied-automotive-soa) which may actually be a *Microkernel*.
- *SOA*-topology [*Nanoservices*](#nanoservices).


### Distributed Monolith


![There are three segmented layers: tasks, services and infrastructure. Each component of a layer accesses multiple components in layers below it.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Distributed%20Monolith.png)


If a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] gets too complex and resource-hungry, the most simple & stupid way out of the trouble is to deploy each of its component modules to a separate, dedicated hardware. The resulting services still communicate synchronously and are subject to domino effect on failure. Such an architecture may be seen as a (hopefully) intermediate [[wiki/concepts/source/introduction/system-topologies|topology]] in transition to more independent and stable event-driven [[wiki/concepts/source/basic-metapatterns/services|*Services*]] (or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]]).

### Enterprise SOA


![An Enterprise Service Bus interconnects multilayered segmented subsystems each using its own protocol.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Enterprise%20SOA.png)


Multiple systems of [[wiki/concepts/source/basic-metapatterns/services|*Services*]], each featuring an [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]] and sometimes a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]], are integrated, resulting in new cross-connections. Much of the orchestration logic is removed from the *API Gateways* and reimplemented in an [[wiki/concepts/source/extension-metapatterns/orchestrator|*orchestrating*]] [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] called [[wiki/concepts/source/extension-metapatterns/orchestrator|*Enterprise Service Bus*]] (*ESB*). This option allows for fast and only moderately intrusive integration (as no changes to the services, which implement the mass of the domain logic, are required), but the single [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestrating]] component (*ESB*) often becomes the bottleneck for future development of the system due to its size and complexity. It is likely that if the orchestration were encapsulated in the individual *API Gateways*, the system would be easier to deal with (making what is now [marketed by WSO2](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) as [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell-Based Architecture*]]).

The layers of *SOA* are:

- *Business Process* (*Task*) – the definitions of [[wiki/concepts/source/basic-metapatterns/layers|use cases]] for a single business department, similar to the *API Gateways* layer of [*BFF*](<Backends for Frontends (BFF)>).
- *Services* (*Enterprise*, *Entity*) – the implementation of the [[wiki/concepts/source/basic-metapatterns/layers|business logic of a subdomain]], to be used by the *tasks*.
- *Components* (*Application* & *Infrastructure*, *Utility*) – external libraries and in-house utilities that are designed for shared use by the *services* layer.


### Domain-Oriented Microservice Architecture (DOMA)


![There are five layers: segmented gateways, segmented presentation, segmented product made of cells, segmented business made of cells, and monolithic infrastructure.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/DOMA.png)


A huge business may build a *SOA* of [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]] (called *Domains*) instead of plain [[wiki/concepts/source/basic-metapatterns/services|*Services*]]. That greatly simplifies:

- administration (by reducing the number of components at the system level – Uber [packed](https://www.uber.com/blog/microservice-architecture/) 2200 [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] into 70 *Domains*),
- refactoring of individual subsystems (which are isolated behind [[wiki/concepts/source/extension-metapatterns/proxy|*Cell Gateways*]]),
- development of business logic (as programmers need to learn much fewer interfaces of components they rely on).


Uber’s *DOMA* also [makes heavy use](https://www.uber.com/blog/microservice-architecture/) of [[wiki/concepts/source/implementation-metapatterns/plugins|*Ambassador Plugins*]] which programmers from a client service team develop for the services which they rely on. That allows for cross-*Domain* customization (injection of business logic from another *Cell*) of a service’s behavior without making slow and possibly failing interservice calls.

### (misapplied) [[wiki/concepts/source/implementation-metapatterns/microkernel|Automotive SOA]]


![User applications run on top of a system-wide Virtual Functional Bus which communicates to various services that run on different chips in the system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/SOA%20-%20AUTOSAR.png)


*Automotive* architectures were inspired by *SOA*, but the old [[wiki/concepts/source/implementation-metapatterns/microkernel|*AUTOSAR Classic*]] looks more like [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] (which indeed is similar to a 2-layered *SOA* with an [[wiki/concepts/source/extension-metapatterns/orchestrator|*ESB*]]) while the newer system diagrams resemble a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]. Therefore, they are addressed in the corresponding chapters.

### Nanoservices

It seems that some proponents of [[wiki/concepts/source/basic-metapatterns/services|*Nanoservices*]] [take them](https://medium.com/@ido.vapner/unlocking-the-power-of-nano-services-a-new-era-in-microservices-architecture-22647ea36f22) for a novel version of *SOA* – with the old good promise of reusable components. However, as that promise was failing miserably ever since the ancient days of OOP, it is of no surprise that [in practice](https://increment.com/software-architecture/the-rise-of-nanoservices/) *Nanoservices* are used instead to build [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]] with little to no reuse.

## Evolutions

*SOA* suffers from excessive reuse and fragmentation. To fix that, first and foremost, each service of the *components* ([[wiki/concepts/source/basic-metapatterns/layers|*utility*]]) layer should be duplicated:

- Into every *service* that uses it, giving the developers who write the business logic full control over all the code which they use. Now they have several projects to support on their own (instead of asking other teams to make changes to their components).



![The shared components are replicated into services which use them.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/SOA%20-%201.png)


- Or into [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]] if you employ a [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]], resulting in much fewer network hops (thus lower latency) in request processing, but retaining the inter-team dependencies.



![The shared components are replicated into sidecars.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/SOA%20-%202.png)


That removes the largest and most obvious part of the fragmentation, making the [[wiki/concepts/source/extension-metapatterns/orchestrator|*ESB*]] (if you use one) [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrate*]] only the *entity* layer.

Afterwards you may deal with the remaining orchestration. The idea is to move the orchestration logic from the *ESB* to an explicit *layer* of [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]]:

- Either a monolithic *Orchestrator* over all the services.
- Or [*Backends for Frontends*](<Backends for Frontends (BFF)>) with an *Orchestrator* per client type (department of an enterprise) if each client uses most of the services.
- Or go for [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]] with an *Orchestrator* per subdomain if your clients are subdomain-bound.
- Or a combination of the above.



![Diagrams for Services with an orchestrator, Backends for Frontends, and Cell-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/SOA%20-%203.png)


Still another step is unbundling the [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]], which supports multiple protocols via [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]]:

- If you have a [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]], the *Adapters* may be added to [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]].
- Otherwise there is an option of a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*hierarchical Middleware*]] (*Bus of Buses*) if closely interacting components share protocols.


Still, these evolutions of [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] may not bring any real benefit except for removing the [[wiki/concepts/source/extension-metapatterns/orchestrator|*ESB*]] altogether, which may not be that bad after all when it is not misused.

In any case, many of the evolutions will likely be very expensive, thus it makes sense to conduct some of them gradually via a kind of [strangler fig approach](https://martinfowler.com/bliki/StranglerFigApplication.html). Or let the architecture live and die as it is.

## Summary

*Service-Oriented Architecture* divides each of the *integration*, *domain*, and *utility* layers into shared services. The extensive fragmentation and reuse degrade performance and speed of development. Nevertheless, huge projects are known to survive with this architecture.
