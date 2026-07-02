---
title: "Hierarchy"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Fragmented metapatterns/Hierarchy.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Fragmented%20metapatterns/Hierarchy
source_license_note: "See namespace README; preserve attribution and source links."
---

# Hierarchy

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Fragmented metapatterns/Hierarchy.md`.


![A diagram for Hierarchy, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Hierarchy.png)


*Command and conquer.* Build a tree of responsibilities.

<ins>Structure:</ins> A tree of components.

<ins>Type:</ins> System topology or extension component.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Very good in decoupling logic | Global use cases may be hard to debug |
| Supports multiple development teams and technologies | Poor latency for global use cases |
| Components may vary in their qualities | Operational complexity |
| Low-level components are easy to replace | Slow start of the project |
| Limited fault tolerance |  |

<ins>References:</ins> None good I know of.

Though not applicable to every domain, hierarchical decomposition is arguably the best way to distribute responsibilities between components. It limits the connections (thus the number of interfaces and contracts for the team to keep in mind) of each component to its parent and a few children, allowing for the building of complex (and even complicated) systems in a simple way. The hierarchical structure is very flexible as it features [multiple layers of indirection](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering) (and often polymorphism), which makes addition, replacement, or [stubbing/mocking](https://stackoverflow.com/questions/3459287/whats-the-difference-between-a-mock-stub) of leaf components trivial. It is also quite fault-tolerant as individual subtrees operate independently.

This architecture is not ubiquitous because few domains are truly hierarchical. Its high fragmentation results in increased latency and poor debugging experience. Moreover, component interfaces must be designed beforehand and are hard to change.

### Performance

No kind of distributed hierarchy is latency-friendly as many use cases involve several network hops. The fewer layers of the hierarchy are involved in a task, the better its performance.


![Comparison of latency for decision-making at various levels of a hierarchy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Hierarchy%20-%20speed.png)


Maintaining high throughput usually requires deployment of multiple instances of the root component, which is not possible if it is stateful (as in [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control systems*]]) and the state cannot be split into [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]]. The following tricks may help unloading the root:

- *Aggregation* ([[wiki/concepts/source/basic-metapatterns/layers|first met]] in [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]): a node of a hierarchy collects reports from its children, aggregates them into a single package, and sends the aggregated data up to its parent. This greatly reduces traffic to the root in large [IIoT](https://en.wikipedia.org/wiki/Industrial_internet_of_things) networks.
- *Delegation* (resembles [[wiki/concepts/source/basic-metapatterns/layers|strategy injection and batching]] for [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]): a node should try to handle all the low-level details of communication with its children without consulting its parent node. For a [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|control system]] that means that its mid-level nodes should implement control loops for the majority of incoming events. For a [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|computational system]] that means that its mid-level nodes should expose coarse-grained interfaces to their parent(s) while translating each API method call into multiple calls to their child nodes.
- *Direct communication channels* ([[wiki/concepts/source/extension-metapatterns/orchestrator|previously described]] for [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]): if the low-level nodes need to exchange data, their communication should not always go through the higher-level nodes. Instead, they may negotiate a direct link (open a socket) that bypasses the root of the hierarchy.



![Aggregation of data in mid-level nodes; autonomous decision-making by mid-level nodes; direct communication between low-level nodes of a hierarchy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Hierarchy%20-%20optimizations.png)


### Dependencies

A parent node would usually define one (for polymorphic children) or more (otherwise) [*SPIs*](https://en.wikipedia.org/wiki/Service_provider_interface) for its child nodes to implement. The interfaces reside on the parent side because low-level nodes tend to be less stable (new types of them are often added and old ones replaced) therefore we don’t want our main business logic to depend on them.


![In Hierarchy a child component depends on an SPI of its parent component. If the children are polymorphic, their parent has a single SPI.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Hierarchy.png)


### Applicability

*Hierarchy* <ins>fits</ins> with:

- *Large and huge projects.* The natural division by both level of abstractness and subdomain allows for using smaller modules, ideally with intuitive interfaces. The APIs for each team to learn are limited to just a few which their component interacts with directly.
- *Systems of hardware devices.* Real-world [IIoT](https://en.wikipedia.org/wiki/Industrial_internet_of_things) systems may use a hierarchy of controllers to benefit from [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|autonomous decision-making and data aggregation]].
- *Customization*. The tree-like structure provides opportunities for easy customization. A medium-sized hierarchical system may integrate hundreds of leaf types.
- *Survivability*. A distributed hierarchy retains limited functionality even if several of its nodes fail.


*Hierarchy* <ins>fails</ins> with:

- *Cohesive domains.* Horizontal interactions between nodes that belong to the same layer bloat interfaces as they have to pass through parent nodes.
- *Quick start*. Finding (and verifying) a good hierarchical domain model may be hard if at all possible. Debugging an initial implementation will not be easy.
- *Low latency*. System-wide scenarios involve many cross-component interactions which are slow in distributed systems.


### Relations


![Diagrams of Orchestrator of Orchestrators, Middleware of Middlewares, and Services of Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Hierarchy.png)


*Hierarchy*:

- Can be applied to [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]*,* [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] or [[wiki/concepts/source/basic-metapatterns/services|*Services*]].


## Variants by structure (may vary per node)

*Hierarchy* comes in various shapes as it is more of a design approach than a ready-to-use pattern:

### Polymorphic children

All the child nodes managed by a given parent node expose the same interface and contract. This tends to simplify the implementation of the parent and resembles the inheritance of OOD.

Example: a fire alarm system may treat all of its fire sensors as identical devices, even though the real hardware comes from many manufacturers.

### Functionally distinct children

The managing node is aware of several kinds of children that vary in their APIs and contracts, just like with the composition in OOD.

Example: an intrusion alarm logic may need to discern between cat-affected IR sensors and mostly cat-proof glass break detectors.

## Variants by direction

A *Hierarchy* may have its root [at the top](#top-down-hierarchy-orchestrator-of-orchestrators-presentation-abstraction-control-pac-hierarchical-model-view-controller-hmvc) (client side), [at the bottom](#bottom-up-hierarchy-bus-of-buses-network-of-networks-hierarchical-middleware) (deep infrastructure), or [no root at all](#in-depth-hierarchy-cell-based-microservice-architecture-wso2-version-segmented-microservice-architecture-services-of-services-clusters-of-services) (recursive decomposition):

### Top-Down Hierarchy: [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]] of Orchestrators, Presentation-Abstraction-Control (PAC), Hierarchical [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Model-View-Controller]] (HMVC)


![A single component calls two components in the layer below it, each of which calls two or three lower-level leaf components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Hierarchy%20-%20Top-down.png)


In the most common case *Hierarchy* is applied to business logic to build a layered system which grows from a single generic high-level root into a swarm of specialized low-level pieces. The most obvious applications are protocol parsers, decision trees, [IIoT](https://en.wikipedia.org/wiki/Industrial_internet_of_things) (e.g. a fire alarm system of a building), and [modern automotive](https://semiengineering.com/managing-todays-advanced-vehicle-networks-design-challenges/) networks. A marketplace that allows for customized search and marketing algorithms within each category of its goods may also be powered by a hierarchy of category-specific services.

[*Presentation-Abstraction-Control*](https://en.wikipedia.org/wiki/Presentation%E2%80%93abstraction%E2%80%93control) (*PAC*) \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\] applies *Top-Down Hierarchy* to a user-facing application, providing each of the resulting [[wiki/concepts/source/basic-metapatterns/layers|*layered*]] nodes with its own widget (*presentation*) on the UI screen (which is the *presentation* of the root node). *Controls* are responsible for inter-node communication and [[wiki/concepts/source/basic-metapatterns/layers|integration logic]], while [[wiki/concepts/source/basic-metapatterns/layers|domain logic]] and data reside in *abstractions*.

[*Hierarchical Model-View-Controller*](https://herbertograca.com/2017/08/17/mvc-and-its-variants/#hierarchical-model-view-controller) (*HMVC*) is similar, but its *views* access *models* directly, like in [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVC*]], and every model synchronizes with the global data. This pattern [was used](https://web.archive.org/web/20060319064042/http://www.javaworld.com/javaworld/jw-09-2000/jw-0908-letters.html) in [rich clients](https://en.wikipedia.org/wiki/Rich_client).


![Both Presentation-Abstraction-Control and Hierarchical Model-View-Controller are top-down hierarchies with three-component nodes, which share a database in the second pattern.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/PAC.png)


### Bottom-Up Hierarchy: [[wiki/concepts/source/extension-metapatterns/middleware|Bus]] of Buses, Network of Networks, Hierarchical Middleware


![An integration middleware interconnects the middlewares of two systems.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Hierarchy%20-%20Bottom-up.png)


Other cases require building a common base for intercommunication between several networks which vary in their protocols (and often their hardware). The root of such a *Hierarchy* is a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] generic and powerful enough to cover the needs of all the specialized networks which it interconnects.

Example: [Automotive networks](https://www.mdpi.com/1424-8220/21/23/7917), integration of corporate networks, [the Internet](https://en.wikipedia.org/wiki/Internet_service_provider).

### In-Depth Hierarchy: [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Cell]]-Based (Microservice) Architecture (WSO2 version), Segmented Microservice Architecture, [[wiki/concepts/source/basic-metapatterns/services|Services]] of Services, Clusters of Services


![Cells of different kinds communicate with each other through cell gateways.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Cell-Based%20Architecture.png)


When several [[wiki/concepts/source/basic-metapatterns/services|*services*]] in a system grow large, in some cases it is possible to divide each of them into *subservices*. Each group of the resulting subservices (known as a [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]], [*Domain*](https://www.uber.com/blog/microservice-architecture/) or *Cluster* \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\]) usually implements a *bounded context* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]. It is hidden behind its own [[wiki/concepts/source/extension-metapatterns/proxy|*Cell Gateway*]] and may even use its own [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]. Subservices of a *Cell* may [[wiki/concepts/source/extension-metapatterns/shared-repository|*share a database*]] and may be deployed as a single unit. This keeps the system’s integration complexity (the length of its APIs and the number of deployable units) reasonable while still scaling development among many teams or individuals, each owning a service. If each instance of a *Cell* owns a [[wiki/concepts/source/basic-metapatterns/shards|*shard*]] of its database, the system [becomes more stable](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html) as there is no single point of failure (except for the [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] called *Cell Router*). Another benefit is that *Cells* can be deployed to regional data centers to improve locality for users of the system. However, that will likely cause data synchronization traffic between the data centers.

The [*Cell-Based Architecture*](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) ([*Segmented Microservice Architecture*](https://github.com/wso2/reference-architecture/blob/master/api-driven-microservice-architecture.md)) may be seen as a combination of an *Orchestrator of Orchestrators* and a *Bus of Buses* where the subservices are leaf nodes of both *hierarchies* while the [[wiki/concepts/source/extension-metapatterns/proxy|*API Gateways*]] of the *Cells* are their internal nodes.

Uber [compacted](https://www.uber.com/blog/microservice-architecture/) 2200 [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] into 70 *Cells* arranged in a [*SOA*](<Service-Oriented Architecture (SOA)>)-style topology called [*Domain-Oriented Microservice Architecture*](<Service-Oriented Architecture (SOA)#domain-oriented-microservice-architecture-doma>).

## Evolutions

- The upper component of a *Top-Down Hierarchy* can be split into [*Backends for Frontends*](<Backends for Frontends (BFF)>).



![The upper layer of a top-down hierarchy is subdivided into Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Hierarchy%20-%201.png)


## Summary

*Hierarchy* fits a project of any size as it evenly distributes complexity among the system’s many components. However, it is not without drawbacks in performance, debuggability, and operational complexity. Moreover, very few domains allow for seamless application of this architecture.
