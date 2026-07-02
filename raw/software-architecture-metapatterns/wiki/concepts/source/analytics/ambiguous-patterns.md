---
title: "Ambiguous patterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/Ambiguous patterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/Ambiguous%20patterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Ambiguous patterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/Ambiguous patterns.md`.

We’ve seen a single pattern come under many names, as happens with [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], and also one name used for multiple [[wiki/concepts/source/introduction/system-topologies|topologies]], as with [[wiki/concepts/source/basic-metapatterns/services|*Services*]], which may [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestrate each other]], make a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], or be components of a [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) \(*SOA*\)\. On top of that, there are several pattern names which are often believed to be unambiguous while each of them sees conflicting definitions in books or over the web, thanks to [*Semantic Diffusion*](https://martinfowler.com/bliki/SemanticDiffusion.html) or independent coining of the term by multiple authors\. Let’s explore the last kind, which is the most dangerous both for your understanding of other people and for your time wasted in arguments\.

### Monolith


![Diagrams of a Monolith as a single component, a co-deployed system, a synchronous distributed system, a Layered Architecture, and modules with a shared database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Ambiguous-Monolith.png)


The old books, namely \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] and \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\], described a *tightly coupled* [[wiki/concepts/source/basic-metapatterns/monolith|*unstructured* system]], where everything depends on everything, as *monolithic*, which matched the meaning of the word in Latin – “single stone”\.

Then something evil happened – I believe that the proponents of [*SOA*](<Service-Oriented Architecture (SOA)>), backed by the hype and money which they had earned from corporations, started labeling any *non\-distributed* system as *monolithic*, obviously to contrast the negative connotation of that word to their own most progressive design\.

It took only a decade for the karma to strike back – when the new generation behind [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] redefined *monolithic* as a *single unit of deployment* – to call the now obsolescent *SOA* systems [*Distributed Monoliths*](<Service-Oriented Architecture (SOA)#distributed-monolith>) \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] because their services used to grow so coupled that they had to be deployed together\.

The novel misnomers, [[wiki/concepts/source/basic-metapatterns/layers|*Layered Monolith*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] and [[wiki/concepts/source/basic-metapatterns/services|*Modular Monolith*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], which denote an application partitioned by abstractness or subdomain, respectively, add to the confusion\.

### Reactor


![Control flow diagrams for Reactor, Proactor, and Half-Sync/Half-Async.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Subtypes%20of%20Monolith.png)


People [tend to call](http://ithare.com/category/reactors/) any event\-driven service a *Reactor*\. In fact, there are three patterns that describe different threading models for an event\-handling system:

- A [[wiki/concepts/source/basic-metapatterns/monolith|*Reactor*]] \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] runs each task in a dedicated thread and blocks it on any calls outside of the component\. That allows for normal *imperative programming* but is resource\-consuming and not very responsive or flexible\.
- A [[wiki/concepts/source/basic-metapatterns/monolith|*Proactor*]] \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] relies on a single thread to serve all the system’s tasks in an interleaved manner, just like an OS uses a single CPU core to run multiple processes\. The resulting non\-blocking code is fragmented \(thus known as *callback hell*\) but it can address any incoming event immediately\. This suits [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|real\-time control systems]]\.
- [[wiki/concepts/source/basic-metapatterns/monolith|*Half\-Sync/Half\-Async*]] \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] is what we know better as *coroutines* or *fibers* – there are multiple *Reactor*\-like lightweight threads that block on a *Proactor*\-like engine which translates between synchronous calls from the user code and asynchronous system events\.


In most cases we’ll hear of *Proactor* being called *Reactor* – probably because *Reactor* was historically the first and the simplest of the three patterns, and it is similar in name to *reactive programming* found in *Proactor*\.

### Microkernel


![Diagrams of Microkernel according to Pattern-Oriented Software Architecture and of Plugins Architecture](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Ambiguous-Microkernel.png)


*Microkernel* is another notable case\. The confusion over it goes all the way back to \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\] which used [[wiki/concepts/source/implementation-metapatterns/microkernel|operating systems]] as examples of [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugin Architecture*]]\. I believe that it was a mismatch:

- An operating system is mainly about sharing the resources of producers among consumers, where both the producers and consumers may be written by external teams\. The *kernel* itself does not feature much logic – its role is to connect the other components together\.
- *Plugins*, on the other hand, extend or modify the business logic of the *core* – which is the sole reason for the system to exist and is in no way “*micro\-*” as it got the bulk of the system’s code\. In many such systems *plugins* are utterly optional – which cannot be said of *OS drivers*\.


Thus, here we have two architectural patterns of arguably similar structure \([[wiki/concepts/source/implementation-metapatterns/plugins|*Microkernel/Plugins*]] of \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\] omit 3 of 5 components of the original [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] of \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\]\) but very different intent and action known under the same name\.

### Domain Services


![Diagrams of domain services according to Domain-Driven Design and Fundamentals of Software Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Ambiguous-DomainServices.png)


I was told that [[wiki/concepts/source/basic-metapatterns/services|*Domain Services*]] of \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] are an incorrect term – because a *domain service* is always limited to the [[wiki/concepts/source/basic-metapatterns/layers|*domain* layer]] of \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] while those of \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] also cover the [[wiki/concepts/source/basic-metapatterns/layers|*application*]] and, maybe, *infrastructure*\.

I believe that both definitions are technically correct, if the difference in the meaning of *domain* is accounted for\. In \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] *domain* is almost synonymous with a *bounded context* of \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\], while \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] more often uses that word for the name of its [[wiki/concepts/source/basic-metapatterns/layers|middle layer]] which contains *business rules*\.

### Service\-Based Architecture


![Diagrams of Service-Based Architecture, Microservices, and Service-Oriented Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Ambiguous-ServiceBasedArchitecture.png)


\[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] calls anything made of services a *service\-based architecture*\.

\[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] differentiates [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] and [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>), leaving whatever remains \(large [[wiki/concepts/source/basic-metapatterns/services|subdomain\-scale services]]\) under the name of [[wiki/concepts/source/basic-metapatterns/services|*Service\-Based Architecture*]]\.

Both definitions are technically correct\. One is wider than the other\.

### Front Controller


![Diagrams of Front Controller according to Patterns of Enterprise Application Architecture and Software Architecture: the Hard Parts.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Ambiguous-FrontController.png)


\[[wiki/concepts/source/appendices/books-referenced|[PEAA]] and [[wiki/concepts/source/appendices/books-referenced|POSA4]]\] define [*Front Controller*](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff648617(v=pandp.10)?redirectedfrom=MSDN) as an [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVC*]] \(or, more likely, a [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVP*]]\) derivative for backend programming\. In this pattern multiple web pages share a request processing component which turns the incoming requests into commands and forwards them to appropriate page classes\.

The definition from \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] is much more interesting – it describes an [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture*]] with a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]] embedded in the first \(client\-facing\) service\. The [[wiki/concepts/source/extension-metapatterns/orchestrator|*Front Controller*]] subscribes to notifications from downstream services to know the status of every request which it has passed to the [[wiki/concepts/source/basic-metapatterns/pipeline|*pipeline*]]\.

### Cells


![Diagrams of WSO2 Cells and Amazon Cells.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Ambiguous-Cells.png)


The fresh *Cell\-Based Architecture* also has multiple definitions\.

- [WSO2 defined](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]] as a group of services which is encapsulated from the remaining system by a [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] \(for incoming traffic\) and sometimes [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] \(for outgoing traffic\) and often uses a dedicated [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] – causing each *Cell*, though internally distributed, to be treated by other components as a single service\. This makes designing and managing a large system much simpler by introducing a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*hierarchy*]]\.
- Amazon [promotes](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html) its [[wiki/concepts/source/basic-metapatterns/shards|*Cells*]] as [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] of the whole system which run in multiple geographic regions\. That grants fault tolerance and improves performance as each client has an instance of the system deployed to a nearby datacenter, but it does not have much impact on the organization and complexity of the code\.


This case looks like Amazon’s hijacking and redefining a popular emerging technology, though I may be wrong about that as I did not investigate the history of the term\.

### Nanoservices


![Diagrams of Nanoservices as an API layer over a shared database, a pipeline, a Space-Based Architecture, actors, and a Service-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Ambiguous-Nanoservices.png)


The *Nanoservices* pattern is another emerging technology and it seems to have never been strictly defined\. Most sources agree that a [[wiki/concepts/source/basic-metapatterns/services|*nanoservice*]] is a cloud\-based function \([*FaaS*](https://en.wikipedia.org/wiki/Function_as_a_service)\), similar to a *service* with a single API method but, just as with the old good [[wiki/concepts/source/basic-metapatterns/services|*services*]], they differ in the ways to use the novel technology:

- Diego Zanon in *Building Serverless Web Applications* proposes a [[wiki/concepts/source/basic-metapatterns/services|single layer of nanoservices]], each implementing a method of the system’s public API, to be used as a thin backend\.
- [Here](https://increment.com/software-architecture/the-rise-of-nanoservices/) we have nanoservices [[wiki/concepts/source/basic-metapatterns/pipeline|comprising]] a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], similar to [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture*]]\.
- [Another article](https://medium.com/@ido.vapner/unlocking-the-power-of-nano-services-a-new-era-in-microservices-architecture-22647ea36f22) proposes to [\(re\)use them](<Service-Oriented Architecture (SOA)#nanoservices>) in [*SOA*](<Service-Oriented Architecture (SOA)>) style\.


Moreover, there are a couple of sources that call a nanoservice something totally different:

- [There is a concept](https://nanoservices.io/docs/docs/building/introduction/) of nanoservice as a module that can run both as a separate service and as a part of a binary – allowing for a team to choose if they want their system to run as a single process or become distributed\. *Nano\-* is because an in\-process module is more lightweight than a [[wiki/concepts/source/basic-metapatterns/services|*microservice*]]\. This idea resembles [[wiki/concepts/source/basic-metapatterns/services|*Modular Monolith*]] and [[wiki/concepts/source/basic-metapatterns/services|*Actor Frameworks*]]\.
- And [here](https://dev.to/siy/nanoservices-or-alternative-to-monoliths-and-microservices-12bb) we have something akin to [[wiki/concepts/source/implementation-metapatterns/mesh|*Space\-Based Architecture*]] but it is also called *Nanoservices* – as the proposed framework makes new components so easy to create that programmers tend to write many smaller *nanoservices* instead of a single [[wiki/concepts/source/basic-metapatterns/services|*microservice*]]\.


In my opinion, the disarray happened because the notion of *making smaller microservices* got hyped but was never adopted widely enough to become an industry standard, therefore everybody follows their own vision about what “smaller” means\.

### Summary

Several names of architectural patterns cause confusion as the meaning of each of them changes from source to source\. This book aims at identifying such issues and building a cohesive understanding of software and systems architecture, similar to the *ubiquitous language* of \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\.

| \<\< [[wiki/concepts/source/analytics/indirection-in-commands-and-queries|Indirection in commands and queries]] | ^ [[wiki/concepts/source/analytics/analytics|Analytics]] ^ | [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|Architecture and product life cycle]] \>\> |
| --- | --- | --- |
