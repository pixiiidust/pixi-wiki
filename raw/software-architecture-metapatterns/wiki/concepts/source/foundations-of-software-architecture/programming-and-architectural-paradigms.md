---
title: "Programming and architectural paradigms"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Foundations of software architecture/Arranging communication/Programming and architectural paradigms.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Foundations%20of%20software%20architecture/Arranging%20communication/Programming%20and%20architectural%20paradigms
source_license_note: "See namespace README; preserve attribution and source links."
---

# Programming and architectural paradigms

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Foundations of software architecture/Arranging communication/Programming and architectural paradigms.md`.

Sharing a database is the greatest sin when you architect [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] yet [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]] is built around shared data\. How do these approaches coexist? Does *Microservice Architecture* make any sense if blatantly violating its principles still results in successful projects?

Another programming paradox holds a clue\. There was C\. Then there came C\+\+ to kill C\. Then we’ve got Rust to kill C\+\+\. Now we have C, C\+\+, and Rust, all of them alive and kickin’\.

## Technologies are specialized

When a new technology emerges, it must show its superiority over existing mature methods\. In most cases that is achieved by specialization\. Is a car superior to a donkey? It depends\. Probably yes, when there are good roads, plenty of gas, and spare parts\. A car is narrowly specialized, thus some areas have successfully adopted cars, while others still rely on donkeys\.

The same holds true for programming languages and architectures\. C is good when you work close to hardware and need complete control over whatever happens in the system\. C\+\+ is great at partitioning business logic, but it lost the simplicity of its predecessor\. Rust will likely shine in communication libraries, which are often targeted by hackers, though we have yet to see its wide adoption\. Hence the usefulness \(and choice\) of a tool or programming language depends on the circumstances\.

Let’s turn our attention to your average code\. It often mixes together:

- *Object\-oriented* programming that divides the application into a tree of loosely interacting pieces\.
- *Functional* programming, with the output of one function becoming the input to another, [method chaining](https://en.wikipedia.org/wiki/Method_chaining) included\.
- *Procedural* programming, where multiple functions access the same set of data, which also happens inside classes whose many methods operate their private data members\.


Each [programming paradigm](https://en.wikipedia.org/wiki/Programming_paradigm) fits its own kind of tasks\. Moreover, the same three approaches reemerge at the system level:

## Object\-oriented \(centralized, shared nothing\) paradigm – orchestration

Almost every software project is too complex for a programmer to keep all the details of its requirements and implementation in their mind\. Notwithstanding, those details must be written down and run as code\.

The good old way out of the trouble is called [*divide and conquer*](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm)\. The global task is divided into several subtasks, and each subtask is subdivided again and again – till the resulting pieces are either simple enough to solve directly or [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|too messy]] to allow for further subdivision\. Essentially, we need to split our domain’s *control*, *logic*, and *data* into a single hierarchy of moderately sized components\.

We have heard a lot about keeping *logic and data* together: an object \(or [[wiki/concepts/source/basic-metapatterns/services|actor]], or [[wiki/concepts/source/basic-metapatterns/services|module]], or [[wiki/concepts/source/basic-metapatterns/services|service]] – no matter what you call it\) must own its data to assure its consistency and hide the complexity of the component’s internals from its users\. If the encapsulation of an object's data is violated, the object’s code can neither trust nor ever restructure it\. On the other hand, if the data is bound to the logic that deals with it, the entire thing becomes a useful black box which one does not need to look into to operate\.

Adding *control* to the blend is more subtle, but no less crucial than the encapsulation discussed above\. If an object commands another thing to do something, it must receive the result of the delegated action to know how to proceed with its own task\. Returning control after the action is conducted enables separation of high\-level supervising \(orchestration, integration\) logic from low\-level algorithms which it drives, adding depth to the structure\.


![A diagram of an object-oriented system built through composition.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Paradigms%20-%20Object-oriented.png)


The ability to address complex domains by reducing the whole to self\-contained pieces makes object\-oriented design ubiquitous\. This paradigm, when applied to distributed systems, gives birth to [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrated Services*]], and [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>)\.


![Diagrams of: Microservices, Orchestrated Services, and Service-Oriented Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Paradigms%20-%20Object-oriented%20-%20Variants.png)


## Functional \(decentralized, streaming\) paradigm – choreography

Sometimes you don’t need that level of fine\-tuning for the behavior of the system you build – it operates as an [assembly line](https://en.wikipedia.org/wiki/Assembly_line) with high throughput and little variance: its logic is made of steps that resemble work stations along a [conveyor belt](https://en.wikipedia.org/wiki/Conveyor_belt) through which identically structured pieces of data flow\. In that case there is very little to control: if an item is good, it goes further, otherwise it just falls off the line\. Here the *control* resides in the graph of connections*,* the [[wiki/concepts/source/basic-metapatterns/layers|domain *logic*]] is subdivided, while the *data* is copied \(or, more rarely, moved\) between the components\.


![A diagram of a pipeline with components implementing steps of data processing.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Paradigms%20-%20Functional.png)


Functional or pipelined design is famous for its simplicity and high performance as the majority of processing steps can be scaled\. However, its straightforward application lacks the depth needed for handling complex processes, which would translate into webs of relations between hundreds of functions present at the same level of design\. It is also inefficient for choose\-your\-own\-adventure\-style \([[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control*]]\) systems where too many too short conveyor belts would be required, negating the paradigm’s benefits\. And it may not be the right tool for making small changes in large sets of data as you’ll likely need to copy the whole dataset between the constituent functions\.

In distributed systems the functional paradigm is disguised as [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture*]], [[wiki/concepts/source/basic-metapatterns/pipeline|*Data Mesh*]], and various [[wiki/concepts/source/basic-metapatterns/pipeline|batch or stream]] processing \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]]\.


![Diagrams of Event-Driven Architecture and Data Mesh.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Paradigms%20-%20Functional%20-%20Variants.png)


## Procedural \(data\-centric\) paradigm – shared data

The final approach is integration through data\. There are cases where the domain data and business logic differ in structure – you cannot divide your project into objects because each of the many pieces of its logic needs to access several \(seemingly unrelated\) parts of its data\.


![A diagram of a procedural system where logic and data make independent hierarchies.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Paradigms%20-%20Data-centric.png)


In the data\-centric paradigm *logic* and *data* are orthogonal\. There are two ways to deal with the control:

- In procedural programming, like in object\-oriented paradigm, *control* is implemented inside the logic, making the logic layer hierarchical \([[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrated*]]\), as on the diagram above\.
- Another, much less common, option relies on [*Observer*](https://refactoring.guru/design-patterns/observer) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] to provide data change notifications, resulting in decentralized \([[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreographed*]]\) application logic, as shown below\.



![Components of a data-centric system rely on data change notifications.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Paradigms%20-%20Data-centric%20-%20Notifications.png)


The data\-centric approach works well for moderately\-sized projects with a stable data model \(like reservation of seats in trains or the game of chess\)\. The best\-known distributed data\-centric architectures include [[wiki/concepts/source/extension-metapatterns/shared-repository|*Services with a Shared Database*]] and [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]]\.


![Diagrams for Services with a shared database and Space-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Paradigms%20-%20Data-centric%20-%20Variants.png)


## Composite cases

The three programming paradigms tend to collaborate:

- An ordinary class is object\-oriented on the outside but procedural inside: each of its methods can access any of its private data members\. Moreover, a class  method may chain function calls, applying the functional paradigm to two or three lines of its code\.
- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]] tends to use [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]] \(pub/sub\) between [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]] and [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]] or communication via a [[wiki/concepts/source/foundations-of-software-architecture/shared-data|*shared database*]] inside them \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\]\.
- A system of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] \(or [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]]\) may be integrated through both [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] \(or [[wiki/concepts/source/extension-metapatterns/orchestrator|*processing grid*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*data grid*]], respectively\), see [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]]\.


## Reality is more complex

We have reviewed a few cases directly supported by common programming languages\. However, there is a wide variety of possible combinations of \(at least\) the following dimensions, each making a unique programming paradigm:

- Synchronous \(method calls\) vs asynchronous \(messaging\), with closely related:
  - Imperative vs reactive\.
  - Blocking vs non\-blocking\.
- Centralized \(orchestrated\) vs decentralized \(choreographed\) flow\.
- Shared data \(tuple space\) vs [shared nothing](https://en.wikipedia.org/wiki/Shared-nothing_architecture) \(messaging\)\.
- Commands \(actors\) vs notifications \(agents\)\.
- One\-to\-one \(channels\) vs many\-to\-one \(mailboxes\) vs one\-to\-many \(multicast\) vs many\-to\-many \(gossip\) communication\.


Some of the combinations look impossible or impractical, others are narrowly specialized thus uncommon, while many more are commonplace\. Discussing all of them would require insights from people who have used them in practice and would likely take a dedicated book\.

## Summary

We have deconstructed the most common programming paradigms into their driving forces and shown how those forces shape distributed architectures:

- An object\-oriented system relies on hierarchical decomposition of a complex domain, just like [*SOA*](<Service-Oriented Architecture (SOA)>) and [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrated \(Micro\-\)Services*]] do\.
- Functional programming streams data through a sequence of transformations, which is the idea behind [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture*]] and [[wiki/concepts/source/basic-metapatterns/pipeline|*Data Mesh*]]\.
- Procedural style lets any piece of logic access the entire project’s data, resembling [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*Services with a Shared Database*]]\.


Now let’s examine each of these approaches in depth:

| \<\< [[wiki/concepts/source/foundations-of-software-architecture/arranging-communication|Arranging communication]] | ^ [[wiki/concepts/source/foundations-of-software-architecture/arranging-communication|Arranging communication]] ^ | [[wiki/concepts/source/foundations-of-software-architecture/orchestration|Orchestration]] \>\> |
| --- | --- | --- |
