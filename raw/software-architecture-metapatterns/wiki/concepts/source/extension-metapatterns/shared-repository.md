---
title: "Shared Repository"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Extension metapatterns/Shared Repository.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Extension%20metapatterns/Shared%20Repository
source_license_note: "See namespace README; preserve attribution and source links."
---

# Shared Repository

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Extension metapatterns/Shared Repository.md`.


![A diagram for Services with a shared repository, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Shared%20Repository.png)


*Knowledge itself is power.* Sharing data is simple (& stupid).

<ins>Known as:</ins> Shared Repository \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\].

<ins>Structure:</ins> A layer of data shared among higher-level components.

<ins>Type:</ins> Extension for [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]].

| *Benefits* | *Drawbacks* |
| --- | --- |
| Supports domains with coupled data | A single point of failure |
| Implements data access and synchronization (consistency) concerns | All the services depend on the schema of the shared data |
| Helps saving on hardware, licenses, traffic, and administration | A single data store technology may not fit the needs of all the services equally well |
| Quick start for a project | Limits scalability |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] is all about databases; \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] has chapters on *Service-Based Architecture* and *Space-Based Architecture*; \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] deals with *Shared Event Store.*

A *Shared Repository* builds communication in the system around its data, which is natural for [[wiki/concepts/source/foundations-of-software-architecture/shared-data|data-centric domains]] and multiple [[wiki/concepts/source/basic-metapatterns/shards|instances of stateless services]] and may often simplify the development of a system of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] which need to exchange data. It covers the following concerns:

- Storage of the entire domain data.
- Keeping the data self-consistent by providing atomic transactions for use by the application code.
- Communication between the services (if the repository supports notifications on data change).
- Data aggregation and analytics (if the database engine supports complex queries).


The drawbacks are extensive coupling (it’s hard to alter a thing which is used in many places throughout the entire system) and limited scalability (even distributed databases struggle against distributed locks and the need to keep their nodes’ data in sync).

### Performance

A shared database with consistency guarantees ([ACID](https://en.wikipedia.org/wiki/ACID)) is likely to lower the total resource consumption compared to one database per service (as the services don’t need to implement and keep updated [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS views*]] of other services’ data) but it increases latency and it may become the system’s performance bottleneck. Moreover, by using a shared database services lose the ability to choose the database technologies which best fit their tasks and data.

Another danger lies with locking records inside the database. Different services may use different order of tables in transactions, hitting deadlocks in the database engine which show up as transaction timeouts.

Non-transactional distributed data stores may be very fast when colocated with the services (see [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]]) but the resource consumption becomes very high because of the associated data duplication (as every instance of each service gets a copy of the entire dataset) and simultaneous writes may corrupt the data (cause inconsistencies or merge conflicts).

### Dependencies

Normally, every service depends on the repository. If the repository does not provide notifications on changes to the data, the services may need to communicate directly, in which case they will also depend on each other through [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]] or *mutual* [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]].


![If the shared repository supports notifications, services depend only on the repository. Otherwise each service also depends on its event sources.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/SharedRepository-1.png)


Any dependencies on the repository technology and the data schema are dangerous for long-running projects as both of them may need to change sooner or later. Decoupling the code from the data storage is done with [yet another layer of indirection](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering) which is called a [[wiki/concepts/source/extension-metapatterns/proxy|*Database Abstraction Layer*]] (*DAL*), a *Database Access Layer* \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\], or a *Data Mapper* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\]. The DAL, which translates between the data schema and database’s API on one side and the business logic’s SPI on the other side, may reside inside each service or wrap the database:


![Each service may have a private Database Abstraction Layer, or there may be one shared Database Abstraction Layer colocated with the shared repository.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/SharedRepository-2.png)


Still, the DAL does not remove shared dependencies and only adds some flexibility. It seems that there is a peculiar kind of coupling through shared components: if one of the services needs to change the database schema or technology to better suit its needs, it is unable to do so because other components rely on (and exploit) the old schema and technology. Even deploying a second database, private to the service, is often not an option, as there is no convenient way to keep the databases in sync.

### Applicability

*Shared Repository* is <ins>good</ins> for:

- *Data-centric domains.* If most of your domain’s data is used in every subdomain, keeping any part of it private to a single service will be a pain in the system design. Examples include a [[wiki/concepts/source/foundations-of-software-architecture/shared-data|ticket reservation system]] and even the minesweeper game.
- *A scalable service.* When you run several [[wiki/concepts/source/basic-metapatterns/shards|instances]] of a service, like in [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]], the instances are likely to be identical and stateless, with the service’s data pushed out to a database shared among the instances.
- *Huge datasets*. Sometimes you may need to deal with a lot of data. It is unwise (meaning expensive) to stream and replicate it between your services just for the sake of ensuring their isolation. Share it instead. If the data does not fit in an ordinary database, some kind of [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]] (which [was invented to this end](https://en.wikipedia.org/wiki/Space-based_architecture#History)) may become your friend.
- *Quick simple projects.* Don’t over-engineer if the project won’t live long enough to benefit from its flexibility. You may also save a buck or two on the storage.


*Shared Repository* is <ins>bad</ins> for:

- *Quickly evolving, complex projects.* As everything changes, you just cannot devise a stable schema, while every change of the database schema breaks all the services.
- *Varied forces and algorithms*. Different services may require different kinds of data stores to work efficiently.
- *Big data with random writes*. Your data does not fit on a single server. If you want to avoid write conflicts, you must keep all the database nodes synchronized, which kills performance. If you let them all broadcast their changes asynchronously, you get collisions. You may want to first decouple and [[wiki/concepts/source/basic-metapatterns/shards|*shard*]] the data as much as possible, and then turn your attention to esoteric data stores, specialized caches, and even tailor-made [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] to get out of the trouble.


### Relations


![A shared repository for Services, Shards, and Service-Oriented Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Shared%20Repository.png)


*Shared Repository*:

- Extends [[wiki/concepts/source/basic-metapatterns/services|*Services*]], [*Service-Oriented Architecture*](<Service-Oriented Architecture (SOA)>), [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], or occasionally [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]].
- Is a part of a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]], [[wiki/concepts/source/extension-metapatterns/middleware|persistent *Middleware*]], or [[wiki/concepts/source/basic-metapatterns/pipeline|*Nanoservices*]].
- Is [closely related](https://itnext.io/a-practical-guide-to-modular-monoliths-with-net-59da23c01137) to [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]].
- May be implemented by a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]].


## Examples

*Shared Repository* is a sibling of [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]. While a *Middleware* assists direct communication between services (*shared-nothing* messaging), a *Shared Repository* grants them indirect communication through access to an external state (similar to *shared memory*) which usually stores all the data for the domain.

A *Shared Repository* may provide a generic interface (e.g. SQL) or a custom API (with a domain-aware [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] / [*ORM*](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) for the database). The *repository* itself can be anything ranging from a trivial OS file system or a memory block accessible from all the components to an ordinary database to a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]-based, distributed [*tuple space*](https://en.wikipedia.org/wiki/Tuple_space):

- A [*Shared Database*](#shared-database-integration-database-data-domain-database-of-service-based-architecture), [*Shared File System*](#shared-file-system), and [*Shared Memory*](#shared-memory) are just what you think they are.
- A [*Blackboard*](#blackboard) provides a shared solution space for several algorithms to cooperate on a task.
- A [*Data Grid*](#data-grid-of-space-based-architecture-sba-replicated-cache-distributed-cache) is a distributed in-memory data store that replicates data among many instances of multiple services.
- A [*Persistent Event Log*](#persistent-event-log-shared-event-store) stores every message sent between services for a possible future use.
- [*Stamp Coupling*](#inexact-stamp-coupling) is an approach for collecting data spread over the components of a *Pipeline*.


### Shared Database, Integration Database, Data Domain, Database of [[wiki/concepts/source/extension-metapatterns/sandwich|Service-Based Architecture]]


![Several services access a shared database and optionally communicate with each other directly.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Shared%20Database.png)


*Shared Database* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\], [*Integration Database*](https://martinfowler.com/bliki/IntegrationDatabase.html)*,* or *Data Domain* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] is a single database available to several [[wiki/concepts/source/basic-metapatterns/services|services]]. The services may subscribe to data change triggers in the database itself or notify each other directly about domain events. The latter is often the case with [[wiki/concepts/source/basic-metapatterns/services|*Service-Based Architecture*]] which consists of large services dedicated to subdomains.

### Shared File System


![An algorithm processes a batch of input files and writes output files. Its output becomes an input for another algorithm. The algorithms make a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Shared%20files.png)


As a file system is a kind of shared dictionary, writing and reading files can be used to transfer data between applications. A [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|data processing]] [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] which stores intermediate results in files benefits from the ability to restart its calculation from the last successful step because files are persistent \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\].

### Shared Memory


![Areas of shared memory (ring buffers) between two processes make a pair of event channels.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Shared%20memory.png)


Several actors (processes, modules, device drivers) communicate through one or more mutually accessible data structures (arrays, trees, or dictionaries). Accessing a shared object may require some kind of synchronization (e.g. taking a *mutex*) or employ [*atomic variables*](https://codescoddler.medium.com/concurrency-made-simple-the-role-of-atomic-variables-8327b9b35023). Notwithstanding that communication via *shared memory* is the archenemy of ([*shared-nothing*](https://www.scylladb.com/glossary/shared-nothing-architecture/)) messaging it is actually used to implement messaging: high-load multi-process systems (web browsers and high-frequency trading) rely on shared memory *mailboxes* for messaging between their [[wiki/concepts/source/basic-metapatterns/services|constituent processes]].

### [[wiki/concepts/source/extension-metapatterns/sandwich|Blackboard]]


![A Blackboard System includes a control which orchestrates knowledge sources which access a blackboard with shared data.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Blackboard.png)


[*Blackboard*](https://hillside.net/plop/plop97/Proceedings/lalanda.pdf) \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\] was used for non-deterministic calculations where several algorithms were concurring and collaborating to gradually build a solution from incomplete inputs. The *control* ([[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]) component schedules the work of several *knowledge sources* ([[wiki/concepts/source/basic-metapatterns/services|*Services*]]) which encapsulate algorithms for processing the data stored in the *blackboard* (*Shared Repository*) named after the well-known collaborative tool used for a brainstorming session. This approach has mostly been superseded by convolutional neural networks.

Examples: several use cases are [mentioned on Wikipedia](https://en.wikipedia.org/wiki/Blackboard_system).

### Data Grid of [[wiki/concepts/source/extension-metapatterns/sandwich|Space-Based Architecture]] (SBA), [[wiki/concepts/source/extension-metapatterns/proxy|Replicated Cache, Distributed Cache]]


![A layer of scaled processing units each connected to a node of an in-memory database over a data replication engine which communicates with a persistent database through readers and writers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Data%20Grid.png)


The [*Space-Based Architecture*](https://en.wikipedia.org/wiki/Space-based_architecture) (*SBA*) \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\] is a [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]] (a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]-based [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] with at least one [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] per service instance) which also implements an in-memory [*tuple space*](https://en.wikipedia.org/wiki/Tuple_space) (shared dictionary). Although it does not provide a full-featured database interface it has very good performance, elasticity, and fault tolerance, while some implementations allow for dealing with datasets which are much larger than anything digestible by ordinary databases. Its drawbacks include write collisions and high operating costs (huge traffic for data replication and lots of RAM to store the [[wiki/concepts/source/basic-metapatterns/shards|replicas]]).

The main components of the architecture are:

- *Processing Units* – the [[wiki/concepts/source/basic-metapatterns/services|*Services*]] with the business logic. There may be one class of *Processing Units*, making *SBA* look like [[wiki/concepts/source/basic-metapatterns/shards|*Replicated Load-Balanced Services*]], or multiple classes, in which case the architecture becomes similar to [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] with a *Shared Database*.
- *Data Grid* (*Replicated Cache* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\]) – a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]-based in-memory data store. Each node of the *Data Grid* is co-located with a single instance of a *Processing Unit*, providing the latter with very fast access to the data. Changes to the data are replicated across the grid by its virtual *Data Replication Engine* which is usually implemented by every node of the grid.
- *Persistent Database* – an external database which the *Data Grid* replicates (caches). Its schema is encapsulated in the *Readers* and *Writers*.
- *Data Readers* – components that read any data not found in the *Data Grid* from the *Persistent Database*. Most setups employ *Readers* upon starting the system to upload the entire contents of the database into the memory of the nodes.
- *Data Writers* – components that replicate the changes done in the *Data Grid* to the persistent storage to assure that no updates are lost if the system is shut down. There can be a pair of *Reader* and *Writer* per class of *Processing Units* (subdomain) or a global pair that processes all read and write requests.


*SBA* provides nearly perfect scalability (high read and write throughput as all the data is [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|cached]]) and elasticity (new instances of *Processing Units* are created and initialized very quickly as they copy their data from already running units with no need to access the *Persistent Database*). Though for smaller datasets the entire database is [[wiki/concepts/source/basic-metapatterns/shards|replicated]] to every node of the grid (the *Replicated Cache* mode), *Space-Based Architecture* also allows for processing datasets that don’t fit into the memory of a single node by assigning each node a [[wiki/concepts/source/basic-metapatterns/shards|*shard*]] of the dataset (the *Distributed Cache* mode).

The drawbacks of this architecture include:

- Structural and operational complexity.
- Very basic dictionary-like interface of the *tuple space* (no joins or other complex operations).
- High traffic for data replication among the nodes.
- Data collisions if multiple clients change the same piece of data simultaneously.


### [[wiki/concepts/source/extension-metapatterns/middleware|Persistent Event Log, Shared Event Store]]


![A service posts a message to a shared event log which both persists the message to a shared event store and forwards the message to other services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Shared%20Database%20-%20Event%20Log.png)


A data store for events (an *event log* for interservice events or an *event store* for internal state changes) [[wiki/concepts/source/foundations-of-software-architecture/shared-data|can be used]] as a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]: an event producer writes its events to a topic in the repository while the event consumers get notified as soon as a new record appears.

### (inexact) Stamp Coupling


![A message collects pieces of data while passing through a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Stamp%20Coupling.png)


*Stamp Coupling* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] happens when a single data structure passes through an entire [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], with separate fields of the data structure matching individual processing steps.

A [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreographed*]] system with no shared databases does not provide any way to aggregate the data spread over its multiple services. If we need to collect everything known about a user or purchase, we pass a query message through the system, and every service appends to it whatever it knows of the subject, just as administrative offices used to rubber stamp the paper documents which passed through them. The unified message becomes a kind of virtual (temporary) *Shared Repository* which the services (*Content Enrichers* according to \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\]) write to. This also manifests in the dependencies: all the services [[wiki/concepts/source/foundations-of-software-architecture/choreography|depend on the format of the query message]] as they would on the schema of a *Shared Repository*, instead of depending on one of their neighbors, as is usual with *Pipelines*.

## [[wiki/concepts/source/appendices/evolutions-of-a-shared-repository|Evolutions]]

Once a database appears, it is unlikely to go away. I see the [[wiki/concepts/source/appendices/evolutions-of-a-shared-repository|following evolutions]] to improve performance of the data layer:

- [[wiki/concepts/source/basic-metapatterns/shards|Shard]] the database.



![The shared database is sharded so that each database instance holds a subset of data,](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Shared%20Database_%20Shard.png)


- Use [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]] for dynamic scalability.



![The shared database is migrated to a Data Grid, resulting in Space-Based Architecture](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Shared%20Database%20to%20Space-Based%20Architecture.png)


- Divide the data into private databases.



![The shared database is split into databases dedicated to subdomains, resulting in Layered Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Shared%20Database%20to%20Services.png)


- Deploy specialized data stores ([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]).



![The shared database is migrated to specialized databases.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Shared%20Database%20to%20Polyglot%20Persistence.png)


## Summary

A *Shared Repository* encapsulates a system’s data, allowing for [[wiki/concepts/source/foundations-of-software-architecture/shared-data|data-centric]] development and kickstarting [[wiki/concepts/source/basic-metapatterns/services|*Service-Based*]] architectures through simplifying interservice interactions. Its downsides are a frozen data schema and limited performance.
