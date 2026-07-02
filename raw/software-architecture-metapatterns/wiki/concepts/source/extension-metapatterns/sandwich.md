---
title: "Sandwich"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Extension metapatterns/Sandwich.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Extension%20metapatterns/Sandwich
source_license_note: "See namespace README; preserve attribution and source links."
---

# Sandwich

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Extension metapatterns/Sandwich.md`.


![A diagram for Sandwich Architecture, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Sandwich.png)


*Follow the line of least resistance\.* Divide where it is loosely coupled\.

<ins>Structure:</ins> A layer of domain\-level services between shared integration and data layers\.

<ins>Type:</ins> System topology, implementation\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Supports medium to large codebases | Aggressive optimization is impossible |
| Multiple specialized development teams | Low fault tolerance |
| There are many ways to evolve the system |  |

<ins>References:</ins> None I know of\.

A *Sandwich* is a \(sub\)system midway between [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\. It emerges when a *layered* component outgrows its architecture and its middle \([[wiki/concepts/source/basic-metapatterns/layers|*domain*]]\) layer – which tends to be both the largest and least cohesive – is divided into subdomains while the [[wiki/concepts/source/basic-metapatterns/layers|*application*]] and [[wiki/concepts/source/basic-metapatterns/layers|*data*]] layers remain intact\. Another, less common, origin is a \(sub\)system of [[wiki/concepts/source/basic-metapatterns/services|*\(Micro\)Services*]] which becomes so tightly coupled that it needs to be partially merged\.

A *Sandwich*, named after the shape of its diagram, includes the following components:

- A shared [[wiki/concepts/source/introduction/system-topologies|*managing layer*]] which receives client requests and dispatches them to the underlying *domain\-level services*\. Though this layer may either implement [[wiki/concepts/source/basic-metapatterns/layers|*use cases*]] as an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], forward each client action to a matching service as a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], or do both as an [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]], it remains the component that ties the entire system together\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Domain\-level*]] [[wiki/concepts/source/basic-metapatterns/services|*services*]] \(if distributed\) or [[wiki/concepts/source/basic-metapatterns/services|*modules*]] \(otherwise\) that implement the bulk of the system’s business logic and thus contain most of the system’s code\.
- A shared [[wiki/concepts/source/basic-metapatterns/layers|*data layer*]] which the upper layer’s services operate on\. It may be a persistent database or an in\-memory application state\.


*Sandwiches* often occur naturally without being recognized as a distinct architecture\. In fact, I had to make up a name for this [[wiki/concepts/source/introduction/system-topologies|system topology]]\.

### Performance

As [[wiki/concepts/source/basic-metapatterns/layers|*domain*\-level]] services rarely interact among themselves, the performance of a *Sandwich* is similar to that of [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] with the same kind of deployment \(components of a *Sandwich* may or may not be colocated\)\.


![Control and data flow is identical in Sandwich and Layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Sandwich.png)


### Dependencies

The *Sandwich*’s [[wiki/concepts/source/basic-metapatterns/layers|*integration* layer]] depends on every service inside the *Sandwich*\. The services themselves depend on the [[wiki/concepts/source/basic-metapatterns/layers|*data* layer]]\.


![The integration layer depends on every service. Every service depends on the data layer.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Sandwich.png)


Having two shared layers provides three options for invoking the [[wiki/concepts/source/basic-metapatterns/layers|*domain*]] components:

- The most common approach is [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]] by the integration layer\.
- [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|Data\-centric]] domains may rely on [[wiki/concepts/source/foundations-of-software-architecture/shared-data|*data change notifications*]]\.
- [[wiki/concepts/source/foundations-of-software-architecture/choreography|*Choreography*]] via publish/subscribe is rare because it is inferior to the other two options:
  - It is not enough to decouple the subdomain services which are already bound together by the shared data layer\.
  - *Publish/subscribe* requires additional libraries and setup, while the data store, which often supports notifications, is already in place\.
  - Furthermore, *orchestration* allows for much better control over use case logic and error handling than *choreography*\.


### Applicability

*Sandwich* <ins>fits</ins>:

- *Medium\-sized projects with complex domain logic\.* The subdivision of the *domain* layer keeps the code complexity under control and supports development by multiple teams with little increase of operational burden\.
- *Rapid development of ordinary systems\.* If you don’t face any challenging forces, you should keep your architecture [simple and stupid](https://en.wikipedia.org/wiki/KISS_principle) but still flexible – which is the pragmatic *Sandwich*\. You will be able to evolve it in the future if needed\.
- *Data\-centric domains\.* This architecture allows all the services to work on the same dataset, each reading and writing the parts that are involved in its business logic\.


*Sandwich* <ins>does not help</ins>:

- *Projects with a large number of use cases\.* As the [[wiki/concepts/source/basic-metapatterns/layers|*integration* layer]] remains monolithic, it still can grow out of control, requiring the system to transform into [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]]\.
- *Huge systems\.* Both the [[wiki/concepts/source/basic-metapatterns/layers|*integration*]] and [[wiki/concepts/source/basic-metapatterns/layers|*data*]] layers are cumbersome in that case\.
- *Demanding forces\.* The *Sandwich* architecture is a jack of all trades, master of none\. In general, it is an average backend, and is neither highly elastic, flexible, nor low latency\.


### Relations


![Transitions between Layers, a Sandwich, a Service-Based Architecture, and Layered Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Sandwich.png)


*Sandwich*:

- Is a system in transition between [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- Is [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] with a middle layer split into services or [[wiki/concepts/source/basic-metapatterns/services|*Services*]] sandwiched between layers\.
- May implement a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or *service*\.
- Often provides the internals of a [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]]\.
- Includes a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] and an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and/or [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]]\.


> A [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]] encapsulates several services so that they can be treated as a single entity with the goal of reducing the number of top\-level system components\. Typically, interdependent and closely communicating services are clustered into a single *Cell*, predisposing the *Cell*’s internals for further merging to reduce the communication overhead and the amount of boilerplate code\. Such a scenario often results in a *Sandwich* trapped inside a *Cell*\.

## Examples

Though most real\-world *Sandwiches* stay beneath the radar as non\-standard architectures, there are two well\-documented and highly specialized occurrences of this topology in [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|data\-centric]] domains and a few less stringent generic cases:

- [*Blackboard System*](#blackboard-system) describes how specialized algorithms cooperate to try solving a non\-deterministic problem\.
- [*Space\-Based Architecture*](#space-based-architecture) runs multiple instances of services co\-located with a distributed in\-memory data store\.
- [*Service\-Based Architecture*](#service-based-architecture) comprises large services that often share a database\.
- [*Nanoservices*](#nanoservices) is a system of functions deployed to a cloud\.
- [*Command Query Responsibility Segregation*](#command-query-responsibility-segregation-cqrs) uses different models for read\-write and read\-only scenarios\.
- [*Replicated Load\-Balanced Services*](#inexact-replicated-load-balanced-services-lambdas) are identical instances of a stateless service that access a shared database\.


### [[wiki/concepts/source/extension-metapatterns/shared-repository|Blackboard]] System


![A Blackboard System includes a control which orchestrates knowledge sources which access a blackboard with shared data.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Blackboard.png)


Some domains are [complex and ill\-structured](http://i.stanford.edu/pub/cstr/reports/cs/tr/86/1123/CS-TR-86-1123.pdf): there is only a vague understanding of how the inputs relate to outputs, therefore you cannot write a single algorithm to solve it\. If you are lucky to have a huge labeled dataset, you can attempt training a neural network\. If there are not so many examples, you are in trouble\.

[*Blackboard Systems*](https://en.wikipedia.org/wiki/Blackboard_system) \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\] were invented half a century ago to tackle non\-deterministic problems: speech or image recognition, X\-ray crystallography of proteins, or even tracking enemy submarines or stealth aircraft\. In these cases inputs are noisy and scarce and outputs can vary indefinitely, therefore one must go through trial and error proposing, refining, and comparing many possible solutions to arrive at something plausible\.

The system consists of:

- A [[wiki/concepts/source/extension-metapatterns/shared-repository|*blackboard*]] – a [[wiki/concepts/source/extension-metapatterns/shared-repository|*shared data store*]] that contains all the current knowledge about the problem, namely inputs and hypotheses\. It is subdivided into abstraction levels which range from the original inputs through multiple intermediate representations to the output data structure\. Each level usually contains multiple solution attempts\.
- *Knowledge sources* – independent, specialized components that process data from a lower level to create a higher\-level hypothesis\. For example, in voice recognition, a knowledge source may read a sound wave and write a letter which that wave encodes\. Another knowledge source may read letters and output English words, while another one tries to find French words\. And the final one collects words into sentences\.
- A [[wiki/concepts/source/extension-metapatterns/orchestrator|*control*]] – a [[wiki/concepts/source/extension-metapatterns/proxy|*scheduler*]] that assigns processor time to knowledge sources\. It balances the quality and speed of the solution attempts based on the current progress and remaining time\.


This architecture makes best use of every system layer:

- The *control* is required to prune the exponential growth of possible solutions because there are not enough system resources to check all of them\.
- The independent *knowledge sources* are easy to add or remove, allowing the developers to try various algorithms without touching other components\.
- The *blackboard* enables the cooperation of knowledge sources, each of which is limited to a small part of the overall solution\.


### [[wiki/concepts/source/implementation-metapatterns/mesh|Space\-Based Architecture]]


![Space-Based Architecture comprises the following layers: a messaging grid, a processing grid, scaled processing units, a data grid, a deployment manager, and a persistent database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Multifunctional%20-%20Space-Based%20Architecture.png)


*Space\-Based Architecture* \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\] is an extremely elastic alternative to [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] which works well for [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|data\-centric]] domains\. Each *processing unit* – a [[wiki/concepts/source/basic-metapatterns/layers|domain\-level]] service – is co\-located with an in\-memory replica of the entire system’s data, which makes both data access and creation of new instances of *processing units* blazingly fast\. As is common for *Sandwiches*, *processing units* can be [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrated*]] by the [[wiki/concepts/source/extension-metapatterns/orchestrator|*processing grid*]] or they can [[wiki/concepts/source/foundations-of-software-architecture/shared-data|*subscribe to changes*]] in the shared [[wiki/concepts/source/extension-metapatterns/shared-repository|*data grid*]], this architecture being flexible enough to allow for choosing a [[wiki/concepts/source/foundations-of-software-architecture/arranging-communication|communication paradigm]] on per request basis\.

Aside from *processing units*, which contain the main business logic, *Space\-Based Architecture* involves:

- A *messaging grid* which is a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] \(combination of [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Dispatcher*]], and [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]]\) that receives, preprocesses, and persists client requests\. Simple requests are forwarded to the least loaded *processing unit* while anything complicated goes to the *processing grid*\.
- A [[wiki/concepts/source/extension-metapatterns/orchestrator|*processing grid*]] is an optional [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] which manages multi\-step workflows for complicated requests that involve branching and error handling\.
- A [[wiki/concepts/source/extension-metapatterns/shared-repository|*data grid*]] is a distributed in\-memory data store\. It is built of caching [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] nodes which are co\-located with instances of *processing units*, making the data store access extremely fast\. However, the speed and scalability is paid for with stability – any data in memory is prone to disappearing\. Therefore the *data grid* backs up all the changes to a slower *persistent database*\.
- A [[wiki/concepts/source/extension-metapatterns/middleware|*deployment manager*]] is a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] that creates and destroys instances of *processing units* \(which are paired to the nodes of the *data grid*\), just like [[wiki/concepts/source/extension-metapatterns/middleware|*Service Mesh*]] does for [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] \(which are paired to [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]]\)\. However, in contrast to *Service Mesh*, it does not provide a messaging infrastructure because *processing units* communicate by sharing data via the *data grid*, not by sending messages\.


As *Space\-Based Architecture* runs every component in a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]], it avoids the fault tolerance and database performance drawbacks inherent to *Sandwich*, trading them for possibility of write conflicts when multiple clients cause changes to the same piece of data simultaneously\.

### [[wiki/concepts/source/basic-metapatterns/services|Service\-Based Architecture]]


![A Sandwich-like topology with user interface, a layer of domain services, and a shared database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Service-Based%20Architecture.png)


*Service\-Based Architecture* \[[wiki/concepts/source/appendices/books-referenced|[FSA]] [[wiki/concepts/source/analytics/ambiguous-patterns|but not]] [[wiki/concepts/source/appendices/books-referenced|DEDS]]\] is the most pragmatic and loosely defined of topologies based on *Services* \(hence the name\)\. In a basic *Service\-Based Architecture* the [[wiki/concepts/source/basic-metapatterns/services|*subdomain services*]] are integrated by a [[wiki/concepts/source/extension-metapatterns/proxy|*User Interface*]] layer, usually a *Frontend*, and there is a single [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]]\. However, as there are no written rules for *Service\-Based Architecture*, multiple databases or finer\-grained *GUI*s may be used for programmers’ convenience, disintegrating the *Sandwich* topology for the sake of less coupled [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Service*s]]\.


![A Sandwich-like topology with shared user interface and database is gradually transformed into layered services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Service-Based%20to%20Layered%20Services.png)


### [[wiki/concepts/source/basic-metapatterns/services|Nanoservices]]


![Nanoservices form a Sandwich-shaped architecture. The upper layer is an API Gateway for an orchestrated system or a gateway for pipelined Nanoservices. The lower layer is a shared datastore.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Nanoservices.png)


*Nanoservices* is another loosely defined architecture built of single\-purpose *functions* \([FaaS](https://en.wikipedia.org/wiki/Function_as_a_service)\) individually deployed to the cloud\. It is highly elastic and relies on a cloud provider for operational support, saving costs for small businesses\.

As a single *nanoservice* is too small to implement a use case, there must be an [[wiki/concepts/source/basic-metapatterns/layers|*integration layer*]] that receives client or user requests, runs several *nasoservices* to execute it, and returns a response\. The integration layer may be a [[wiki/concepts/source/extension-metapatterns/proxy|*Frontend*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]], an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Event Mediator*]] for [[wiki/concepts/source/basic-metapatterns/services|*orchestrated Nanoservices*]], or an ordinary [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] that initiates a [[wiki/concepts/source/basic-metapatterns/pipeline|*pipelined*]] scenario and receives its response from a [[wiki/concepts/source/basic-metapatterns/pipeline|*choreographed* system]]\.

As each *nanoservice* is stateless, for the system to be stateful there must be a *data store*\. And as each *nanoservice* can do only one thing \(either read, write, or search\), the *data store* must be [[wiki/concepts/source/extension-metapatterns/shared-repository|*shared*]] to be of any use\.

Please note how a fine\-grained decomposition of business logic necessarily results in a *Sandwich* architecture\.

### [[wiki/concepts/source/fragmented-metapatterns/layered-services|Command Query Responsibility Segregation]] \(CQRS\)


![A large read and smaller write models between a user interface and database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/CQRS.png)


[*Command Query Responsibility Segregation*](https://martinfowler.com/bliki/CQRS.html) \(*CQRS*\) is a principle which calls for separation of components that process *commands* \(requests that change the system’s data\) and *queries* \(requests that analyze the data\)\. The subdivision necessarily happens at the [[wiki/concepts/source/basic-metapatterns/layers|*domain*]] \(*model*\) level, resulting in separate [*Write Model*](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) \([*Command Model*](https://martinfowler.com/bliki/CQRS.html)\) and [*Read Model*](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) \([*Query Model*](https://martinfowler.com/bliki/CQRS.html), [*Thin Read Layer*](https://cqrs.wordpress.com/wp-content/uploads/2010/11/cqrs_documents.pdf)\)\. In the simplest case the [[wiki/concepts/source/basic-metapatterns/layers|*data* layer]] is kept monolithic, as shown in the diagram above\.

*CQRS* helps decouple the logic\-heavy object\-oriented code which maintains data consistency and business constraints during editing data records from the search and aggregation code that needs direct database access to run complex SQL queries\. If that is not enough, it is possible to trade complexity for performance by employing specialized databases: [*OLTP*](https://en.wikipedia.org/wiki/Online_transaction_processing) for use with the *Write Model* and [*OLAP*](https://en.wikipedia.org/wiki/Online_analytical_processing) for the *Read Model*, as described in the [[wiki/concepts/source/fragmented-metapatterns/layered-services|corresponding section of the *Layered Services* chapter]]:


![The single database of a Sandwich-like CQRS with a shared database is subdivided into OLTP and OLAP databases, forming Layered Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/CQRS%20to%20Layered%20Services.png)


### \(inexact\) [[wiki/concepts/source/basic-metapatterns/shards|Replicated Load\-Balanced Services]], Lambdas


![A load balancer connects a new client to a free instance of a stateless backend that accesses a database shared among all the backend instances.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Shards%20-%20Pool.png)


Replicating a system’s [[wiki/concepts/source/basic-metapatterns/layers|*domain*]] [[wiki/concepts/source/basic-metapatterns/layers|*tier*]] along the [[wiki/concepts/source/introduction/metapatterns|*sharding* axis]] also results in a *Sandwich*\-like [[wiki/concepts/source/introduction/system-topologies|topology]], albeit with altered properties: while the original *Sandwich*’s subdivision of the codebase along the [[wiki/concepts/source/introduction/metapatterns|*subdomain* axis]] allows for multiteam development and easy integration of new functionality, replication along the *sharding* axis only makes it simple to add or remove instances of the middle tier as the system load changes\.

*Replicated Load\-Balanced Services* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] is the general name for running multiple instances of a stateless service that [[wiki/concepts/source/extension-metapatterns/shared-repository|*share a database*]] and run under a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]]\. [*Lambdas*](https://jesseduffield.com/Notes-On-Lambda/) is a synonym for a similar setup from cloud computing providers \(see also [*Nanoservices*](#nanoservices)\)\.

## Evolutions

The components of a *Sandwich* provide plenty of ways to alter the system, with unique evolutions detailed in [[wiki/concepts/source/appendices/evolutions-of-a-sandwich|Appendix E]]:

### [[wiki/concepts/source/appendices/evolutions-of-a-sandwich|Primary evolutions]]

[[wiki/concepts/source/appendices/evolutions-of-a-sandwich|Some evolutions]] involve the system’s [[wiki/concepts/source/basic-metapatterns/layers|domain logic]] or its topology:

- The *domain\-level services* are independent enough to be easily added or removed\.



![One of the domain-level services is removed and another one is added.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20add%20remove%20Service.png)


- In most cases they share technologies, allowing for splitting or merging of the services\.



![One domain-level service is split in half while two other services are merged together.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20split%20merge%20Services.png)


- If the services are found to be strongly coupled, they can be merged into a monolithic layer, likely to be subdivided in a better way later on\.



![The entire domain layer is merged, resulting in Layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20to%20Layers.png)


- Alternatively, the subdomains can be further decoupled\.



![The integration and data layers are divided into subdomains, producing Three-Layered Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20to%20Layered%20Services.png)


### [[wiki/concepts/source/appendices/evolutions-of-a-shared-repository|Evolutions of the data layer]]

If the [[wiki/concepts/source/basic-metapatterns/layers|*data* layer]] becomes a performance bottleneck, it can be [[wiki/concepts/source/extension-metapatterns/shared-repository|split as a *Shared Repository*]]:

- [[wiki/concepts/source/basic-metapatterns/shards|*Shard*]] the database if its records are mutually independent or [[wiki/concepts/source/basic-metapatterns/shards|*replicate*]] it if it is the read traffic which overloads the system\.
- Apply [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]] if elasticity is more important than consistency\.
- Divide the data into databases, private to the domain\-level services, thus transforming the system into [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrated*]] [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- Deploy specialized data stores \([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\)\.


### [[wiki/concepts/source/appendices/evolutions-of-an-orchestrator|Evolutions of the application layer]]

If the [[wiki/concepts/source/basic-metapatterns/layers|*integration* layer]] contains use cases and becomes cumbersome, it should be subdivided following the [[wiki/concepts/source/extension-metapatterns/orchestrator|evolutions of *Orchestrator*]]:

- Into [[wiki/concepts/source/basic-metapatterns/services|*Services*]] if the use cases cluster around subdomains\.
- Into [*Backends for Frontends*](<Backends for Frontends (BFF)>) if the system serves several kinds of clients\.
- Into [[wiki/concepts/source/extension-metapatterns/orchestrator|*Layers*]] if some use cases are simple while others are complicated\.
- Into a [[wiki/concepts/source/extension-metapatterns/orchestrator|*Hierarchy*]] if the use cases include both generic and specialized logic\.


## Summary

*Sandwich* is a pragmatic architecture midway between [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\. It combines simplicity and flexibility, avoiding unnecessary effort for the present while retaining many paths to evolve in the future\.

| \<\< [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]] | ^ [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|Extension metapatterns]] ^ | [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Fragmented metapatterns]] \>\> |
| --- | --- | --- |
