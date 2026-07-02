---
title: "Pipeline"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Basic metapatterns/Pipeline.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Basic%20metapatterns/Pipeline
source_license_note: "See namespace README; preserve attribution and source links."
---

# Pipeline

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Basic metapatterns/Pipeline.md`.


![A diagram for Pipeline, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Pipeline.png)


*Never return.* Push your data through a chain of processors.

<ins>Known as:</ins> Pipeline \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\].

<ins>Structure:</ins> A component per step of data processing.

<ins>Type:</ins> System topology, implementation.

| *Benefits* | *Drawbacks* |
| --- | --- |
| It is very easy to add or replace components | Becomes too complex when the number of scenarios grows |
| Multiple development teams and technologies | Poor latency |
| Good scalability | Significant communication overhead |
| The components can be reused | Error handling may be non-trivial |
| The components can be tested in isolation |  |

<ins>References:</ins> *Pipes and Filters* are defined in \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\] and are the foundation for part 3 (Derived Data) of \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]. \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] has an overview of all kinds of *Pipelines* in general while \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] has a chapter on *Event-Driven Architecture*. \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] is dedicated to *Event-Driven Architecture*. The \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\] chapter on *Data Mesh* was written by the pattern’s author. \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\] is a whole book about distributed *Pipelines*.

*Pipeline* is a variation of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] with no user sessions \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\], a unidirectional data flow, and often a single message type per communication channel (which thus becomes a *data stream*). As processed data does not return to the module that requested processing, there is no common concept of request ownership or high-level ([[wiki/concepts/source/basic-metapatterns/layers|*integration*, *application*]]) business logic, which is instead defined by the graph of connections between the system’s components. On the one hand, as all the services involved are equal and know nothing about each other (their interfaces are often limited to a single entry point), it is very easy to reshape the overall algorithm. On the other hand, the system lacks the abstractness dimension, thus any new use case builds a separate pipeline, threatening to turn the architecture into a mess of thousands of intricately interrelated pieces when the number of scenarios grows. Moreover, error handling requires dedicated pipelines that roll back changes to the system’s state which had been committed by the earlier steps of a failed use case.

### Performance

Because any task for a pipeline is likely to involve all (or most of, if branched) its steps, there is no way to optimize away communication. Therefore, latency tends to be high. However, as pipeline components are often stateless, multiple instances of individual services or entire pipelines can run in parallel, making *Pipeline* a highly scalable architecture.

Another point to observe is that a local pipeline naturally spreads the load among the available CPU cores (by using one thread per component) without any explicit locks or thread synchronization.

### Dependencies

There are three ways to build communication in a pipeline, each with different dependencies:

- *Commands* make each service depend on the services it sends messages to. It is easy to add a new input to such a pipeline.
- With *publish/subscribe* each service depends on the services it subscribes to. That case favors downstream branching with multiple consumers.
- Services may share a *message schema*, in which case all of them depend on it, not on each other. That allows for reshuffling the services.



![Commands cause downstream dependencies. Notifications cause upstream dependencies. If a shared message schema is used, every component depends on the shared message.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Pipeline.png)


See the [[wiki/concepts/source/foundations-of-software-architecture/choreography|*Choreography* chapter]] for a more detailed discussion.

### Applicability

*Pipeline* is <ins>good</ins> for:

- *Experimental algorithms.* This architecture allows for the data processing steps both to be tested in isolation and connected into complex systems without changing their code.
- *Easy scaling.* Pipelines tend to evenly saturate all the available CPU cores without any need for custom schedulers. Stateless services can run distributed, thus the *Pipeline*’s scalability is limited only by its data channels.
- *Tailoring projects*. Many pipeline components are abstract enough to be easily reused, greatly reducing the cost of serial development of customized projects once the company builds a collection of common reusable services.


*Pipeline* <ins>does not work</ins> for:

- *High number of use cases.* The number of components and their interactions is going to be roughly proportional to the number of supported use cases and will easily overwhelm any developer or architect if new scenarios continue to be added over time.
- *Complex use cases*. Any conditional logic written as two or three lines of code with [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestration*]] is likely to need a separate pipeline and dedicated services with [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]]. Errors and corner cases are remarkably difficult to handle \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\].
- *Low latency*. Every step of a data packet along its journey between services takes time, not in the least because of data serialization. Moreover, the next service in the chain may still be busy processing previous data packets or its activation involves the OS scheduler.


### Relations

*Pipeline*:

- Is a kind of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] with unidirectional communication which often processes a single kind of data records.
- Is [[wiki/concepts/source/analytics/pipelines-in-architectural-patterns|involved]] in [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]], [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence* with derived databases]], and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVC*]].
- Can be extended with a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]], or [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]].


## Variants by scheduling

A pipeline may be either always active or run once in a while:

### Stream processing, Nearline system

*Stream processing* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] is when the pipeline components (*jobs, processors, filters, services* – whatever you prefer to call them) are actively waiting for input and process each incoming item immediately. This results in *near-real-time* (*nearline*) latency \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] but the pipeline will then always use resources, even when there is nothing for it to process.

### Batch processing, Offline system

*Batch processing* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]], [[wiki/concepts/source/appendices/books-referenced|DDS]]\] happens when a batch of input items is first collected into storage, and then the pipeline is run (often on a schedule) to process it. Such a mode of action is called *offline* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\] as the processing results are delayed. However, the company saves on resources because the pipeline is only active for brief periods of time.

## Examples

*Pipelines* can be local or distributed, linear or branched (usually trees, but cycles may happen in practice), they may utilize a feedback engine to keep the throughput of all their components uniform by slowing down faster steps or scaling out slower ones. In some systems *pipes* (channels) or *filters* (services) persist data. *Pipes* may store the processed data in files or databases to enable error recovery and [*event sourcing*](https://microservices.io/patterns/data/event-sourcing.html). Filters may need to read or write to a database, which is often [[wiki/concepts/source/extension-metapatterns/shared-repository|*shared*]], if the data processing relies on the system’s state. Moreover, transferring data through a pipe may be implemented as anything ranging from a method call on the next filter to a pub/sub framework to polling a database or file system.

Such a variety of options enables the use of pipelines in a wide range of domains. Notwithstanding, there are a few mainstream types of *Pipeline* architectures:

- [*Pipes and Filters*](#pipes-and-filters-workflow-system) for local processing of data streams.
- Distributed and usually branched [*Choreographed Event-Driven Architecture*](#choreographed-broker-topology-event-driven-architecture-eda-event-collaboration).
- [*Data Mesh*](#data-mesh) which builds a reporting pipeline for analytical data.
- Extremely elastic [*Pipelined Nanoservices*](#function-as-a-service-faas-nanoservices-pipelined).


### Pipes and Filters, Workflow System


![A pipeline chaining: source, three filters, and sink.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Pipes%20and%20Filters.png)


*Pipes and Filters* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]], [[wiki/concepts/source/appendices/books-referenced|EIP]]\] usually name a linear local system which obtains data with its *source*, passes the data through a chain of *filters*, connected by *pipes*, and outputs it via a *sink*. The entire *pipeline* may run as a single process to avoid the overhead of data serialization. It may range from a Unix shell script which passes file contents through a series of utilities to a hardware pipeline for image processing in a video [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|camera]]. The filters tend to be single-purpose (handling only one type of payload) and nearly stateless. In some cases a filter may use dedicated hardware (e.g. for encryption or audio/video processing). The entire pipeline often operates a single data format ([[wiki/concepts/source/extension-metapatterns/shared-repository|*Stamp Coupling*]]).

Though most commonly a filter waits for data to appear in its input pipe, processes it, and pushes the result to its output pipe, which allows for multiple filters to run in parallel, some implementations may let the source push the data through the entire pipeline all the way through to the sink. In that case either each filter calls the next filter in the line directly or the sink pulls the data by making direct upstream calls itself \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\]. The last two approaches remove the need for pipes yet are limited to using a single CPU core.

*Workflow* \[[wiki/concepts/source/appendices/books-referenced|[DDIA]], [[wiki/concepts/source/appendices/books-referenced|DDS]]\] is a more modern name for similar stepwise processing which often stores intermediate results in a file or database and may run distributed. However, the same word generally describes the sequence of high-level steps in a use case \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\], and is another name for [[wiki/concepts/source/basic-metapatterns/layers|*application* or *integration* logic]], therefore we will avoid  using “workflow” as a synonym for “pipeline”.

Examples: Unix shell pipes, processing of video streams, many types of hardware.

### Choreographed (Broker Topology) Event-Driven Architecture (EDA), Event Collaboration


![Event-Driven Architecture as a branched pipeline built from a group of services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Event-Driven%20Architecture.png)


*Event-Driven Architecture* (*EDA*) means that the system is built of services which use events to communicate in a non-blocking way. The idea is similar to the [actor model](https://en.wikipedia.org/wiki/Actor_model) of telecom and embedded programming. Thus, *EDA* itself does not define anything about the structure of the system (except that it is not [[wiki/concepts/source/basic-metapatterns/monolith|*monolithic*]]).

In practice, there are [two kinds](https://theburningmonk.com/2020/08/choreography-vs-orchestration-in-the-land-of-serverless/) of *Event-Driven Architectures*:

- [[wiki/concepts/source/foundations-of-software-architecture/choreography|*Choreographed*]] */ Broker Topology* / [*Event Collaboration*](https://martinfowler.com/eaaDev/EventCollaboration.html) \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] – the events are notifications (usually via publish/subscribe) and the services form tree-like structures, matching our definition of *Pipeline*.
- [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*Orchestrated*]] */ Mediator Topology* / [*Request-Response Collaboration*](https://martinfowler.com/eaaDev/RequestResponseCollaboration.html) – the events are request/confirmation pairs and usually there is a single entity that drives a use case by sending requests and receiving confirmations. Such a system corresponds to our [[wiki/concepts/source/basic-metapatterns/services|*Services*]] metapattern with the supervisor being an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], discussed in a dedicated chapter.


An ordinary *Choreographed Event-Driven Architecture* \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]], [[wiki/concepts/source/appendices/books-referenced|DDS]]\] is built as a set of subdomain services (similar to those of the parent [[wiki/concepts/source/basic-metapatterns/services|*Services*]] metapattern). Each of the services subscribes to notifications from other services which it uses as action / data inputs and produces notifications which other services may rely on. For example, an email service may subscribe to error notifications from other services in the system to let the users know about issues that occur while processing their orders. It will also subscribe to the user data service’s add / edit / delete notifications to keep its user contact database updated.

This example shows several differences from a typical *Pipes and Filters* implementation:

- The system supports multiple use cases (e.g. user registration and order processing).
- A service has several entry points (the email service involves an order error handler and user created handler).
- A notification which a service produces may have many subscribers or no subscribers (nobody needs to act on our sending an email to a user).


Those points translate to difference in structure: while *Pipes and Filters* is usually a linear chain of components, *EDA* entails multiple branched (and sometimes looped) event flow graphs over a single set of subdomain services.

Pipelined *Event-Driven Architecture* (often boosted with [event sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)) works well for highly loaded systems of moderate size, but larger projects are likely to grow prohibitively complex graphs of event flows and service dependencies. This architecture’s scalability is limited by the services’ databases and the pub/sub framework employed.

*Event-Driven Architecture* may involve a [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] as a user-facing event source and sink and a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] for an application-wise pub/sub engine. [[wiki/concepts/source/extension-metapatterns/orchestrator|*Front Controller*]] or [[wiki/concepts/source/extension-metapatterns/shared-repository|*Stamp Coupling*]] are used if it is important to know the state of requests that are being processed by the pipeline.

Examples: high performance web services.

### Data Mesh


![Data Mesh builds an extra graph of services that stream and process analytical data.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Data%20Mesh.png)


First and foremost, [*Data Mesh*](https://martinfowler.com/articles/data-mesh-principles.html) \[[wiki/concepts/source/appendices/books-referenced|[LDDD]], [[wiki/concepts/source/appendices/books-referenced|SAHP]]\] is not a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]], but rather a *Pipeline*. This architecture applies [*CQRS*](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) on the system level: it separates the interfaces and channels through which the services change their state (matching *commands* of *CQRS* or [*OLTP*](https://en.wikipedia.org/wiki/Online_transaction_processing)) and the ones used to retrieve their data (similar to *queries* or [*OLAP*](https://en.wikipedia.org/wiki/Online_analytical_processing)). That results in two overlapping subsystems, *operational* and *analytical*, that share most of their nodes.

The *operational system* is an ordinary [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]] or [*Event-Driven Architecture*](#choreographed-broker-topology-event-driven-architecture-eda-event-collaboration).

The *analytical system* contains *Data Product Quanta* (*DPQ*) – services that provide convenient access (streaming, replaying, and possibly querying) to parts of the system’s data. The *DPQs* are assembled into a graph akin to *Event-Driven Architecture*. There are three kinds of *DPQs* \[[wiki/concepts/source/appendices/books-referenced|[SAHP]]\]:

- A *source-aligned (native) DPQ* (*sDPQ*) is coupled to an operational service and streams (or provides queries into) its data. It is likely to be implemented as a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Reporting Database*]].
- An *aggregate DPQ* (*aDPQ*) merges and transforms inputs from several sources (*sDPQs* or other *aDPQs*). It is similar to a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Query Service*]].
- A *fit-for-purpose (custom-made) DPQ* (*fDPQ*) is an end-user (leaf application) of the *Data Mesh*’s data. It may collect a dataset for machine learning or let a business analyst do their research. *fDPQs* tend to be short-lived one-off components.


There is a pragmatic option to allow an operational service to resort to the analytical system’s *DPQs* to query other services’ data instead of messaging them directly or implementing a [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS View*]] and subscribing it to events that flow in the operational system.

### Function as a Service (FaaS), [[wiki/concepts/source/extension-metapatterns/sandwich|Nanoservices]] (pipelined)


![Many Nanoservices access a shared database to implement CRUD functionality.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/1/Nanoservices.png)


A [[wiki/concepts/source/basic-metapatterns/services|*nanoservice*]] is literally a [function as a service](https://en.wikipedia.org/wiki/Function_as_a_service) (*FaaS*) \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] – a stateless (thus perfectly scalable) component whose API comprises a single input method. *Nanoservices* run in proprietary cloud [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] over a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] and are [chained into pipelines](https://increment.com/software-architecture/the-rise-of-nanoservices/) dedicated to specific use cases. The code complexity stays low, but as the project grows, the integration will quickly turn into a nightmare of hundreds or thousands of interconnected nanoservices.

*Nanoservices* are good for rapid development of small elastic (dynamically scalable) applications. The supported load is limited by the *Shared Database*, and the project evolvability is limited by the complexity of scenarios. As any use case is going to involve many asynchronous steps, latency is not a strong side of *Nanoservices*.

## [[wiki/concepts/source/appendices/evolutions-of-a-pipeline|Evolutions]]

*Pipeline* [[wiki/concepts/source/basic-metapatterns/services|inherits its set of evolutions from *Services*]]. Filters can be added, split in two, merged, or replaced. Many systems employ a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] (a pub/sub or pipeline framework), a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] (which may be a database or a file system), or [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]].

There are a couple of [[wiki/concepts/source/appendices/evolutions-of-a-pipeline|pipeline-specific evolutions]], with more details provided in [[wiki/concepts/source/appendices/evolutions-of-architectures|Appendix E]]:

- The first service of the *Pipeline* can be promoted to a [[wiki/concepts/source/extension-metapatterns/orchestrator|*Front Controller*]] which tracks the status updates for every request it handles.



![The first service of a pipeline subscribes to notifications from other services and thus becomes a Front Controller.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Pipeline%20promote%20Front%20Controller.png)


- Adding an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] turns a *Pipeline* into normal [[wiki/concepts/source/basic-metapatterns/services|*Services*]]. As the high-level business logic moves into the orchestration layer, the domain-level filters don’t need to interact directly, therefore the inter-filter communication channels disappear and the system becomes identical to *Orchestrated Services*.



![Adding an orchestrator transforms a pipeline into Orchestrated Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Pipeline%20use%20Orchestrator.png)


## Summary

A *Pipeline* represents a data processing algorithm as a sequence of steps. It not only subdivides the system’s code into smaller components but is also very flexible: its parts are easy to add, remove, or replace. Several use cases can be built over the same set of services. Scalability is good. Event replay helps with debugging. However, this architecture lacks support for complex scenarios and error handling which limits it to smaller domains with a few use cases.
