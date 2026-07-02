---
title: "Polyglot Persistence"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Fragmented metapatterns/Polyglot Persistence.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Fragmented%20metapatterns/Polyglot%20Persistence
source_license_note: "See namespace README; preserve attribution and source links."
---

# Polyglot Persistence

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Fragmented metapatterns/Polyglot Persistence.md`.


![A diagram for Services with Polyglot Persistence, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Polyglot%20Persistence.png)


*Unbind your data\.* Use multiple specialized data stores\.

<ins>Known as:</ins> Polyglot Persistence\.

<ins>Structure:</ins> A layer of data services used by higher\-level components\.

<ins>Type:</ins> Extension component, derived from [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Performance is fine\-tuned for various data types and use cases | The peculiarities of each data store need to be learned |
| Less load on each data store | Muсh more work for the DevOps team |
| The data stores may satisfy conflicting forces | More points of failure in the system |
|  | Consistency is hard or slow to achieve |

<ins>References:</ins> The [original](https://martinfowler.com/bliki/PolyglotPersistence.html) and closely related [CQRS](https://martinfowler.com/bliki/CQRS.html) articles from Martin Fowler, chapter 7 of \[[wiki/concepts/source/appendices/books-referenced|[MP]]\], chapter 11 of \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] and much information dispersed all over the Web\.

You can choose a dedicated technology for each kind of data or pattern of data access in your system\. That improves performance \(as each data store engine is optimized for a few use cases\), distributes load between the data stores, and may solve conflicts between forces \(like when you need both low latency and large storage\)\. However, you may need to hire several experts to get the best use of and to support the multiple data stores, especially if those are full\-featured databases\. Moreover, having your data spread over multiple data stores makes it the application’s responsibility to keep the data in sync \(by implementing some kind of distributed transactions or making sure that the clients don’t get stale data\)\.

> A *database* is a complex service which provides both data storage and such high\-level functionality as transactions and analytical queries\. A [*data store*](https://en.wikipedia.org/wiki/Data_store) is anything where data can be placed and retrieved: a shared memory, file system, cloud storage, or a database\. Though this chapter mostly deals with databases, several patterns which it discusses pertain to non\-database storage\.

### Performance

*Polyglot Persistence* aims at improving performance through the following means:

- Optimize for [specific data use cases](#specialized-databases)\. It is impossible for a single database to be good at everything\.
- Redirect read traffic to [read\-only database *replicas*](#read-only-replicas)\. The write\-enabled *leader* database then processes only the write requests\.
- [*Cache* any frequently used data](#database-cache-cache-aside) in a fast in\-memory data store to let the majority of client requests be served without hitting the slower persistent storage\.
- Build a [*view* of the states of other services](#reporting-database-cqrs-view-database-event-sourced-view-source-aligned-native-data-product-quantum-dpq-of-data-mesh) in the system to avoid querying them\.
- Maintain an external [*index*](#external-search-index) or [*Memory Image*](#memory-image-materialized-view) for use with tasks that don’t need the history of changes\.
- [Purge old data](#historical-data-data-archiving) to a slower storage\.
- Store read\-only sequential [data as files](#data-file-content-delivery-network-cdn), often close to the end users who download them\.


Beware that the read\-write separation introduces a replication lag \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] which is a headache when both data consistency and responsiveness are important for the system’s clients\.

### Dependencies

In general, each service depends on all of the data stores which it uses\. There may also be an additional dependency between the data stores if they share a dataset \(one or more data stores are derived\)\.


![The business logic depends on every database. A derived database depends on its data source.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/PolyglotPersistence.png)


### Applicability

*Polyglot Persistence* <ins>helps</ins>:

- *High load and low latency projects\.* [*Specialized Databases*](#specialized-databases) shine when given fitting tasks\. [*Caching*](#database-cache-cache-aside) and [*Read\-Only Replicas*](#read-only-replicas) take the load off the main database\. [*External Search Indices*](#external-search-index) may occasionally save the day as well\.
- [*Event sourcing*](https://martinfowler.com/eaaDev/EventSourcing.html) *and* [*event collaboration*](https://martinfowler.com/eaaDev/EventCollaboration.html)*\.* A [*Memory Image*](#memory-image-materialized-view) maintains the current state of an event\-sourced component\. A [*CQRS View*](#reporting-database-cqrs-view-database-event-sourced-view-source-aligned-native-data-product-quantum-dpq-of-data-mesh) aggregates domain events to provide its host service with whatever data from other subdomains it may need to use\.
- *Conflicting forces*\. An instance of a stateless service inherits many of the qualities of the data store which it accesses for any given request it is processing\. When there are several data stores, the qualities \(e\.g\. latency\) of a service instance may vary from request to request, depending on which data store is involved\.


*Polyglot Persistence* may <ins>harm</ins>:

- *Small projects\.* Properly setting up and maintaining multiple databases is not that easy\.
- *High availability*\. Each data store which your system uses will tend to fail in its own crazy way\.
- *User experience*\. For systems with read\-write database separation the replication lag between the databases will make you [choose](https://medium.com/@Ian_carson/replication-lag-82c736081e32) between reading changes from the *leader* \(write database\), adding synchronization code to your application to wait for the read database to be updated, and risking returning outdated results to the users\.


### Relations


![Polyglot Persistence for Monolith, Layers, Shards, and Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Polyglot%20Persistence.png)


*Polyglot Persistence*:

- Extends [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], or [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- Is derived from [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] \(the persistence layer\) or [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\.
- Variants with derived databases have an aspect of [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] and are closely related to [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]]\.


## Examples with independent storage

Many cases of *Polyglot Persistence* use multiple data stores just because there is no single technology that matches all the application’s needs\. The data stores used are filled with different subsets of the system’s data:

- Each service may have its own private data while [another dataset is shared](#private-and-shared-databases)\.
- [Specialized databases](#specialized-databases) that differ in storage and analytical technologies may be used\.
- Many kinds of data can be [stored as files](#data-file-content-delivery-network-cdn)\.


### Private and Shared Databases


![A subset of data shared between shards and between services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/PP%20-%20Private%20and%20Shared.png)


If several services or shards become coupled through a subset of the system’s data, that subset can be put into a separate database which is accessible to all the participants\. All the other data remains private to the [[wiki/concepts/source/basic-metapatterns/shards|shards]] or [[wiki/concepts/source/basic-metapatterns/services|services]]\.

### Specialized Databases


![A service which uses both SQL and NoSQL databases.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/PP%20-%20Specialized.png)


Databases [vary in their optimal use cases](https://www.jamesserra.com/archive/2015/07/what-is-polyglot-persistence/)\. You can employ several different databases to achieve the best performance for each kind of data that you persist\.

### Data File, Content Delivery Network \(CDN\)


![A backend reads page templates while a frontend reads content from a content delivery network.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/PP%20-%20File%20Storage.png)


Some data is happy to stay in files\. Web frameworks load web page templates from OS files and store images and videos in a *Content Delivery Network* \(*CDN*\) which replicates the data all over the world so that each user downloads the content from the nearest server \(which is faster and cheaper\)\.

## Examples with derived storage

In other cases there is a single writable data store \(called *system of record* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]\) which is the main *source of truth* from which the other data stores are derived\. The primary reason to use several data stores is to [relieve the main database of read requests](#read-only-replicas) and maybe support some additional qualities: special kinds of queries, aggregation for [*materialized*](#memory-image-materialized-view) and [*CQRS views*](#reporting-database-cqrs-view-database-event-sourced-view-source-aligned-native-data-product-quantum-dpq-of-data-mesh), full text search for [*text indices*](#external-search-index), huge dataset size for [*historical data*](#historical-data-data-archiving), or high performance for an [*in\-memory cache*](#database-cache-cache-aside)\.

The updates to the derived data stores may come from:

- the main database as [*Change Data Capture*](https://www.dremio.com/wiki/change-data-capture/) \(*CDC*\) \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] \(a log of changes\),
- the application after it changes the main data store \(see caching strategies [below](#database-cache-cache-aside)\),
- another service as an *event stream* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]], [[wiki/concepts/source/appendices/books-referenced|MP]]\],
- a dedicated *indexer* that periodically crawls the main data store or web site\.



![A derived database is fed data from the main database, from an indexer which scans the main database, from application events, or from events originating with another service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/PP%20-%20Derived%20Storage.png)


### Read\-Only [[wiki/concepts/source/basic-metapatterns/shards|Replicas]]


![An instance of a backend writes to a leader database which streams updates to database replicas. Other backend instances read from the replicas.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Read-only%20Replica.png)


Multiple instances of the database are deployed and one of them is the *leader* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] instance which processes all writes to the system’s data\. The changes are then replicated to the other instances \(via [*Change Data Capture*](https://www.dremio.com/wiki/change-data-capture/) \(*CDC*\)\) which are used for read requests\. Distributing workload over multiple instances increases maximum read throughput which the system is capable of, as the database is usually the system’s bottleneck\. Having several running [[wiki/concepts/source/basic-metapatterns/shards|*replicas*]] greatly improves reliability and allows for nearly instant recovery of database failures as any replica may quickly be promoted to the leader role to serve write traffic\.

### Database [[wiki/concepts/source/extension-metapatterns/proxy|Cache]], Cache\-Aside


![A cache hit only reads from the cache; a cache miss reads from the cache, reads from the database, and writes to the cache; a write writes to the database and to the cache.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Cache-Aside.png)


Database queries are resource\-heavy while databases scale only to a limited extent\. That means that a highly loaded system benefits from bypassing its main database in as many queries as possible, which is usually achieved by storing recent queries and their results in an in\-memory data store \([*Cache\-Aside*](https://www.enjoyalgorithms.com/blog/cache-aside-caching-strategy)\)\. Each incoming query is first looked for in the fast cache, and if it is found then you are lucky to get the result immediately without having to consult the main database\.

Keeping the cache consistent with the main database is the hard part\. There are quite a few strategies \(some of them treat the [[wiki/concepts/source/extension-metapatterns/proxy|cache as a *Proxy*]] for the database\): [write\-through](https://www.enjoyalgorithms.com/blog/write-through-caching-strategy), [write\-behind](https://www.enjoyalgorithms.com/blog/write-behind-caching-pattern), [write\-around](https://www.enjoyalgorithms.com/blog/write-around-caching-pattern) and [refresh\-ahead](https://www.enjoyalgorithms.com/blog/refresh-ahead-caching-pattern)\.

### Memory Image, Materialized View


![At startup a service reads from an event store and writes to a memory image. At runtime it reads from the memory image and updates both the memory image and event store.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Memory%20Image.png)


[*Event sourcing*](https://martinfowler.com/eaaDev/EventSourcing.html) \(of [[wiki/concepts/source/basic-metapatterns/pipeline|*Event\-Driven Architecture*]] or [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]]\) is all about changes\. A service persists only *changes* to its data instead of its *current* data\. As a result, the service needs to aggregate its history into a [*Memory Image*](https://martinfowler.com/bliki/MemoryImage.html) \(*Materialized View* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]\) by loading a snapshot and replaying any further events to rebuild its current state \(which other architectural styles store in databases\) to start operating\.

### Reporting Database, CQRS View Database, Event\-Sourced View, Source\-Aligned \(Native\) Data Product Quantum \(DPQ\) of [[wiki/concepts/source/basic-metapatterns/pipeline|Data Mesh]]


![A service reads from a CQRS view which aggregates updates streamed by another service. An analyst queries a reporting database which aggregates a stream of events from the main database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Reporting%20DB%20and%20CQRS%20View.png)


It is common wisdom that a database is good for either *OLTP* \(transactions\) or *OLAP* \(queries\)\. Here we have two databases: one optimized for commands \(write traffic protected with transactions\) and another one for complex analytical queries\. The databases differ at least in their schemas \(the OLAP schema is optimized for queries\) and often vary in type \(e\.g\. SQL vs NoSQL\)\.

A [*Reporting Database*](https://martinfowler.com/bliki/ReportingDatabase.html) \(or *Source\-Aligned \(Native\) Data Product Quantum* of [[wiki/concepts/source/basic-metapatterns/pipeline|*Data Mesh*]] \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\]\) derives its data from a write\-enabled database in the same subsystem \(service\) while a *CQRS View* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] or *Event\-Sourced View* \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] is fed a stream of events from another service from which it filters the data relevant to its owner\. This way a *CQRS View* lets its host service query \(its replica of\) the data that originally belonged to other services\.

### Query Service, [[wiki/concepts/source/extension-metapatterns/orchestrator|Front Controller]], Data Warehouse, Data Lake, Aggregate Data Product Quantum \(DPQ\) of [[wiki/concepts/source/basic-metapatterns/pipeline|Data Mesh]]


![Several services both stream updates and query data from a shared query service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Query%20Service.png)


A *Query Service* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] \(or *Aggregate Data Product Quantum* of [[wiki/concepts/source/basic-metapatterns/pipeline|*Data Mesh*]] \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\]\) subscribes to events from several full\-featured services and aggregates them into its data store, making it a [*CQRS View*](#reporting-database-cqrs-view-database-event-sourced-view-source-aligned-native-data-product-quantum-dpq-of-data-mesh) of several services or even the whole system\. If any other service or a data analyst needs to process data which belongs to multiple services, it retrieves it from the *Query Service* which has already joined the data streams and represents the join in a convenient way\.

A [[wiki/concepts/source/extension-metapatterns/orchestrator|*Front Controller*]] \[[wiki/concepts/source/appendices/books-referenced|[SAHP]] [[wiki/concepts/source/analytics/ambiguous-patterns|but not]] [[wiki/concepts/source/appendices/books-referenced|PEAA]]\] is a *Query Service* embedded in the first \(user\-facing\) service of a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\. It collects status updates from the downstream components of the *Pipeline* to track the state of every request being processed by the *Pipeline*\.

*Data Warehouse* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] and *Data Lake* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] are *analytical* data stores that connect directly to and import all the data from the *operational* \(main\) databases of all the system’s services\. A *Data Warehouse* transforms the imported data into its own unified schema while a *Data Lake* stores the imported data in its original format\(s\)\.

### External Search Index


![An external index receives events from the main datastore. A service queries the external index to find ids of specific records which it later reads from the main database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Search%20Index.png)


Some domains require a kind of search which is not naturally supported by ordinary database engines\. Full text search, especially [NLP](https://en.wikipedia.org/wiki/Natural_language_processing)\-enabled, is one such case\. Geospatial data may be another\. If you are comfortable with your main data store\(s\), you can set up an *External Search Index* by deploying a product dedicated to the special kind of search that you need and feeding it updates from your main data store\.

Alternatively, you may just need a way to quickly search through text documents or videos stored in a file system or in a cloud, which requires some kind of index\.

### Historical Data, Data Archiving


![A service works with an operational database. An archiver reads from the operational database and writes to an archive. An analyst reads from both the archive and operational database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/3/Historical%20Data.png)


It is common to store the history of sales in a database\. However, once a month or two has passed, it is very unlikely that the historical records will ever be edited\. And though they are queried on very rare occasions, like audits, they still slow down your database\. Some businesses offload any data older than a couple of months to a cheaper [*archive storage*](https://www.datacore.com/glossary/what-is-data-archiving/) which does not allow for changing the data and has limited query capabilities\. That helps keep the main datasets small and fast\.

## Evolutions

*Polyglot Persistence* with derived storage can often be made subject to *CQRS*:

- The service that uses the read and write databases is [[wiki/concepts/source/fragmented-metapatterns/layered-services|split into separate read and write services]]\.



![The backend layer that uses OLAP and OLTP databases is subdivided into command and query backends, resulting in full-featured Command-Query Responsibility Segregation.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/3/Polyglor%20Persistence%20-%201.png)


## Summary

*Polyglot Persistence* employs several specialized data stores to improve performance, often at the cost of eventual data consistency or implementing transactions in the application\.

| \<\< [[wiki/concepts/source/fragmented-metapatterns/layered-services|Layered Services]] | ^ [[wiki/concepts/source/fragmented-metapatterns/fragmented-metapatterns|Fragmented metapatterns]] ^ | [Backends for Frontends \(BFF\)](<Backends for Frontends (BFF)>) \>\> |
| --- | --- | --- |
