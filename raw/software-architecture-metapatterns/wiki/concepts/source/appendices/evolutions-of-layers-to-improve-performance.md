---
title: "Evolutions of Layers to improve performance"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Layers to improve performance.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Layers%20to%20improve%20performance
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Layers to improve performance

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Layers to improve performance.md`.

There are several ways to improve the performance of a [[wiki/concepts/source/basic-metapatterns/layers|*layered system*]]. One we have [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-data|already discussed]] for [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]]:

- [[wiki/concepts/source/implementation-metapatterns/mesh|*Space-Based Architecture*]] co-locates the data store and business logic and scales both dynamically.



![The database is migrated to a Data Grid, resulting in a scalable Space-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Space-Based%20Architecture.png)


Others are new and thus deserve more attention:

- Merging several layers improves latency by eliminating the communication overhead.
- Scaling some of the layers may improve throughput but degrade latency.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] is the name for using multiple specialized data stores.


## Merge several layers


![The application and domain layers are merged.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Merge.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]] or [[wiki/concepts/source/basic-metapatterns/monolith|Monolith]].

<ins>Goal</ins>: improve performance.

<ins>Prerequisite</ins>: the layers share programming language, hardware setup, and qualities.

If your system’s development [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|is finished]] (no changes are expected) and you really need that extra 5% performance improvement, then you can try merging everything back into a *Monolith* or a [[wiki/concepts/source/basic-metapatterns/layers|*3-Tier*]] system (front, back, data).

<ins>Pros</ins>:

- Enables aggressive performance optimizations.
- The system may become easier to debug.


<ins>Cons</ins>:

- The code is frozen – it will be much harder to evolve.
- Your teams lose the ability to work independently.


<ins>Further steps</ins>:

- [[wiki/concepts/source/basic-metapatterns/shards|*Shard*]] the entire system.


## Scale individual layers


![The application and domain layers are independently sharded.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers_%20Shard.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]], [[wiki/concepts/source/basic-metapatterns/shards|Shards]], often [[wiki/concepts/source/extension-metapatterns/proxy|Load Balancer]] ([[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]).

<ins>Goal</ins>: scale the system.

<ins>Prerequisite</ins>: some layers are [[wiki/concepts/source/basic-metapatterns/shards|stateless]] or limited to the [[wiki/concepts/source/basic-metapatterns/shards|data of a single client]].

Multiple instances or layers can be created, with their number and deployment [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|varying from layer to layer]]. That may work seamlessly if each instance of the layer which receives an event which can start a use case knows the instance of the next layer to communicate to. Otherwise you will need a *Load Balancer*.

<ins>Pros</ins>:

- Flexible scalability.
- Better fault tolerance.
- Co-deployment with clients is possible.


<ins>Cons</ins>:

- More complex operations (more parts to keep an eye on).


<ins>Further steps</ins>:

- [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space-Based Architecture*]] scales the data layer.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] improves performance of the data layer.


## Use multiple databases


![The database layer is subdivided into specialized databases, resulting in Polyglot Persistence.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Polyglot%20Persistence.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]], [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]].

<ins>Goal</ins>: optimize performance of data processing.

<ins>Prerequisite</ins>: there are isolated use cases for or subsets of the data.

If you have separated *commands* (write requests) from *queries* (read requests), you can serve the queries with [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|read-only replicas]] of the database while the main database is reserved for the commands.

If your types of data or data processing algorithms vary, you may deploy several [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|specialized databases]], each matching some of your needs. That lets you achieve the best performance in a wide range of cases.

<ins>Pros</ins>:

- The best performance for all the use cases.
- Specialized data processing algorithms out of the box.
- Replication may help with error recovery.


<ins>Cons</ins>:

- Someone will need to learn and administer all those databases.
- Keeping the databases consistent takes effort and the replication delay may negatively affect the UX.


<ins>Further steps</ins>:

- Serve the read and write requests with different backends in accordance with [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Command-Query Responsibility Segregation (CQRS)*]].
- Separate the backend into [[wiki/concepts/source/basic-metapatterns/services|*services*]] which match the already separated databases.
