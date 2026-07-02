---
title: "Evolutions of a Shared Repository"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Shared Repository.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Shared%20Repository
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Shared Repository

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Shared Repository.md`.

Once a database appears, it is unlikely to go away\. I see the following evolutions to improve performance of the data layer:

- [[wiki/concepts/source/basic-metapatterns/shards|*Shard*]] the database\.
- Use [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]] for dynamic scalability\.
- Divide the data into a private database per service\.
- Deploy specialized databases \([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\)\.


## Shard the database

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database_%20Shard.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database_%20Shard.png" alt="The shared database is sharded so that each database instance holds a subset of data," loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Sharding]] \([[wiki/concepts/source/basic-metapatterns/shards|Shards]]\), [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]], maybe [[wiki/concepts/source/extension-metapatterns/proxy|Sharding Proxy]]\.

<ins>Goal</ins>: increase capacity and performance of the database\.

<ins>Prerequisite</ins>: the data is shardable \(consists of independent records\)\.

If your database is overloaded and the data which it contains describes independent entities \(users, companies, or sales\) you can deploy multiple instances of the database with subsets of the data distributed among them\. You will need to deploy a *Sharding Proxy* or the services will have to find out which database *shard* to access by themselves, likely through hashing the record’s *primary key* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] or with the help of an [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassador*]]\. There is also a good chance that several smaller tables will have to be replicated to all the shards or moved to a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|dedicated *Shared Database*]] \(resulting in [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]]\)\.

Modern distributed databases support sharding out of the box, but an overgrown table may still impact the performance of the database\.

<ins>Pros</ins>:

- Unlimited scalability\.
- You don’t need to change your database vendor\.
- Failure of a single database instance affects few users\.


<ins>Cons</ins>:

- You will need to manage many instances of the database\.
- The application or a custom script may have to synchronize shared tables among the instances\.
- There is no way to do joins or run aggregate functions \(such as *sum* or *count*\) over multiple shards – all that logic moves to the services that use the database\.


<ins>Further steps</ins>:

- [[wiki/concepts/source/basic-metapatterns/shards|*Replicate*]] each shard to improve fault tolerance and, possibly, read throughput\.
- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] or [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]] describe pre\-calculating aggregates into another analytical database \([*Reporting Database*](https://martinfowler.com/bliki/ReportingDatabase.html)\)\.
- [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] may be cheaper as it scales dynamically\. However, in its default and highly performant configuration it is prone to write collisions\.


## Use Space\-Based Architecture

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database%20to%20Space-Based%20Architecture.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database%20to%20Space-Based%20Architecture.png" alt="The shared database is migrated to a Data Grid, resulting in Space-Based Architecture" loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/implementation-metapatterns/mesh|Space\-Based Architecture]] \([[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]], [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]\)\.

<ins>Goal</ins>: dynamically scale throughput of the database\.

<ins>Prerequisite</ins>: data collisions are acceptable\.

*Space\-Based Architecture* \(SBA\) duplicates the contents of a persistent database to a distributed in\-memory *cache* co\-located with the services managed by the *SBA*’s *Middleware*\. That makes most data access operations very fast unless one needs to avoid write collisions\. The [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh Middleware*]] autoscales both the services and the associated data cache under load, granting nearly perfect scalability\. However, this architecture is costly because of the amount of traffic and CPU time spent on replicating the data between the *Mesh nodes*\.

<ins>Pros</ins>:

- Nearly unlimited dynamic scalability\.
- Off\-the\-shelf solutions are available\.
- Very high fault tolerance\.


<ins>Cons</ins>:

- Choose one: data collisions or mediocre performance\.
- Low latency is guaranteed only when the entire dataset fits in the memory of a node\.
- High operational cost because the nodes will send each other lots of data\.
- No support for analytical queries\.


## Move the data to private databases of services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database%20to%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database%20to%20Services.png" alt="The shared database is split into databases dedicated to subdomains, resulting in Layered Services." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/services|Services]], [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: decouple the services, remove the performance bottleneck \(*Shared Database*\)\.

<ins>Prerequisite</ins>: the domain data is weakly coupled\.

If the data clearly follows subdomains, it may be possible to subdivide it accordingly\. The services will become [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreographed*]] \(or [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrated*]] if they have an [[wiki/concepts/source/extension-metapatterns/orchestrator|*integration layer*]]\) instead of communicating through the [[wiki/concepts/source/foundations-of-software-architecture/shared-data|shared data]]\.

<ins>Pros</ins>:

- The services become independent in their persistence and data processing technologies\.
- Performance of the [[wiki/concepts/source/basic-metapatterns/layers|*data layer*]], which tends to limit the scalability of the system, will likely improve thanks to the use of smaller specialized databases\.


<ins>Cons</ins>:

- The communication between the services and the synchronization of their data becomes a major issue\.
- Joins of the data from different subdomains will not be available\.
- Costs are likely to increase because of data transfer and duplication between the services\.
- You will have to administrate multiple databases\.


<ins>Further steps</ins>:

- [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS Views*]] or a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]] help a service access and join data that belongs to other services\.


## Deploy specialized databases

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database%20to%20Polyglot%20Persistence.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Shared%20Database%20to%20Polyglot%20Persistence.png" alt="The shared database is migrated to specialized databases." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]]\.

<ins>Goal</ins>: improve performance and maybe fault tolerance of the data layer\.

<ins>Prerequisite</ins>: there are diverse data types or patterns of data access\.

It is very likely that you can either use [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*specialized databases*]] for various data types or deploy [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*read\-only replicas*]] of your data for queries\.

<ins>Pros</ins>:

- You can choose one of the many specialized databases available on the market\.
- There is a good chance to significantly improve performance\.
- Replication improves fault tolerance of your data layer\.


<ins>Cons</ins>:

- It may take effort to learn the new technologies and use them efficiently\.
- Someone needs to see to the new database\(s\)\.
- You’ll likely need to work around *replication lag* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\]\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-middleware|Evolutions of a Middleware]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-a-proxy|Evolutions of a Proxy]] \>\> |
| --- | --- | --- |
