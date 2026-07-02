---
title: "Evolutions of Services that add layers"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Services that add layers.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Services%20that%20add%20layers
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Services that add layers

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Services that add layers.md`.

The most common modifications to a [[wiki/concepts/source/basic-metapatterns/services|system of *Services*]] involve supplementary system-wide *layers* which compensate for the inability of the *services* to share anything among themselves:

- A [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] knows of all the deployed service [[wiki/concepts/source/basic-metapatterns/shards|instances]]. It mediates [[wiki/concepts/source/basic-metapatterns/layers|communication]] between them and may manage their scaling and failure recovery.
- The [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]] of a [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]] make a virtual layer of [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|shared libraries]] for the [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] it hosts.
- A [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] simplifies the initial phases of development and provides data consistency and [[wiki/concepts/source/foundations-of-software-architecture/shared-data|interservice communication]].
- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] stand between the system and its clients and take care of shared aspects that otherwise would need to be implemented by every service.
- An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] is the single place for the high-level logic of every [[wiki/concepts/source/basic-metapatterns/layers|use case]].
- Transforming *Services* into a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] greatly simplifies their integration.


## Add a Middleware


![The communication aspect of services can be covered by a dedicated middleware.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20add%20Middleware.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]], [[wiki/concepts/source/basic-metapatterns/services|Services]].

<ins>Goal</ins>: take care of scaling, recovery, and interservice communication without programming it.

<ins>Prerequisite</ins>: communication between the services is uniform.

Distributed systems may fail in a zillion ways. You want to ruminate neither on that nor on [heisenbugs](https://en.wikipedia.org/wiki/Heisenbug). And you probably want to have a framework for scaling the services and restarting them after failure. Get a third-party *Middleware*! Let your programmers write the business logic, not infrastructure.

<ins>Pros</ins>:

- You don't invest your time in infrastructure.
- Scaling and error recovery are made easy.


<ins>Cons</ins>:

- There may be a performance penalty which becomes worse for uncommon patterns of communication.
- The *Middleware* may become a single point of failure.


<ins>Further steps</ins>:

- Use a [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]] for dynamic scaling and as a way to implement [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|shared aspects]].


## Use a Service Mesh


![Scaled services reside on a shared layer of sidecars which is placed on top of a shared mesh engine. All instances of each service access the service's database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Multifunctional%20-%20Service%20Mesh.png)


<ins>Patterns</ins>: [[wiki/concepts/source/implementation-metapatterns/mesh|Service Mesh]] ([[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]], [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]]), [[wiki/concepts/source/extension-metapatterns/proxy|Sidecar]] ([[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]), [[wiki/concepts/source/basic-metapatterns/services|Services]].

<ins>Goal</ins>: support dynamic scaling and interservice communication out of the box; share libraries among the services.

<ins>Prerequisite</ins>: service instances are mostly [[wiki/concepts/source/basic-metapatterns/shards|stateless]].

The [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] architecture boasts dynamic scaling under load thanks to its *Mesh*-based *Middleware*. It also allows for the services to share libraries via their *Sidecars* – additional containers co-located with each service instance – to avoid duplication of [[wiki/concepts/source/basic-metapatterns/layers|generic code]] among the services.

<ins>Pros</ins>:

- Dynamic scaling and error recovery.
- Available out of the box.
- Provides a way to implement shared aspects (cross-cutting concerns) once and use the resulting libraries in every service.


<ins>Cons</ins>:

- Performance degrades because of the complex distributed infrastructure.
- You may suffer vendor lock-in.


## Use a Shared Repository


![The data of individual services is merged into a shared repository.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20to%20Shared%20Database.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]], [[wiki/concepts/source/basic-metapatterns/services|Services]].

<ins>Goal</ins>: let the services [[wiki/concepts/source/foundations-of-software-architecture/shared-data|share data]], don’t invest in operating multiple databases.

<ins>Prerequisite</ins>: the services use a uniform approach to persisting their data.

You don’t really need every service to have a private database. A shared one is enough in many cases.

<ins>Pros</ins>:

- It is easy for the services to share and synchronize data.
- Lower operational complexity.
- No data duplication.


<ins>Cons</ins>:

- All the services depend on the database schema which becomes hard to alter.
- The single database will limit performance of the system.
- It may also become a single point of failure.


<ins>Further steps</ins>:

- [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]] scales the [[wiki/concepts/source/basic-metapatterns/layers|data layer]] but it is a simple key-value store.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] is about having multiple specialized data stores.


## Add a Proxy


![Generic aspects of services move to a shared proxy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20add%20Proxy.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]], [[wiki/concepts/source/basic-metapatterns/services|Services]].

<ins>Goal</ins>: use a standard infrastructure component on behalf of your entire system.

<ins>Prerequisite</ins>: the system serves its clients in a uniform way.

Putting a generic component between the system and its clients helps the programmers concentrate on business logic rather than protocols, infrastructure, or even security.

<ins>Pros</ins>:

- You get a choice of generic functionality without investing development time.
- It is an additional layer that isolates your system from both its clients and attackers.


<ins>Cons</ins>:

- There is a latency penalty caused by the extra network hop.
- Each *Proxy* may be a single point of failure, or at least needs some admin oversight.


<ins>Further steps</ins>:

- You can always add another kind of [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]].
- If there are multiple clients that differ in their protocols, you can employ a stack of *Proxies* per client, resulting in [*Backends for Frontends*](<Backends for Frontends (BFF)>).


## Use an Orchestrator


![The application logic is extracted from individual services into a shared orchestrator.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20use%20Orchestrator.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]], [[wiki/concepts/source/basic-metapatterns/services|Services]].

<ins>Goal</ins>: have the high-level logic of use cases distilled as intelligible code.

<ins>Prerequisite</ins>: the use cases comprise sequences of high-level steps (which is very likely to be true for a system of [[wiki/concepts/source/basic-metapatterns/services|*subdomain services*]]).

When a use case jumps over several services in a dance of [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]], there is no easy way to understand it as there is no single place to see it in the code. It may be even worse with [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelined*]] systems where the use cases are embodied in the structure of event channels between the components.

Extract the [[wiki/concepts/source/basic-metapatterns/layers|high-level business logic]] from the choreographed services or their interconnections and put it into a dedicated component.

<ins>Pros</ins>:

- You are not limited in the number and complexity of use cases anymore.
- The global use cases become much easier to debug.
- You have a new team dedicated to the interaction with customers, freeing the other teams to study their parts of the domain or work on code improvements.
- Many changes in the high-level logic can be implemented and deployed without touching the main services.
- The extra layer decouples the main services from the system’s clients and from each other.


<ins>Cons</ins>:

- There is a performance penalty because the number of messages per use case doubles.
- The *Orchestrator* may become a single point of failure.
- Some flexibility is lost as the *Orchestrator* couples the services’ qualities.


<ins>Further steps</ins>:

- If there are several clients that strongly vary in workflows, you can apply [*Backends for Frontends*](<Backends for Frontends (BFF)>) with an *Orchestrator* per client.
- If the *Orchestrator* grows too large, it [[wiki/concepts/source/extension-metapatterns/orchestrator|can be divided]] into layers, services, or both; the latter option resulting in a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top-Down Hierarchy*]].
- The *Orchestrator* can be [[wiki/concepts/source/extension-metapatterns/orchestrator|scaled]] and can have its own database.


## Make a Sandwich


![The application and data parts of services are separated from the domain logic and merged into system-wide layers, resulting in a Sandwich.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20to%20Sandwich.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/sandwich|Sandwich]] ([[wiki/concepts/source/basic-metapatterns/layers|Layers]], [[wiki/concepts/source/basic-metapatterns/services|Services]], [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Database]] ([[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]), [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]).

<ins>Goal</ins>: simplify the integration of tightly coupled services.

<ins>Prerequisite</ins>: the services use compatible technologies in their application and data layers.

Tightly coupled services waste a lot of programming effort and performance on boilerplate communication and data transfer. At the same time, their [[wiki/concepts/source/basic-metapatterns/layers|*domain* logic]] remains fairly independent, making full merge into a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] impractical.

Try merging only the [[wiki/concepts/source/basic-metapatterns/layers|*use cases*]] and [[wiki/concepts/source/basic-metapatterns/layers|*persistence*]] while leaving the *domain* layer subdivided.

<ins>Pros</ins>:

- *Use cases* become much easier to debug.
- No boilerplate code for communication between the services.
- No data duplication or data transfer among the services.
- You have a new team dedicated to use cases and interaction with the customers.
- Many changes in *use cases* can be implemented and deployed without touching the *domain* logic.


<ins>Cons</ins>:

- The services are coupled in their properties.
- There are now single points of failure that leave the system totally inoperational.
- The *Shared Database* limits the system’s performance.


<ins>Further steps</ins>:

- [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]] scales the *data* layer.
