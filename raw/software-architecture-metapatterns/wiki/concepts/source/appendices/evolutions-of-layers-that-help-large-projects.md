---
title: "Evolutions of Layers that help large projects"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Layers that help large projects.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Layers%20that%20help%20large%20projects
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Layers that help large projects

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Layers that help large projects.md`.

The main drawback (and benefit) of [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] is that much or all of the business logic is kept together in one or two components. That allows for easy debugging and fast development in the initial stages of the project but slows down and complicates work as the project [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|grows in size]]. The only way for a growing project to continue evolving at a reasonable speed is to subdivide its business logic into several smaller, thus less [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|complex]], components that match subdomains (*bounded contexts* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]). There are several options for such a change with their applicability depending on the domain:

- In a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] the middle layer with the bulk of business logic is divided into [[wiki/concepts/source/basic-metapatterns/services|*Services*]], leaving the upper [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and lower [[wiki/concepts/source/extension-metapatterns/shared-repository|*database*]] layers intact for possible future evolutions.
- Sometimes the business logic can be represented as a set of directed graphs which is known as [[wiki/concepts/source/basic-metapatterns/pipeline|*Event-Driven Architecture*]].
- If you are lucky, your domain is naturally a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top-Down Hierarchy*]].


## Divide the domain layer into Services


![The domain layer is split into subdomain components, making a Sandwich.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Split%20Domain%20to%20Services.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/sandwich|Sandwich]] ([[wiki/concepts/source/basic-metapatterns/layers|Layers]], [[wiki/concepts/source/basic-metapatterns/services|Services]], [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Database]] ([[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]), [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]).

<ins>Goal</ins>: make the code simpler and let several teams work on the project efficiently.

<ins>Prerequisite</ins>: the low-level business logic comprises loosely coupled subdomains.

It is very common for a system’s domain to comprise weakly interacting *bounded contexts* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]. They are integrated through high-level use cases and/or [[wiki/concepts/source/foundations-of-software-architecture/shared-data|relations in data]]. For such a system it is relatively easy to subdivide the [[wiki/concepts/source/basic-metapatterns/layers|domain logic]] into *Services* while leaving the integration and data layers shared, yielding a *Sandwich*.

<ins>Pros</ins>:

- You get multiple specialized development teams.
- The largest and most complex piece of code is split into several smaller components.
- There is more flexibility with deployment and scaling.


<ins>Cons</ins>:

- Future changes in the overall structure of the domain will be harder to implement.
- System-wide use cases become somewhat harder to debug as they span over many components.
- Performance will degrade as soon as the *Services* and their *Orchestrator* become distributed.


<ins>Further steps</ins>:

- Continue by subdividing the *Orchestrator* and *database*, turning the system into [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Orchestrated Three-Layered Services*]].
- Divide the *Orchestrator* (by type of client) into [*Backends for Frontends*](<Backends for Frontends (BFF)>).
- Use multiple databases ([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]).
- Scale well with [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]].


## Build an Event-Driven Architecture over a Shared Database


![A backend is subdivided into a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Split%20to%20Event-Driven%20Architecture.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/pipeline|Event-Driven Architecture]] ([[wiki/concepts/source/basic-metapatterns/pipeline|Pipeline]] ([[wiki/concepts/source/basic-metapatterns/services|Services]])), [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Database]] ([[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]).

<ins>Goal</ins>: untangle the code, support multiple teams, and improve scalability.

<ins>Prerequisite</ins>: the use cases are trivial sequences of loosely coupled, coarse-grained steps.

If your system features well-defined and simple workflows for processing every kind of input request, then it can be divided into several [[wiki/concepts/source/basic-metapatterns/services|*subdomain services*]], each hosting a few related steps of multiple use cases. Each service subscribes to inputs from other services and/or system’s clients and publishes output events.

<ins>Pros</ins>:

- The code is divided into much smaller (and simpler) segments.
- It is easy to add new steps or use cases as this structure is quite flexible.
- You open a way to having several almost independent teams, one per service.
- You can achieve flexible deployment and scaling as the services are stateless, but you need to add a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] for that.
- This architecture naturally supports event replay as the means of reproducing bugs or testing / benchmarking individual components.
- There is no need for explicit scheduling or thread synchronization.


<ins>Cons</ins>:

- The system as a whole is hard to debug.
- You will have to live with high latency.
- You may end up with too many components which are interconnected in too many ways.


<ins>Further steps</ins>:

- Add a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] that supports scaling and failure recovery.
- Split the *Shared Database* by subdomain, yielding [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Choreographed Two-Layered Services*]].
- Scale with [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]].
- Extract the logic of use cases into an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]].


## Build a Top-Down Hierarchy


![The lower layers of a system are subdivided, resulting in a hierarchy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Hierarchy.png)


<ins>Patterns</ins>: [[wiki/concepts/source/fragmented-metapatterns/hierarchy|Top-Down Hierarchy]] ([[wiki/concepts/source/fragmented-metapatterns/hierarchy|Hierarchy]]).

<ins>Goal</ins>: untangle the code, support multiple teams, and achieve fine-grained scalability.

<ins>Prerequisite</ins>: the domain is hierarchical.

Splitting the lower layers into independent components with identical interfaces simplifies the managing code and allows the managed components to be deployed, developed, and run independently of each other. Ideally, the mid-layer components should participate in decision-making so that the uppermost component is kept relatively simple.

<ins>Pros</ins>:

- Hierarchy is easy to develop and support with multiple teams.
- Individual components are straightforward to add, modify, or replace.
- The components scale, deploy, and run independently.
- The system is quite fault tolerant.


<ins>Cons</ins>:

- It takes time and skill to figure out good interfaces.
- There are many components to administer.
- Latency is suboptimal for system-wide use cases.
