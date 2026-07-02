---
title: "Sharing functionality or data among services"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/Comparison of architectural patterns/Sharing functionality or data among services.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/Comparison%20of%20architectural%20patterns/Sharing%20functionality%20or%20data%20among%20services
source_license_note: "See namespace README; preserve attribution and source links."
---

# Sharing functionality or data among services

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/Comparison of architectural patterns/Sharing functionality or data among services.md`.

Architectural patterns manifest several ways of sharing functionality or data among their components\. Let’s consider a basic example: calls to two pieces of business logic need to be logged, while the logger is doing something more complex than mere console prints\. Additionally, the business logic also needs to access a system\-wide counter\.

## Direct call

The simplest way to use a shared functionality \(an *aspect*\) is to call the module which implements it directly\. This is possible if the users and the provider of the aspect reside in the same process, as in a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or module\-based \(single application\) [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]\.

Sharing data inside a process is similar, but usually requires some kind of protection, such as an [RW lock](https://en.wikipedia.org/wiki/Readers%E2%80%93writer_lock), around it to serialize access from multiple threads\.


![A logger and counter accessible for direct calls inside a monolith or in an infrastructure layer of Layered Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Sharing-DirectCall.png)


## Make a dedicated service

In a distributed system you can place the functionality or data to share into a separate service to be accessed over the network, yielding [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) for shared utilities or a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] / [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence*]] for shared data\.


![A shared logger deployed as a service in Service-Oriented Architecture. A shared counter deployed as a stand-alone shared database in Polyglot Persistence.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Sharing-DedicatedService.png)


## Delegate the aspect

A less obvious solution is [delegating](https://datatracker.ietf.org/doc/html/rfc1925) our needs to another layer of the system\. To continue our example of logging, a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] may log the user requests and a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] – the interservice communication\. In many cases one of these generic components is configurable to record every call to the methods which we need to log – with no changes to the code\!

In a similar way a service may [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|behave as a function]]: receive all the data it needs in an input message and send back all its work as an output – and let the database access remain the responsibility of its caller\.


![Message loggers in a proxy and middleware. A request counter in a gateway of a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Sharing-Delegate.png)


## Replicate it

Finally, each user of a component can get its own replica\. This is done implicitly in [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], and explicitly in [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]] of [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] for libraries or [[wiki/concepts/source/extension-metapatterns/shared-repository|*Data Grid*]] of [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] for data\.

Another case of replication is importing the same code in multiple services, which happens in [[wiki/concepts/source/basic-metapatterns/services|single\-layer *Nanoservices*]]\.


![Replicated loggers in each instance of a service in Shards, in code imported by every Nanoservice, and in sidecars of Microservices. A replicated counter in a Data Grid.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Sharing-Duplicate.png)


## Summary

There are four basic ways to share functionality or data in a system:

- Deploy everything together – messy yet fast and simple\.
- Place the component in question into a shared service to be accessed over the network – slow and less reliable\.
- Let another layer of the system both implement and use the needed function on your behalf – easy but generic, thus it may not always fit your code’s needs\.
- Make a copy of the component for each of its users – fast and reliable, but the copies are hard to keep in sync\.


| \<\< [[wiki/concepts/source/analytics/comparison-of-architectural-patterns|Comparison of architectural patterns]] | ^ [[wiki/concepts/source/analytics/comparison-of-architectural-patterns|Comparison of architectural patterns]] ^ | [[wiki/concepts/source/analytics/pipelines-in-architectural-patterns|Pipelines in architectural patterns]] \>\> |
| --- | --- | --- |
