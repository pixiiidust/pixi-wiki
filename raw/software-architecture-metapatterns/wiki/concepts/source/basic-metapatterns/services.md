---
title: "Services"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Basic metapatterns/Services.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Basic%20metapatterns/Services
source_license_note: "See namespace README; preserve attribution and source links."
---

# Services

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Basic metapatterns/Services.md`.


![A diagram for Services, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Services.png)


*Divide and conquer.* Scale development through decoupling subdomains.

<ins>Known as:</ins> Services, Domain Services \[[wiki/concepts/source/appendices/books-referenced|[FSA]] and [[wiki/concepts/source/appendices/books-referenced|SAHP]], [[wiki/concepts/source/analytics/ambiguous-patterns|but not]] [[wiki/concepts/source/appendices/books-referenced|DDD]]\], Modules \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\].

<ins>Structure:</ins> A component per subdomain.

<ins>Type:</ins> System topology.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Supports large codebases | Global use cases are hard to debug |
| Multiple development teams and technologies | Poor latency in global use cases |
| Forces may vary by subdomain | No good way to share state between services |
|  | The domain structure should never change |
|  | Operational complexity |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] has a chapter on *Service-Based Architecture*; \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] is dedicated to *Microservices*.

Splitting a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] by *subdomain* allows for mostly independent properties, development, and deployment of the resulting components (distributed *services* or colocated *modules*). However, for the system to benefit from the division, its subdomains must be loosely coupled and, ideally, of comparable size. In that case the partitioning can reduce complexity of the project’s code by cutting accidental dependencies between the subdomains. Moreover, if one of the resulting services grows unmanageably large, it can often be further partitioned by sub-subdomains to form a [*Cell*](#cell-wso2-definition-service-of-services-domain-uber-definition-cluster). This flexibility is paid for through the complexity and performance of use cases which involve multiple subdomains. Another issue to remember is that boundaries between services are [nearly impossible](https://martinfowler.com/bliki/MonolithFirst.html) to move at later project stages as the services grow to vary in technologies and implementation styles, thus separation into services assumes perfect practical knowledge of the domain and relatively stable requirements.

> [Research](https://www.qsm.com/team-size-can-be-key-successful-software-project) shows that when more than five programmers work on the same subject, their performance degrades. Therefore, if we want our employees to be efficient, they should be grouped into small teams and each team should be given ownership of a dedicated component.

### Performance

Interservice communication is relatively slow and resource-consuming, therefore it should be kept to a minimum.


![Performance of Services is the best when the request is limited to a single service and the worst when the state of several services needs to be synchronized.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Services.png)


The perfect case is when a single service has enough authority to answer a client’s request or process an event. That case should not be that rare as a service often covers a whole subdomain while subdomains are expected to be loosely coupled (by definition).

Worse is when an event starts a chain reaction throughout the system, likely looping back a response to the original service or changing the target state of another controlled subsystem.

In the slowest scenario a service needs to synchronize its state with multiple other services, usually via *locks* and *distributed transactions*.

Multiple [[wiki/concepts/source/basic-metapatterns/shards|instances]] of an individual service may be deployed to improve throughput of the system. However, that will likely need a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] or [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] to distribute interservice requests among the instances and a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] to store and synchronize any non-shardable (accessed by several instances) state.

### Dependencies

When we see a service to *request* help from other services and then receive the results (in a *confirmation* message), that service [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrates*]] the services it uses. Services often orchestrate each other because the subdomain a service is dedicated to is not independent of other subdomains.


![With request/confirm a service depends on whatever it uses.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Services-1.png)


Another way for services to communicate is [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]] – when a service sends a *command* or publishes a *notification* and does not expect any response. This is characteristic of [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]] which are covered in the next chapter. Right now we should note that orchestration and choreography may be intermixed, in which case a service depends on all the services it uses or subscribes to.


![With pub/sub a service depends on its notification sources.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Services-2.png)


If the system relies on notifications (services publish *domain events*), it is possible to avoid interservice *queries* (pairs of a *read* request and confirmation with the data retrieved) by aggregating data from notifications in a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS* (or *materialized*) *View*]], which can reside [in memory](https://martinfowler.com/bliki/MemoryImage.html) or in a database. Views can be planted inside every service that needs data owned by other services or can be gathered into a dedicated [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]]. Though the main goal of *CQRS Views* is to resolve distributed joins from databases of multiple services, they also help [[wiki/concepts/source/analytics/indirection-in-commands-and-queries|remove dependencies]] in the code of services and optimize out interservice queries, simplifying APIs and improving performance. Further examples will be discussed in the chapter on [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]].


![A CQRS view breaks dependencies between services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Services-3.png)


In general, a large service should wrap its dependencies with an [[wiki/concepts/source/extension-metapatterns/proxy|*Anticorruption Layer*]], following the ideas of [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]. The layer consists of [*Adapters*](https://refactoring.guru/design-patterns/adapter) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] between the internal domain model of the service and the APIs of the components it uses. The *Adapters* isolate the business logic from the external environment, granting that no change in the interface of an external service or library may ever take much work to support on the side of the team that writes its own business logic as all the ensuing updates are limited to a small adapter.


![Adapters isolate a service from its dependencies.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Services-4.png)


### Applicability

*Services* are <ins>good</ins> for:

- *Large projects.* With multiple services developed independently, a project may grow well above 1 000 000 lines of code and still be comfortable to work on as every team needs to know only the medium-sized component it owns.
- *Specialized teams.* Each service would often be written and supported by a dedicated team that invests its time in learning its subdomain. This way no one needs to have a detailed knowledge of the full set of requirements, which is next to impossible in large domains.
- *Varied forces*. In systems and embedded programming, components of wildly varying behaviors need to be managed. Each of them is controlled by a dedicated service (called *driver*) which adapts to the specifics of the managed subsystem.
- *Flexible scaling.* Some services may be under more load than others. It makes sense to deploy multiple instances of heavily loaded services.


*Services* <ins>should be avoided</ins> in:

- *Cohesive domains.* If everything strongly depends on everything, any attempt to cut the knot with interfaces is going to [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|make things worse]] unless the project is already dying because of its huge codebase, in which case you have little to lose.
- *Unfamiliar domains*. If you don’t understand the intricacies of the system you are going to build, you may [misalign the interfaces](https://martinfowler.com/bliki/MonolithFirst.html) and, by the time that the mistakes come to light, the architecture will be too hard to change \[[wiki/concepts/source/appendices/books-referenced|[LDDD]]\]. The coupled *Services* you get may actually be worse than a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]].
- *Quick start*. It takes effort to design good interfaces and contracts for *Services* and managing multiple deployment units is not free of trouble. Debugging will also be an issue.
- *Low latency*. If the system as a whole needs to react to events in real time, complex services should be avoided. Nevertheless, an individual service can provide low latency for local use cases (when a single service has enough authority to react to the incoming event), wherefore [simple non-blocking actors](#asynchronous-modules-modular-monolith-modulith-embedded-actors) are widely used in [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|control software]].


### Relations


![Splitting an Orchestrator into Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Services.png)


- Division by subdomain can be applied to [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] to form [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] (partial subdivision) or [*Service-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) (layers of services); to [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], or [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]] to make [*Backends for Frontends*](<Backends for Frontends (BFF)>); to a [[wiki/concepts/source/extension-metapatterns/shared-repository|(shared) database]] resulting in [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]].
- Services can be extended with a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]], or [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]].
- Each service can be implemented by [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] (making a [[wiki/concepts/source/fragmented-metapatterns/layered-services|*layered service*]]), [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]], or a [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]].


## Variants by isolation

Division by subdomain is so commonplace that no universal terminology has emerged over the years. Below is my summary, in no way complete, of several ways such systems can vary. Each section lists the well-known architectures it applies to.

First and foremost, there are multiple stages between a cohesive [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] and distributed *Services*. You should be careful to stop these incremental changes as soon as the benefits of the next step (color-coded below) don’t outweigh its drawbacks for your project.

> I review here only the most common options while a few more esoteric architectures are found in [Volodymyr Pavlyshyn’s overview](https://volodymyrpavlyshyn.medium.com/monoliths-microlith-moduliths-self-contained-systems-a-system-of-systems-nano-services-cf3e9e1869c0).

### Synchronous modules: Modular Monolith (Modulith)

The first step to take when designing a large project is the division of its codebase into loosely coupled modules that match subdomains (*bounded contexts* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]). If successful, that parallelizes development to a team per module while the entire application still runs in a single process, thus it stays easy to debug, the modules can share data, and any crash kills the whole system (meaning that you don’t need to take care of partial failures). You pay by establishing boundaries which will not be easy to move in the future.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Multi-team development | Subdomain boundaries are settled |

### Asynchronous modules: Modular Monolith (Modulith), Embedded [Actors](#actors)

The next stage is separating the modules’ execution threads and data. Each module becomes a kind of [*actor*](https://en.wikipedia.org/wiki/Actor_model) that communicates with other components through messaging. Now your modules don’t block each other’s execution and you can [replay events](http://ithare.com/chapter-vc-modular-architecture-client-side-on-debugging-distributed-systems-deterministic-logic-and-finite-state-machines/) at the cost of nightmarish debugging and no clean way to share data between or synchronize the state of the components.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Multi-team development | Subdomain boundaries are settled |
| Event replay | No good way to share data or synchronize state |
| Some independence of module qualities | Hard to debug |

### Multiple processes

There is also the option of running system components as separate binaries which lets them vary in technologies, allows for granular updates, and addresses stability (a web browser does not stop when one of its tabs crashes). But it adds a whole new dimension of painful error recovery that includes partially executed scenarios. Moreover, if the technologies of the components diverge, it is impossible to move code between them.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Multi-team development | Subdomain boundaries are frozen |
| Event replay | No good way to share data or synchronize state |
| Independence of component qualities and technologies | Hard to debug |
| Single-component updates | Needs error recovery routines |
| Software fault isolation | Data inconsistencies after partial crashes |
| Limited granular scalability |  |

### Distributed runtime: Backend [Actors](#actors)

Modern distributed [runtimes](https://en.wikipedia.org/wiki/Runtime_system) create virtual namespaces that can be deployed on a single machine or over a network. They may redistribute running components among servers in a way to minimize network communication and may offer distributed debugging. With [*Actors*](https://en.wikipedia.org/wiki/Actor_model), if one of them crashes, that generates a message to another actor which may decide on how to handle the error. The convenience of using a runtime has the dark side of vendor lock-in.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Multi-team development | Subdomain boundaries are frozen |
| Event replay | No good way to share data or synchronize state |
| Independence of component qualities ~and technologies~ | Hard to debug |
| Single-component updates | Needs error recovery routines |
| Full fault isolation | ~Data inconsistencies after partial crashes~ |
| Full dynamic granular scalability | Vendor lock-in |
|  | Moderate communication overhead |
|  | Moderate performance overhead caused by the framework |

### Distributed services: Service-Based Architecture, Space-Based Architecture, Microservices

Fully autonomous services run on dedicated servers or virtual machines. This way you employ resources of multiple servers, but the communication between them is both unstable (requests may be lost, reordered or duplicated) and slow and debugging tends to be very hard. [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]-based ([[wiki/concepts/source/implementation-metapatterns/mesh|*Microservices*]] and [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based*]]) architectures provide dynamic scaling under load.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Multi-team development | Subdomain boundaries are frozen |
| Event replay | No ~good~ way to share data or synchronize state |
| Independence of component qualities and technologies | Very hard to debug |
| Single-component updates | Needs error recovery routines |
| Full fault isolation | Data inconsistencies after partial crashes |
| Full (dynamic for *Mesh*) granular scalability | High communication overhead |

## Variants by communication

Services also differ in the way they communicate which influences some of their properties:

### Direct method calls

When components run inside the same process and share execution threads, one component can call another. That is blazingly fast and efficient, but you should take care to protect the module’s state from simultaneous access by multiple threads (and yes, [*deadlocks*](https://en.wikipedia.org/wiki/Deadlock_(computer_science)) do happen in practice). Moreover, it is hard to know what the module you call is going to call in its turn, while you are waiting on it – thus no matter how much you optimize your code, its performance depends on that of other components, often in subtle ways.

### RPCs and commands (request/confirm pairs)

If a service [calls another service](https://en.wikipedia.org/wiki/Remote_procedure_call) or requests it to act and return results (this is how method calls are implemented in distributed systems) it has to store the state of the scenario it is executing for the duration of the call (until the confirmation message is received). That uses resources: the stored state is kept in RAM and the interruption and resumption of the execution wastes CPU cycles on context switch and on the resulting cache misses. Blocked [[wiki/concepts/source/basic-metapatterns/monolith|threads]] are especially heavy while [[wiki/concepts/source/basic-metapatterns/monolith|coroutines or fibers]] are more lightweight but are still not free.

Another trouble with distributed systems comes from error recovery: if your component did not receive a timely response, you don’t know if your request was (or is being, or will be) executed by its target – and you need to be really careful about possible data corruption if you retry it and it is executed twice \[[wiki/concepts/source/appendices/books-referenced|[MP]]\].

> If a request is duplicated (as a slow network, overloaded service, or lost confirmation may cause a retry), it is important to make sure that the second (or parallel) execution of the request does not change the system’s data. This is achieved either by using [*idempotent*](https://en.wikipedia.org/wiki/Idempotence#Computer_science_examples) logic (which is based on assignment instead of increasing or decreasing values in place), or by writing the id of the last processed message to the database (and checking that the incoming message’s id is greater than the one found in the database) \[[wiki/concepts/source/appendices/books-referenced|[MP]]\].

On the bright side, [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]] is human- and debugger-friendly as it keeps consecutive actions close together in the code. Therefore, synchronous interaction is still the default mode of communication in many projects.

### Notifications (pub/sub) and shared data

A service may do its part, then publish a notification or [[wiki/concepts/source/foundations-of-software-architecture/shared-data|write results to a shared data store]] for other services to process, and finally forget about the task as it has completed its role. [[wiki/concepts/source/foundations-of-software-architecture/choreography|*Choreography*]] is resource-efficient, but you need to find and read multiple pieces of code which are spread out over several services to understand or debug the whole use case.

### (inexact) No communication

Finally, some kinds of services, namely [*device drivers*](#inexact-device-drivers-pedestal) and [*Nanoservices*](#inexact-nanoservices-api-layer), never communicate with each other. Strictly speaking, such services don’t make a system – instead, they are isolated *Monoliths* which are managed by a higher-level component (OS kernel for drivers, client or a [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] for *Nanoservices*).

Nevertheless, it is a fun fact that if the services don’t intercommunicate, the main drawbacks of the *Services* architecture disappear:

- There is no slow and error-prone interservice communication (they never communicate!).
- It’s not hard to debug multi-service use cases (there are no such scenarios!).
- The services don’t corrupt data on crash (there are no distributed transactions).


## Variants by size

Last but not least, the simplest classification of subdomain-separated components is by their size:

### Whole subdomain: [[wiki/concepts/source/extension-metapatterns/sandwich|(Sub-)Domain Services, Macroservices]]

Each *Domain Service* \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] (*Macroservice*) of [*Service-Based Architecture*](#service-based-architecture-sba-macroservices) implements a whole subdomain. It is the product of the full-time work of a dedicated team. A project is unlikely to have more than a dozen of such services (in part because the number of top-level subdomains in any domain is usually limited).

### Part of a subdomain: [Microservices](#microservices)

*Microservices* enthusiasts estimate the optimal size of a component of their architecture to be below a month of development by a single team. That allows for a complete rewrite instead of refactoring in case the requirements change. When a team completes one microservice it can start working on another, probably related, one while still maintaining its previous work. A system of *Microservices* is likely to contain from tens to few hundreds of them.  Some projects will cluster these into [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]].

### Class-like: [Actors](#actors)

An [*actor*](https://volodymyrpavlyshyn.medium.com/actors-actor-systems-as-massively-distributed-scalability-architecture-5e40f5ea9e86) is an object with a message-based interface. They are used correspondingly. Though the size of an actor may vary, as does the size of an OOP class, it is still very likely to be written by a single programmer.

### Single function: FaaS, Nanoservices

A [*nanoservice*](https://medium.com/@ido.vapner/unlocking-the-power-of-nano-services-a-new-era-in-microservices-architecture-22647ea36f22) is a single function ([FaaS](https://en.wikipedia.org/wiki/Function_as_a_service) \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\]) usually deployed to a *serverless* provider. Nanoservices are used as API method handlers or as building blocks for [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]].

## Variants by internal structure

A service is not necessarily monolithic inside. Because a service is encapsulated from its users by its interface, it can have any kind of internal structure. The most common cases, which can be intermixed together, are:


![A monolithic service, layered service, hexagonal services, scaled service, and a Cell interconnected into a single system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Subtypes%20of%20Services.png)


### [[wiki/concepts/source/basic-metapatterns/monolith|Monolithic]] service


![A diagram of a monolithic component.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Service%20-%20Monolithic.png)


A *monolithic service* is a service with no definite internal structure, probably small enough to allow for complete rewrite instead of refactoring – the ideal of proponents of [*Microservices*](#microservices). It is [simple & stupid](https://en.wikipedia.org/wiki/KISS_principle) to implement but relies on external sources of persistent data. For example, *device drivers* and [*actors*](#actors) usually get their (persisted) configuration during initialization. A monolithic backend service may receive all the data it needs in incoming requests, via a query to another service, or by reading it from a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]].

### [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal]] service


![A core connected to: a protocol adapter, a Database Abstraction Layer with a database behind it, and an adapter with a library behind it.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Service%20-%20Hexagonal.png)


A *hexagonal service* has its external dependencies isolated behind vendor-agnostic interfaces.

This is a real-world application of [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] which both ensures that the business logic does not depend on specific technologies and protects from vendor lock-in. It is highly recommended for long-lived projects.

### [[wiki/concepts/source/basic-metapatterns/shards|Scaled]] service


![Stateless instances between a load balancer and a database; stateful shards behind a sharding proxy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Service%20-%20Scaled.png)


With *scaled services* there are multiple [[wiki/concepts/source/basic-metapatterns/shards|*instances*]] of a service. In most cases they [[wiki/concepts/source/extension-metapatterns/shared-repository|*share a database*]] (though sometimes the database may be [[wiki/concepts/source/basic-metapatterns/shards|*sharded*]] or [[wiki/concepts/source/basic-metapatterns/shards|*replicated*]] together with the service that uses it) and get their requests through a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer* or *Sharding Proxy*]], making [[wiki/concepts/source/extension-metapatterns/sandwich|a kind of *Sandwich*]].

### [[wiki/concepts/source/basic-metapatterns/layers|Layered]] service


![The integration, core and database layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Service%20-%20Layered.png)


A *layered service* is [[wiki/concepts/source/fragmented-metapatterns/layered-services|divided into *layers*]]. This approach is very common both with backend *(micro-)services*, where at least the database is separated from the business logic, and with *device drivers* in system programming, where hardware-specific low-level interrupt handlers and register access are separated from the main logic and high-level OS interface.

Layering provides all of the benefits of the [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] pattern, including support for [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|conflicting forces]], which may manifest, for example, as the ability to deploy the database to a dedicated server for a backend or as a very low latency in the hardware-facing layer of a device driver.

Another benefit comes from the existence of the upper integration layer which may [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestrate interactions with other services]], isolating the lower layers from external dependencies.

### [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Cell]] (WSO2 definition) (service of services), Domain (Uber definition), Cluster


![Three subservices behind a Cell gateway. Two of them share a database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Service%20-%20Cell.png)


When a service is split into a set of subservices, it makes [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|a kind of *Hexagonal Architecture*]] called [*Cell*](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) (WSO2 name), [*Domain*](https://www.uber.com/blog/microservice-architecture/) (Uber name), or *Cluster* \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\]. All the incoming communication passes through a [[wiki/concepts/source/extension-metapatterns/proxy|*Cell Gateway*]] which encapsulates the *Cell* from its environment. Outgoing communication may involve the *Cell Gateway* or dedicated [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] (which constitute an *Anticorruption Layer* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]) A *Cell* may deploy its own [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] and/or [[wiki/concepts/source/extension-metapatterns/shared-repository|*share a database*]] among its components.

[[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell-Based Architecture*]] ([according to WSO2](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md), as opposed to [Amazon's alias](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html) for [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]]) appears when there is a need to recursively split a service, either because it grew too large or because it makes sense to use several incompatible technologies for its parts. It may also be applied to group services if there are too many of them in the system.

[*Domain-Oriented Microservice Architecture*](<Service-Oriented Architecture (SOA)#domain-oriented-microservice-architecture-doma>) (DOMA) is a more complex [*SOA*](<Service-Oriented Architecture (SOA)>)-style layered system of *Cells*.

## Examples

*Services* are ubiquitous among advanced architectures which either build around a layer of services that contains the bulk of the business logic (see [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]) or use small services as an extension of the main monolithic component ([[wiki/concepts/source/implementation-metapatterns/plugins|*PlugIns*]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]). [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]], [*Backends for Frontends*](<Backends for Frontends (BFF)>) and [*Service-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) go all out partitioning the system into interconnected layers of services. [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] and [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] often require the services to implement or use a polymorphic interface to simplify the components that manage them.

Examples of *Services* include:

- [*Service-Based Architecture*](#service-based-architecture-sba-macroservices) with subdomain-sized services which may share a database.
- Highly scalable, and usually smaller, [*Microservices*](#microservices).
- [*Actors*](#actors) that are like classes with asynchronous interfaces.
- [*Nanoservices*](#inexact-nanoservices-api-layer) – stand-alone functions deployed to a cloud.
- [*Device Drivers*](#inexact-device-drivers-pedestal) that interface hardware components inside an operating system.


### [[wiki/concepts/source/extension-metapatterns/sandwich|Service-Based Architecture]] (SBA), [Macroservices](#whole-subdomain-sub-domain-services-macroservices)


![Three interconnected services, two of which share a database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Service-Based%20Architecture.png)


Being the simplest use of *Services* where each subdomain gets a dedicated component, a *Service-Based Architecture* (*SBA*) \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] (aka *Macroservices*) tends to consist of a few coarse-grained services, some of which may [[wiki/concepts/source/extension-metapatterns/shared-repository|*share a database*]] and thus have little direct communication. An [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]] is often present as well, making the *SBA* into a kind of [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]].

### Microservices


![Multiple instances of several services connected to their sidecars which are connected to a shared mesh engine. Instances of each service access its single database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Microservices.png)


*Microservices* \[[wiki/concepts/source/appendices/books-referenced|[MP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\] are usually smaller than components in *Service-Based Architecture* and feature multiple services per subdomain with strict decoupling: they never use a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] and are scaled and deployed independently (and often dynamically). Even [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]] and distributed transactions ([[wiki/concepts/source/extension-metapatterns/orchestrator|*Sagas*]]) are considered to be a smell of bad design.

*Microservices* fit loosely coupled domains with parts which [vary drastically](https://medium.com/swlh/stop-this-microservices-madness-8e4e0695805b) in both forces and technologies. Any attempt to use them for an unfamiliar domain is [calling for trouble](https://martinfowler.com/bliki/MonolithFirst.html). Some authors insist that the “micro-” means that a microservice should not be larger in scope than a couple of weeks of work for a programming team. That allows rewriting one from scratch instead of refactoring. Others assert that too high a granularity makes everything [overcomplicated](https://dwmkerr.com/the-death-of-microservice-madness-in-2018/). Such a diversity of opinions may mean that the applicability and the very definition of *Microservices* varies from domain to domain.

This architecture usually relies on a [[wiki/concepts/source/extension-metapatterns/middleware|*Service Mesh*]] for [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] where common functionality, like logging, is implemented in co-located [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]]. A layer of [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]] (called *Integration Microservices*) [may be present](https://github.com/wso2/reference-architecture/blob/master/api-driven-microservice-architecture.md), resulting in [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell-Based Architecture*]] or [*Backends for Frontends*](<Backends for Frontends (BFF)>).

*Dynamically scaled* [[wiki/concepts/source/basic-metapatterns/shards|*Pools*]] of service instances are common thanks to the elasticity of hosting in a cloud. Extreme elasticity requires [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]], which puts a [[wiki/concepts/source/extension-metapatterns/shared-repository|distributed in-memory data store]] node within each *Sidecar*.

> Some authors [distinguish](https://medium.com/@ali.gelenler/architectural-styles-vs-architectural-patterns-7fab51713470) between *architectural patterns* and *architecture styles* (*architectures*) \[[wiki/concepts/source/appendices/books-referenced|[FSA]], [[wiki/concepts/source/appendices/books-referenced|MP]]\]. The difference is similar to that between libraries and frameworks: you use a library or pattern (e.g. division of a component into [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] or [*Services*](#)) when you think that it will help your needs, but you build your entire system according to the rules of a framework or style (such as *Microservices* or [*Enterprise SOA*](<Service-Oriented Architecture (SOA)#enterprise-soa>)). This book does not accent that difference – instead, it boils down styles to combinations of patterns.

### [[wiki/concepts/source/implementation-metapatterns/mesh|Actors]]


![Actors running over an actor framework.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Actors.png)


An [*actor*](https://volodymyrpavlyshyn.medium.com/actors-actor-systems-as-massively-distributed-scalability-architecture-5e40f5ea9e86) is an entity with private data and a public message queue. They are like objects with the difference that actors communicate only by sending each other asynchronous messages. The fact that a single execution thread may serve thousands of actors makes actor systems an extremely lightweight approach to asynchronous programming. As an actor is usually single-threaded, there is no place for *mutexes* and *deadlocks* in the code and it is possible to [replay events](https://martinfowler.com/eaaDev/EventSourcing.html). Non-blocking [[wiki/concepts/source/basic-metapatterns/monolith|*Proactors*]] are often found in [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|real-time systems]].

> A [*deadlock*](https://en.wikipedia.org/wiki/Deadlock_(computer_science)) happens when several threads in a system wait for each other to release unique resources they have each taken. As no thread involved in the *deadlock* can continue its operation, the system cannot complete its task. A single-threaded actor cannot *deadlock* because it does not contain multiple threads in the first place.

*Actors* have long been used in telephony (which is a domain where real-time communication meets complex logic and low resources) and with the invention of distributed runtime environments (e.g. Erlang/OTP or Akka) they expanded to messengers and banking which need to interconnect millions of users while providing personalized experience and history for everyone. Every user gets an actor that represents them in the system by communicating both with other actors (forming a kind of [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]) and with the user’s client application(s).

If we apply a bit of generalization, we can deduce that any server or backend service is an actor because its data cannot be accessed from outside and asynchronous IP packets are its only means of communication. Services of [[wiki/concepts/source/basic-metapatterns/pipeline|*Event-Driven Architecture*]] closely match this definition.

### (inexact) [[wiki/concepts/source/basic-metapatterns/pipeline|Nanoservices]] (API layer)


![Nanoservices dedicated to Get and Post methods between a client and a shared database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Nanoservices%20-%20API%20Layer.png)


Though *Nanoservices* are defined by their size (a single function), not system topology, I want to mention a specific application from Diego Zanon’s book *Building Serverless Web Applications*. That example is interesting because it comprises a single layer of isolated functions (each providing one API method) which may share functionality by including code from a common repository. As nanoservices of this kind never interact directly ([[wiki/concepts/source/foundations-of-software-architecture/shared-data|they rely]] on a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] instead) the common drawbacks of *Services* (poor debugging and high latency) don’t apply to them.

### (inexact) [[wiki/concepts/source/extension-metapatterns/proxy|Device Drivers]], [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Pedestal]]


![Applications call a System Call Interface which dispatches their requests to device drivers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Drivers.png)


An operating system must run efficiently with an unpredictable combination of hardware components, any of which can come from different manufacturers. It is impossible to know all the combinations beforehand. Thus it builds a [*Pedestal*](https://alistair.cockburn.us/hexagonal-architecture) by employing one service (called [[wiki/concepts/source/extension-metapatterns/proxy|*driver*]]) per hardware device. A driver *adapts* a manufacturer- and model-specific hardware interface to the generic interface of the OS *kernel*, allowing for the kernel to operate the hardware it controls without the detailed knowledge of the model. Internally, a driver is usually [[wiki/concepts/source/basic-metapatterns/layers|*layered*]]:

- The lowest layer, called the [[wiki/concepts/source/extension-metapatterns/proxy|*Hardware Abstraction Layer*]] (*HAL*), provides a model-independent interface for a whole family of devices from a manufacturer.
- The next layer of a driver is likely to contain manufacturer-specific algorithms for efficient use of the hardware.
- The third layer, if present, is probably busy with high-level tasks which are common for all devices of the given type and may be implemented by the kernel programmers.


The whole system of kernel, drivers, and user applications comprises the [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] architecture which bridges resource consumers and resource providers. As the drivers don’t need to coordinate themselves (this is done by the kernel), they don’t really make a system of *Services* and thus don’t have the corresponding drawbacks.

## Evolutions

*Services* are subject to a wide array of evolutions, just like the other basic metapatterns. These are summarized below and detailed in [[wiki/concepts/source/appendices/evolutions-of-architectures|Appendix E]].

### [[wiki/concepts/source/appendices/evolutions-of-services-that-restructure-services|Evolutions that restructure services]]

*Services* work well when each service matches a subdomain and is developed by a single team. If those premises change, you’ll need to restructure the services:

- A new feature request may emerge outside of any of the existing subdomains, creating a new service, or a service may grow too large to be developed by a single team, calling for division.



![A service is split in half.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services_%20Split.png)


- Two services may become so strongly coupled that they fare better if merged together, or the entire system may need to be glued back into a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] if the domain knowledge changes or if interservice communication strongly degrades performance.



![Two services are merged.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services_%20Merge.png)


- Alternatively, coupled services may be clustered into co-deployed [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]] to reduce operational complexity.



![Services are grouped into Cells, reducing their interdependencies.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services_%20Cluster.png)


### [[wiki/concepts/source/appendices/evolutions-of-services-that-add-layers|Evolutions that add layers]]

The most common modifications of a system of *Services* involve supplementary system-wide layers which compensate for the inability of the services to [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|share]] anything among themselves:

- A [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] tracks all the deployed service instances. It mediates the [[wiki/concepts/source/basic-metapatterns/layers|communication]] between them and may manage their scaling and failure recovery.



![The communication aspect of services can be covered by a dedicated middleware.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20add%20Middleware.png)


- [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]] of a [[wiki/concepts/source/extension-metapatterns/middleware|*Service Mesh*]] make a virtual layer of [[wiki/concepts/source/basic-metapatterns/layers|shared libraries]] for the [*Microservices*](#microservices) it hosts.



![Scaled services reside on a shared layer of sidecars which is placed on top of a shared mesh engine. All instances of each service access the service's database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Multifunctional%20-%20Service%20Mesh.png)


- A [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] simplifies the initial phases of development and interservice communication and enables the use of *Services* in [[wiki/concepts/source/foundations-of-software-architecture/shared-data|data-centric domains]].



![The data of individual services is merged into a shared repository.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20to%20Shared%20Database.png)


- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] stand between the system and its clients and take care of shared aspects that otherwise would need to be implemented by every service.



![Generic aspects of services move to a shared proxy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20add%20Proxy.png)


- An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] is the single place where the high-level logic of all [[wiki/concepts/source/basic-metapatterns/layers|use cases]] resides.



![The application logic is extracted from individual services into a shared orchestrator.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20use%20Orchestrator.png)


- Transforming *Services* into a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] greatly simplifies their integration.



![The application and data parts of services are separated from the domain logic and merged into system-wide layers, resulting in a Sandwich.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Services%20to%20Sandwich.png)


### Evolutions of individual services

Each service starts as either a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or as [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and may undergo the corresponding evolutions:

- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] help to reuse third-party components (e.g. a database), organize the code, support conflicting forces, and the upper layer of the service may [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestrate other services]].
- [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]] subdivide the code into smaller components and allow for the deployment of  multiple teams.
- A service may use a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] or a load balancing [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] to scale. Its [[wiki/concepts/source/basic-metapatterns/shards|*instances*]] usually rely on a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] for persistence.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] or [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]] may be used inside a service to improve the performance of its data layer.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS Views*]] or a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]] help reconstruct the state of other services from *event sourcing*.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] isolates the business logic of the service from external dependencies.
- Occasionally, [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] or [[wiki/concepts/source/implementation-metapatterns/microkernel|*Scripts*]] are used to customize the behavior of a service.


## Summary

*Services* deal with large projects by dividing them into subdomain-aligned components of smaller sizes which can be handled by dedicated teams. These may vary in technologies and qualities. However, services have a hard time cooperating in anything, from sharing data to debugging, and come with an innate performance penalty. There are several options halfway between [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] and distributed *Services* that have milder benefits and drawbacks.
