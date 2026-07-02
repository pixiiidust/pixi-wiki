---
title: "Choreography"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Foundations of software architecture/Arranging communication/Choreography.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Foundations%20of%20software%20architecture/Arranging%20communication/Choreography
source_license_note: "See namespace README; preserve attribution and source links."
---

# Choreography

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Foundations of software architecture/Arranging communication/Choreography.md`.

Another integration option, named *choreography* after seemingly spontaneous interactions between dancers, is to build a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] to pass every client’s request through a chain of components:


![After a monolith is subdivided into services, the services are assembled into a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Services%20to%20Pipeline.png)


In that case there is no owner for *workflows* – each request is just a data packet which is transformed multiple times as it passes through the *Pipeline*. Debugging is mostly limited to reading logs as there is no dedicated component to connect a debugger to for single-step execution of a use case. Nor is there a single piece of code to define each of the system-wide scenarios – their logic emerges from the graph of event channels between services and from message types that each involved event handler sends. Maintaining the consistency of the services’ states is the responsibility of the services themselves as there is none to supervise them.

On the bright side, there is no communication overhead caused by response messages as there are no responses – the processing cost is one message per service, half of the cost for an orchestrated architecture. Still, messages in choreographed systems tend to be longer than those used with [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestration]] as each message needs to carry the entire request’s state – there is no [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] to own the state and distribute parts of the request’s payload among involved services.


![A request collects data from every service in a pipeline as it passes those services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Pipeline%20Enricher.png)


Latency may also be suboptimal as parallelizing execution of a request is easier said than done because in a purely choreographed system there is no place (called *Aggregator* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\]) to collect multiple related messages, which also means that there is no associated cost in resources (RAM and CPU time) for storing their payloads. Please note that an *Aggregator*, when added, starts orchestrating the system – it stands between the client and services and meddles with the traffic and logic. It spends resources to store the received messages for aggregation, and the messages start forming request/confirm pairs – which are characteristic of orchestration.


![An Orchestrator can run subrequests in parallel which is impossible for a sequential pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Pipeline%20Not%20Parallel.png)


Still another trouble with choreography comes from its weakness in error processing. When a service in the middle of a request processing pipeline encounters an error, it cannot generate the normal output which would have been sent further downstream. One option is to fill in a null (or error) value but in that case each receiver of the message should remember to check for null and know how to deal with the error. Another way is adding a dedicated error channel for each service to push failed requests into, but that complicates the high-level system’s architecture. Moreover, a failure in the middle of processing a request may cause the services to end up with inconsistent data if no special attention (i.e. a new kind of request to compensate the original one) is paid to roll back the partial change.

Please note that all of the above is comfortably handled by an *Orchestrator*. Essentially, the exception handling, which an *Orchestrator* covers within its code, in a choreographed system escalates to the system’s architecture level.


![Rollback of changes done by services arranged into a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Pipeline%20Error.png)


## Early response

The ordinary mode of action for a pipeline – sending the final results of processing to the client – requires either for the tail of the pipeline to send data to its head or for existence of a stateful intermediate component – [[wiki/concepts/source/extension-metapatterns/proxy|*Gateway*]] – to receive the client’s request, forward it to the head of the pipeline, wait on the pipeline’s tail for the result of processing, and return it to the client. That is necessary because a client would usually open a single connection which is impossible to share between multiple services, namely the (receiving) head and (sending) tail of the pipeline.


![The component that receives a client request should send back the response. It can be a dedicated Gateway or the first service of a looped pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Pipeline%20Gateway.png)


The gateway, if used, may parallelize processing of [scatter-gather](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/scatter-gather.html) requests by turning into an [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]] which is a kind of *Orchestrator*. Which means that the system changes its paradigm from choreography to orchestration.


![An API Gateway runs subrequests in parallel while a pipeline runs them consecutively by passing a message through a chain of services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Gateway%20to%20API%20Gateway.png)


It is possible to avoid both adding a *Gateway* and having the cyclic dependency if clients don’t immediately need the final results of processing their requests. In such a case the service which receives the original request does its (first) step of processing, sends the response to the client, and then notifies services down the pipeline. Though such a use case seems to be unlikely, it happens in real life, for example, with pizza delivery. As soon as a buyer fills in their contact details and pays for the food, the order can be confirmed and forwarded to the kitchen. When it is ready it’s forwarded to the delivery, and finally the physical goods appear at the buyer’s door.


![The first service of a pipeline responds to the client immediately while forwarding the client's request to other services, which will eventually produce the result.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Pipeline%20Early%20Response.png)


*Early response* allows for choreography to shine in its purest form: with extensibility, high performance, but also high latency. A similar approach may be used in [[wiki/concepts/source/basic-metapatterns/services|*Service-Based Architecture*]] (aka *Macroservices*) [for communication between the services](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography) (*bounded contexts* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]) if they only need to notify each other of events without waiting for responses.

## Dependencies

A pipeline may be built with downstream or upstream dependencies or with a shared schema.

If services communicate through commands, each service depends on all the direct destinations of its commands as it must know each of the APIs which it uses. This mode of communication is mostly used with [[wiki/concepts/source/basic-metapatterns/services|*Actors*]] that power embedded, telecom, messengers, and some banking systems. Downstream dependencies make it easy to add input chains (upstream services that deal with new hardware or external clients) although changing anything at the output end of the pipeline is going to break the input parts that send messages to the component changed.


![Adding an upstream component in a command-based pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Downstream%20Dependencies.png)


Upstream dependencies come from the [publish/subscribe](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) model ([*Event Collaboration*](https://martinfowler.com/eaaDev/EventCollaboration.html)) where each service broadcasts notifications to any interested subscriber about what it has done. This way of building systems engines [[wiki/concepts/source/basic-metapatterns/pipeline|*Event-Driven Architecture*]] which is used in high-load backends. Extending or truncating an already implemented request processing tree is as easy as adding or removing subscribers to existing events but the creation of a new event source will require changes in the downstream components. The easy addition of downstream branches supports new customer experiences and analytical features which businesses are hungry for.


![Downstream services are easily added to a pub/sub pipeline, turning it into a tree.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Upstream%20Dependencies.png)


The final option is for the entire pipeline to use a uniform message format ([[wiki/concepts/source/extension-metapatterns/shared-repository|*Stamp Coupling*]]) which often contains one dedicated field per service involved. This way a service depends only on the message header (with the list of the fields and a record id) and the format of the single field it reads (stores data) or writes (retrieves data as a *Content Enricher* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\]). That works well with system-wide queries but binds all the services to the schema of the message in a way similar to accessing a shared database (to be discussed [[wiki/concepts/source/foundations-of-software-architecture/shared-data|below]]). Such an architecture decouples the services to the extent that any of them can be freely added or removed, together with the message field(s) it fills or reads.


![Each component depends on the message header and the message field(s) it accesses.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Shared%20Message%20Format.png)



![A service in a pipeline with a shared message format can be replaced with another service if the message fields which it uses are also replaced.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Add%20Remove%20with%20Shared%20Message.png)


A peculiar feature of choreography is the ability to cut and cross-link pipelines with compatible interfaces by changing a single service (or even system configuration if you build it with communication channels). That gives it a lot of flexibility – as long as you can comprehend all the dependencies (and channels) in the system, which becomes non-trivial as it grows.


![Cross-linking independent pipelines by establishing new data or event streams.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Cross-link%20Pipeline.png)


## Multi-choreography

It is very common for a service to participate in multiple pipelines, especially if it owns a database – as there should be a use case which fills in the data and at least one other scenario which reads from that database. Each pipeline makes the service depend on one or more of the interfaces it communicates with, which often belong to multiple services, thus increasing the coupling between system components and impairing future structural changes.


![A set of services participates in multiple pipelines.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Multi-choreography.png)


## Summary

Overall, choreography seems to be a lightweight approach that prioritizes throughput over latency and is suitable for highly-loaded scenarios of limited complexity. However, a choreographed system will likely become unintelligible if it is made to support more than a few use cases.

There is a decent [overview from Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography).
