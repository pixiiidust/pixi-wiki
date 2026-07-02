---
title: "Deconstructing patterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/The heart of software architecture/Deconstructing patterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/The%20heart%20of%20software%20architecture/Deconstructing%20patterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Deconstructing patterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/The heart of software architecture/Deconstructing patterns.md`.

Imagine a dungeon with dragons\. It is made of halls connected by tunnels\. Each hall is *cohesive*\. Tunnels are narrow interfaces that *decouple* them\. A hall is amorphous – it can have any shape but it cannot open to another hall except through a tunnel – such are the rules of the game\. The tunnels both restrict the freedom of the halls and interconnect them\.

## SOLID principles

If *cohesion* and *decoupling* dictate software architecture, they should surface in its principles\. Let’s take a look at [SOLID](https://en.wikipedia.org/wiki/SOLID):

- The *single responsibility principle*, also known as [*do one thing and do it well*](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well), is a general advice for keeping unrelated functionality decoupled\.
- The *open\-closed principle* and *Liskov substitution principle* decouple the logic of the parent class or the code that uses it, respectively, from the functionality of its subclasses\.
- The *interface segregation principle* decouples independent parts of an object’s interface\.
- The *dependency inversion principle* decouples an object’s users from its implementation\.


Please beware that each of those principles in and of themselves invokes decoupling which is not free – your software may end up having too many moving parts and strict rules to remain easy to read and support\.

> When we choose between cohesion and decoupling, we choose between a single component and a pair of components connected through a constraint rule\. The more decoupling, the more components and rules we have to handle\. Sooner, rather than later, the number of individual components and rules will overwhelm any developer\.

## Gang of Four patterns

Let’s now discuss something more practical, namely the \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] [patterns](https://en.wikipedia.org/wiki/Design_Patterns#Patterns_by_type) which seem to be ingenious, yet hacky, ways for rearranging the roles in your code\. They override ordinary OOP rules, which is useful when you need extra flexibility\. For example, the *creational patterns* interfere with the normally cohesive *select type – create – initialize – use* sequence of operating an object\.

Some patterns provide a basic decoupling:

- [*Adapter*](https://refactoring.guru/design-patterns/adapter) translates between two interacting components so that they may evolve independently\.
- [*Observer*](https://refactoring.guru/design-patterns/observer) decouples an event from the reactions which it causes by registering the event handlers at runtime\.
- [*Chain of Responsibility*](https://refactoring.guru/design-patterns/chain-of-responsibility) separates the method invocation from the method execution\. A client’s calling a method of an object runs the corresponding method of another object\.


Others break the functionality or data of a class into two or more parts, juggling them at runtime:

- [*Proxy*](https://refactoring.guru/design-patterns/proxy) separates an object’s representation from its implementation, enabling lazy loading or remote access\.
- [*Flyweight*](https://refactoring.guru/design-patterns/flyweight) extracts an immutable data member of a class and merges multiple instances of that identical data to save memory\.
- [*Strategy*](https://refactoring.guru/design-patterns/strategy) and [*Decorator*](https://refactoring.guru/design-patterns/decorator) decouple a dimension of an object’s functionality to allow runtime changes in or composition of the object's behavior, respectively\.
- [*State*](https://refactoring.guru/design-patterns/state) separates an object’s behavior into multiple classes based on the object’s current state\.
- [*Template Method*](https://refactoring.guru/design-patterns/template-method) decouples several aspects of a class’s behavior from its main algorithm and envelops the variations of those aspects into subclasses\.
- [*Bridge*](https://refactoring.guru/design-patterns/bridge) separates a high\-level hierarchy of classes from their low\-level implementation details which may comprise an orthogonal hierarchy\.
- [*Memento*](https://refactoring.guru/design-patterns/memento) decouples the lifetime of an object’s state from the object itself\.


On the other hand, several patterns gather separate components together:

- [*Command*](https://refactoring.guru/design-patterns/command) collects all the data required to call a method\.
- [*Mediator*](https://refactoring.guru/design-patterns/mediator) is a cohesive implementation of multi\-object use cases\.
- [*Composite*](https://refactoring.guru/design-patterns/composite) and [*Facade*](https://refactoring.guru/design-patterns/facade) represent multiple objects as a cohesive entity\. A *Composite* broadcasts a call made to its interface to every object which it contains, while a *Facade* [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestrates]] the subsystem which it wraps\.
- [*Abstract Factory*](https://refactoring.guru/design-patterns/abstract-factory) and [*Builder*](https://refactoring.guru/design-patterns/builder) encapsulate *type selection* and *initialization* for several related hierarchies, so that the client code gets objects from a consistent set of types\. On top of that, a *Builder* cross\-links the objects it creates into a cohesive subsystem, which is then returned to the *builder*’s client as a whole\.


The remaining patterns pick an aspect or two of an object’s behavior and move them elsewhere:

- [*Iterator*](https://refactoring.guru/design-patterns/iterator) moves the code for traversal of a container’s elements from the container’s clients into the container’s implementation, decoupling the clients from the iteration algorithm\.
- [*Visitor*](https://refactoring.guru/design-patterns/visitor) aggregates the actions that a client needs to perform on each kind of object in a hierarchy, decoupling them from the classes that constitute the hierarchy\.
- *Interpreter* decouples client scenarios from the rest of the system by having them written in a dedicated language and run in a protected environment\.
- [*Prototype*](https://refactoring.guru/design-patterns/prototype) binds the *type selection* and *initialization* together and decouples them from the object *creation*\.
- [*Singleton*](https://refactoring.guru/design-patterns/singleton) binds the *creation* and *initialization* of a global object to every call of its methods\.
- [*Factory Method*](https://refactoring.guru/design-patterns/factory-method) decouples the *initialization* from *type selection* and hides both from the class’s users\.


As we see, every \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] pattern boils down to binding \(making *cohesive*\) and/or separating \(*decoupling*\) some kind of functionality or responsibilities\.

## Architectural metapatterns

Finally, let’s close the book by iterating over the metapatterns and looking into their roots through the lens of unification and separation\.


![Diagrams of Monolith, Shards, Layers, Services, and Pipeline, with cohesive and decoupled components highlighted.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Heart/Basic.png)


[[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic architectures]]:

- [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] keeps everything together for quick and dirty projects:
  - Total *cohesiveness* results in low latency, cost\-efficient performance, and easy debugging\.
- [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] slice a large\-scale application into multiple instances:
  - *Decoupling* the instances enables scaling but sacrifices the consistency of shared data\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] separate the high\-level code from the low\-level implementation:
  - *Cohesion* within a layer makes it easy to implement and debug\.
  - *Decoupled* layers may vary among themselves in technologies and properties, but are somewhat slower and hard to debug in\-depth\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] divide a complex system into subdomains:
  - *Cohesiveness* within a service keeps it simple and efficient when it does not need to consult with other services\.
  - *Decoupling* enables the development of larger codebases by multiple specialized teams but any global use cases become complicated\.
- [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] segregates data processing into self\-contained steps:
  - *Decoupling* simplifies reassembling or expanding the system but increases its latency\.



![Diagrams of Services with a middleware, Services with a shared repository, Services with a proxy, Services with an orchestrator, and Sandwich, with cohesive and decoupled components highlighted.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Heart/Extension.png)


[[wiki/concepts/source/extension-metapatterns/extension-metapatterns|Grouping related functionality]]:

- [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] separates the implementation of communication and/or instance management from the business logic:
  - The *cohesive* communication layer is not only reliable, but also uniform, which makes it easy to learn\.
  - *Decoupling* the communication concerns from the business logic simplifies the latter\.
- [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] dissociates data from code, enabling [[wiki/concepts/source/foundations-of-software-architecture/shared-data|data\-centric programming]]:
  - *Cohesive* data is consistent and easy to handle\.
  - *Decoupled* business logic can be scaled or subdivided [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|independently]] of the data\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] mediates between a system and its clients, taking care of some aspects of their communication:
  - A *cohesive* edge component is easier to manage and secure\.
  - *Decoupling* generic aspects simplifies the business logic but usually increases latency\.
- [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] collects a multitude of complex use cases into a dedicated layer:
  - *Cohesive* use cases are easy to comprehend and debug\.
  - *Decoupling* the [[wiki/concepts/source/basic-metapatterns/layers|use cases]] from the [[wiki/concepts/source/basic-metapatterns/layers|domain logic]] allows for variation in technologies but increases latency and complicates in\-depth debugging\.
- [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] distantiates both control and data from the domain rules, which become segmented:
  - *Cohesive* use cases and data integrate the system\.
  - *Decoupling* the subdomain components from each other and from the system\-wide layers keeps every part of the system reasonably small and independent\.



![Diagrams of Layered Services, Services with Polyglot Persistence, Backends for Frontends, Service-Oriented Architecture, and Top-Down Hierarchy, with cohesive and decoupled components highlighted.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Heart/Fragmented.png)


[[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Decoupled topologies]]:

- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]] first decouple the subdomains, and then the layers within each subdomain:
  - *Decoupled* subdomains allow for multi\-team development and large codebases but complicate global use cases\. *Decoupled* layers enable variation in technologies within a subdomain and [[wiki/concepts/source/foundations-of-software-architecture/orchestration|limit interdependencies]] between subdomains to a single layer\.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] divides data among multiple data stores:
  - *Decoupling* improves performance through data store specialization at the cost of consistency\.
- [*Backends for Frontends*](<Backends for Frontends (BFF)>) dedicate one or two components \(a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] and/or [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\) to each kind of client\.
  - *Decoupling* allows for customization on a per\-client\-type basis but makes it hard to share functionality among the clients\.
- [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) first segregates a large system into layers, then subdivides each layer into services:
  - *Decoupling* layers strangely enables reuse as any component of an upper layer can access every component below it\. *Decoupling* services within the layers allows for multi\-team development\. Drawbacks include high latency, system complexity, and interdependencies\.
- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] recursively separates general and specialized logic, tackling complexity:
  - *Cohesive* general and subdomain\-specific business logic helps readability and debugging\.
  - *Decoupled* layers and subdomains allow for modification and expansion of local functionality at the cost of performance\.



![Diagrams of Plugins, Hexagonal Architecture, Microkernel, and Mesh, with cohesive and decoupled components highlighted.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Heart/Implementation.png)


[[wiki/concepts/source/implementation-metapatterns/implementation-metapatterns|Component implementation]]:

- [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] separate customizable aspects of a system’s behavior:
  - *Decoupling* several aspects of a system allows for it to be fine\-tuned but requires careful design and may lower performance\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] isolates the business logic from its external dependencies:
  - *Decoupling* protects from vendor lock\-in and supports automatic testing at the cost of lost optimization opportunities\.
- [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] mediates between resource consumers and resource producers:
  - *Cohesive* resource management optimizes resource usage\.
  - *Decoupling* allows for seamless replacement of resource providers\.
- [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] aggregates distributed components into a virtual layer:
  - Virtual *cohesion* hides the complexity of distributed communication from the client code\.
  - Actual *decoupling* \(distribution\) of the nodes enables scaling and fault tolerance\.


| \<\< [[wiki/concepts/source/analytics/cohesers-and-decouplers|Cohesers and decouplers]] | ^ [[wiki/concepts/source/analytics/the-heart-of-software-architecture|The heart of software architecture]] ^ | [[wiki/concepts/source/analytics/choose-your-own-architecture|Choose your own architecture]] \>\> |
| --- | --- | --- |
