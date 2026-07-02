---
title: "Evolutions of a Monolith that lead to Shards"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Monolith that lead to Shards.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Monolith%20that%20lead%20to%20Shards
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Monolith that lead to Shards

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Monolith that lead to Shards.md`.

One of the main drawbacks of the monolithic architecture is its lack of scalability – a single running instance of your system may not be enough to serve all its clients no matter how many resources you add in. If that is the case, you should consider [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] – *multiple instances* of a monolith. There are following options:

- Self-managed [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] – each instance owns a part of the system’s data and may communicate with every other instance (forming a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]).
- *Shards* with a [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] – each instance owns a part of the system’s data and relies on the external component to choose the right shard for the client.
- A [[wiki/concepts/source/basic-metapatterns/shards|*Pool of stateless instances*]] with a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] and a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] – any instance can process any request, but the database limits the throughput.
- A [[wiki/concepts/source/basic-metapatterns/shards|*stateful instance per client*]] with an external persistent storage – each instance owns the data related to its client and runs in a virtual environment (i.e. web browser or an [[wiki/concepts/source/basic-metapatterns/services|actor framework]]).


## Implement a Mesh of self-managed shards


![Several instances of a monolith are run as intercommunicating shards, each of which holds a subset of the system's data.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Mesh%20of%20Shards.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Sharding]] ([[wiki/concepts/source/basic-metapatterns/shards|Shards]]), [[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]].

<ins>Goal</ins>: scale a low-latency application with weakly coupled data.

<ins>Prerequisite</ins>: the application’s data can be split into semi-independent parts.

It is possible to run several instances of an application (*shards*), with each instance owning a part of the data. For example, a chat may deploy 16 servers, each responsible for a subset of users whose hashed names end in specific 4 bits (0 to 15). However, some scenarios (e.g. renaming a user or adding a contact) may require the shards to intercommunicate. And the more coupled the shards become, the more complex a *mesh engine* is required to support their interactions, up to implementing distributed transactions, at which point you will have written a distributed database.

<ins>Pros</ins>:

- The system scales to a predefined number of instances.
- Perfect fault tolerance if [[wiki/concepts/source/basic-metapatterns/shards|replication]] and error recovery are implemented.
- Latency is kept low.


<ins>Cons</ins>:

- Direct communication between the shards (the mesh engine logic) is likely to be quite complex.
- Intershard transactions are slow and/or complicated and may corrupt the data if undertested.
- A client must know which shard owns its data to benefit from low latency. An [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassador*]] [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] may be used on the client’s side.


## Split the data into isolated shards and add a Sharding Proxy


![Multiple instances of a monolith, each a subset of the system's data, are run behind a sharding proxy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Isolated%20Shards%20with%20Load%20Balancer.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Sharding]] ([[wiki/concepts/source/basic-metapatterns/shards|Shards]]), [[wiki/concepts/source/extension-metapatterns/proxy|Sharding Proxy]] ([[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]), [[wiki/concepts/source/basic-metapatterns/layers|Layers]].

<ins>Goal</ins>: scale an application with sliceable data.

<ins>Prerequisite</ins>: the application’s data can be sliced into independent, self-sufficient parts.

If all the data a user operates on, directly or indirectly, is never accessed by other users, then multiple independent instances (*shards*) of the application can be deployed, each owning an instance of a database with data for a subset of the system’s users. A special kind of *Proxy*, called *Sharding Proxy*, redirects a user request to a shard that has the user’s data.

<ins>Pros</ins>:

- Perfect static (predefined number of instances) scalability.
- Failure of one shard does not affect the users of the other shards.
- [*Canary Release*](https://martinfowler.com/bliki/CanaryRelease.html) is supported.


<ins>Cons</ins>:

- The *Sharding Proxy* is a single point of failure unless [[wiki/concepts/source/basic-metapatterns/shards|*replicated*]], and it also increases latency unless deployed as an [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassador*]].


## Separate the data layer and add a Load Balancer


![A monolith is transformed into stateless instances which run behind a load balancer and access a shared database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Stateless%20Shards%20with%20Shared%20DB.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Pool]] ([[wiki/concepts/source/basic-metapatterns/shards|Shards]]), [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]], [[wiki/concepts/source/extension-metapatterns/proxy|Load Balancer]] ([[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]), [[wiki/concepts/source/basic-metapatterns/layers|Layers]].

<ins>Goal</ins>: achieve limited scalability and elasticity with little effort.

<ins>Prerequisite</ins>: the persistent data is of manageable size.

As data moves into a dedicated layer ([[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] or [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared File System*]]), the application becomes stateless and instances of it can be created and destroyed dynamically depending on the system’s load. However, the *Shared Repository* becomes the system’s bottleneck unless [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space-Based Architecture*]] is used.

<ins>Pros</ins>:

- Easy to implement.
- Dynamic scalability.
- Failure of a single instance only affects a few users transiently.
- [*Canary Release*](https://martinfowler.com/bliki/CanaryRelease.html) is supported.


<ins>Cons</ins>:

- The database limits the system’s scalability and performance.
- The *Load Balancer* and *Shared Repository* increase latency and are single points of failure.


## Dedicate an instance to each client


![Each user is allocated a temporary instance of a subsystem which loads their data at the start of the session and persists any changes to the database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Instance%20per%20Client.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Create on Demand]] ([[wiki/concepts/source/basic-metapatterns/shards|Shards]]), [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]], [[wiki/concepts/source/implementation-metapatterns/microkernel|Virtualizer]] ([[wiki/concepts/source/implementation-metapatterns/microkernel|Microkernel]]), [[wiki/concepts/source/basic-metapatterns/layers|Layers]].

<ins>Goal</ins>: very low latency, dynamic scalability, and failure isolation.

<ins>Prerequisite</ins>: each client’s data is small and independent of other clients.

Each client gets an instance of the application which preloads their data into memory. This way all the data is instantly accessible and a processing fault associated with one client never affects the other clients. As systems tend to have thousands to millions of clients, it is inefficient to spawn a process per client. Instead, more lightweight entities are used: a web app in a browser or an *actor* in a [[wiki/concepts/source/basic-metapatterns/services|distributed framework]].

<ins>Pros</ins>:

- Nearly perfect dynamic scalability (limited by the persistence layer).
- Good latency as everything happens in memory.
- Fault isolation is one of the features of distributed frameworks.
- The frameworks are available out of the box.


<ins>Cons</ins>:

- Virtualization frameworks tend to introduce a performance penalty.
- You may need to learn an uncommon technology.
- Scalability and performance are still limited by the shared persistence layer.


## Further steps

In most cases *sharding* does not change much inside the application, thus the common evolutions for [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] (to [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], [[wiki/concepts/source/basic-metapatterns/services|*Services*]], and [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]) remain applicable after sharding. We’ll focus on the scalability of the resulting architectures:

- [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] can be scaled (often to a dramatic extent) and deployed individually, as [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|exemplified by the *Three-Tier Architecture*]].
- [[wiki/concepts/source/basic-metapatterns/services|*Services*]] allow for subdomains to scale independently with the help of [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancers*]] or a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]. They also improve performance of the data storage as each service uses its own database which is often chosen to best fit its specific needs.
- Granular scaling also applies to [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]], but in many cases it does not make much sense because pipeline components tend to be lightweight and stateless, making it easy to scale the pipeline as a whole.



![Diagrams of Layers with individual scaling, Services with a middleware and individual scaling, and pipeline scaled as a whole.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Shards%20-%20Further%201.png)


A few specific evolutions of [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] deal with the drawbacks:

- [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]] reimplements [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] with a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]. Its main goal is to make the [[wiki/concepts/source/basic-metapatterns/layers|data layer]] dynamically scalable, but the results are limited by the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem) thus, depending on the mode of action, it can either provide very high performance with no consistency guarantees for a small dataset, or reasonable performance for a huge dataset. It blends the best features of stateful [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] (being an option for either pattern to evolve to) but may be quite expensive to run and lacks support for analytical queries.
- [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], a mirror image of [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]], is another option for implementing use cases that deal with data of multiple shards without the need for the shards to intercommunicate. Stateless *Orchestrators* scale perfectly but may corrupt the data if two of them write to an overlapping set of records.



![Diagrams of Space-Based Architecture that replicates data and Shards with multiple orchestrators.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Shards%20-%20Further%202.png)
