---
title: "Monolith"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Basic metapatterns/Monolith.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Basic%20metapatterns/Monolith
source_license_note: "See namespace README; preserve attribution and source links."
---

# Monolith

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Basic metapatterns/Monolith.md`.

Let’s take a look at the simplest possible [[wiki/concepts/source/introduction/metapatterns|metapattern]] – *Monolith* – and see what it can teach us\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Monolith.png" alt="A diagram for Monolith, in abstractness-subdomain-sharding coordinates." loading="lazy" width=100%/>
</a>
</div>

*Keep it simple, stupid\!* If you don’t need a modular design, why bother?

<ins>Known as:</ins> Monolith, Monolithic Architecture\.

<ins>Structure:</ins> A monoblock with no strong internal modularity\.

<ins>Type:</ins> System topology, the root of the hierarchy of metapatterns\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Rapid start of development | Quickly deteriorates with project growth |
| Easy debugging | Hard to develop with multiple teams |
| Best latency | Does not scale |
| Low resource consumption | Lacks support for conflicting forces |
| The system’s state is self\-consistent | Any failure crashes the entire system |

<ins>References:</ins> [Big Ball of Mud](http://www.laputan.org/mud/) for a philosophical discussion, [my article](https://itnext.io/introduction-to-software-architecture-with-actors-part-2-on-handling-messages-940c62cb06dc) and \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] for subtypes of *Monolith*, Martin Fowler’s discussion on [starting development with *Monolith*](https://martinfowler.com/bliki/MonolithFirst.html), \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] for the [definition of *monolithic hell*](https://livebook.manning.com/book/microservices-patterns/chapter-1/25) and a post describing the [first\-hand experience of it](https://news.ycombinator.com/item?id=18442941)\.

We distance ourselves from the [[wiki/concepts/source/analytics/ambiguous-patterns|systems architecture’s definition]] of *Monolith* as a single unit of deployment because our main focus lies with the internal structure of systems\. Instead, we will use the old definition of a *monolithic* application as a cohesive lump of code which does not contain any discernible components \[[wiki/concepts/source/appendices/books-referenced|[GoF]], [[wiki/concepts/source/appendices/books-referenced|POSA1]]\]\.

A *Monolith* is non\-modular \(not divided by interfaces\) along all the [[wiki/concepts/source/introduction/metapatterns|structural dimensions]]\. Its thorough cohesiveness is both its blessing \(single\-step debugging, system\-wide optimizations, and self\-consistent data\) and its curse \(messy code, no scalability of development and deployment, zero flexibility\)\.

### Performance

On one hand, monolithic applications provide perfect opportunities for performance optimizations as every piece of code is readily accessible from any other\. On the other hand, if the application is stateful, access to the state may [limit the performance benefit](https://stackoverflow.com/questions/16571381/degrading-performance-when-increasing-number-of-cores) of using multiple CPU cores\. Furthermore, large *Monoliths* may become too messy, too complicated, and too fragile for programmers to identify and implement any non\-local optimizations that could drastically improve performance\.

> There are many kinds of bottlenecks which limit an application’s performance\. As soon as you change your code to use multiple CPU cores you may find that the program’s throughput [is constrained](https://en.wikipedia.org/wiki/Resource_contention) by the speed of your hard drive or network interface\. And when you upgrade those two, you may well hit something more subtle, like OS interrupts or [CPU cache coherence](https://www.youtube.com/watch?v=wGSSUSeaLgA)\.

Overall, tiny *Monoliths* provide the best latency and throughput per CPU core\. Larger performance\-critical projects may need to partition the code into [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] or [[wiki/concepts/source/basic-metapatterns/services|*Services*]] so that any manually optimized part remains small enough to be manageable\. Higher throughput is attainable through distributing the software over multiple computers: [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] employ several copies of the whole system while a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] may run each step of data processing on a separate server\.

### Dependencies

Even though a *Monolith* is a single module, meaning that there are no dependencies among its parts \(in fact, everything depends on everything\), it still may depend on some external components or services which it uses\. Those dependencies tend to cause [*vendor lock\-in*](https://en.wikipedia.org/wiki/Vendor_lock-in) or make the software OS\- or hardware\-dependent\. [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] \(including [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVP*]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVC*]]\) decouples a monolithic system from its dependencies by isolating the latter behind [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]]\.

### Applicability

*Monolith* is <ins>good</ins> for cases which are harmed by the introduction of modularity:

- *Tiny projects\.* The project is relatively small \(below 10 000 lines\) and the requirements will never change \(like when you need to implement an application for running a specific mathematical calculation or a library supporting a well\-established communication protocol\)\.
- *Ultra optimization\.* You already have a working and thoroughly optimized system, but you still need that extra 5% performance improvement achievable through merging all the components together\.
- *Low latency\.* If you need ultra low latency for the entire application, any asynchronous communication between its modules is not a viable option\. Example: [high\-frequency trading](https://en.wikipedia.org/wiki/High-frequency_trading)\.
- *Prototyping\.* You are writing a prototype in a domain which you are not familiar with, and gathering requirements in the process\. Chances for a correct initial identification of weakly coupled subdomains \(to become [[wiki/concepts/source/basic-metapatterns/services|modules or services]]\) are [quite low](https://martinfowler.com/bliki/MonolithFirst.html) and it is worse to have wrong module boundaries than to use no modules at all\. [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|At the later stages]] of the project, when you will know the domain much better and your users will have approved the initial implementation, you will be able to split the system into components in a much better way, if and when that will be needed\. Nevertheless, you may already know enough to apply [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] which keep the business logic monolithic while isolating it from the periphery and third\-party libraries\.
- *Quick and dirty\.* You are out of time and money and need to show your customers something right now\. There is no time to think, no money to perfect the code, and no day after tomorrow\.


*Monolith* <ins>should be avoided</ins> when we need modules:

- *Incompatible forces\.* There are [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|conflicting *forces*]] for different subsets of functionality\. They require splitting the system into \(usually asynchronous\) components each of which is specifically designed to satisfy its own subset of forces\. Your main tool is the careful selection of technologies and architectures on a per component basis which may allow the project to satisfy all the non\-functional requirements even if the task looks impossible during the initial analysis\.
- *Long\-running projects\.* The project is going to evolve over time and you believe you can predict the general direction of the future changes\. Modularity brings flexibility which you will need for sure\.
- *Larger codebases\.* The project grows above average size \(100 000 lines of code\)\. If you don’t split it into smaller components it will descend into a [monolithic hell](https://livebook.manning.com/book/microservices-patterns/chapter-1/25) with development and debugging slowing down year after year till it reaches [terminal stage](https://news.ycombinator.com/item?id=18442941)\. Slow development is a waste of money, both in salary and in time to market\.
- *Multiple teams\.* You have multiple teams to work on the project\. Inter\-team communication is hard and error\-prone whereas merging several teams together is known to greatly reduce the programmers’ productivity \(which peaks with teams of 5 or less members\)\. Explicit interfaces between components will formalize interdependencies between the teams, lowering communication overhead\.
- *Fault tolerance\.* Your domain requires fault tolerance which is next to impossible for large monolithic applications\.
- *Resource\-limited\.* Your project is too resource\-hungry for commodity hardware\. Even if you buy the best server for its needs right now, it is going to crave more tomorrow \(or on the next Black Friday\)\.
- *Distributed setup\.* Your project needs to run on multiple hardware devices\. One of common examples is a [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|web service]] containing frontend and backend\.


### Relations

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Monolith.png" alt="Intermediary architectures between Monolith and distributed Shards, Layers, and Services." loading="lazy" width=100%/>
</a>
</div>

*Monolith*:

- Can be extended with a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], or turned into a [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] or [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]]\.
- Yields [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], [[wiki/concepts/source/basic-metapatterns/services|*Services*]], or [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] if divided along the [[wiki/concepts/source/introduction/metapatterns|*abstractness*, *subdomain*, or *sharding*]] dimensions, respectively\. All the known architectures are combinations of those three metapatterns\.
- Is the bird’s\-eye view of any architecture\.


## Variants by the internal structure

*Monoliths* are the atoms to create more complex architectures from, the opaque building blocks, each of which satisfies a consistent set of [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|forces]]\. Any individual component of a more complex architecture either is monolithic or encapsulates another architectural pattern, decomposable into *Monoliths*, and any architecture looks monolithic to its clients\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/MonolithAsUnzoomed.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/MonolithAsUnzoomed.png" alt="A Sandwich Architecture looks like a monolith when the details of its internal structure are omitted." loading="lazy" width=100%/>
</a>
</div>

There is a misunderstanding because *software architecture* inspects the internals of *applications* at the level of *modules* or even classes while *systems architecture* deals with *distributed systems* and operates *deployment units* which tend to incorporate multiple modules or even applications\. Each branch of the architecture [[wiki/concepts/source/analytics/ambiguous-patterns|calls]] its atomic unit a *Monolith*, leading to the term sticking both to a *module that cannot be subdivided*, as in \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] and \[[wiki/concepts/source/extension-metapatterns/shared-repository|[POSA1]]\], and to a *\(sub\)system which must be deployed as a whole*, as per present\-day literature\.

As we aspire to build a unified classification for both distributed and local systems, we must treat both kinds of components in the same way, whether they are [[wiki/concepts/source/basic-metapatterns/services|distributed services]], [[wiki/concepts/source/basic-metapatterns/services|co\-located *Actors*]], or [[wiki/concepts/source/basic-metapatterns/services|in\-process modules]]\. Thus, for the scope of the current book, we will follow the definition of *Monolith* from \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\]: “Tight coupling leads to *monolithic* systems, where you can't change or remove a class without understanding and changing many other classes”\. Still, we need to account for a couple of misnomers from systems architecture\.

### True Monolith, Big Ball of Mud

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/True%20Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/True%20Monolith.png" alt="A square that represents a non-modular monolith." loading="lazy" width=83%/>
</a>
</div>

A true *Monolith* features [no clear internal structure](http://laputan.org/mud/)\. If it has any components, they are so tightly coupled that the entire thing behaves as a single cohesive module\. This is the subject of the current chapter\.

### \(inexact\) Lambda Monolith, Monolambda, [[wiki/concepts/source/basic-metapatterns/shards|Lambdalith]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Lambdalith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Lambdalith.png" alt="Instances of a stateless component between a load balancer and a database." loading="lazy" width=80%/>
</a>
</div>

A [*Monolambda*](https://jesseduffield.com/Notes-On-Lambda/) or [*Lambdalith*](https://theburningmonk.com/2025/03/the-pros-and-cons-of-lambdalith/) is a dynamic [[wiki/concepts/source/basic-metapatterns/shards|*Pool* of stateless instances]] of a system\. Though each instance may contain [[wiki/concepts/source/basic-metapatterns/layers|*layers*]] or [[wiki/concepts/source/basic-metapatterns/services|*subdomain modules*]], the whole is often called a *Monolith* [[wiki/concepts/source/analytics/ambiguous-patterns|because it is deployed as a single unit]]\.

### \(misapplied\) [[wiki/concepts/source/basic-metapatterns/layers|Layered Monolith]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Layered%20Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Layered%20Monolith.png" alt="Application, domain, and infrastructure layers." loading="lazy" width=81%/>
</a>
</div>

When they say [[wiki/concepts/source/basic-metapatterns/layers|*Layered Monolith*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], that refers to a non\-distributed application with a layered structure, which is a proper [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] architecture and will be discussed in the corresponding chapter\. It is called a *Monolith* for the [[wiki/concepts/source/analytics/ambiguous-patterns|sole reason that it is not distributed]]\. Nevertheless, *Layers* resemble *Monolith* in many aspects, including easy debugging and the risk of outgrowing the comfort zone of developers\.

### \(misapplied\) [[wiki/concepts/source/basic-metapatterns/services|Modular Monolith]] \(Modulith\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Modular%20Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Modular%20Monolith.png" alt="A diagram of subdomain services." loading="lazy" width=88%/>
</a>
</div>

A [[wiki/concepts/source/basic-metapatterns/services|*Modular Monolith*]] \(*Modulith*\) \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] is a single\-process application subdivided into modules that correspond to subdomains\. If the modules communicate via in\-process messaging, the architecture is nearly identical to coarse\-grained [[wiki/concepts/source/basic-metapatterns/services|*Actors*]], thus it is a *Monolith* only in name\. *Modulith* [is a kind of](https://en.wikipedia.org/wiki/Duck_typing) [[wiki/concepts/source/basic-metapatterns/services|*Services*]] – it supports development by multiple teams and its asynchronous variant is hard to debug\. The relation to *Monolith* is mostly limited to the inability to scale individual parts of the system\.

### \(misapplied\) [Distributed Monolith](<Service-Oriented Architecture (SOA)#distributed-monolith>)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Distributed%20Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Distributed%20Monolith.png" alt="A distributed monolith as three layers of services." loading="lazy" width=100%/>
</a>
</div>

A [*Distributed Monolith*](<Service-Oriented Architecture (SOA)#distributed-monolith>) \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] is a highly distributed system \(usually [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) or [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\) where all the components still need to be deployed together because of their interdependencies\. It is said to have the drawbacks of both *Monolith* \(low fault tolerance and coupled release cycles\) and *Services* \(poor debuggability, high latency, and operational complexity\)\.

### \(inexact\) [[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal Architecture]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Hexagonal%20Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Hexagonal%20Monolith.png" alt="Hexagonal Architecture with adapters between its core and each component the core interacts with." loading="lazy" width=93%/>
</a>
</div>

[[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] extend a \(sub\)system with external components\. These architectures can be applied to a *Monolith* without drastically changing its properties – it still remains relatively easy to write and debug but hard to support when it has grown large\. Therefore, we will not currently discuss these modifications, mainly because each of them has a dedicated chapter\.

## Examples

Let’s take a look inside a *Monolith*\.

Any software module reacts to incoming events or data and produces outgoing events or data\. But there are a few basic ways to implement that cycle:

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Subtypes%20of%20Monolith.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Subtypes%20of%20Monolith.png" alt="Control flow diagrams for Reactor, Proactor, and Half-Sync/Half-Async." loading="lazy" width=100%/>
</a>
</div>

- *Reactor* runs each request in a separate thread:
  - A [single\-threaded version](#single-threaded-reactor-one-thread-one-task) is used to serialize access to a hardware device\.
  - A [multi\-threaded *Reactor*](#multi-threaded-reactor-a-thread-per-task) is the simplest backend implementation\.
- [*Proactor*](#proactor-one-thread-many-tasks) relies on short event handlers to run multiple requests in a single thread\.
- [*Half\-Sync/Half\-Async*](#inexact-half-synchalf-async-coroutines-or-fibers) implements coroutines by changing call stacks of a thread\.
- [*\(Re\)Actor\-with\-Extractors*](#inexact-reactor-with-extractors-phased-processing) passes the whole system through alternating planning and execution phases to run lock\-free\.


### Single\-threaded Reactor \(one thread, one task\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Reactor%20-%20Single%20Thread.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Reactor%20-%20Single%20Thread.png" alt="A single thread that blocks on calls to an operating system executes a request and then another request which has to wait in a queue." loading="lazy" width=100%/>
</a>
</div>

In a [*Reactor*](https://www.dre.vanderbilt.edu/~schmidt/PDF/reactor-siemens.pdf) \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] a single thread waits for an incoming event, request, or data packet, processes it with blocking calls to the underlying OS, hardware, and external dependencies, and returns the result, rinse and repeat\.

That makes sense when the module wraps a hardware component which cannot do several actions at once, for example, a communication bus or a HDD firmware capable of a single read or write at any given moment\.

### Multi\-threaded Reactor \(a thread per task\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Reactor%20-%20Multiple%20Threads.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Reactor%20-%20Multiple%20Threads.png" alt="Two threads, each runs a single request and blocks on accessing an operating system." loading="lazy" width=100%/>
</a>
</div>

A [*Reactor*](https://www.dre.vanderbilt.edu/~schmidt/PDF/reactor-siemens.pdf) \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] may employ multiple threads by having a [[wiki/concepts/source/basic-metapatterns/shards|*pool*]] of them waiting for a request or data to arrive\. The incoming event activates one of the waiting threads, which thereby becomes dedicated to processing it, makes several blocking calls and, finally, sends back a response\. When the request processing is complete, the thread returns to the pool of idle threads to wait for the next event to process\.

This is the default [simple & stupid](https://en.wikipedia.org/wiki/KISS_principle) implementation of backend services\. Its pitfalls include contention for shared resources, deadlocks, and high memory consumption by OS\-level threads\.

### Proactor \(one thread, many tasks\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Proactor.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Proactor.png" alt="A single thread handles messages that belong to several use cases in an interleaved manner." loading="lazy" width=100%/>
</a>
</div>

In [*Proactor*](https://hillside.net/plop/plop97/Proceedings/pyarali.proactor.pdf) \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] a single thread processes all of the incoming events, both from the module’s clients and from the hardware or dependencies which it manages\. When an event is received, the thread goes through a short piece of corresponding business logic \(*event handler*\) which usually does one or more non\-blocking actions, such as sending messages to other components, writing to registers of the managed hardware, or initiating an async I/O\. As soon as the event handler returns, the thread becomes ready to process further events\. As the thread never blocks, it is resource\-efficient \(does not hold anything for a noticeable amount of time\) and can serve many interleaved tasks\.

This approach is good for real\-time systems where thread synchronization is largely forbidden because of the associated delays and for reactive [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|control]] applications which mostly adapt to the environment instead of running pre\-programmed scenarios\. The drawback is very poor structure of the code and nightmarish debuggability as any complex behavior is broken into a swarm of separate event handlers\.

### \(inexact\) Half\-Sync/Half\-Async \(coroutines or fibers\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Half-Sync%20Half-Async.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Half-Sync%20Half-Async.png" alt="A system subdivided into two layers: the upper one with a coroutine per request and the lower one with a generic event handling thread." loading="lazy" width=100%/>
</a>
</div>

[*Half\-Sync/Half\-Async*](https://www.dre.vanderbilt.edu/~schmidt/PDF/PLoP-95.pdf) \[[wiki/concepts/source/appendices/books-referenced|[POSA2]]\] originally described the interaction between user space and kernel threads in operating systems which is not much different from what happens under the hood in coroutines or fibers\. A single thread \(or a thread pool with one thread per CPU core\) handles all the incoming events and switches its call stack in the process\.

Every incoming request is allocated a call stack which stores the processing state \(local variables and methods called\) of the request\. When it needs to access an external component, the [runtime system](https://en.wikipedia.org/wiki/Runtime_system) saves the request’s stack, makes a non\-blocking call, and the executing thread returns to its original stack to wait for any new event to handle while the request processing stack remains frozen until the action it has initiated completes asynchronously, raising an event\. Then the runtime, upon receiving the event, switches the execution thread back to the stored request’s stack and continues processing the request until it completes and its stack is deleted\.

This makes programming and debugging feel as easy as they are with [*Reactor*](#single-threaded-reactor-one-thread-one-task) \(imperative style\) while partially retaining the low resource consumption and high performance of [*Proactor*](#proactor-one-thread-many-tasks) \(reactive paradigm\)\. Coroutines and fibers are used in highly efficient [game engines](https://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine) and [databases](https://docs.seastar.io/master/tutorial.html#coroutines)\. Though *Half\-Sync/Half\-Async* has two layers \(is not truly monolithic\), I believe it belongs next to *Reactor* and *Proactor* which make up its upper and lower halves, respectively\.

### The state of the art

These patterns are not widely recognized and programmers tend to mix them together, for better or for worse\. One is likely to encounter a heavily multithreaded [big ball of mud](https://www.laputan.org/mud/) where some threads serve user requests while others are dedicated to periodic service routines\.

Moreover, people [[wiki/concepts/source/analytics/ambiguous-patterns|often call]] any event\-driven service a *Reactor*, causing confusion among those who distinguish between the three patterns\.

### \(inexact\) \(Re\)Actor\-with\-Extractors \(phased processing\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Reactor%20with%20Extractors.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Reactor%20with%20Extractors.png" alt="In the extraction phase components call each other and add actions to their queues. In the reaction phase they execute the actions from their queues but don't interact. The phases alternate." loading="lazy" width=100%/>
</a>
</div>

As a bonus, let’s review an [unconventional execution model](http://ithare.com/multi-coring-and-non-blocking-instead-of-multi-threading-with-a-script/3/) that fits game development and other kinds of simulations with many interacting objects\.

We have a long\-running system where each simulated object with a complex behavior depends on the objects around it\. Common wisdom proposes two ways to implement it:

- [*Actors*](https://doc.akka.io/libraries/akka-core/current/typed/guide/actors-intro.html) \(asynchronous messaging, reactive programming\) – each [[wiki/concepts/source/basic-metapatterns/services|*actor*]] \(simulated object\) runs single\-threaded and wakes up only to process incoming messages\. While processing a message, an actor may change its state and/or send messages to other actors\. The entire actor’s data is private and there are no synchronous calls between the actors\. The good thing is that actors are very efficient in highly parallel tasks as there are no locks in their code\. The bad thing is that actors have no way to synchronize their states: you can only request another actor to tell you about its state, and its response may become outdated even before you receive it\. Also, any complex logic that involves multiple actors is fragmented into many event handlers\.
- The opposite approach is to have the simulated objects access each other synchronously\. This allows for complex logic that depends on states of several objects yet gets in trouble with changing the objects’ states from multiple threads: you need to protect them with those inefficient locks and you get those dreadful deadlocks as the outcome\.


Here we see two bad options to choose from\. However, it is the simulated nature of the system that saves the day: we can *stop the world to get off*\. The objects’ querying each other and their changing their states neither needs to happen at the same time nor obey the same rules\!

The simulation runs in steps\. Each step consists of two phases:

- *Query phase* \(*extraction*\) is when the object states are immutable, thus the objects can communicate synchronously with no need for locks\. In this phase each object collects information from its surroundings \(other objects\), plans its actions and posts them as commands to its own message queue\. I suppose that objects may also post events to each other’s queues in this phase\.
- *Command phase* \(*reaction*\) is when each object executes its planned \(queued\) actions that change its state, but it cannot access other objects\.


Each phase lasts until every object in the system completes its tasks scheduled for that particular phase\. The phase toggle is supervised by a [[wiki/concepts/source/extension-metapatterns/proxy|*Scheduler*]] which runs the objects on all the available CPU cores\. The entire process resembles the [game of Mafia](https://en.wikipedia.org/wiki/Mafia_(party_game)) with public daily conversations and covert nightly actions\.

*\(Re\)Actor\-with\-Extractors* is the perfect example of earning the benefits of two architectural styles without paying their penalties\. It utilizes both the lockless parallelism of *Actors*\-style [*shared\-nothing*](https://en.wikipedia.org/wiki/Shared-nothing_architecture) and the simplicity of synchronous access in [*shared\-memory*](https://en.wikipedia.org/wiki/Shared-memory_architecture) by alternating between those two modes through applying the [*CQRS principle*](https://en.wikipedia.org/wiki/Command_Query_Responsibility_Segregation) to the time dimension\.

## Evolutions

Every architecture has drawbacks and tends to evolve in a variety of ways to address them as soon as they start causing trouble\. Below is a brief summary of common evolutions of *Monolith* with more information available in [[wiki/concepts/source/appendices/evolutions-of-architectures|Appendix E]]\.

### [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-lead-to-shards|Evolutions to Shards]]

One of the main drawbacks of the *Monolithic Architecture* is its lack of scalability – a single running instance of your system may not be enough to serve all the clients no matter how many resources you add in\. If that is the case, you should consider [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] – *multiple instances* of a *Monolith*\. There are following options:

- Self\-managed [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] – each instance owns a part of the system’s data and may communicate with all the other instances \(forming a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\)\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Mesh%20of%20Shards.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Mesh%20of%20Shards.png" alt="Several instances of a monolith are run as intercommunicating shards, each of which holds a subset of the system's data." loading="lazy" width=100%/>
</a>
</div>

- *Shards* with a [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] – each instance owns a part of the system’s data and relies on an external component to choose a shard for a client\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Isolated%20Shards%20with%20Load%20Balancer.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Isolated%20Shards%20with%20Load%20Balancer.png" alt="Multiple instances of a monolith, each a subset of the system's data, are run behind a sharding proxy." loading="lazy" width=100%/>
</a>
</div>

- A [[wiki/concepts/source/basic-metapatterns/shards|*Pool*]] of stateless instances with a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] and a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] – any instance can process any request, but the shared database or file system limits the throughput\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Stateless%20Shards%20with%20Shared%20DB.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Stateless%20Shards%20with%20Shared%20DB.png" alt="A monolith is transformed into stateless instances which run behind a load balancer and access a shared database." loading="lazy" width=100%/>
</a>
</div>

- A [[wiki/concepts/source/basic-metapatterns/shards|*Stateful Instance*]] per client with an external persistent storage – each instance owns the data related to its client and runs in a virtual environment \(i\.e\. web browser or an [[wiki/concepts/source/implementation-metapatterns/microkernel|*Actor Framework*]]\)\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Instance%20per%20Client.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Instance%20per%20Client.png" alt="Each user is allocated a temporary instance of a subsystem which loads their data at the start of the session and persists any changes to the database." loading="lazy" width=100%/>
</a>
</div>

### [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-result-in-layers|Evolutions to Layers]]

Another drawback of *Monolith* is its… er… monolithism\. The entire application exposes a single set of qualities and all its parts \(if they ever emerge\) are deployed together\. However, life awards flexibility: parts of a system may benefit from being written in varying languages and styles and deployed with different frequency and amount of testing, sometimes to specific hardware or end users’ devices\. They may need to [[wiki/concepts/source/foundations-of-software-architecture/forces-asynchronicity-and-distribution|vary in security and scalability]] as well\. Enter [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] – a subdivision by the *level of abstractness*:

- Most *Monoliths* can be divided into 3 or 4 layers of different abstractness\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Layers.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Layers.png" alt="A monolith is split into application, domain and database layers." loading="lazy" width=100%/>
</a>
</div>

- It is common to see the database separated from the main application\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20add%20Database.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20add%20Database.png" alt="The data of a monolithic system is moved to a database, leaving the business logic stateless." loading="lazy" width=100%/>
</a>
</div>

- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] \(e\.g\. [[wiki/concepts/source/extension-metapatterns/proxy|*Firewall*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Cache*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Reverse Proxy*]]\) are common additions to the system\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20add%20Proxy.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20add%20Proxy.png" alt="A part of generic functionality of a monolith is moved to a proxy." loading="lazy" width=100%/>
</a>
</div>

- An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] adds a layer of indirection to make the system’s external API more user\-friendly\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20add%20Orchestrator.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20add%20Orchestrator.png" alt="An orchestrator is added to a monolithic system, allowing for higher-level client requests." loading="lazy" width=100%/>
</a>
</div>

### [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-make-services|Evolutions to Services]]

The final major drawback of *Monolith* is the cohesiveness of its code\. The rapid start of development with *Monolith* begets a major obstacle as the project grows: every developer needs to know the entire codebase to be productive while changes made by individual developers overlap and may break each other\. Such distress is usually solved by dividing the project into modules along *subdomain boundaries* \(which usually match [*bounded contexts*](https://martinfowler.com/bliki/BoundedContext.html)\)\. However, that requires much work, and good boundaries and APIs are hard to design, wherefore many organizations prefer a slower iterative transition\.

- A *Monolith* can be split into [[wiki/concepts/source/basic-metapatterns/services|*Services*]] right away\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Services.png" alt="A monolith is subdivided into services." loading="lazy" width=100%/>
</a>
</div>

- A feature may be added or a weakly coupled part of the Monolith separated into a new service\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20Split%20Service.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20Split%20Service.png" alt="A service is split from a monolith." loading="lazy" width=100%/>
</a>
</div>

- Some domains allow for sequential data processing best described by [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]]\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Pipeline.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Pipeline.png" alt="A Monolith is transformed into a pipeline." loading="lazy" width=100%/>
</a>
</div>

### [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-rely-on-plugins|Evolutions with Plugins]]

The last group of evolutions does not really change the monolithic nature of the application\. Instead, its goal is to improve the customizability of the *Monolith*:

- Vanilla [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] is the most direct approach which relies on replaceable bits of logic\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Plugins.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Plugins.png" alt="Plugins customize the monolith's behavior." loading="lazy" width=100%/>
</a>
</div>

- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] is a subtype of *Plugins* which is all about isolating the main code from any third\-party components which it uses\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Hexagonal.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Hexagonal.png" alt="The database, external libraries, and a protocol support component are separated from the business logic and isolated with adapters." loading="lazy" width=100%/>
</a>
</div>

- [[wiki/concepts/source/implementation-metapatterns/microkernel|*Scripts*]] is a kind of [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] – yet another subtype of *Plugins* – which gives users of the system full control over its behavior\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Interpreter.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Monolith/Monolith%20to%20Interpreter.png" alt="The high-level logic is rewritten as scripts which are run by an interpreter." loading="lazy" width=100%/>
</a>
</div>

## Summary

A *Monolith* is an unstructured application\. It is the best architecture for rapid prototyping by a small team and it usually grants the best performance to costs ratio\. However, it does not scale, lacks any flexibility and becomes unmanageable as the amount of code grows\.

| \<\< [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic metapatterns]] | ^ [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic metapatterns]] ^ | [[wiki/concepts/source/basic-metapatterns/shards|Shards]] \>\> |
| --- | --- | --- |
