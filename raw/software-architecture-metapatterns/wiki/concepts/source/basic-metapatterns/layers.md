---
title: "Layers"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Basic metapatterns/Layers.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Basic%20metapatterns/Layers
source_license_note: "See namespace README; preserve attribution and source links."
---

# Layers

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Basic metapatterns/Layers.md`.


![A diagram for Layered Architecture, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Layers.png)


*Yet another layer of indirection\.* Separate business logic from implementation details\.

<ins>Known as:</ins> Layers \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\], Layered Architecture \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]], [[wiki/concepts/source/appendices/books-referenced|LDDD]]\], Multitier Architecture, and N\-tier Architecture \[[wiki/concepts/source/appendices/books-referenced|[LDDD]]\]\.

<ins>Structure:</ins> A component per level of abstractness\.

<ins>Type:</ins> System topology, implementation\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Rapid start for development | Quickly deteriorates as the project grows |
| Easy debugging | Hard to develop with more than a few teams |
| Good performance | Does not solve force conflicts between subdomains |
| Development teams may specialize | Does not support aggressive optimizations |
| Business logic is encapsulated |  |
| Allows for the resolution of conflicting forces, including the use of specialized technologies |  |
| Deployment to dedicated hardware |  |
| Layers with no business logic are reusable |  |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\] and \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] discuss layered software in depth; \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] promotes the layered style; most of the architectures in Herberto Graça’s [Software Architecture Chronicles](https://herbertograca.com/2017/07/03/the-software-architecture-chronicles/) are layered\. The Wiki has a reasonably [good article](https://en.wikipedia.org/wiki/Multitier_architecture)\.

*Layering* a system creates interfaces between its levels of abstractness \(high\-level [use cases](#application-use-cases-or-integration), lower\-level [domain logic](#domain-business-rules-or-model), and infrastructure\) while also retaining monolithic cohesiveness within each of the levels\. That allows both for easy debugging inside each individual layer \(no need to jump into another programming language or re\-attach the debugger to a remote server\) and enough flexibility to have a dedicated development team, tools, deployment, and scaling policies for each layer\. Though layered code is slightly better than that of [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], thanks to the separation of concerns, one of the upper \(business logic\) layers may nonetheless grow too large for efficient development\.

Splitting a system into layers tends to resolve conflicts of forces between its abstract and highly optimized parts: the top\-level business logic changes rapidly and does not require much optimization \(as its methods are called infrequently\), thus it can be written in a high\-level programming language\. In contrast, infrastructure, which is called thousands of times per second, has stable workflows and interfaces but must be thoroughly optimized and extremely well tested\.

Many patterns have one or more of their layers split into subdomains, resulting in a layer of *services*\. That causes no penalties as long as the services are completely independent \(when the original layer had zero coupling between its subdomains\), which happens if each of the services deals with a separate subset of requests \(as in [*Backends for Frontends*](<Backends for Frontends (BFF)>)\) or is choreographed by an upper layer \(as in [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]], [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]], or [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]\) which boils down to the same “separate subset of subrequests” under the hood\. However, if the services which form a layer need to intercommunicate, you immediately get a whole set of troubles with debugging, sharing data, and performance characteristic of the [[wiki/concepts/source/basic-metapatterns/services|*Services*]] architecture\.


![Diagrams of Backends for Frontends and Services with Polyglot Persistence.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Misc/Layers%20of%20Services.png)


> Thanks to its substantial benefits and minor drawbacks, and the many evolutions it supports, *Layers* became the default architecture for starting new projects\.

### Performance

The performance of a layered system is shaped by two factors:

- Communication between layers is slower than within a layer\. Components of a layer may access each other’s data directly, while accessing another layer involves data transformation \(as interfaces tend to operate generic data structures\), serialization, and often [IPC](https://en.wikipedia.org/wiki/Inter-process_communication) or networking\.
- The frequency and granularity of events or actions increases as we move from the upper more abstract layers to lower\-level components that interface an OS or hardware\.


> An ideal component should be replaceable and reusable\. As soon as a component exposes details of its implementation, such as workflows or data types, in its interface, it becomes incompatible with other possible implementations, and its interface may even see major changes as the related internals of the component evolve\. Therefore, well\-behaving components tend to have their interfaces written in most generic terms, which requires inputs to be transformed to their internal formats and thus penalizes performance\.

There is a number of optimizations to reduce interlayer calls:


![Caching the latest known state of the system in its highest layer.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Layers-caching.png)


*Caching*: an upper layer tends to *model* \(cache last known state of\) the layers below it\. This way it can behave as if it knew the state of the whole system without querying the actual state from the hardware present at the bottom of the system’s stack of layers\. Such an approach is universal for [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control software*]]\. For example, a network monitoring suite shows you the last known state of all the components it observes without actually querying them – it is subscribed to various notifications and remembers what and when each device has previously reported\.


![Aggregation of events from hardware by the lowest layer of a layered system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Layers-aggregation.png)


*Aggregation*: a lower layer collects multiple events before notifying the layer above it to avoid being overly chatty\. An example is an [IIoT](https://en.wikipedia.org/wiki/Industrial_internet_of_things) field gateway that collects data from all the sensors in the building and sends it in a single report to the server\. Or consider a data transfer over a network where a low\-level driver collects multiple data packets that come from the hardware and sends an acknowledgement for each of them while waiting for a datagram or file transfer to complete\. It notifies its client software only once when all the data has been collected and its integrity confirmed\.


![Sending a batch of commands all the way down to the lowest layer of a system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Layers-batching.png)


*Batching*: an upper layer forms a queue of commands and sends it as a single job to the layer below it\. This takes place in drivers for complex low\-level hardware, like printers, or in database access as *stored procedures*\. \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] describes variants of this approach as the *Combined Method*, *Enumeration Method*, and *Batch Method* patterns\. Programming languages and frameworks may implement *foreach* and *MapReduce* which allow for a single command to operate on multiple pieces of data\.


![Moving a part of the business logic from the highest layer to the lowest layer of the system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Layers-injection.png)


*Strategy injection*: an upper layer installs an event handler \(hook or [[wiki/concepts/source/implementation-metapatterns/plugins|*Ambassador Plugin*]]\) into the lower layer\. The goal is for the hook to do basic pre\-processing, filtering, aggregation, and decision making to process the majority of events autonomously while escalating to the upper layer in exceptional or important cases\. That may help in such time\-critical domains as [high\-frequency trading](https://en.wikipedia.org/wiki/High-frequency_trading)\.

Layers can be scaled independently, as [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|exemplified]] by common web applications that comprise a highly scalable and resource\-consuming frontend, somewhat scalable backend, and unscalable data layer\. Another example is an OS \(lower layer\) that runs multiple user applications \(upper layer\)\.

### Dependencies

Usually an upper layer depends on the *API* \(*application programming interface*\) of the layer directly below it\. That makes sense as the lower the layer is, the more stable it tends to be: a user\-facing software gets updated on a daily or weekly basis while hardware drivers may not change for years\. As every update of a component may destabilize other components that depend on it, it is much more preferable for a quickly evolving component to depend on others instead of the other way round\.

Some domains, including embedded systems and telecom, require their lower layers to be polymorphic as they deal with varied hardware or communication protocols\. In that case an upper layer \(e\.g\. OS kernel\) defines a *service provider interface* \(*SPI*\) which is implemented by every variant of the lower layer \(e\.g\. a device driver\)\. That allows for a single implementation of the upper layer to be interoperable with any subclass of the lower layer\. Such an approach enables [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]], [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]], and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]\.

There may also be an [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] layer between your system’s SPI and an external API\. It is called *Anticorruption Layer* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\], [*Database Abstraction Layer*](https://en.wikipedia.org/wiki/Database_abstraction_layer) / *Database Access Layer* \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] / *Data Mapper* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\], *OS Abstraction Layer*, or *Platform Abstraction Layer / Hardware Abstraction Layer*, depending on what kind of component it adapts\.


![Individual layers may depend on other layers' APIs, SPIs, or both. In the last case the layer between the SPI and API is an adapter.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Layers-1.png)


A layer can be *closed* \(*strict*\) or *open* \(*relaxed*\)\. A layer above a closed layer depends only on the closed layer right below it – it does not see through it\. Conversely, a layer above an open layer may depend on both the open layer and the layer below it – the open layer is transparent\. That helps keep a layer which encapsulates only one or two subdomains small: if such a layer were closed, it would have to copy much of the interface of the layer below it just to pass the incoming requests which it does not know how to handle through to the layer below\. The size optimization of open layers has a cost: the team that works on the layer above an open layer needs to learn APIs of both layers below it, which may even differ in their terminologies\.


![Dependencies for open and closed layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Layers-2.png)


If you ever need to *scale* \(run multiple instances of\) a layer, you may notice that a layer which sends requests naturally supports multiple instances, either through the use of communication channels or with the instance address being appended to each request so that its destination layer knows where to send the response\. On the other hand, if there are multiple instances of a layer you call into, you need a kind of [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] to dispatch requests among the instances\.


![A load balancer helps access multiple instances of a layer directly below it.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Layers-3.png)


### Applicability

*Layers* are <ins>good</ins> for:

- *Small and medium\-sized projects\.* Separating the business logic from the low\-level code should be enough to work comfortably on codebases below 100 000 lines in size\.
- *Specialized teams*\. You can have a team per layer: some people, who are proficient in optimization, work on the highly loaded infrastructure, while others talk to the customers and write the business logic\.
- *Deployment to a specific hardware\.* Frontend instances run on client devices, a backend needs much RAM, the data layer demands a large HDD and security\. There is no way to unite them into a single generic component\.
- *Flexible scaling\.* It is common to have hundreds or thousands of frontend instances being served by several backend processes that use a single database\.
- *Real\-time systems*\. Hardware components and network events often need the software to respond within a set time limit\. This is achievable by separating the time\-critical code from normal priority calculations\. See [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]], [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]], and [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] for improved solutions\.


*Layers* are <ins>bad</ins> for:

- *Large projects\.* You are still going to enter *monolithic hell* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] much sooner than your project will reach 1 000 000 lines of code\.
- *Low\-latency decision making*\. If your business logic needs to be applied in real time, you cannot tolerate the extra latency caused by the interlayer communication\.


### Relations


![Splitting a layer into services and splitting a service into layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Layers.png)


*Layers*:

- Can be applied to the internals of any component, for example, layering [[wiki/concepts/source/basic-metapatterns/services|*Services*]] results in [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]]\.
- Can be altered by [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] or extended with a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], and/or [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] which would become an extra layer\.
- Can be implemented by [[wiki/concepts/source/basic-metapatterns/services|*Services*]] yielding layers of services present in [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]], [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>), [*Backends for Frontends*](<Backends for Frontends (BFF)>), and [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\.
- May be closely related to [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]\.
- A layer often serves as a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], and/or [[wiki/concepts/source/extension-metapatterns/shared-repository|*\(Shared\) Repository*]], see [below](#variants-of-layer-roles)\.


## Variants by isolation

There are [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|several grades]] of layer isolation between unstructured [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] and distributed [*Tiers*](#three-tier-architecture)\. All of them are widely used in practice: each step adds its specific benefits and drawbacks to those of the previous stages until at some point it makes more sense to reject the next deal because its cons are too inconvenient for you\.

### Synchronous layers, Layered Monolith

First you separate the high\-level logic from low\-level implementation details\. Then draw interfaces between them\. The layers will still call each other directly, but at least the code has been sorted out into some kind of structure, and you can now have two or three dedicated teams, one per layer\. The cost is quite low – it is that the newly created interfaces will stand in the way of aggressive performance optimization\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Structured code | Lost opportunities for interlayer optimization |
| Two or three teams |  |

### Asynchronous layers

The next step you may decide to take could be to isolate the layers’ execution threads and data\. The layers will communicate only through in\-process messages, which are slower than direct calls and harder to debug, but now each layer can run at its own pace – a must for [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|interactive systems]]\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Structured code | No opportunities for interlayer optimization |
| Two or three teams | Some troubles with debugging |
| The layers may differ in latency |  |

### A process per layer

Next, you may run each layer in a separate process\. You have to devise an efficient means of communication between them, but now the layers may differ in technologies, security, frequency of deployment, and even stability – the crash of one layer does not directly impact any of the others\. Moreover, you may scale each layer to make good use of the available CPU cores\. However, you will pay through even harder debugging, lower performance, and you will have to take care of error recovery, because if one of the components crashes, the others are likely to remain in an inconsistent state\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Structured code | No opportunities for interlayer optimization |
| Two or three teams | Troublesome debugging |
| The layers may differ in latency | Some performance penalty |
| The layers may differ in technologies | Error recovery must be addressed |
| The layers are deployed independently |  |
| Software security isolation |  |
| Software fault isolation |  |
| Limited scalability |  |

### Distributed Tiers

Finally, you may separate the hardware which the processes run on – going all out for distribution\. This allows you to fine\-tune the resources available for each layer, run parts of the system close to its clients, and physically isolate the most secure components, with your scalability limited only by your budget\. The price is paid in latency and debugging experience\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Structured code | No opportunities for interlayer optimization |
| Two or three teams | Even worse debugging |
| The layers may differ in latency | Definite performance penalty |
| The layers may differ in technologies | Error recovery must be addressed |
| The layers are deployed independently |  |
| Full security isolation |  |
| Full fault isolation |  |
| Full scalability |  |
| Layers vary in hardware setup |  |
| Deployment close to clients |  |

## Variants of layer roles

Though the structure of every software system is unique, there is a common set of roles or functions that need to be covered by its code\. It is generally accepted that a piece of code should [*do one thing, and do it well*](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well), which often makes the code written to support the same kind of functionality stick together and end up in a dedicated layer of a system\. That also helps your teams specialize and keeps their cognitive load low by limiting the amount of code they deal with, which [allows for high productivity](https://realmensch.org/2018/05/04/we-are-all-10x-developers/)\.

That clarity of design, which separates technically different pieces, is opposed by a host of more pragmatic [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|*forces*]] that compel you to keep your code together:

- Performance can be easily optimized inside a component, while any communication between components will likely be much slower\.
- If many distinct workflows traverse a set of components, those components require large interfaces which take much effort to design, implement, and support\. You may end up spending more time maintaining your perfect architecture than writing the business logic which earns money for the company\.
- The more components you have, the harder it is to deploy them and keep them consistent, not to mention error recovery\. Moreover, as the number of system components increases, the big picture becomes elusive, and soon there is nobody who knows how to change the system if need arises\.


Balancing the [[wiki/concepts/source/analytics/cohesers-and-decouplers|cohesers and decouplers]] listed above usually results in coarse\-grained system components each of which covers several concerns, with some real\-world system compositions shown in the [Examples section](#examples) later in this chapter\. However, first we need to see which kinds of roles a system layer may incorporate:


![A stack of layers: client or user, interface, application, domain, generic code, communication, data, and operating system and hardware.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Layer%20Roles.png)


### Interface \(API or UI\)

If a system serves a human user or remote client software, there is a part of it, called an *interface*, that deals with communication and translation between the system’s internal data model and one convenient for its clients\.

As an interface represents the system to its clients, it is a kind of [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] by definition \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\]\. If the client is another software system, the interface is called an *Application Programming Interface* \(*API*\) and is likely to be implemented by a [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] which will receive a message through a well\-known protocol, check its correctness and authenticity of the sender, and forward the message’s payload to a layer below it\. In most cases it will also send response and notification messages by executing the converse tasks: translation from the system’s internal data format to something more convenient for its clients and sending the resulting message over a network protocol\.

When a system interacts with a human, it exposes another kind of interface – [[wiki/concepts/source/extension-metapatterns/proxy|*Human\-Machine Interface* \(*HMI*\) or *User Interface* \(*UI*\)]]\. The basics of its action are similar to the case of software\-to\-software interaction described above save that humans prefer visual or textual information instead of a highly structured Internet protocol\.

Another, less common kind of interface is called *Service Provider Interface* \(*SPI*\)\. It is declared by a system that relies on an external component and is implemented by that component’s authors to make it pluggable into the system\. *SPI*s are in use by [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] and [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] architectures, with *device drivers* being the best known example of pluggable components\.

There are also other kinds of *Proxies* which adapt a system to foreign interfaces:

- An [[wiki/concepts/source/extension-metapatterns/proxy|*Anticorruption Layer* or *Open Host Service*]] translates between two software subsystems to loosen dependencies between them\.
- A [[wiki/concepts/source/extension-metapatterns/proxy|*Hardware Abstraction Layer* or *Operating System Abstraction Layer*]] stands between a system and an underlying hardware or OS, respectively, to make the system portable\.



![A service wrapped with: a gateway with its API, a user interface, an Anticorruption Layer, a plugin and an Open Host Service with a Published Language.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Interface%20-%20Kinds.png)


A *Proxy* that implements an interface may reside in a dedicated layer \(and there may be multiple *Proxies* stacked together, for example, a *Gateway* behind a [[wiki/concepts/source/extension-metapatterns/proxy|*Firewall*]]\) or be merged with a neighboring layer: for example, an [[wiki/concepts/source/extension-metapatterns/proxy|*API Gateway*]] fills the roles of both interface and [*application*](#application-use-cases-or-integration)\.

An interface layer can contain multiple components \(services, modules, or high\-level classes\) when the system below it supports several kinds of clients: a bank is likely to provide a web interface, a mobile application, and a SWIFT endpoint\. See [*Backends for Frontends*](<Backends for Frontends (BFF)>) for a detailed description\.


![Diagrams of an API Gateway and Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Interface%20-%20Derived.png)


### Application \(use cases or integration\)

The *application* determines *what* a system does\. If it faces clients, the application runs client commands, called *use cases*, by executing chains of calls to its [*model*](#domain-business-rules-or-model) which knows *how* to do simple actions – the building blocks from which a use case is composed\.

For example, to transfer money between accounts, the application asks the model to:

- Verify that the client is the owner of the account to be charged\.
- Calculate the bank’s fee for the transfer\.
- Subtract the amount to be transferred and the fee from the client’s account\.
- Add the fee to the bank’s account\.
- Tell the recipient’s bank to add the transferred amount to the target account\.


It is also responsible for dealing with any error that may occur in the process\. For example, if the target account does not exist or is blocked, the application will need to both refund the client’s account and return a meaningful error message in the client’s preferred language\.

Another kind of software, called [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control systems*]], is written to supervise hardware or software entities\. In that case there are no client requests or use cases – instead, the system reacts to signals from the components controlled\. It is the application layer which is responsible for the system’s behavior: if a smoke sensor detects fire, the application tells an alarm to sound\. This role is called *integration* – the system acts as a living organism, all its parts orderly moving in response to a stimulus perceived by its senses\.

When an application resides in a dedicated layer, it is called an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\. Like the [*interface*](#interface-api-or-ui) layer, the application layer may also contain multiple components: the bank will likely have distinct applications for its clients and for its managers\. The corresponding pattern is also called [*Backends for Frontends*](<Backends for Frontends (BFF)>) \(there is little distinction between [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] and *Orchestrators* in that topology\)\.

Some systems lack the application role – they are structured as [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]], so that whatever enters one end of the system passes through all its components and pops out, digested, at the other end\. In that case it is the very structure of the system – the connections between its components – that drive its workflow\.


![Backends for Frontends between a gateway and a monolithic service; a pipeline with use case logic hardwired into the graph of connections.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Application%20-%20Derived.png)


### Domain \(business rules or model\)

The *domain* layer \(aka *model*\) models the real\-world system which your software operates or emulates\. It contains rules that describe *how* to do anything that your clients may want or *how* the hardware which you control needs to operate\.

Back to the banking example, the domain layer can:

- Find if an account is valid and who owns it\.
- Calculate a fee\.
- Add money to or subtract it from an account\.
- Transfer money to another bank\.


And it has some tricks up its sleeves to assure that nothing it does about money is ever lost, even if the network is disconnected or the hardware it runs on fails\.

In most cases the domain layer is the largest one and it is the one which makes your software valuable for business because it actually *does* whatever your software is about\. It is also [the only layer in which OOP classes may correspond to real\-world entities](http://tedfelix.com/software/jacobson1992.html)\.

As the largest layer, the domain is often the first among them to be subdivided:

- The most common way is to partition it into *subdomains* – loosely coupled subsets of your system’s functionality – yielding [[wiki/concepts/source/basic-metapatterns/services|*Services*]] \(when other layers are fragmented along the same lines or replicated among the subdomain components\) or a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]]\.
- Rare cases allow for [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*hierarchical* decomposition]] where most components blend [*application*](#application-use-cases-or-integration) and domain roles\.
- Last but not least, we can use separate models for making changes \(executing *commands*\) and for analytics \(running *queries*\), giving rise to [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Command Query Responsibility Segregation* \(*CQRS*\)]]\. This makes sense because a command usually involves many fields of a single record \(database row\) while a query runs over select rows of all the records – they vary in how they access and treat the data, which is why it is common to have a record wrapped into an OOP class in the command model, while the query model, if it is not omitted completely, provides for direct access to the database\.



![Diagrams of Services, Sandwich, Hierarchy, and Command-Query Responsibility Segregation.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Domain%20-%20Derived.png)


### Generic code \(libraries and utilities\)

*Generic code* is something not directly related to your business but still used by your logic: a graph traversal algorithm, an e\-mail server, or even a computer vision framework to identify duplicate user avatars\.

In most cases generic code stays together with the [*domain*\-level code](#domain-business-rules-or-model) which calls it\. However, when the domain layer gets subdivided into services, there emerge [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|multiple options]]:

- If the generic code is not shared, it moves into the service that uses it\. See [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- If it needs to be shared, it can be:
  - Extracted into a dedicated service, as in [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>)\.
  - Replicated as a [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecar*]] attached to every instance of each service that uses it\.
  - Copied into the codebases of the services to allow each team to change it independently from other teams – see *Separate Ways* in \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\.



![Diagrams of Services, Service-Oriented Architecture, and Microservices with sidecars, with components that carry generic code highlighted.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Generic%20Code%20-%20Derived.png)


### Communication \(middleware\)

If your system is made of multiple components, they need a way to communicate, which may be as simple as in\-process method calls or as complex as a [distributed consensus protocol](https://en.wikipedia.org/wiki/Paxos_(computer_science))\. The *communication infrastructure*, when used consistently throughout a system, makes a distinct virtual \(conjoining separately deployed nodes\) system layer, called [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] and often implemented with a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\.


![Multiple instances of a communication library represented as a virtual middleware layer.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Communication%20-%20Derived.png)


### Data \(persistence\)

Most systems but the simplest [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]] are stateful – they remember something about their users or their environment:

- A backend would usually *persist* useful facts to a *database* which makes a dedicated *persistence layer*\.
- A [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|real\-time *control system*]] does not have the leisure to access anything remote, therefore its state is embedded in its [*domain* layer](#domain-business-rules-or-model)’s memory\.
- Complex distributed frameworks that implement [[wiki/concepts/source/basic-metapatterns/services|*Actors*]] or [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] both keep each service’s data inside the service’s memory for fast access and back all the changes to a persistent data store to support failure recovery\.



![Diagrams of a three-tier system, hierarchical control system, and Space-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Data%20-%20Derived.png)


If the persistence layer becomes a system’s performance bottleneck, as it often does, one of [[wiki/concepts/source/extension-metapatterns/shared-repository|the cures]] is using several specialized data stores, leading to [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\.


![A load-balanced service over a database evolves into a monolith with two specialized databases or into a load-balanced stateless service over database replicas with a single leader.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Data%20-%20Evolutions.png)


### Operating system and hardware

All software always runs on *hardware* and usually relies on an *operating system* \(*OS*\) for file and network access and memory management\. Even though many modern backends don’t care about such low\-level details and omit them on their diagrams, embedded or systems software communicates with its OS or hardware directly, making the corresponding components indispensable parts of its topology\.

Integrating multiple pieces of hardware into an intelligently behaving system is usually what [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control software*]] is written for\. Such systems [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|often follow]] the [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Pedestal*]], [[wiki/concepts/source/basic-metapatterns/services|*Actors*]], or [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] architectures\.


![Diagrams of control systems with the following architectures: monolithic, actors, Pedestal, hierarchical.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/4Kinds/Control%20-%20variants.png)


## Examples

The notion of layering seems to be so natural to our minds that most known architectures are layered to an extent\. Not surprisingly, there are several approaches to assigning functionality to and naming the layers:

- [*ECB*](#entity-control-boundary-ecb-entity-boundary-control-ebc-boundary-control-entity-bce) distinguishes a client\-facing layer, use cases and domain logic\.
- [*DDD*](#domain-driven-design-ddd-layers) adds the infrastructure layer\.
- [*Tiers*](#three-tier-architecture) are distributed *Layers* that usually include frontend, backend, and database\.
- [Layering of an embedded system](#embedded-systems) often matches its supply chain\.


### Entity\-Control\-Boundary \(ECB\), Entity\-Boundary\-Control \(EBC\), Boundary\-Control\-Entity \(BCE\)


![The boundary, control and entity layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/ECB.png)


[*Entity\-Control\-Boundary*](https://en.wikipedia.org/wiki/Entity%E2%80%93control%E2%80%93boundary) \(*ECB*\) or other combinations of these words \(*EBC* and *BCE*\) designate a system composed of the following layers:

- *Boundary* – the layer which [interacts with the system’s *clients* or *users*](#interface-api-or-ui)\. See [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]]\.
- *Control* – the layer which [contains *use cases*](#application-use-cases-or-integration) – sequences of actions on the system’s internals that should be made to process a client’s request or respond to a user’s action\. See [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\.
- *Entity* – the bulk of the system’s business logic and data\.


A closer look at an *ECB* system may reveal a finer\-grained structure that resembles [*Backends for Frontends*](<Backends for Frontends (BFF)>) or [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) as each layer is composed of modules or objects:


![The boundary, control and entity layers, each subdivided into several services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/ECB%20as%20SOA.png)


### Domain\-Driven Design \(DDD\) Layers


![The four layers of Domain-Driven Design: presentation, application, domain, and infrastructure.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/DDD.png)


*Domain\-Driven Design* \(*DDD*\), as given in \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\], is a methodology for enterprise\-scale backend development which extends the more generic [*Entity\-Control\-Boundary*](#entity-control-boundary-ecb-entity-boundary-control-ebc-boundary-control-entity-bce) with a new *Infrastructure* layer responsible for [*communication*](#communication-middleware) and [*persistence*](#data-persistence) roles which don’t exist in most desktop applications\. Its layers are called:

- *Presentation* \([[wiki/concepts/source/extension-metapatterns/proxy|*User Interface*]]\) – the user\-facing component \(frontend, UI\)\. It should be highly responsive to the user's input\. See [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Separated Presentation*]]\.
- *Application* \([*Integration*](#application-use-cases-or-integration), *Service*\) – the high\-level scenarios which build upon the API of the *domain* layer\. It should be easy to change and to deploy\. See [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\.
- *Domain* \([*Model*](#domain-business-rules-or-model), *Business Rules*\) – the bulk of the mid\- and low\-level business logic\. It should usually be well\-tested and performant\.
- *Infrastructure* \(*Utility*, *Data Access*\) – the utility components devoid of business logic\. Their stability and performance is business\-critical but updates to their code are rare\.


For example, an online banking system comprises:

- the presentation layer which is its frontend;
- the application layer which implements sequences of steps for payment, card to card transfer, and viewing a client’s history of transactions;
- the domain layer with its classes for various kinds of cards and accounts;
- the infrastructure layer with a database and libraries for encryption and interbank communication\.


However, in practice you are much more likely to encounter the derived [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*DDD\-style Hexagonal Architecture*]] than the original *DDD Layers*\.

### Three\-Tier Architecture


![Four instances of the presentation layer accessing two instances of the logic layer accessing a single database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Three-Tier.png)


Here the focus lies with the distribution of the components over heterogeneous hardware \(*Tiers*\):

- *Presentation* \([[wiki/concepts/source/extension-metapatterns/proxy|*Frontend*]]\) tier – a user\-facing application which runs on a user’s hardware\. It is very scalable and responsive, but insecure\.
- *Logic* \(*Backend*\) tier – the business logic which is deployed on the service provider’s side\. Its scalability is limited mostly by the funding committed, security is good, but latency is high\.
- *Data* \(*Database*\) tier – a service provider’s database which runs on a dedicated server\. It is not scalable yet is very secure\.


In this case the division into layers resolves the conflict between scalability, latency, security, and cost as discussed in detail in the [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|chapter on distribution]]\.

> *Tiers* don’t map directly to *Layers*\. For example, a protocol support library which is used for communication between services belongs to the lowest \(infrastructure\) layer but to the middle \(backend\) tier\. The discrepancy is rooted in different natures \([views of the *4\+1 model*](https://en.wikipedia.org/wiki/4%2B1_architectural_view_model)\) of the patterns in question: *Layers* show the logical composition \(codebase\) of the system while *Tiers* deal with its physical structure \(deployment\)\.

### Embedded systems


![An embedded system with the following pairs of layers: user interface and human-machine interface, software development kit and hardware abstraction layer, firmware and hardware.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Embedded.png)


Bare metal and micro\-OS systems which run on low\-end chips use a different terminology, which is not unified across domains\. A generic example involves:

- *Presentation* – a UI engine used by the *HMI*\. It may be a third\-party library or come as a part of the *SDK*\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*Human\-Machine Interface*]] \(*HMI* aka *MMI*\) – the UI and high\-level business logic for user scenarios, written by a [value\-added reseller](https://en.wikipedia.org/wiki/Value-added_reseller)\.
- *Software Development Kit* \(*SDK*\) – the mid\-level business logic and device drivers, written by the [original equipment manufacturer](https://en.wikipedia.org/wiki/Original_equipment_manufacturer)\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*Hardware Abstraction Layer*]] \(*HAL*\) – the low\-level code that hides hardware registers to enable code reuse between hardware platforms\.
- *Firmware of Hardware Components* – usually closed\-source binary pre\-programmed into chips by chipmakers\.
- *Hardware* itself\.


It is of note that in this approach the layers form strongly coupled pairs\. Each pair is implemented by a separate party of the supply chain, which is an extra force that shapes the system into layers\.

An example of such a system can be found in an old mobile phone or a digital camera\.

## Evolutions

Layers are not without drawbacks which may force a layered system to evolve\. A summary of such evolutions is given below while more details can be found in [[wiki/concepts/source/appendices/evolutions-of-architectures|Appendix E]]\.

### [[wiki/concepts/source/appendices/evolutions-of-layers-that-make-more-layers|Evolutions that make more layers]]

Not all the layered architectures are equally layered\. A [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] with a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] or database has already stepped into the realm of *Layers* but is far from reaping all its benefits\. Such a system may continue its course in a few ways that were previously [[wiki/concepts/source/basic-metapatterns/monolith|discussed for *Monolith*]]:

- Employing a *database* \(if you don’t have one yet\) lets you rely on a thoroughly optimized state\-of\-the\-art subsystem for data processing and storage\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] are similarly reusable generic modules to be added at will\.
- Implementing an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] on top of your system may improve programming experience and runtime performance for your clients\.



![A diagram of calls in a layered system. A single request from a client is translated by an Orchestrator into multiple calls to lower layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Layers.png)


It is also common to:

- Have the business logic divided into two layers\.



![A backend is subdivided into application and domain layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Split%20in%20Two.png)


### [[wiki/concepts/source/appendices/evolutions-of-layers-that-help-large-projects|Evolutions that help large projects]]

The main drawback \(and benefit as well\) of *Layers* is that much or all of the business logic is kept together in one or two components\. That allows for easy debugging and fast development in the initial stages of the project but slows down and complicates work as the project grows in size \[[wiki/concepts/source/appendices/books-referenced|[MP]]\]\. The only way for a growing project to survive and continue evolving at a reasonable speed is to subdivide its business logic into several smaller, [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|thus less complex]], components that match subdomains \(*bounded contexts* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\)\. There are several options for such a change, with their applicability depending on the domain:

- In a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] the middle layer with the main business logic is divided into [[wiki/concepts/source/basic-metapatterns/services|*Services*]], leaving the upper [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and lower [[wiki/concepts/source/extension-metapatterns/shared-repository|*database*]] layers intact for future evolutions\.



![The domain layer is split into subdomain components, making a Sandwich.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Split%20Domain%20to%20Services.png)


- Sometimes the business logic can be represented as a set of directed graphs which is known as [[wiki/concepts/source/basic-metapatterns/pipeline|*Event\-Driven Architecture*]]\.



![A backend is subdivided into a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Split%20to%20Event-Driven%20Architecture.png)


- If you are lucky, your domain makes a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top\-Down Hierarchy*]]\.



![The lower layers of a system are subdivided, resulting in a hierarchy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Hierarchy.png)


### [[wiki/concepts/source/appendices/evolutions-of-layers-to-improve-performance|Evolutions that improve performance]]

There are several ways to improve the performance of a layered system\. One we have [[wiki/concepts/source/basic-metapatterns/shards|already discussed for *Shards*]]:

- [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] co\-locates the data store and business logic and scales both dynamically\.



![The database is migrated to a Data Grid, resulting in a scalable Space-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Space-Based%20Architecture.png)


Others are new:

- Merging several layers improves latency by eliminating the communication overhead\.



![The application and domain layers are merged.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Merge.png)


- [[wiki/concepts/source/basic-metapatterns/shards|Scaling]] some of the layers may improve throughput\.



![The application and domain layers are independently sharded.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers_%20Shard.png)


- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] is the name for using multiple specialized data stores\.



![The database layer is subdivided into specialized databases, resulting in Polyglot Persistence.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Polyglot%20Persistence.png)


### [[wiki/concepts/source/appendices/evolutions-of-layers-to-gain-flexibility|Evolutions to gain flexibility]]

The last group of evolutions to consider is about making the system more adaptable\. We have already discussed the following [[wiki/concepts/source/basic-metapatterns/monolith|evolutions for *Monolith*]]:

- The behavior of the system may be modified with [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]]\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] allows for abstracting the business logic from the technologies used in the project\.
- [[wiki/concepts/source/implementation-metapatterns/microkernel|*Scripts*]] allow for customization of the system’s logic on a per client basis\.



![Diagrams of Layers with plugins, Layers with scripts, and Hexagonal Architecture with a layered core.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Layers%20-%20Further%202.png)


There is also one new evolution which modifies the upper \(*orchestration*\) layer:

- The [[wiki/concepts/source/extension-metapatterns/orchestrator|orchestration layer]] may be split into [*Backends for Frontends*](<Backends for Frontends (BFF)>) to match the individual needs of several kinds of clients\.



![The application layer is split into Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Backends%20for%20Frontends.png)


## Summary

*Layered architecture* separates the high\-level logic from the low\-level details\. It is superior for medium\-sized projects as it supports rapid development by two or three teams, is flexible enough to resolve conflicting forces, and provides many options for further evolution, which will come in handy when the project grows in size and complexity\.

| \<\< [[wiki/concepts/source/basic-metapatterns/shards|Shards]] | ^ [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic metapatterns]] ^ | [[wiki/concepts/source/basic-metapatterns/services|Services]] \>\> |
| --- | --- | --- |
