---
title: "System topologies"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Introduction/System topologies.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Introduction/System%20topologies
source_license_note: "See namespace README; preserve attribution and source links."
---

# System topologies

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Introduction/System topologies.md`.

In the [[wiki/concepts/source/introduction/metapatterns|previous chapter]] we started with architectural patterns and grouped them in accordance with their structure and function into *metapatterns*\. Now let’s traverse in the opposite direction: from *topology* \(the structure of a system\) to the patterns which describe it\. We will draw and analyze a map of common system topologies and along the way outline the scope of this book\.

## Methodology

We will rely on our finding that any system has a characteristic representation in the [[wiki/concepts/source/introduction/metapatterns|abstractness\-subdomain\-sharding space]]\. The amounts of a system’s partitioning along each of the three dimensions can be used as its coordinates on a map of system topologies:

- *Abstractness* corresponds to the *technical partitioning* \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] – subdivision of a system into [[wiki/concepts/source/basic-metapatterns/layers|*layers*]] with different roles and technologies\. Any use case will likely involve all the layers\.
- *Subdomain* represents the *domain partitioning* \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] – segregation of a system into [[wiki/concepts/source/basic-metapatterns/services|*modules* or *services*]] that encapsulate distinct parts of the business knowledge\. A use case is often localized in one or two subdomains\.
- *Sharding* is about running multiple instances \([[wiki/concepts/source/basic-metapatterns/shards|*shards*]] or [[wiki/concepts/source/basic-metapatterns/shards|*replicas*]]\) of a component\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Partitioning.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Partitioning.png" alt="Technical partitioning into Layers, domain partitioning into Services, and multiple instances of a system." loading="lazy" width=100%/>
</a>
</div>

### From theory to practice

Having a distribution of architectures in a 3D space sounds great, but how do we represent it as human\-readable media?

There are at least the following issues:

- Many system topologies feature similar levels of segregation into layers and services, meaning that they belong to the same neighborhood on the map\.
- It makes a difference whether a system’s business logic or its infrastructure is subdivided because business logic comprises the bulk of the code\. Therefore we cannot estimate a system’s coordinates only from the number of layers or services it contains, which means that we are limited to something like “major layering” and “minor layering” instead of numeric values\.
- Sharding of many architectures varies widely and is hard to represent on a flat drawing\.


As a result, the following adjustments were necessary to make the map of system topologies comprehensible:

- Sharding is omitted, transforming 3D coordinates into a flat map\. Yes, much information is lost, but *too much information is no information*\. Now the map is easier to read\.
- I took the liberty of shifting topologies from their real positions to resolve overlaps\.
- Even worse, I moved some of the topologies around to group similar architectures\.
- Exotic \(e\.g\. [[wiki/concepts/source/implementation-metapatterns/mesh|*Leaf\-Spine Architecture*]]\) and duplicate \(e\.g\. [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]]\) topologies are omitted\.


## The map of system topologies

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Topologies%20Map.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Topologies%20Map.png" alt="A map of system topologies arranged according to the amount of their partitioning into layers and services." loading="lazy" width=100%/>
</a>
</div>

The map contains only basic architectures which are easy to apprehend and name\. Any complex system is very likely to be a combination of these simple topologies\.

I somewhat arbitrarily divided the map of system topologies into five partially overlapping regions:

- [*Monolithic*](#monolithic-systems), where the bulk of the system is kept in a single component\.
- [*Layered*](#layered-architectures), with mostly technical partitioning and specialized components \(drawn in one or two colors which correspond to different kinds of code\)\.
- [*Services*](#services-area) with domain partitioning, meaning that each of the main components includes several kinds of code\.
- [*Fragmented*](#fragmented-patterns) *systems* built of many smaller parts\.
- [*Plugins*](#plugins-family) that usually have a cohesive core and external modular layers\.


This grouping allows us to study the topologies piecemeal without getting lost in their numbers and features\.

## Monolithic systems

In the simplest cases a project is too small for any internal structure to be justified – you can code it in a couple of hours without any preliminary design\. In other cases the domain is known to be so cohesive that you cannot find good module boundaries – any internal interfaces result in much boilerplate code or degrade performance\. Or there is no time left for a thoughtful design\!

### True Monoliths

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/True%20Monoliths.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/True%20Monoliths.png" alt="Diagrams of Monolith, Shards, and Replicas." loading="lazy" width=100%/>
</a>
</div>

Few system topologies are truly monolithic with one kind of system components:

- [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] keeps everything together in a single cohesive application which makes sense for small, one\-off projects\. A long\-running *Monolith* may need to handle inputs and events, for which there are several options:
  - [[wiki/concepts/source/basic-metapatterns/monolith|*Reactor*]] uses a thread for each request and blocks on calls to the OS or other components\. This is the simplest server\-side implementation\.
  - [[wiki/concepts/source/basic-metapatterns/monolith|*Proactor*]] relies on callbacks that all run in a single thread to achieve real\-time latency and avoid locks\. It is widely used in embedded programming\.
  - [[wiki/concepts/source/basic-metapatterns/monolith|*Half\-Sync/Half\-Async*]] is an internally layered approach that allocates a coroutine or fiber to each task\. It is more resource\-efficient than [[wiki/concepts/source/basic-metapatterns/monolith|*Reactor*]] but lacks the real\-time responsiveness and flexibility of [[wiki/concepts/source/basic-metapatterns/monolith|*Proactor*]]\.
- [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] are multiple instances of a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], each owning a slice of the system’s data\. A client must know which shard to access either through storing its address or by querying an [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassador Proxy*]] library written by the team that deploys the shards\. This is the architecture of choice when clients are independent from each other but the entire dataset is too large to fit in a single server\.
- [[wiki/concepts/source/basic-metapatterns/shards|*Replicas*]] are instances of a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] with identical data used to achieve fault tolerance and high throughput\. Any writes to one replica must be propagated to the other replicas:
  - With [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|semi\-specialized replicas]] all write requests go to a single *leader* instance which publishes the changes for the other replicas, called *followers*, to apply to their datasets\. Read requests usually go to the followers, and the more read traffic there is, the more followers are deployed\.
  - If all the replicas are identical, any of them can handle a write request and publish the update for the other replicas to apply\. This scales write throughput but involves the chance of data conflicts when the same data record is simultaneously changed on multiple replicas\. See [[wiki/concepts/source/extension-metapatterns/shared-repository|*Data Grid* of *Space\-Based Architecture*]]\.


### Monoliths with auxiliary layers

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Monoliths%20with%20Layers.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Monoliths%20with%20Layers.png" alt="Diagrams of Monolith with Backends for Frontends, Managed Shards, Peer-to-Peer Mesh, Monolith with a database, and Monolith with Polyglot Persistence." loading="lazy" width=100%/>
</a>
</div>

In other kinds of systems, common in server\-side programming, some functionality moves to a dedicated layer while the business logic remains monolithic:

- [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] *with a database* relies on an external [[wiki/concepts/source/basic-metapatterns/layers|data storage component]] for persistence\.
- [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] *with* [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] uses specialized databases to improve performance\.
- [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] *with* [*Backends for Frontends*](<Backends for Frontends (BFF)>) employs a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] for each kind of client to address variations in the clients’ protocols and security\.
- *Managed* [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] run behind a single [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] which connects each system’s client to the shard that has that client’s data thus isolating the clients from the knowledge of the system’s internal composition\.
- [[wiki/concepts/source/implementation-metapatterns/mesh|*Peer\-to\-Peer Mesh*]] interconnects multiple instances of an application, acting as a distributed [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]\.


### Monoliths with Plugins

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Monoliths%20with%20Plugins.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Monoliths%20with%20Plugins.png" alt="Diagrams of Monolith with Plugins, Model-View-Controller, and Hexagonal Architecture." loading="lazy" width=100%/>
</a>
</div>

A monolithic core can be extended with disposable additions:

- [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] allow for parts of the core’s workflow to be supplied by internal or external teams, customizing the experience of the system’s users without modifications to its main code\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Controller* and related patterns]] provide a [[wiki/concepts/source/extension-metapatterns/proxy|*presentation layer*]] that isolates the main code from dependencies on the UI framework or network protocol, thus minimizing the effort of porting the software to another platform\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] keeps the entire business logic self\-sufficient by wrapping every dependency with a dedicated [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]], which not only improves portability but also helps with testing and allows for changing vendors late in the development cycle\.


### Underdeveloped Moduliths

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Underdeveloped%20Moduliths.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Underdeveloped%20Moduliths.png" alt="Diagrams of Monolith with libraries and Modulith with shared code." loading="lazy" width=72%/>
</a>
</div>

If a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] evolves for a long time, it will likely become segmented into subdomain components, yielding a [[wiki/concepts/source/basic-metapatterns/services|*Modulith*]]\. As that process is not instantaneous, there are a couple of transitional architectures:

- [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] *with* [[wiki/concepts/source/basic-metapatterns/layers|*libraries*]] involves subdomain\-specific third\-party components which are called by its cohesive business logic\.
- [[wiki/concepts/source/basic-metapatterns/services|*Modulith*]] *with shared code* has the business logic largely separated into subdomain modules which still rely on a common codebase for shared functionality\.


## Layered architectures

Layering enables the use of specialized technologies and third\-party components while avoiding the [risky](https://martinfowler.com/bliki/MonolithFirst.html) subdivision of business logic\. It also allows for parts of the system to [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|differ in their qualities, placement, and scalability]]\. All of that makes layered architectures suitable for full\-featured, medium\-sized projects run by one or two teams where both the speed of development and supportability matter\.

### Ordinary Layers

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Ordinary%20Layers.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Ordinary%20Layers.png" alt="Diagrams of DDD-Style Layers, Layers with Polyglot Persistence, Layers with Backends for Frontends, and Monolith with a database." loading="lazy" width=100%/>
</a>
</div>

Typical layered architectures include:

- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] of various composition, for example:
  - [[wiki/concepts/source/basic-metapatterns/layers|*Entity\-Control\-Boundary*]] which represent the [[wiki/concepts/source/basic-metapatterns/layers|*domain model*]], [[wiki/concepts/source/basic-metapatterns/layers|*use cases*]], and [[wiki/concepts/source/basic-metapatterns/layers|*interface*]], respectively\. This pattern originated in the age of complex desktop applications\.
  - [[wiki/concepts/source/basic-metapatterns/layers|*Domain\-Driven Design* decomposition]] into *presentation* \(interface\), *application* \(use cases\), *domain* \(business rules\), and *infrastructure* \(communication and persistence\)\. It targets enterprise systems\.
  - [[wiki/concepts/source/basic-metapatterns/layers|*Embedded systems*]] with pairs of UI \+ HMI, SDK \+ HAL, and FW \+ HW implemented by distinct parties in the supply chain\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] *with* [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] where the [[wiki/concepts/source/basic-metapatterns/layers|*persistence*]] layer involves multiple databases, usually chosen for their performance with specialized payloads\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] *with* [*Backends for Frontends*](<Backends for Frontends (BFF)>) with a dedicated [[wiki/concepts/source/basic-metapatterns/layers|*interface*]] and/or [[wiki/concepts/source/basic-metapatterns/layers|*application*]] component for each kind of client when the clients differ in their protocols and/or workflows\.
- [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] *with a* [[wiki/concepts/source/basic-metapatterns/layers|*database*]] as a case of rudimentary layering of server\-side systems\.


### Scaled Layers

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Scaled%20Layers.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Scaled%20Layers.png" alt="Diagrams of Three-Tier System, MapReduce, Managed Shards, Scaled Service, and Peer-to-Peer Mesh." loading="lazy" width=87%/>
</a>
</div>

Several layered architectures build around scalability:

- [[wiki/concepts/source/basic-metapatterns/layers|*Three\-Tier Architecture*]] contains a frontend layer with an instance per system’s user, scaled backend, and non\-scaled database\. It exploits the physical distribution of the system to reap [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|cost, performance, and security benefits]]\.
- [[wiki/concepts/source/basic-metapatterns/services|*Scaled service*]] runs multiple instances of a stateless application between a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]], which evenly distributes user requests among the instances, and a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]]\. It is the default approach for scaling a server\-side service\.
- [[wiki/concepts/source/extension-metapatterns/orchestrator|*MapReduce* or *Scatter\-Gather*]] runs a coupled part of a calculation in a non\-scaled layer while mutually independent parts are delegated to multiple worker shards\.
- *Managed* [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] rely on a [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] layer to connect a client to the appropriate shard\. This removes the need for the client to know which shard contains its data\.
- [[wiki/concepts/source/implementation-metapatterns/mesh|*Peer\-to\-Peer Mesh*]] builds a distributed [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] layer that interconnects instances of a client application\.


### Other layered systems

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Other%20Layered.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Other%20Layered.png" alt="Diagrams of Model-View-Presenter, Onion Architecture, and Sandwich." loading="lazy" width=100%/>
</a>
</div>

Besides that, there are a few peculiar layered systems:

- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Presenter* family of patterns]] features layered user interfaces which decouple the main system from a GUI or web framework with the goal of being able to easily switch to another framework version or vendor\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Onion Architecture* or *Clean Architecture*]] is a [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] \(see [below](#hexagonal-architecture)\) with a layered core structured along the ideas of [[wiki/concepts/source/basic-metapatterns/layers|*Domain\-Driven Design*]]\.
- [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] architectures are [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] with the [[wiki/concepts/source/basic-metapatterns/layers|*domain logic* layer]] split into subdomains\. It is a pragmatic low effort approach to tackle complexity in quickly evolving projects that can afford several development teams\. It also addresses [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|data\-centric]] domains\.


## Plugins family

Some architectures specialize in separating complex core logic from miscellaneous details to make the *core* independent and reusable under changing conditions\. In most cases the core contains monolithic business logic but that may vary among patterns\. This family of topologies is prevalent in long\-living or highly customizable products whose codebases are too expensive to rewrite to address every trend or fad\.

### Plugin Architecture

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Plugin%20Architecture.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Plugin%20Architecture.png" alt="A plugin, library, and extension called by a core." loading="lazy" width=84%/>
</a>
</div>

[[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] are external components which supply predefined parts of a host component’s workflow\. They may be created by the company that makes the product, often for the sake of selling several flavors with limited or specialized functionality\. Or they may come from external programmers, as codecs in video players or customizations for accounting software, to extend the usefulness of a product without overburdening its core codebase\.

### Separated Presentation

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Separated%20Presentation.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Separated%20Presentation.png" alt="Diagrams of Model-View-Presenter and Model-View-Controller." loading="lazy" width=100%/>
</a>
</div>

[[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Separated Presentation*]] extracts the [[wiki/concepts/source/basic-metapatterns/layers|user or network interface]] functionality into a dedicated layer which is often further subdivided\. This makes the main codebase reusable in different environments:

- The [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Controller* family of patterns]] has separate modules for platform\-specific input and for output which is beneficial when there is no web or GUI framework that can provide a unified high\-level user interface\.
- The [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Presenter* family]] builds on top of a pre\-existing platform\-specific [[wiki/concepts/source/basic-metapatterns/layers|presentation layer]]\. Most of these patterns add an intermediate [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] between the platform\-dependent code and the core application\.


### Control patterns

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Control%20Patterns.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Control%20Patterns.png" alt="Diagrams of Pedestal and Microkernel." loading="lazy" width=100%/>
</a>
</div>

A couple of topologies originate with embedded or systems programming where it is important to abstract the business logic from the hardware components which tend to quickly go out of production and thus need to be replaced with incompatible models:

- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Pedestal*]] wraps each hardware component in a system with a dedicated driver to reduce the dependency of the business logic on hardware specifications thus allowing for the software to be reused with different hardware setups\.
- [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel Architecture*]] relies on an eponymous layer to mediate between resource consumers and resource producers which implement generic interfaces and thus are replaceable\. This approach is surprisingly ubiquitous:
  - [[wiki/concepts/source/implementation-metapatterns/microkernel|*Operating systems*]] are the origin of [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]], with user space applications competing for system resources owned by the device drivers\.
  - [[wiki/concepts/source/implementation-metapatterns/microkernel|*Interpreters*]] run user scripts in a sandbox and provide them access to installed libraries\.
  - [[wiki/concepts/source/implementation-metapatterns/microkernel|*Software frameworks*]] follow a similar approach, building a [*Facade*](https://refactoring.guru/design-patterns/facade) to grant user code a managed access to the framework’s internal components\.
  - [[wiki/concepts/source/implementation-metapatterns/microkernel|*Hypervisors*, *Virtualizers*, and *Distributed Runtimes*]] abstract a guest operating system or applications from the platform they run on\.


### Hexagonal Architecture

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Hexagonal%20Architecture.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Hexagonal%20Architecture.png" alt="Diagrams of Ports and Adapters and Onion Architecture." loading="lazy" width=100%/>
</a>
</div>

A few architectures fully isolate business logic from its environment, resulting in great portability, simpler automated testing and improved separation of concerns:

- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Ports and Adapters*]] \(the original [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]\) inserts an [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] into every communication pathway in or out of its business logic core but does not specify the structure of the core itself, which makes the pattern universally applicable\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Onion Architecture* or *Clean Architecture*]] structures the core in accordance with the [[wiki/concepts/source/basic-metapatterns/layers|rules of *Domain\-Driven Design*]], limiting the applicability of this topology to enterprise systems or complex backends\.


### Cell

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/4/Cell.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/4/Cell.png" alt="Several intercommunicating subservices are wrapped with a cell gateway that receives client requests, adapters for outgoing communication, and a plugin." loading="lazy" width=100%/>
</a>
</div>

[[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]] is a building block of huge systems that follow [*Domain\-Oriented Microservice Architecture*](<Service-Oriented Architecture (SOA)#domain-oriented-microservice-architecture-doma>) or [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]]\. It is a kind of [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] with a modular and often distributed core\. The internals of a *Cell* are hidden behind a [[wiki/concepts/source/extension-metapatterns/proxy|*Cell Gateway*]] which implements the *Cell*’s public interface\. Any outgoing communication, initiated from inside the *Cell*, goes through its [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] or through [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins* supplied by peer *Cells*]]\.

## Services area

Partitioning a system into [[wiki/concepts/source/basic-metapatterns/services|*modules*]] or [[wiki/concepts/source/basic-metapatterns/services|*services*]] which match its subdomains and assigning the components to dedicated teams greatly reduces the cognitive load that the programmers face as each person needs to comprehend only the service they work on\. Given that it is [cognitive load that determines development speed](https://realmensch.org/2018/05/04/we-are-all-10x-developers/), most large projects have service\-based topologies\.

However, full domain partitioning \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] is [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|beneficial only when the system’s subdomains are weakly coupled]] along every level of their functionality, which is why many real\-world topologies mix cohesive system\-wide layers and decoupled subdomain services\.

### Barebone services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Barebone%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Barebone%20Services.png" alt="Diagrams of Services, Three-Layered Services, Pipeline, and Two-Layered Services." loading="lazy" width=100%/>
</a>
</div>

A few architectures are completely segmented into subdomains:

- Distributed [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or in\-process [[wiki/concepts/source/basic-metapatterns/services|*Modules*]] rely on [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*mutual orchestration*]]\. They come in several kinds:
  - [[wiki/concepts/source/basic-metapatterns/services|*Service\-Based Architecture*]] tends to employ single instances of services which cover entire subdomains\. It is used for multi\-team server\-side projects with no special performance considerations\.
  - [[wiki/concepts/source/basic-metapatterns/services|*Modulith*]] \(*Modular Monolith*\) runs subdomain\-sized components in a single process, sacrificing fault tolerance for consistency and operational costs\. This architecture fits smaller Internet businesses\.
  - [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] with highly scalable sub\-subdomain components implement high load and high budget systems with well\-established domain knowledge but frequently changing business needs\.
  - [[wiki/concepts/source/basic-metapatterns/services|*Actors*]] are asynchronous objects used for real\-time tasks that range from embedded telephony to instant messengers to financial systems\. Consider them if you benefit from modeling every user of your system as a lightweight independently acting entity\.
- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Three\-Layered Services*]] subdivide each service into the [[wiki/concepts/source/basic-metapatterns/layers|*use cases*]], [[wiki/concepts/source/basic-metapatterns/layers|*domain logic*]], and [[wiki/concepts/source/basic-metapatterns/layers|*persistence*]] layers, allowing for further specialization of staff and technologies\.
- [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] is a [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreographed*]] system where each component implements a single stage of data or event processing:
  - [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipes and Filters*]] is a local and usually linear [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] that processes a data stream\. It is the architecture of choice for systems with customizable workflows and polymorphic algorithms such as video capture or replay\.
  - [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture*]] runs multiple branched [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]], each implementing a single use case, over a shared set of services\. It is an easily extendable alternative to [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] for domains with a few highly loaded yet simple scenarios\.
  - [[wiki/concepts/source/basic-metapatterns/pipeline|*Data Mesh*]] collects, transforms, and processes analytical data from a system of services\.
- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Two\-Layered Services*]] split each component of a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] \(usually a [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture*]]\) into [[wiki/concepts/source/basic-metapatterns/layers|*domain logic*]] and [[wiki/concepts/source/basic-metapatterns/layers|*persistence*]] layers, emphasizing the use of databases private to their services\. Noticeably, the [[wiki/concepts/source/basic-metapatterns/layers|*use case logic*]] is present only through the connections between the services\.


### Services with extensions

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Services%20with%20Extensions.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Services%20with%20Extensions.png" alt="Diagrams of Services with a Gateway; Orchestrated Services; Services with: an API Gateway, Backends for Frontends, Shared Repository, Middleware, and Pplyglot Persistence; and of Service Mesh." loading="lazy" width=100%/>
</a>
</div>

[[wiki/concepts/source/basic-metapatterns/services|*Services*]] become simpler when common aspects are extracted to a dedicated layer:

- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with a* [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] rely on an external [[wiki/concepts/source/basic-metapatterns/layers|transport and deployment layer]] which is usually a framework available off\-the\-shelf:
  - [[wiki/concepts/source/extension-metapatterns/middleware|*Service Mesh*]] is a distributed [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] for highly scalable systems\.
  - [[wiki/concepts/source/extension-metapatterns/middleware|*Message Bus*]] interconnects services that use different communication technologies by translating between their protocols\. It is useful in integration of legacy systems\.
  - [[wiki/concepts/source/extension-metapatterns/middleware|*Event Mediator*]] drives communication in [[wiki/concepts/source/basic-metapatterns/pipeline|*Event\-Driven Architectures*]]\.
  - [[wiki/concepts/source/extension-metapatterns/middleware|*Enterprise Service Bus*]] is an [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrating*]] [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] that unites several historically separate subsystems into an [*Enterprise Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)#enterprise-soa>)\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with a* [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] share a [[wiki/concepts/source/basic-metapatterns/layers|data storage or exchange layer]] and are eligible to implement [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|data\-centric]] domains:
  - [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] simplifies architectural design and makes data synchronization trivial \(see [[wiki/concepts/source/extension-metapatterns/sandwich|*Service\-Based Architecture*]]\)\.
  - [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared File System*]] is among the simplest methods of organizing [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]] for processing large volumes of data records\.
  - [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Memory*]] is the fastest method of data exchange especially suitable for low latency software\.
  - [[wiki/concepts/source/extension-metapatterns/shared-repository|*Data Grid*]] is a highly scalable, distributed in\-memory data store of [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]]\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with* [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] employ several data stores, usually to improve performance by using each data store in the role it is optimized for\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with a* [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] rely on a shared [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] layer to handle [[wiki/concepts/source/basic-metapatterns/layers|communication with clients]]\. Third\-party *Proxies* reliably cover security and networking concerns with very little effort from the programmers’ side\.
- In [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrated Services*]] it is the [[wiki/concepts/source/basic-metapatterns/layers|*use cases*]] which are extracted into a system\-wide layer\. Such subdivision of business logic saves the day when there are many complex system\-wide scenarios while the business rules are specific to particular subdomains\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with an* [[wiki/concepts/source/extension-metapatterns/proxy|*API Gateway*]] implement public\-API\-related tasks – both [[wiki/concepts/source/basic-metapatterns/layers|protocol support]] and [[wiki/concepts/source/basic-metapatterns/layers|basic orchestration]] – in a single component which calls underlying services with the [[wiki/concepts/source/basic-metapatterns/layers|domain logic]]\. This is a simplified architecture for ordinary server\-side systems\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with* [*Backends for Frontends*](<Backends for Frontends (BFF)>) have a layer of client\-specific components that encapsulate clients’ [[wiki/concepts/source/basic-metapatterns/layers|protocols]] and/or [[wiki/concepts/source/basic-metapatterns/layers|scenarios]] and are useful when a system serves drastically different kinds of clients\.


### Hierarchies of services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Hierarchies%20of%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Hierarchies%20of%20Services.png" alt="Diagrams of Cell-Based Architecture and Hierarchical Middleware." loading="lazy" width=100%/>
</a>
</div>

Services are building blocks for a couple of hierarchical architectures used in huge projects:

- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]] is a system of clusters of \(often co\-deployed\) services called [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]]\. Recursive decomposition lowers the top\-level system complexity and decouples the subdomains by making their interdependencies explicit\.
- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchical Middleware*]] interconnects several subsystems of services which belong to different organizations or physical networks\.


### Partially merged services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Partially%20Merged%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Partially%20Merged%20Services.png" alt="Diagrams of Sandwich and Modulith with shared code." loading="lazy" width=73%/>
</a>
</div>

There are systems in\-between [[wiki/concepts/source/basic-metapatterns/services|*Services*]] and [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]:

- In [[wiki/concepts/source/basic-metapatterns/services|*Modulith*]] *with shared code* the business logic is split into subdomains but still relies on a shared codebase\. It is a transitional architecture often seen in growing projects that [explore subdomain boundaries](https://martinfowler.com/bliki/MonolithFirst.html)\.
- In [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] only the [[wiki/concepts/source/basic-metapatterns/layers|*domain logic* layer]], which is usually the largest part of the codebase, is segmented into subdomains\. This is the most natural subdivision for many real\-world systems, which inspires multiple architectures:
  - [[wiki/concepts/source/extension-metapatterns/sandwich|*Service\-Based Architecture*]] – the pragmatic approach to server\-side development – often uses a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] and an [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]]\.
  - [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]] provides unparalleled elasticity and scalability for data\-centric domains with its *replicated cache* called [[wiki/concepts/source/extension-metapatterns/shared-repository|*Data Grid*]]\.
  - [[wiki/concepts/source/extension-metapatterns/sandwich|*Blackboard Architecture*]] schedules specialized algorithms to solve ill\-structured problems\.
  - [[wiki/concepts/source/extension-metapatterns/sandwich|*Nanoservices*]] are independently scalable functions that run in a cloud and share an [[wiki/concepts/source/extension-metapatterns/orchestrator|*\(API\) Gateway*]] and a [[wiki/concepts/source/extension-metapatterns/shared-repository|database]]\.


## Fragmented patterns

Finally, some architectures are subdivided into both layers of abstraction and subdomains, resulting in topologies containing many small components\. This happens when interacting parts of a system vary in their qualities and technologies and thus should stay separate, ordinary decomposition results in components too large for comfortable development, or both\.

### Layers of services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Layers%20of%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Layers%20of%20Services.png" alt="Diagrams of Services with Polyglot Persistence, Services with Backends for Frontends, and Service-Oriented Architecture." loading="lazy" width=100%/>
</a>
</div>

A few topologies are made of layers, each of which is subdivided into services:

- In [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with* [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] there are several specialized data stores with shared access\. This topology may emerge from a [[wiki/concepts/source/appendices/evolutions-of-a-shared-repository|performance optimization]] of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with a* [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] *with* [*Backends for Frontends*](<Backends for Frontends (BFF)>) employ a dedicated [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], or [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]] for each kind of client\. This makes sense when the system's clients have very little in common\.
- [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) features fragmented application, domain, and utility layers, with each component of a higher level calling multiple components from a layer below it\. It enables code reuse, for better or worse, and has reasonably small services even in huge projects but suffers from slow development caused by extensive interdependencies between teams\.


### Layered services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Layered%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Topologies/Layered%20Services.png" alt="Diagrams of Orchestrated Three-Layered Services and Choreographed Two-Layered Services." loading="lazy" width=100%/>
</a>
</div>

More often than not, services are layered internally:

- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Orchestrated Three\-Layered Services*]] distinguish between the [[wiki/concepts/source/basic-metapatterns/layers|*application*]] \(use cases\), [[wiki/concepts/source/basic-metapatterns/layers|*domain*]] \(business rules\), and [[wiki/concepts/source/basic-metapatterns/layers|*persistence*]] \(database\) layers\.
- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Choreographed Two\-Layered Services*]] contain only the [[wiki/concepts/source/basic-metapatterns/layers|*domain*]] and [[wiki/concepts/source/basic-metapatterns/layers|*persistence*]] layers because the [[wiki/concepts/source/basic-metapatterns/layers|*application*]] logic resides in the graph of connections between the services\.


### Hierarchies

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Hierarchy.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Hierarchy.png" alt="Diagrams of Orchestrator of Orchestrators, Middleware of Middlewares, and Services of Services." loading="lazy" width=100%/>
</a>
</div>

Finally, there are [[wiki/concepts/source/fragmented-metapatterns/hierarchy|hierarchical]] topologies with recursive partitioning:

- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top\-Down Hierarchy*]] is arguably the best way to implement a system that involves many kinds of somewhat related entities\. It emerges in domains as diverse as compilers, industrial automation, graphical user interfaces, and online marketplaces\.
- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchical Middleware*]] interconnects subsystems that differ in their communication protocols\.
- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]] splits every large subdomain service into a group of subservices encapsulated with a [[wiki/concepts/source/extension-metapatterns/proxy|*Cell Gateway*]]\. This keeps individual services small without spreading hundreds of them into the system level\.


## Common motifs

Every area of the topologies map highlights certain design principles:

- Small and simple systems may stay cohesive as [[wiki/concepts/source/basic-metapatterns/monolith|*Monoliths*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]]\.
- Medium\-sized software benefits from functional partitioning \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] into [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]\.
- Long\-lived projects become stabilized by extracting any volatile code into expendable modules\. Different applications of this principle yield [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]], [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]], and [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]]\.
- Large software is decomposed into subdomains owned by dedicated teams\. See [[wiki/concepts/source/basic-metapatterns/services|*Services*]] and [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.
- Huge systems require recursive decomposition as found in [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) and [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]\.


Other motifs are harder to notice as they apply to both scaled layered systems and those subdivided into services:

- There is often a *managing layer* that makes use of underlying components:
  - A [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] is an [[wiki/concepts/source/basic-metapatterns/layers|*interface*]] that receives and pre\-processes client input, then forwards the resulting request to whatever is behind it\.
  - An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] is an [[wiki/concepts/source/basic-metapatterns/layers|*application*]] that implements complex use cases which turn a single event or client request into a chain of calls to the lower layer\.
  - [*Backends for Frontends*](<Backends for Frontends (BFF)>) segment a managing layer into client\-specific services\.
- A *platform layer* provides some functionality to other system components:
  - A [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] deploys and [[wiki/concepts/source/basic-metapatterns/layers|interconnects]] [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Replicas*]]\.
  - A [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] stores the system’s [[wiki/concepts/source/basic-metapatterns/layers|data]], offering consistency and persistence\.
  - [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] subdivides a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] layer\.
- [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] wraps [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Replicas*]] with both managing and platform layers\.
- A [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] interconnects any components that use it\.


As we see, [[wiki/concepts/source/introduction/metapatterns|metapatterns]] emerge as archetypes shared among system topologies\.

## Summary

There are many system topologies with various degrees of segregation into layers and subdomains\. No single architecture is a silver bullet, each topology has its use depending on the circumstances\. The following chapters of this book explore archetypes shared among topologies which are called *metapatterns*\.

| \<\< [[wiki/concepts/source/introduction/metapatterns|Metapatterns]] | ^ [[wiki/concepts/source/introduction/introduction|Introduction]] ^ | [[wiki/concepts/source/foundations-of-software-architecture/foundations-of-software-architecture|Foundations of software architecture]] \>\> |
| --- | --- | --- |
