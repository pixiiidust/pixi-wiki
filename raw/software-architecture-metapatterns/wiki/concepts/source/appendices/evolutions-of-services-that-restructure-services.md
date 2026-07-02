---
title: "Evolutions of Services that restructure services"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Services that restructure services.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Services%20that%20restructure%20services
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Services that restructure services

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Services that restructure services.md`.

[[wiki/concepts/source/basic-metapatterns/services|*Services*]] work well when each service matches a subdomain and is developed by a dedicated team\. If those premises change, you’ll need to restructure the system:

- A new feature request may emerge outside of any of the existing subdomains, creating a new service\.
- A service may grow too large to be developed by a single team, calling for division\.
- Two services may become so strongly coupled that they fare better when merged together\.
- The entire system may need to be glued back into a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] if the domain knowledge changes or interservice communication strongly degrades performance\.
- Alternatively, coupled services may be clustered into co\-deployed [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]] to reduce operational complexity\.


## Add or split a service

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Services/Services_%20Split.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Services/Services_%20Split.png" alt="A service is split in half." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/services|Services]]\.

<ins>Goal</ins>: get one more team to work on the project, decrease the size of an existing service\.

<ins>Prerequisite</ins>: there is a loosely coupled \(new or existing\) subdomain that does not have a dedicated service \(yet\)\.

If you need to add a new functionality that does not naturally fit into one of the existing services, you may create a new service and, maybe, get a new team for it\.

If one of your services has grown too large, you should look for a way to subdivide it \(likely through a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] stage with a shared [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*database*]]\) to decrease the size and, correspondingly, complexity of its code and get multiple teams to work on the resulting \(sub\)services\. However, that makes sense only if the old service is not highly cohesive – otherwise [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|the resulting subsystem may be more complex]] than the original service\.

<ins>Pros</ins>:

- You get an extra development team\.
- The complexity of the code decreases \(splitting an existing service\) or does not increase \(adding a new one\)\.
- The new service is independently scalable\.


<ins>Cons</ins>:

- You add to the operations complexity by creating a new system component and several inter\-component dependencies\.
- There is a new point of failure, which means that bugs and outages become more likely\.
- Performance \(or at least the latency and cost efficiency\) of the system will deteriorate because interservice communication is slow\.
- You may have a hard time debugging use cases that involve both the old and new service\.


## Merge services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Services/Services_%20Merge.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Services/Services_%20Merge.png" alt="Two services are merged." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/services|Services]], [[wiki/concepts/source/basic-metapatterns/monolith|Monolith]] or [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: accept the coupling of subdomains and improve performance\.

<ins>Prerequisite</ins>: the services use compatible technologies\.

If you see that several services communicate with each other almost as intensely as they call their internal methods, then they probably belong together\.

If your use cases have too high a latency or you pay too much for CPU and traffic, the issue may originate with the interservice communication, and merging the services should help\. No services, no headache\.

Alternatively, as the domain knowledge changes \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\], you may have to merge much of the code together only to subdivide it later along the updated subdomain boundaries\. Which means that you face [lots of work for no reason](https://martinfowler.com/bliki/MonolithFirst.html)\.

<ins>Pros</ins>:

- Improved performance\.
- It becomes easy for parts of the merged code to access each other and share data\.
- The new merged *service* or *Monolith* is easier to debug than the original *Services*\.


<ins>Cons</ins>:

- The development teams become even more interdependent\.
- There is no good way to vary qualities by subdomain\.
- You lose granular scalability by subdomain\.
- The merged codebase may be too large for comfortable development\.
- If anything fails, everything fails\.


## Cluster services

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Services/Services_%20Cluster.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Services/Services_%20Cluster.png" alt="Services are grouped into Cells, reducing their interdependencies." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Cell]] \([[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal Architecture]], [[wiki/concepts/source/basic-metapatterns/services|Services]]\)\.

<ins>Goal</ins>: reduce operational complexity, decouple subdomains, and improve performance\.

<ins>Prerequisite</ins>: there are distinct subdomains\.

When there are too many services, none sees the big picture: which components are involved in a use case and why the system works the way it does\. Moreover, managing tens to hundreds of different services with their databases is hard and error\-prone\.

Therefore, cluster the services which share a subdomain into a co\-deployed cohesive *Cell*\.

<ins>Pros</ins>:

- Managing ten *Cells* is much easier than managing a hundred services\.
- More clear and independent subdomains as their interdependencies become explicit\.
- Lower traffic because the closely communicating services are now co\-located\.
- Lower data storage requirements as the contents of the *Cell* may [[wiki/concepts/source/extension-metapatterns/shared-repository|share a database]]\.
- No boilerplate code for versioning or [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|data views]] inside the *Cell*\.


<ins>Cons</ins>:

- The development teams that work on services that belong to a single *Cell* need to synchronize their actions\.
- A *Cell* is usually scaled as a whole\.


<ins>Further steps</ins>:

- Complete the *Cell* encapsulation through the use of [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] and [[wiki/concepts/source/implementation-metapatterns/plugins|*Ambassador Plugins*]]\.
- Transform any strongly coupled *Cells* into [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwiches*]]\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-layers-to-gain-flexibility|Evolutions of Layers to gain flexibility]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-services-that-add-layers|Evolutions of Services that add layers]] \>\> |
| --- | --- | --- |
