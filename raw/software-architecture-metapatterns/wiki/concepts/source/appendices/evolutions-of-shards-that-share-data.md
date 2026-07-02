---
title: "Evolutions of Shards that share data"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Shards that share data.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Shards%20that%20share%20data
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Shards that share data

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Shards that share data.md`.

One issue peculiar to [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] is that of coordinating the instances deployed, especially if their data become coupled\. The most direct solution is to let the instances operate a component that wraps the shared data:

- If the whole dataset needs to be shared, it can be extracted into a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] layer\.
- If data collisions are tolerated, [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] promises low latency and dynamic scalability\.
- If a part of the system’s data becomes coupled, only that part can be moved to a *Shared Repository*, causing each instance to manage two data stores: [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|private and shared]]\.
- Another option is to split out a [[wiki/concepts/source/basic-metapatterns/services|*service*]] to own the coupled data and always deploy it as a single instance\. The remaining parts of the system become coupled to that service, not to each other\.


## Move all the data to a Shared Repository


![The data of shards moves to a shared database. The shards become stateless and are deployed behind a load balancer.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Shards/Shards%20to%20Shared%20DB.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Pool]] \([[wiki/concepts/source/basic-metapatterns/shards|Shards]]\), [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Database]] \([[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]\), [[wiki/concepts/source/extension-metapatterns/proxy|Load Balancer]] \([[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]\), [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: don’t struggle against the coupling of the shards, keep it simple and stupid\.

<ins>Prerequisite</ins>: the system is not under pressure for data size or latency \(which can be addressed by the further evolutions\)\.

In case a shard needs to access data owned by any other shard, the prerequisite of the independence of shards starts to fall apart\. Grab all the data of all the shards and push it into a *Shared Database*, if you can \(there may be too much data or the database access may be too slow\)\. As all the shards become identical, you’ll likely add a *Load Balancer*\.

<ins>Pros</ins>:

- You can choose one of the many specialized databases available\.
- The stateless instances of the main application become dynamically scalable\.
- Failure of a single instance affects a few users for a short time\.
- [*Canary Release*](https://martinfowler.com/bliki/CanaryRelease.html) is supported\.


<ins>Cons</ins>:

- The database limits the system’s scalability and performance\.
- The *Load Balancer* and *Shared Database* increase latency and are single points of failure\.


<ins>Further steps</ins>:

- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] will let you change your database in the future\.
- [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] decreases latency by co\-locating subsets of the data and the instances of your application\.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] uses multiple specialized databases, often discerning between commands and queries\. That may greatly relieve the primary \(write\) database\.
- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]] goes even further by processing read and write requests with dedicated *services*\.


## Use Space\-Based Architecture


![The data of the shards moves to a Data Grid, resulting in a Space-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Shards/Shards%20to%20Space-Based%20Architecture.png)


<ins>Patterns</ins>: [[wiki/concepts/source/implementation-metapatterns/mesh|Space\-Based Architecture]] \([[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]], [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]\), [[wiki/concepts/source/basic-metapatterns/shards|Shards]], [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: don’t struggle against the coupling between the shards, maintain high performance\.

<ins>Prerequisite</ins>: data collisions are acceptable\.

*Space\-Based Architecture* is a *Mesh* of nodes which comprise the application and a cached subset of the system’s data\. A node broadcasts any changes to its data to other nodes, and it may request any data that it needs from the other nodes\. Collectively, the nodes of the *Mesh* keep the entire system’s data cached in memory\.

Though *Space\-Based Architecture* may provide several modes of action, including [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|single write / multiple read]] replicas, it is most efficient when there is no write synchronization between its nodes, in which case data consistency is sacrificed for performance and scalability\.

<ins>Pros</ins>:

- Unlimited dynamic scalability\.
- Off\-the\-shelf solutions are available\.
- Failure of a single instance affects few users\.


<ins>Cons</ins>:

- Choose one: data collisions or mediocre performance\.
- Low latency is supported only for datasets that fit in memory of a single node\.
- High operational costs because the nodes exchange huge amounts of data\.
- No support for analytical queries\.


## Use a Shared Repository for the coupled subset of data


![A coupled subset of the system's data is stored in a shared repository, while the bulk of the data is sharded.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Shards/Shards%20add%20Shared%20DB.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Shards]], [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Private and Shared Databases]] \([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]]\), [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Database]] \([[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]\), [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: solve the coupling between shards without losing performance\.

<ins>Prerequisite</ins>: the shards are coupled through a small subset of data\.

If a subset of the data is accessed by all the shards, that subset can be moved into a dedicated database, which is likely to be fast if only because it is small\. Using a distributed database that keeps its data synchronized among all the shards may be even faster\.

This approach resembles [*Shared Kernel*](https://ddd-practitioners.com/home/glossary/bounded-context/bounded-context-relationship/shared-kernel/) \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\.

<ins>Pros</ins>:

- You can choose one of the many specialized databases available\.


<ins>Cons</ins>:

- The *Shared Database* increases latency and is the single point of failure\.


## Split a service with the coupled data


![Coupled business logic and data is separated from shards into a shared singletone service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Shards/Shards%20split%20Shared%20Service.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/services|Services]], [[wiki/concepts/source/basic-metapatterns/shards|Shards]]\.

<ins>Goal</ins>: solve the coupling between the shards in an honorable way\.

<ins>Prerequisite</ins>: the part of the domain which causes coupling between the shards is weakly coupled to the remaining domain\.

If a part of the domain is too cohesive to be sharded, we can often extract it from the main application into a dedicated service\. That way the main application remains sharded while the new service exists as a single instance\. In rare cases there is a chance to re\-shard the new service with a sharding key which is different from the one used for sharding the main application\.

This approach resembles [*Shared Kernel*](https://ddd-practitioners.com/home/glossary/bounded-context/bounded-context-relationship/shared-kernel/) \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\.

<ins>Pros</ins>:

- The main code should become a little bit simpler\.
- The new service can be given to a new team\.
- The new service may choose a database which best fits its needs\.


<ins>Cons</ins>:

- Now it’s hard to share data between the new service and the main application\.
- Scenarios that use the new service are harder to debug\.
- There is a moderate performance penalty for using the extra service\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-rely-on-plugins|Evolutions of a Monolith that rely on Plugins]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-logic|Evolutions of Shards that share logic]] \>\> |
| --- | --- | --- |
