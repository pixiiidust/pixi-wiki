---
title: "Orchestrator"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Extension metapatterns/Orchestrator.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Extension%20metapatterns/Orchestrator
source_license_note: "See namespace README; preserve attribution and source links."
---

# Orchestrator

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Extension metapatterns/Orchestrator.md`.


![A diagram for Services with an orchestrator, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Orchestrator.png)


*One ring to rule them all.* Make a component to integrate other components.

<ins>Known as:</ins> Orchestrator \[[wiki/concepts/source/appendices/books-referenced|[MP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\], Orchestrated Services, Service Layer \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\], [[wiki/concepts/source/basic-metapatterns/layers|Application Layer]] \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\], Wrapper Facade \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\], Multi-Worker \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\], Control, Workflow Owner \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] of [[wiki/concepts/source/basic-metapatterns/services|Microservices]], and Processing Grid \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] of [[wiki/concepts/source/extension-metapatterns/sandwich|Space-Based Architecture]].

<ins>Structure:</ins> A layer of high-level business logic built on top of lower-level services.

<ins>Type:</ins> Extension component.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Separates integration concerns from the services – decouples the services’ APIs | May increase latency for global use cases |
| Global use cases can be changed and deployed independently from the services | Qualities of the services become coupled to an extent |
| Decouples the services from the system’s clients | API design is an extra step before implementation |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] discusses orchestration in its chapters on *Event-Driven Architecture*, *Service-Oriented Architecture*, and *Microservices*. \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] describes orchestration-based *Sagas* and its Order Service acts as an *Application Service* without explicitly naming the pattern. \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] defines several variants of *Facade*.

An *Orchestrator*, named after the person that assigns musical parts in an orchestra, takes care of global use cases (those involving multiple services) thus allowing each service to specialize in its own subdomain and, ideally, forget about the existence of all the other services. This way the entire system’s high-level logic (which is subject to frequent changes) is kept (and deployed) together, isolated from usually more complex subdomain-specific services. Dedicating a [[wiki/concepts/source/basic-metapatterns/layers|layer]] to global scenarios makes them relatively easy to implement and debug, while the corresponding development team that communicates with clients shelters the other narrowly-focused teams from disruptions. The cost of employing an *Orchestrator* is both degraded performance when compared to basic [[wiki/concepts/source/basic-metapatterns/services|*Services*]] that rely on [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]], [[wiki/concepts/source/appendices/books-referenced|MP]]\] and some coupling of the properties of the orchestrated services as the *Orchestrator* usually treats every service in the same way.

An *Orchestrator* fulfills two closely related roles:

- As a [*Mediator*](https://refactoring.guru/design-patterns/mediator) \[[wiki/concepts/source/appendices/books-referenced|[GoF]], [[wiki/concepts/source/appendices/books-referenced|SAHP]]\] it keeps the states of the underlying components consistent by propagating changes that originate in one component to the rest of the system. This role is prominent in [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control* software]], pervading automotive, aerospace, and IoT industries. The *Mediator* role also emerges as [*Saga*](#orchestrated-saga-saga-orchestrator-saga-execution-component-transaction-script-coordinator).
- As a [*Facade*](https://refactoring.guru/design-patterns/facade) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] it builds high-level scenarios out of smaller steps provided by the services or modules it controls. This role is obvious for [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*processing* systems]] where clients communicate with the *Facade*, but it is also featured in *control* software, because sometimes a simple event may trigger a complex multi-component scenario managed by the system’s *Orchestrator*.



![Control flows in a facade and mediator.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Misc/Orchestrator.png)


[[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|Data *processing*]] systems, such as backends, may deploy multiple [[wiki/concepts/source/basic-metapatterns/shards|instances]] of stateless *Orchestrators* to improve stability and performance. In contrast, an *Orchestrator* in [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control* software]] incorporates a high-level view of the system’s state thus it cannot be easily replicated (as any replicated state must be kept synchronized, introducing delay or inconsistency in decision-making).

### Performance

When compared to [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]], [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]] usually worsens latency as it involves extra steps of communication between the *Orchestrator* and orchestrated components. However, the effects should be estimated on case by case basis, as there are exceptions in at least the following cases:

- An *Orchestrator* may cache the state of the orchestrated system, gaining the ability to immediately respond to read requests with no need to query the underlying components. This is very common with [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control* systems]].
- An *Orchestrator* may persist a write request, respond to the client, and then start the actual processing (similar to the [[wiki/concepts/source/foundations-of-software-architecture/choreography|*early response* optimization]] in choreography). Persistence grants that the request will eventually be completed as it can be restarted.
- An *Orchestrator* may run multiple subrequests in parallel, reducing latency compared to a chain of choreographed events.
- In a highly loaded or latency-critical system, orchestrated services may establish direct data streams that bypass the *Orchestrator*. A classic example is [VoIP](https://en.wikipedia.org/wiki/Voice_over_IP) where the call establishment logic (SIP) goes through an orchestrating server while the voice or video (RTP) streams directly between the clients.



![Caching, early response, parallel execution, and direct communication between services as optimization techniques for Orchestrated Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Orchestrator.png)


I don’t see how orchestration can affect throughput as in most cases the *Orchestrator* can be scaled. However, scaling weakens consistency (or requires centralized locking, with a chance for a locked use case to hang if the *Orchestrator* instance which has locked it crashes) as then no instance of the *Orchestrator* has exclusive control over the system’s state.

### Dependencies

An *Orchestrator* may depend on the *APIs* of the services it orchestrates or define *SPIs* for them to implement, with the first mode being natural for its [*Facade*](https://refactoring.guru/design-patterns/facade) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] aspect and the second one for the [*Mediator*](https://refactoring.guru/design-patterns/mediator) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\]:


![A facade depends on every service. Contrariwise, every service depends on a mediator.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Orchestrator.png)


If an *Orchestrator* is added to integrate existing components, it will use their APIs.

In large projects, where each service gets a separate team, the APIs need to be negotiated beforehand, and will likely be owned by the orchestrated services.

Smaller (single-team) systems tend to be developed top-down, with the *Orchestrator* being the first component to implement, thus it defines the interfaces it uses.

Likewise, [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|control systems]] tend to reverse the dependencies, with their services depending on the orchestrator’s SPI to provide for polymorphism between the low-level components. See the [[wiki/concepts/source/foundations-of-software-architecture/orchestration|chapter on *orchestration*]] for [[wiki/concepts/source/foundations-of-software-architecture/orchestration|more details]].

### Applicability

*Orchestrators* <ins>shine</ins> with:

- *Large projects.* The partition of business logic into a high-level [[wiki/concepts/source/basic-metapatterns/layers|*application*]] (*Orchestrator*) and the multiple [[wiki/concepts/source/basic-metapatterns/services|subdomain *Services*]] it relies on provides perfect code decoupling and team specialization.
- *Specialized teams.* As an improvement over [[wiki/concepts/source/basic-metapatterns/services|*Services*]], the teams which develop deep knowledge of subdomains will delegate communication with customers to the application team.
- *Complex and unstable requirements*. The *integration* layer (*Orchestrator*) should be high-level and simple enough to be easily extended or modified to cover most of the customer requests or marketing experiments without much help from the domain teams.


*Orchestrators* <ins>fail</ins> in:

- *Huge projects.* At least one aspect of complexity is going to hurt. Either the number of the subdomain services and the size of their APIs will make it impossible for an *Orchestrator* programmer to find the correct methods to call, or the *Orchestrator* itself will become unmanageable due to the sheer number and length of its use cases. This can be addressed by dividing the *Orchestrator* into a layer of services (resulting in [*Backends for Frontends*](<Backends for Frontends (BFF)>) or [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell-Based Architecture*]]) or multiple layers (often yielding a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top-Down Hierarchy*]]). It is also possible to go for the [*Service-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) as that has more fine-grained components.
- *Small projects*. The implementation overhead of defining and stabilizing service APIs and the performance penalty of the extra network hop may outweigh the extra flexibility of having the *Orchestrator* as a separate system component.
- *Low latency*. Any system-wide use case will make multiple calls between the application (*Orchestrator*) and services, with each interaction adding to the latency.


### Relations


![Orchestrator for a monolith, layers, shards and services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Orchestrator.png)


*Orchestrator*:

- Extends [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or, rarely, [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], or [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] (forming *Layers*).
- Can be merged with a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] into an [[wiki/concepts/source/extension-metapatterns/proxy|*API Gateway*]], with a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] into an [[wiki/concepts/source/extension-metapatterns/middleware|*Event Mediator*]], or with a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] and [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] into an [[wiki/concepts/source/extension-metapatterns/middleware|*Enterprise Service Bus*]].
- Is a special case (single service) of [*Backends for Frontends*](<Backends for Frontends (BFF)>), [*Service-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) or (2-layer) [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]].
- Is a part of [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]].
- Can be implemented by a [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]].


## Variants by transparency

It seems that an *Orchestrator*, just like a [[wiki/concepts/source/basic-metapatterns/layers|*layer*]], which it is, [[wiki/concepts/source/basic-metapatterns/layers|can be]] *open* (*relaxed*) or *closed* (*strict*):

### Closed or strict


![An orchestrator mediates every request from every client.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20Closed.png)


A *strict* or *closed Orchestrator* isolates the orchestrated services from their users – all the requests go through the *Orchestrator*, and the services don’t need to intercommunicate.

### Open or relaxed


![An orchestrator mediates a multi-step client request while it is transparent to simpler requests.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20Open.png)


An *open Orchestrator* implements a subset of system-wide scenarios that require strict data consistency while less demanding requests go from the clients directly to the underlying services, which rely on [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]] or [[wiki/concepts/source/foundations-of-software-architecture/shared-data|*shared data*]] for communication. Such a system sacrifices the clarity of design to avoid some of the drawbacks of both *choreography* and *orchestration*:

- The orchestrator development team, which may be overloaded or slow to respond, is not involved in implementing the majority of use cases.
- Most of the use cases avoid the performance penalty caused by the orchestration.
- Failure of the *Orchestrator* does not disable the entire system.
- The relaxed *Orchestrator* still allows for synchronized changes of data in multiple services, which is rather hard to achieve with choreography.


## Variants by structure (can be combined)

The orchestration ([[wiki/concepts/source/basic-metapatterns/layers|application]] \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] / [integration](https://github.com/wso2/reference-architecture/blob/master/event-driven-api-architecture.md) / [composite](https://github.com/wso2/reference-architecture/blob/master/event-driven-api-architecture.md)) layer has several structural (implementation) options:

### [[wiki/concepts/source/basic-metapatterns/monolith|Monolithic]]


![An orchestrator communicates with several services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20Monolythic.png)


A single *Orchestrator* is deployed. This option fits ordinary medium-sized projects but fails for anything more demanding as the *Orchestrator* limits throughput, becomes a single point of failure, and may grow too complex for comfortable development.

### [[wiki/concepts/source/basic-metapatterns/shards|Scaled]]


![Multiple instances of a stateless orchestrator are behind a load balancer and they persist their actions into a dedicated shared database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20Scaled.png)


High availability requires multiple [[wiki/concepts/source/basic-metapatterns/shards|instances]] of a stateless *Orchestrator* to be deployed. A *Mediator* ([*Saga*](#orchestrated-saga-saga-orchestrator-saga-execution-component-transaction-script-coordinator), writing *Orchestrator*) may store the current transaction’s state in a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] to assure that if it crashes there is always another instance ready to take up its job.

High load systems also require multiple instances of *Orchestrators* because a single instance is not enough to handle the incoming traffic.

> Not all data is made equal. For example, an online store has different requirements for reliability of its buyers’ cart contents and the payments. If the current buyers’ carts become empty when the store’s server crashes, that makes only a minor annoyance (unless it happens repeatedly). However, any financial data loss or a corrupted money transfer is a real trouble. Therefore, an online store may implement its cart with a simple in-memory *Orchestrator*, but should be very careful about the payments workflow, every step of which must be persisted to a reliable database.

### [[wiki/concepts/source/basic-metapatterns/layers|Layered]]


![A simple orchestrator calls services or a complex orchestrator, which also calls the same services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20Layered.png)


\[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] describes an option of a layered [*Event Mediator*](#event-mediator). A client’s request comes to the topmost layer of the *Orchestrator* which uses the simplest (and least flexible) framework. If the request is found to be complex, it is forwarded to the second layer which is based on a more powerful technology. And if it fails or requires a human decision then it is forwarded again to the even more complex custom-tailored orchestration layer.

That allows the developers to gain the benefits of a high-level declarative language in a vast majority of scenarios while falling back to hand-written code for a few complicated cases. This choice is not free as the programmers need to learn multiple technologies, interlayer debugging is anything but easy, and performance is likely to be worse than that of a monolithic *Orchestrator*.

A similar example is using an [*API Composer*](#api-composer-remote-facade-gateway-aggregation-composed-message-processor-scatter-gather-mapreduce) for the top layer, followed by a [*Process Manager*](#process-manager-orchestrator) and a [*Saga Engine*](#orchestrated-saga-saga-orchestrator-saga-execution-component-transaction-script-coordinator).

### A service per client type ([Backends for Frontends](<Backends for Frontends (BFF)>))


![Each client communicates with its own orchestrator.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20BFF.png)


If your clients strongly differ in workflows (e.g. [OLAP](https://en.wikipedia.org/wiki/Online_analytical_processing) and [OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing), or user and admin interfaces), implementing dedicated *Orchestrators* is an option to consider. That both makes each client-specific *Orchestrator* smaller and more cohesive than the unified implementation would be and gives more independence to the teams responsible for different kinds of clients.

This pattern is known as [*Backends for Frontends*](<Backends for Frontends (BFF)>) and has a chapter of its own.

### A service per subdomain ([[wiki/concepts/source/fragmented-metapatterns/hierarchy|Hierarchy]])


![A top-level orchestrator communicates with lower-level Orchestrators each of which manages a group of services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20Hierarchy.png)


In a large system a single *Orchestrator* is very likely to become overgrown and turn into a development bottleneck (see [*Enterprise Service Bus*](#enterprise-service-bus-esb)). Building a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*hierarchy*]] of *Orchestrators* may help \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], but that requires the domain itself to be hierarchical.

The top-level component may even be a [[wiki/concepts/source/extension-metapatterns/proxy|*Reverse Proxy*]] if no use cases cross subdomain borders or if the sub-orchestrators employ [[wiki/concepts/source/foundations-of-software-architecture/choreography|choreography]], resulting in a flat [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell-Based Architecture*]]. Otherwise it is a tree-like [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Orchestrator of Orchestrators*]].

### A service per use case ([SOA](<Service-Oriented Architecture (SOA)>)-style)


![There are several orchestrators which use the same set of services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Orchestrator%20-%20SOA.png)


\[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] advises for single-purpose *Orchestrators* in [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]]: each *Orchestrator* manages one use case. This enables fine-grained scalability but will quickly lead to integration hell as new scenarios keep getting added to the system. Overall, such a use of *Orchestrators* resembles the [*task layer*](<Service-Oriented Architecture (SOA)#enterprise-soa>) of [*SOA*](<Service-Oriented Architecture (SOA)>).

## Examples

An *Orchestrator* may function in one of the following ways:

- An [*API Composer*](#api-composer-remote-facade-gateway-aggregation-composed-message-processor-scatter-gather-mapreduce) distributes parts of a client request to multiple services for parallel execution.
- A [*Process Manager*](#process-manager-orchestrator) splits a request into consecutive steps and oversees their execution.
- A [*Saga*](#orchestrated-saga-saga-orchestrator-saga-execution-component-transaction-script-coordinator) applies a change to multiple services in an “all or nothing” manner.
- An [*Integration Service*](#integration-micro-service-application-service) is a full-featured service which utilizes other services while providing for its users.
- [*Front Controller*](#inexact-front-controller) describes the first service in a *Pipeline* if it receives notifications from other services to know the ongoing status of every request.


There are also several patterns that have other functions in addition to orchestration:

- An [*API Gateway*](#api-gateway) blends an *API Composer* (orchestrating request) and a *Gateway* (dealing with protocols and logging).
- An [*Event Mediator*](#event-mediator) is a *Process Manager* with *Middleware* capabilities.
- An [*Enterprise Service Bus*](#enterprise-service-bus-esb) is an orchestrating *Message Bus* (multi-protocol *Middleware*).


### API Composer, Remote Facade, Gateway Aggregation, Composed Message Processor, Scatter-Gather, MapReduce


![An API Composer calls services in parallel. A Scatter/Gather or MapReduce calls shards in parallel.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/API%20Composer.png)


*API Composer* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] is a kind of [*Facade*](https://refactoring.guru/design-patterns/facade) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] which decreases the system’s latency by translating a high-level incoming message into a set of lower-level internal messages, sending them to the corresponding [[wiki/concepts/source/basic-metapatterns/services|services]] in parallel, waiting for results, and collecting the latter into a response to the original message. Such a logic may often be defined declaratively in a third-party tool without writing any low-level code. *Remote Facade* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\] is a similar pattern which makes synchronous calls to the underlying components – its goal is implementing a coarse-grained protocol for the system’s clients, so that a client may achieve whatever it needs through a single request. [*Gateway Aggregation*](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation) is a generalization of these patterns.

*Composed Message Processor* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\] disassembles *API Composer* into smaller components: it uses a *Splitter* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\] to subdivide the request into smaller parts, a *Router* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\] to send each part to its recipient, and an *Aggregator* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\] to collect the responses into a single message. Unlike *API Composer*, it can also address [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Replicas*]]. A [*Scatter-Gather*](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/scatter-gather.html) \[[wiki/concepts/source/appendices/books-referenced|[EIP]], [[wiki/concepts/source/appendices/books-referenced|DDS]]\] broadcasts a copy of the incoming message to each recipient, thus it lacks a *Splitter* (though \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] seems to ignore this difference). [*MapReduce*](https://en.wikipedia.org/wiki/MapReduce) \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] is similar to *Scatter-Gather* except that it summarizes the results received in order to yield a single value instead of concatenating them.

If an *API Composer* needs to conduct sequential actions (e.g. first get user id by user name, then get user data by user id), it becomes a [*Process Manager*](#process-manager-orchestrator) which may require some coding.

An *API Composer* is usually deployed as a part of an [*API Gateway*](#api-gateway).

Example: Microsoft has an [article](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation) on aggregation.

### Process Manager, Orchestrator


![The orchestrator calls several services one by one.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Process%20Manager.png)


*Process Manager* \[[wiki/concepts/source/appendices/books-referenced|[EIP]], [[wiki/concepts/source/appendices/books-referenced|LDDD]]\] (referred to simply as *Orchestrator* in \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\]) is a kind of *Facade* that translates high-level tasks into sequences of lower-level steps. This subtype of *Orchestrator* receives a client request, stores its state, runs pre-programmed request processing steps, and returns a response. Each of the steps of a *Process Manager* is similar to a whole task of an *API Composer* in that it generates a set of parallel requests to internal services, waits for the results, and stores them for the future use in the following steps or final response. The scenarios it runs may branch on conditions.

A *Process Manager* may be implemented in a general-purpose programming language, a declarative description for a third-party tool, or a mixture thereof.

A *Process Manager* is usually a part of an [*API Gateway*](#api-gateway), [*Event Mediator*](#event-mediator) or [*Enterprise Service Bus*](#enterprise-service-bus-esb).

Example: \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] provides several examples.

### (Orchestrated) Saga, Saga Orchestrator, [[wiki/concepts/source/implementation-metapatterns/microkernel|Saga Execution Component]], Transaction Script, Coordinator


![An atomically consistent saga rolls back changes after a failed write. An eventually consistent saga retries the failed write till it succeeds.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Saga.png)


*(Orchestrated* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\]*) Saga* \[[wiki/concepts/source/appendices/books-referenced|[LDDD]]\], *Saga Orchestrator* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] or [*Saga Execution Component*](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf) is a subtype of *Process Manager* which is specialized in *distributed transactions*. Its name comes from epic stories woven from multiple episodes.

- An *Atomically Consistent Saga* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] (which is the default meaning of the term) comprises a pre-programmed sequence of \{“do”, “undo”\} action pairs. When it is run, it iterates through the “do” sequence till it either completes (meaning that the transaction succeeded) or fails. A failed *Atomically Consistent Saga* begins iterating through its “undo” sequence to roll back the changes that were already made.
- In contrast, an *Eventually Consistent Saga* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] always retries its writes till all of them succeed.


A *Saga* is often programmed declaratively in a third-party [[wiki/concepts/source/implementation-metapatterns/microkernel|*Saga Framework*]] which can be integrated into any service that needs to run a *distributed transaction*. However, it is quite likely that such a service itself is an [*Integration Service*](#integration-micro-service-application-service) as it seems to [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestrate]] other services.

A *Saga* plays the roles of both *Facade* by translating a single transaction request into a series of calls to the services’ APIs and *Mediator* by keeping the states of the services consistent (the transaction succeeds or fails as a whole). Sometimes a *Saga* may include requests to external services (which are not parts of the system you are developing).

A *Transaction Script* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]], [[wiki/concepts/source/appendices/books-referenced|LDDD]]\] is a procedure that executes a transaction, possibly over multiple data stores \[[wiki/concepts/source/appendices/books-referenced|[LDDD]]\]. Unlike a *Saga*, it is synchronous, written in a general programming language, and does not require a dedicated framework to run. It operates the data store(s) directly while a *Saga* usually sends commands to services. A *Transaction Script* may return data to its caller.

*Coordinator* \[[wiki/concepts/source/appendices/books-referenced|[POSA3]]\] is a generalized pattern for a component which manages multiple tasks (e.g. software updates of multiple components) to achieve “all or nothing” results (if any update fails, other components are rolled back).

Example: \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] investigates many kinds of *Sagas* while \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] has a shorter description.

### Integration (Micro-)Service, Application Service


![An integration service is a full-featured service that stands between the client and the remaining services of the system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Integration%20Service.png)


An [*Integration Service*](https://github.com/wso2/reference-architecture/blob/master/event-driven-api-architecture.md) is a full-scale service (often with a dedicated database) that runs high-level scenarios while delegating the bulk of the work to several other services (remarkably, delegating to a single component forms [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]). Though an *Integration Service* usually features both functions of *Orchestrator*, in a [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control* system]] its *Mediator* role is more prominent while in [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*processing* software]] it is going to behave more like the *Facade*. A system with an *Integration Service* often resembles a shallow [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top-Down Hierarchy*]].

Example: Order Service in \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] seems to fit the description.

### (inexact) [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Front Controller]]


![A Front Controller is the first service of a pipeline which receives status notifications from every other service and responds to the client's get status query.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Front%20Controller.png)


*Front Controller* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]] [[wiki/concepts/source/analytics/ambiguous-patterns|but not]] [[wiki/concepts/source/appendices/books-referenced|PEAA]]\] is the name for the first (client-facing) service of a [[wiki/concepts/source/basic-metapatterns/pipeline|*pipeline*]] in [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event-Driven Architecture*]] when that service collects information about the status of each request it has processed and forwarded down the *pipeline.* The status is received by listening for notifications from the downstream services and is readily available for the *Front Controller*’s clients, which makes *Front Controller* resemble [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]] ([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]) and [*Application Service*](#integration-micro-service-application-service).

### [[wiki/concepts/source/extension-metapatterns/proxy|API Gateway]]


![An API Gateway both translates from the client's to the system's protocol and calls services in parallel.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/API%20Gateway.png)


An *API Gateway* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] is a component that not only processes client requests (and encapsulates an implementation of a client protocol(s)) as a [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] (a kind of [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]]) but also splits every client request into multiple requests to internal services as an [*API Composer*](#api-composer-remote-facade-gateway-aggregation-composed-message-processor-scatter-gather-mapreduce) or [*Process Manager*](#process-manager-orchestrator) (which are *Orchestrators*). It is a common pattern for backend solutions as it does everything necessary to isolate the stable core of the system’s implementation from its fickle clients. Usually a third-party framework implements and colocates both its aspects, namely *Proxy* and *Orchestrator*, thus simplifying deployment and improving latency.

Example: a thorough article from [Microsoft](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway).

### [[wiki/concepts/source/extension-metapatterns/middleware|Event Mediator]]


![An event mediator calls event processors one by one.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Event%20Mediator.png)


*Event Mediator* \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] is an *orchestrating* [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]. It not only receives requests from clients and turns each request into a multistep use case (as a [*Process Manager*](#process-manager-orchestrator)) but it also manages the deployed instances of services and acts as a medium which calls them. Moreover, unlike an ordinary *Middleware*, it seems to be aware of all of the kinds of messages in the system and which service each message must be forwarded to, resulting in overwhelming complexity concentrated in a single component which does not even follow the principle of separation of concerns. \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] recommends [building a stack of *Event Mediators*](#layered) from several vendors, further complicating this architecture.

Example: Mediator Topology in the chapter of \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] on Event-Driven Architecture.

### [[wiki/concepts/source/extension-metapatterns/middleware|Enterprise Service Bus]] (ESB)


![An Enterprise Service Bus is between the fragmented task and entity layers of Service-Oriented Architecture. It mediates all calls and messages between the system components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Enterprise%20Service%20Bus.png)


[*Enterprise Service Bus*](https://www.confluent.io/learn/enterprise-service-bus/) (*ESB*) \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] is an overgrown [*Event Mediator*](#event-mediator) that incorporates lots of [*cross-cutting concerns*](https://en.wikipedia.org/wiki/Cross-cutting_concern), including protocol translation for which it utilizes at least one [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] per service (just as a [[wiki/concepts/source/extension-metapatterns/middleware|*Message Bus*]] does). The combination of a central role in organizations and its complexity was among the main reasons for the demise of [*Enterprise Service-Oriented Architecture*](<Service-Oriented Architecture (SOA)#enterprise-soa>).

Example: Orchestration-Driven Service-Oriented Architecture in \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], [how it is born](http://memeagora.blogspot.com/2009/01/tactics-vs-strategy-soa-tarpit-of.html) and [how it dies](http://memeagora.blogspot.com/2009/03/triumph-of-hope-over-reason-soa-tarpit.html) by Neal Ford.

## [[wiki/concepts/source/appendices/evolutions-of-an-orchestrator|Evolutions]]

Employing an *Orchestrator* has two pitfalls:

- The system becomes slower because too much communication is involved.
- A single *Orchestrator* may grow too large and rigid.


There is [[wiki/concepts/source/appendices/evolutions-of-an-orchestrator|one way to counter the first point and more than one to solve the second]]:

- Subdivide the *Orchestrator* by the system’s subdomains, forming [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]] and minimizing network communication.



![An orchestrator is subdivided into subdomain components which become the application layers of respective services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Orchestrator%20to%20Layered%20Services.png)


- Subdivide the *Orchestrator* by the type of client, forming [*Backends for Frontends*](<Backends for Frontends (BFF)>).



![An orchestrator is subdivided into Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Orchestrator%20to%20Backends%20for%20Frontends.png)


- Add another [[wiki/concepts/source/basic-metapatterns/layers|*layer*]] of orchestration.



![An orchestrator is subdivided into a pair of simple and complex orchestrators.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Orchestrator%20add%20Orchestrator.png)


- Build a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top-Down Hierarchy*]].



![An orchestrator is subdivided into a hierarchy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Orchestrator%20to%20Hierarchy.png)


## Summary

 An *Orchestrator* distills the high-level logic of your system and keeps it together in a layer which integrates other components. However, the separation of business logic into two layers results in much communication which impairs performance.
