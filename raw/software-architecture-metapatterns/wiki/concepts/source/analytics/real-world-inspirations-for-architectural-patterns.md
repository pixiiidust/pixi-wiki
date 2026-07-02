---
title: "Real world inspirations for architectural patterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/Real-world inspirations for architectural patterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/Real-world%20inspirations%20for%20architectural%20patterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Real world inspirations for architectural patterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/Real-world inspirations for architectural patterns.md`.

As architectural patterns are generally technology\-independent, they must mostly be shaped by the foundational principles of software engineering\. And because the same principles are likely at work at every level of a software system, we may expect similar structures to appear on many levels of software, given similar circumstances – which are not always attainable, for the system\-wide scope \(which means that there are multiple clients and libraries\) and distributed nature \(which deals with faults of individual components\) of many patterns of systems architecture don’t have direct counterparts in smaller single\-process software\. Thus we expect to observe the fractal nature for the more generic patterns while narrowly specialized ones are present at only one or two scopes of software design\.

Another thought to consider is that it’s not in human nature to invent something entirely new – we are much more adept in imitating and combining whatever we see around us\. That is why it’s so hard to find a genuine xenopsychology in literature or movies – to the extent that the eponymous Alien is just an overgrown [parasitoid wasp](https://en.wikipedia.org/wiki/Parasitoid_wasp)\. Hence there is another pathway to pursue – identifying the patterns which we know from software engineering in the world around us, as the authors of \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] did decades ago\.

Let’s go\!

## [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic metapatterns]]

The [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|basic topologies]] lay the foundation for any system by paving ways to *divide* it into components to *conquer* its [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|complexity]]\. We are going to observe them everywhere around us:

### [[wiki/concepts/source/basic-metapatterns/monolith|Monolith]]


![A diagram of Monolith, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Monolith.png)


[[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] stands for encapsulation – we use the thing without looking inside:

- You interact with your dog \(or your smartphone\) through their interface without thinking of their internals\.
- A function exposes its name, arguments and, probably, some comments\. The implementation is hidden from its users\.
- An object has a set of public methods\.
- A module or a library exports several functions for use by its clients\.
- A program is configured through its command line parameters and managed through its [CLI](https://en.wikipedia.org/wiki/Command-line_interface)\. We don’t care how the Linux utilities \(e\.g\. *top* or *cat*\) work – we just run them\.
- A whole distributed system may be [hidden behind](https://comic.browserling.com/full-stack.png) a web page in your browser – and you never imagine its complexity unless you have worked on something of a kind\.


### [[wiki/concepts/source/basic-metapatterns/shards|Shards]]


![A diagram of Shards, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Shards.png)


[[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] is about having multiple instances of something, which often differ in their data:

- A company employs many programmers to accelerate development of its projects\.
- Carrying two mobile phones from different operators fits this pattern as well\.
- This is how they make modern processors more powerful: by adding more cores, not by clocking them faster\.
- Objects in OOP are the perfect example of having multiple instances that vary in their data\.
- Running several shells in Linux is a kind of sharding\.
- A client application of a multi\-user online game is a shard as well\.


### [[wiki/concepts/source/basic-metapatterns/layers|Layers]]


![A diagram of Layered Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Layers.png)


[[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] is the separation of responsibilities between external and internal components:

- In winter we wear soft clothes on our body, a warm sweater over them, and a wind\-proof jacket as the external layer\.
- An object comprises high\-level public methods, low\-level privates, and data\.
- An OS has a UI which runs over user\-space software over an OS kernel over device drivers over the hardware\.
- Your web browser executes a frontend which communicates to a backend which uses a database\.


### [[wiki/concepts/source/basic-metapatterns/services|Services]]


![A diagram of Services, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Services.png)


[[wiki/concepts/source/basic-metapatterns/services|*Services*]] boil down to composition and [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns):

- We have legs, arms, and other narrowly specialized members\.
- A gadget contains specialized chips for the activities which it supports\.
- \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] advocates for an object to incorporate smaller, specialized objects \(*composition over inheritance*\)\.
- Applications often delegate parts of their logic to specialized modules or libraries\.
- An OS dedicates a driver for each piece of hardware installed\. Moreover, it provides many tools to its users – instead of tackling all the user needs within the kernel\.
- \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] describes the way to subdivide a large system into \(hopefully\) loosely coupled components\.


### [[wiki/concepts/source/basic-metapatterns/pipeline|Pipeline]]


![A diagram of Pipeline, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Pipeline.png)


[[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] is about the stepwise transformation of data:

- The pattern got its name from real\-world plumbing\.
- You’ll see similar arrangements in [cellular metabolism](https://en.wikipedia.org/wiki/Metabolism)\.
- It is the foundation of [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|functional programming]]\.
- Linux command line tools are often skillfully chained into pipelines\.
- Hardware is full of pipelines: from [CPU](https://en.wikipedia.org/wiki/Instruction_pipelining) and [GPU](https://en.wikipedia.org/wiki/Graphics_pipeline) to audio and video processing\.
- Finally, a UI wizard passes its users through a series of screens\.


## [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|Extension metapatterns]]

An [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|extension pattern]] encapsulates one or two aspects of the system’s implementation\. It may appear only at the design levels which have those particular aspects:

### [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]]


![A diagram of Services with a middleware, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Middleware.png)


A [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] abstracts scaling and/or intercommunication:

- The network of post offices is a middleware – you push a letter into a mailbox and it automagically appears at its destination’s door\.
- A [bus depot](https://en.wikipedia.org/wiki/Bus_depot) may mean a bus garage which deploys as many buses as needed to service the traffic or a bus station where people come to have a ride, regardless of the exact vehicle model they’ll take\.
- Hardware is full of another kind of [buses](https://en.wikipedia.org/wiki/Bus_(computing)) that unify means of communication\.
- TCP and UDP sockets hide the details of the underlying network\.
- A distributed [[wiki/concepts/source/basic-metapatterns/services|actor framework]] allows an actor to address another actor without knowing where it is deployed\.


### [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]


![A diagram of Services with a shared repository, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Shared%20Repository.png)


A [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] provides data storage and/or data change notifications:

- Everybody in the room may use a ~black~whiteboard to express and exchange their ideas\.
- An Internet forum works in a similar way – people post their arguments there for others to see them and get notified on answers\.
- RAM and CPU caches are kinds of shared repositories\. CPU caches are [kept synchronized through notifications](https://en.wikipedia.org/wiki/Cache_coherency_protocols_(examples))\.
- [*Observer*](https://refactoring.guru/design-patterns/observer) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] is about getting notified when a shared object changes\.
- Services or service instances may share a database\.


### [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]


![A diagram of Services with a proxy, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Proxy.png)


A [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] isolates a system from its environment by translating between the internal and external protocols and/or implementing generic aspects of communication:

- You may need a translator to understand foreign people or have a secretary to deal with routine tasks\. A local guide combines both roles\.
- An adapter makes several hardware plugs \(or software frameworks\) mutually interoperable\.
- Your Wi\-Fi router is a proxy between your laptop and the Internet\.
- A compiler is a kind of a proxy between source code and bytecode\.


### [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]


![A diagram of Services with an orchestrator, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Orchestrator.png)


An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] integrates several components by implementing high\-level use cases and/or keeping the components in sync:

- A taxi driver orchestrates their car’s internals\.
- A [*Facade*](https://refactoring.guru/design-patterns/facade) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] provides a high\-level interface for a system while a [*Mediator*](https://refactoring.guru/design-patterns/mediator) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] integrates a system by spreading the changes initiated by the system’s components\.
- A linker composes a working program out of disjunct modules\.


### [[wiki/concepts/source/extension-metapatterns/sandwich|Sandwich]]


![A diagram of Sandwich Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Sandwich.png)


In [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] a varied and segmented layer with the most valuable code is operated and held in place by other, cohesive layers:

- A sandwich is an obvious example\.
- This is how we make down jackets and thermal insulation in general\.
- A [cell membrane](https://en.wikipedia.org/wiki/Cell_membrane) which includes many transporters and receptors looks exactly like that\.


## [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Fragmented metapatterns]]

A [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|fragmented topology]] uses small specialized components to approach a case which is hard to resolve with more generic means\. The high degree of specialization limits the number of available examples:

### [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]]


![A diagram of Services with Polyglot Persistence, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Polyglot%20Persistence.png)


[[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] is about having multiple containers for data:

- A warehouse or a cargo ship has dedicated storage areas with separate facilities for combustible, toxic, and frozen goods\.
- A computer has CPU caches, RAM, flash, and hard drives for temporary or permanent data storage\.
- There are map, list, and array – each with its pros and cons\. A large class would often use two or three kinds of containers, and not without reason\.


### [Backends for Frontends](<Backends for Frontends (BFF)>)


![A diagram of Services with Backends for Frontends, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Backends%20for%20Frontends.png)


[*Backends for Frontends*](<Backends for Frontends (BFF)>) is about treating different kinds of clients individually:

- A bank is likely to reserve a couple of employees to serve rich clients\.
- A Wi\-Fi router has many management interfaces: web, mobile application, CLI, and probably [TR\-069](https://en.wikipedia.org/wiki/TR-069)\.
- A multiplayer game may provide both desktop and mobile client applications\.


### [Service\-Oriented Architecture](<Service-Oriented Architecture (SOA)>)


![A diagram of Service-Oriented Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Service-Oriented%20Architecture.png)


[*SOA*](<Service-Oriented Architecture (SOA)>) applies OOP techniques, including component reuse, to deal with complex systems:

- That’s what you have inside your car\. Many of its internals rely on the car’s battery for power supply instead of having a small battery installed inside every component\.
- Cities are built in the same way – schools, markets, and railways serve multiple houses\.
- It’s the same with user space of operating systems: there is a shared UI framework which interfaces with as\-many\-as\-needed applications, each of which calls shared libraries \(DLLs\)\.


### [[wiki/concepts/source/fragmented-metapatterns/hierarchy|Hierarchy]]


![A diagram of Hierarchy, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Hierarchy.png)


[[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] distributes system’s complexity over multiple levels:

- This is how large companies and armies are managed\.
- Large projects [[wiki/concepts/source/analytics/cohesers-and-decouplers|are made]] of services which contain modules which contain classes which contain methods\.


## [[wiki/concepts/source/implementation-metapatterns/implementation-metapatterns|Implementation metapatterns]]

An [[wiki/concepts/source/implementation-metapatterns/implementation-metapatterns|implementation metapattern]] highlights the peculiar internal arrangements of a component\. Such patterns are deeply specialized:

### [[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]]


![A diagram of Plugins Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Plugins.png)


[[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] make a component’s behavior flexible through delegating its parts to small external additions:

- This is how we use tools for our work – a man becomes a digger when given a shovel\.
- [*Strategy*](https://refactoring.guru/design-patterns/strategy) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] is the thing\.


### [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal Architecture]]


![A diagram of Hexagonal Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Hexagonal%20Architecture.png)


[[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] protects the internals of a system from its environment:

- A drill or a screwdriver has replaceable bits\.
- A living cell is encapsulated by its [membrane](https://en.wikipedia.org/wiki/Cell_membrane) and relies on [protein adapters](https://en.wikipedia.org/wiki/Membrane_protein) for interactions with its environment\. [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|A kind of *Hexagonal Architecture*]] was named after it\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*OS Abstraction Layer* and *Hardware Abstraction Layer*]] in embedded systems or [[wiki/concepts/source/extension-metapatterns/proxy|*Anti\-Corruption Layer*]] in \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] are all about that\.
- The [*impure/pure/impure sandwich*](https://blog.ploeh.dk/2020/03/02/impureim-sandwich/) of functional programming is closely related\. Here also, the core of the system cannot change anything outside of itself directly \(any external communication relies on *adapters*\) and it is [deterministic if single\-threaded](http://ithare.com/chapter-vc-modular-architecture-client-side-on-debugging-distributed-systems-deterministic-logic-and-finite-state-machines/)\.


### [[wiki/concepts/source/implementation-metapatterns/microkernel|Microkernel]]


![A diagram of Microkernel, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Microkernel.png)


[[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] shares the goods of resource providers among resource users:

- It’s like a bank that takes money from the rich to distribute them among the poor\.
- This is what an OS is for\. Its scheduler shares the CPU, the memory subsystem shares RAM, while the device drivers provide access to the peripherals\.
- Cloud services are based on sharing computational resources among clients\.


### [[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]]


![A diagram of Services over a mesh, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Mesh.png)


[[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] resembles grassroots movements – self\-organization and survival through redundancy:

- Ants and bees are small, autonomous, and efficient\. Their strength comes from their numbers\.
- Road networks and power grids don’t collapse if some of their components are damaged as they are highly redundant\.
- Torrents, mobile communications, and the Internet infrastructure are known for their robustness\.


## Summary

Architectural patterns have parallels in the natural world, our society and/or different levels of computer hardware and software\. Learning about them helps us feel the driving forces behind the patterns and be more flexible and creative in both using the patterns which we already know and in devising new ones\.

| \<\< [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|Architecture and product life cycle]] | ^ [[wiki/concepts/source/analytics/analytics|Analytics]] ^ | [[wiki/concepts/source/analytics/the-heart-of-software-architecture|The heart of software architecture]] \>\> |
| --- | --- | --- |
