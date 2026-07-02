---
title: "Shards"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Basic metapatterns/Shards.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Basic%20metapatterns/Shards
source_license_note: "See namespace README; preserve attribution and source links."
---

# Shards

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Basic metapatterns/Shards.md`.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Shards.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Shards.png" alt="A diagram for Shards, in abstractness-subdomain-sharding coordinates." loading="lazy" width=100%/>
</a>
</div>

*Attack of the clones\.* Solve scalability in the most straightforward manner\.

<ins>Known as:</ins> Shards, Instances, Replicas \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\]\.

<ins>Structure:</ins> A set of functionally identical subsystems with little or no intercommunication\.

<ins>Type:</ins> Implementation\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Good scalability | It’s hard to synchronize the whole system’s state |
| Good performance | There is operational effort to deploy or update multiple components |
| Improved latency and/or fault tolerance |  |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[POSA3]]\] is dedicated to pooling and resource management; \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] reviews *Shards*, *Replicas*, and *Stateless Instances*; \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] covers sharding and synchronization of *Replicas* in depth; Amazon promotes full\-system sharding, calling it [*Cell\-Based Architecture*](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html)\.

*Shards* are multiple and, in most cases, independent instances of a component or subsystem which the pattern is applied to\. They provide scalability, often redundancy, and sometimes locality, at the cost of slicing or duplicating the component’s state \(writable data\), which obviously does not affect inherently stateless components\. Most of this pattern’s specific evolutions look for a way to coordinate shards at the logic or data level\.

> There is a sibling metapattern, namely [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]], in which instances of a component closely communicate among themselves\. The difference between the patterns lies in the strength of interactions: while each *shard* exists primarily to serve its clients, a *Mesh node*’s priority is preserving the *Mesh* itself from falling prey to entropy, making the *Mesh* into a reliable distributed \(virtual\) layer\. Some systems, such as distributed databases, hold the middle ground – their shards or nodes both intercommunicate intensely and execute a variety of client requests\.

### Performance

A *shard* retains the performance of the original subsystem \(a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] in the simplest case\) as long as it runs independently\. Any task that involves intershard communication has its performance degraded by data serialization and network latency\. And as soon as multiple shards need to synchronize their states you find yourself on the horns of a dilemma: accept the possibility of  data inconsistency caused by  [write conflicts](https://en.wikipedia.org/wiki/Write%E2%80%93write_conflict) or else kill performance with distributed transactions \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\]\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Performance/Shards.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Performance/Shards.png" alt="Performance of Shards is the best when the request is limited to a single shard and the worst when the state of several shards needs to be synchronized." loading="lazy" width=100%/>
</a>
</div>

A [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] \(or its derivation, the [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]]\) is a common solution to let multiple shards access the same dataset\. However, it does not solve the performance vs consistency conflict \(which is rooted in the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)\) but only encapsulates its complexity inside a ready\-made third\-party component, making your life easier\.

### Dependencies

You may need to make sure that all the shards are instances of the same version of your software or at least that their interfaces and contracts are backward\- and [forward\-compatible](https://en.wikipedia.org/wiki/Forward_compatibility)\.

### Applicability

A *sharded* system features properties of the pattern it replicates \(a single\-component [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], local [[wiki/concepts/source/basic-metapatterns/layers|*layered*]] application or distributed [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\)\. Its peculiarities that originate with the *Shards’* scalability, are listed below\.

*Shards* are <ins>good</ins> for:

- *High or variable load\.* You need to scale your service up \(and sometimes down\)\. With *Shards* you are not limited to a single server’s CPU and memory\.
- *Survival of hardware failures\.* A bad HDD or failing RAM does not affect your business if there is another running instance of your application\. Still, make sure that your [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] and Internet connection are replicated as well\.
- *Improving worst case latency*\. If your service suffers from latency spikes, you can run a few replicas of it in parallel, broadcasting every user request to all of them, and returning the fastest response\. Adding a single replica turns your p90 into [p99](https://dzone.com/articles/mastering-latency-with-p90-p99-and-mean-response-t)\.
- *Improving locality\.* A world\-wide business optimizes latency and costs by deploying an instance of its software to a local data center in every region of interest\. Web and mobile applications that run on client devices are prominent examples of sharding hidden in plain sight\.
- [*Canary Release*](https://martinfowler.com/bliki/CanaryRelease.html)\. It is possible to deploy an instance of your application featuring new code along with the old, stable instances\. That tests the update in production\.


*Shards’* <ins>weak point</ins> is:

- *Shared data\.* If multiple instances of your application need to modify the same dataset, that means that none of them properly owns the data, thus you have to rely on an external component \(a *data layer*, implying [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]] or another kind of [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\)\.


### Relations

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Shards.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Shards.png" alt="Scaling a single service or the entire system." loading="lazy" width=100%/>
</a>
</div>

*Shards*:

- Applies to a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or any kind of subsystem\.
- Can be extended with [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]], [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] or [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\.
- Is the foundation for [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\.


## Variants by isolation

There are intermediate steps between a single\-threaded component and distributed *Shards* which gradually augment the pros and cons of having multiple instances of a subsystem:

### Multithreading

The first and very common advance towards scaling a component is running multiple execution threads\. That attempts to utilize all the available CPU cores or memory bandwidth but [requires](http://ithare.com/multi-threading-at-business-logic-level-is-considered-harmful/) protecting the data from simultaneous access from several threads, which in turn may cause deadlocks\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Limited scalability | More complex data access |

### Multiple processes

The next stage is running several \(usually single\-threaded\) instances of the component on the same system\. If one of them crashes, others survive\. However, sharing data among them and debugging multi\-instance scenarios becomes non\-trivial\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Limited scalability | Non\-trivial shared data access |
| Software fault isolation | Troublesome multi\-instance debugging |

### Distributed instances

Finally, instances of the subsystem may be distributed over a network to achieve nearly unlimited scalability and fault tolerance by [sacrificing](https://en.wikipedia.org/wiki/CAP_theorem) the consistency of the whole system’s state\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Full scalability | No shared data access |
| Full fault isolation | Hard multi\-instance debugging |
|  | No good way to synchronize states of the instances |

## Examples

Sharding can often be transparently applied to individual components of [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|data processing]] systems\. That does not hold for [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|control systems]] which make centralized decisions based on the modeled system’s state, which must be accessible as a whole, thus the main business logic that owns the model \(last known state of the system\) cannot be sharded\.

Many kinds of *Shards* require an external coordinating component \([[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]]\) to assign tasks to the individual instances\. In some cases the coordinator may be implicit, e\.g\. an OS socket or scheduler\. In others it may be replicated and co\-located with each client \(as an [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassador*]]\)\.

Shards usually don’t communicate with each other directly\. The common exception is [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] which includes distributed databases and [[wiki/concepts/source/implementation-metapatterns/mesh|*actor*]] systems that explicitly rely on communication between the instances\.

There are several subtypes of sharding that differ in the way they handle state:

- [*Shards* or *Partitions*](#persistent-slice-sharding-shards-partitions-multitenancy-cells-amazon-definition) are long\-lived service instances which own unique subsets of the system’s data\.
- [*Replicas*](#persistent-copy-replica) are also long\-lived but all of them hold copies of the same dataset\.
- [*Stateless Instances*](#stateless-pool-instances-replicated-load-balanced-services-work-queue-lambdas) reset their state after handling a request\.
- [*Actors*](#temporary-state-create-on-demand-actors) are stateful but exist only for the duration of a client’s session\.


### Persistent slice: Sharding, Shards, Partitions, Multitenancy, Cells \(Amazon definition\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Sharding.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Sharding.png" alt="A sharding proxy connects a new client to a shard that contains data for the first letter of the client's name." loading="lazy" width=100%/>
</a>
</div>

*Shards* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] own non\-overlapping slices of the system’s state\. For example, a sharded phonebook \(or DNS\) would use one shard for all contacts with initial “A”, another shard for contacts with initial “B”, and so on \(in reality they use hashes \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]\)\. A large wiki or forum may run several servers, each storing a subset of the articles\. This is proper [*sharding*](https://learn.microsoft.com/en-us/azure/architecture/patterns/sharding), which is also called *partitioning* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] in the world of databases\.

> Names are not evenly distributed across the letters of the alphabet\. Many names start with A but few start with Q\. If we use the first letter of a user’s name to assign them to a shard, the shard that serves users whose names start with A will be much more loaded than the one responsible for the letter Q\. Therefore, real\-world systems rely on *hashing* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] – calculation of a *checksum* of the user’s name which yields a seemingly random number\. Then we divide the checksum by the total number of shards we have and use the remainder as the id of the shard that has the user’s data\. For example, CRC16\(“Bender”\) = 52722\. If we have 10 shards, Bender goes to \(52722 % 10 = 2\) the 3rd one\.

Another use of *Shards* is when a service provider allocates a whole shard to each of its clients to grant them data isolation, stable performance, and security\. This approach is contrasted against a cheaper option of [*Multitenancy*](https://en.wikipedia.org/wiki/Multitenancy) where several client organizations \(tenants\) share a shard\. In that case different shards may be customized to vary in functionality, available resources, and [SLA](https://en.wikipedia.org/wiki/Service-level_agreement) to provide better service to higher\-paying tenants\.

*Cells*, according to the [Amazon terminology](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html), are copies of a whole system deployed to several data centers, each serving local users\. The locality improves latency and saves on Internet traffic while having multiple instances of the system up and running provides availability\. The downside of this approach is its complexity and the amount of global traffic needed to keep the *Cells* in sync\.

It usually takes a stand\-alone [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] – a kind of *Load Balancer* – to route a client’s requests to the shard that owns its data\. However, there are other options \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]:

- The *Sharding Proxy* may be deployed to each client as a client\-side [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassador*]] to avoid the extra network hop\. This approach requires a means for keeping the *Ambassadors* up\-to\-date with your system’s code\.
- You can publish your *sharding function* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] and the number of shards in your public API to let your clients choose which shard to access without your help\. That may work for internal clients implemented by your own or a neighbor team\.
- Finally, each shard may be able to forward client requests to any other shard – making each shard into a kind of *Sharding Proxy* and an entry point into the resulting [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\. If your client accesses a wrong shard, the request is still served, though a little slower, through being forwarded between the shards \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]\.


*Sharding* solves scaling of an application both in regard to the number of its clients and to the size of its data\. However, it works well only if each client’s data is independent from other clients\. Moreover, if one of the shards crashes, the information it owns becomes unavailable unless [*replication*](#persistent-copy-replica) \(see below\) has been set up as well\.

### Persistent copy: Replica

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Replica.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Replica.png" alt="A load balancer connects a new client to a free replica which propagates the changes made by the client to other replicas." loading="lazy" width=100%/>
</a>
</div>

*Replicas* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] are identical copies of a stateful \(sub\)system\. Replication improves the system’s throughput \(as each replica serves client requests\) and its stability \(as a fault in one replica does not affect others which may quickly take up the failed replica’s clients\)\. Replicas may also be used to improve tail latency through [*Request Hedging*](https://grpc.io/docs/guides/request-hedging/): each request is sent to several replicas in parallel and the first response received is returned to the client\. Mission\-critical hardware [runs as three copies](https://en.wikipedia.org/wiki/Triple_modular_redundancy) and relies on majority voting for computation results\.

The hard part comes from the need to keep the replicas’ data in sync\. The ordinary way is to let the replicas talk to each other on each data update\. If the communication is synchronous that may greatly slow down the processing of requests, yet if it is asynchronous the system suffers data conflicts when multiple clients change the same value simultaneously\. Synchronization code is quite complex, thus you will likely use a ready\-made [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] framework instead of writing one of your own\.

Another option found in the field is keeping the replicas only loosely identical\. That happens when isolated cache servers make a [[wiki/concepts/source/extension-metapatterns/proxy|*Caching Layer*]]\. As clients tend to send similar requests, the data inside each *cache* is more or less the same by the law of large numbers\.

And if your traffic is read\-heavy, you may turn to [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] by segregating your replicas into the roles of a fully\-functional *leader* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] and [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|derived, read\-only *followers*]]\. The followers serve only the read requests while the leader processes the write requests which make it update its data and broadcast the changes to all its followers\. And if the leader dies, one of its followers is elected to become a new leader\. As a refinement of this idea, the code of the service itself may be separated into write \(*command*\) and read \(*query*\) services \(see [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Command Query Responsibility Segregation*]] aka *CQRS*\)\.

Finally, you can mix sharding and replication to make sure that the data of each shard is replicated, either in whole among identical components \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] or piecemeal all over the system \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]\. That achieves fault tolerance for volumes of data too large to store unsharded\.

### Stateless: Pool, Instances, [[wiki/concepts/source/extension-metapatterns/sandwich|Replicated Load\-Balanced Services]], Work Queue, Lambdas

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Pool.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Pool.png" alt="A load balancer connects a new client to a free instance of a stateless backend that accesses a database shared among all the backend instances." loading="lazy" width=100%/>
</a>
</div>

A predefined number \(*pool* \[[wiki/concepts/source/appendices/books-referenced|[POSA3]]\]\) of instances \(*workers*\) is created during the initialization of the system \(sometimes called a *Work Queue* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\]\)\. When the system receives a task, a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] assigns it to one of the idle instances, called *Replicated Load\-Balanced Services* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\], from the pool\. As soon as the instance finishes processing its task it returns to the pool and its state is reset\. A well\-known example of this pattern is [FastCGI](https://en.wikipedia.org/wiki/FastCGI)\.

This approach allows for rapid allocation of a worker to any incoming task, but it uses a lot of resources even when there are no requests to serve, yet the system may still be overwhelmed at peak load\. Moreover, a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] \(database or file storage\) is usually involved for the sake of persistence, further limiting the pattern’s scalability\.

Many cloud services implement *dynamic* pools, the number of instances \([*lambdas*](https://jesseduffield.com/Notes-On-Lambda/)\) growing and shrinking according to the overall load: if all the current instances are busy serving user requests, new instances are created and added to the pool\. If some of the instances are idle for a while, they are destroyed\. Dynamic pooling is often implemented through [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]], as in [[wiki/concepts/source/implementation-metapatterns/mesh|*Microservices*]] or [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]]\.

### Temporary state: Create on Demand, [[wiki/concepts/source/basic-metapatterns/services|Actors]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Create%20on%20Demand.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Shards%20-%20Create%20on%20Demand.png" alt="A new stateful instance is created when a new client connects to the system." loading="lazy" width=100%/>
</a>
</div>

An instance is created for supporting an incoming client session and is destroyed when the session is closed\. Upon creation it is initialized with all the client\-related data which makes the instance able to interact with its client without much help from the backend\. Examples include web applications that run in users’ browsers and user\-dedicated [[wiki/concepts/source/basic-metapatterns/services|*actors*]] in backends of instant messengers\.

This approach provides responsiveness, perfect elasticity, and flexibility of deployment at the cost of slower session establishment and it usually relies on an external shared layer for persistence: instances of a frontend are initialized from and send their updates to a backend which itself uses a database\.

## Evolutions

There are two kinds of evolutions for *Shards*: those intrinsic to the component sharded and those specific to the *Shards* pattern\. All of them are summarized below while [[wiki/concepts/source/appendices/evolutions-of-architectures|Appendix E]] provides more details on the second kind\.

### Evolutions of a sharded monolith

When *Shards* are applied to a single component, which is a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], the resulting \(sub\)system follows most of the [[wiki/concepts/source/basic-metapatterns/monolith|evolutions of *Monolith*]]:

- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] allow for the parts of the system to [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|differ]] in *qualities*, technologies, and [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|deployment]]\. Various third\-party components can be integrated and the code becomes better structured\.
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] help to distribute the work among multiple teams and may decrease the project’s complexity if the division results in loosely coupled components\.
- [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] and its subtypes, namely [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] and [[wiki/concepts/source/implementation-metapatterns/microkernel|*Scripts*]], make the system more adaptable\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20-%20General.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20-%20General.png" alt="Diagrams of scaled Layers, Services with a middleware, Pipeline, Plugins, Hexagonal Architecture, and Scripts." loading="lazy" width=100%/>
</a>
</div>

There is a benefit of such transformations which is important in the context of *Shards*: in many cases the resulting components can be scaled independently, arranging for a better resource utilization by the system when compared to scaling a *Monolith*\. However, scaling individual services usually requires a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] or [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] to distribute requests among the scaled instances\.

### [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-data|Evolutions that share data]]

The issue peculiar to *Shards* is that of coordinating deployed instances, especially if their data becomes coupled\. The most direct solution is to let every instance access the shared data:

- If the whole dataset needs to be shared, it can be split into a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] layer\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20to%20Shared%20DB.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20to%20Shared%20DB.png" alt="The data of shards moves to a shared database. The shards become stateless and are deployed behind a load balancer." loading="lazy" width=100%/>
</a>
</div>

- If data collisions are tolerated, [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]] promises low latency and dynamic scalability\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20to%20Space-Based%20Architecture.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20to%20Space-Based%20Architecture.png" alt="The data of the shards moves to a Data Grid, resulting in a Space-Based Architecture." loading="lazy" width=100%/>
</a>
</div>

- If a part of the system’s data becomes coupled, only that part can be moved to a *Shared Repository*, making each instance manage [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|two stores of data: private and shared]]\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Shared%20DB.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Shared%20DB.png" alt="A coupled subset of the system's data is stored in a shared repository, while the bulk of the data is sharded." loading="lazy" width=100%/>
</a>
</div>

- Another possible option is to split a [[wiki/concepts/source/basic-metapatterns/services|service]] that owns the coupled data and is always deployed as a single instance\. The remaining parts of the system become coupled to that service, not to each other\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20split%20Shared%20Service.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20split%20Shared%20Service.png" alt="Coupled business logic and data is separated from shards into a shared singletone service." loading="lazy" width=100%/>
</a>
</div>

### [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-logic|Evolutions that share logic]]

Other cases are better solved by extracting the logic that couples the shards:

- Splitting a [[wiki/concepts/source/basic-metapatterns/services|service]] \(as discussed above\) yields a component that represents both shared data and shared logic\.
- Adding a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] lets the shards communicate with each other without maintaining direct connections\. It also may do housekeeping: error recovery, replication, and scaling\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Middleware.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Middleware.png" alt="A middleware manages shards and lets them communicate to each other." loading="lazy" width=100%/>
</a>
</div>

- A [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] hides the shards from the system’s clients\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Load%20Balancer.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Load%20Balancer.png" alt="A sharding proxy relieves clients from the need to find the appropriate shard." loading="lazy" width=100%/>
</a>
</div>

- An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] calls multiple shards to serve a user request\. That relieves the shards of the need to coordinate their states and actions by themselves\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20use%20Orchestrator.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20use%20Orchestrator.png" alt="The high-level logic of shards moves to a shared orchestrator which integrates the data stored within and processed by individual shards." loading="lazy" width=100%/>
</a>
</div>

## Summary

*Shards* are multiple instances of a component or subsystem which is thus made scalable and more fault tolerant\. *Sharding* does not change the nature of the component it applies to and it usually relies on a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] or [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] to manage the instances it spawns\. Its main weakness appears when the *shards* need to intercommunicate, often to the end of synchronizing their data\.

| \<\< [[wiki/concepts/source/basic-metapatterns/monolith|Monolith]] | ^ [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic metapatterns]] ^ | [[wiki/concepts/source/basic-metapatterns/layers|Layers]] \>\> |
| --- | --- | --- |
