---
title: "Middleware"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Extension metapatterns/Middleware.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Extension%20metapatterns/Middleware
source_license_note: "See namespace README; preserve attribution and source links."
---

# Middleware

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Extension metapatterns/Middleware.md`.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Middleware.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Main/Middleware.png" alt="A diagram for Services with a middleware, in abstractness-subdomain-sharding coordinates." loading="lazy" width=100%/>
</a>
</div>

*The line between disorder and order lies in logistics\.* Use a shared transport\.

<ins>Known as:</ins> \(Distributed\) Middleware\.

<ins>Structure:</ins> A low\-level layer that provides connectivity\.

<ins>Type:</ins> Extension component\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Separates connectivity concerns from the services that use it | May become a single point of failure |
| Transparent scaling of components | May increase latency |
| Available off the shelf | A generic *Middleware* may not fit specific communication needs |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\] has a lot of content on the implementation of messaging *Middleware*\. \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] features a chapter on *Middleware*\. However, those books are old\. \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] is about Kafka, but it goes too far advertising it as a [*Shared Event Store*](#persistent-event-log-shared-event-store)\. There is also a [Wikipedia article](https://en.wikipedia.org/wiki/Middleware_(distributed_applications))\.

Extracting transport into a separate layer relieves the components that implement business logic of the need to know the addresses and statuses of each other’s instances\. An industrial\-grade, third\-party *Middleware* is likely to be more stable and provide better error recovery than anything an average company can afford to implement on its own\.

A *Middleware* may function as:

- A *Message Broker* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]], [[wiki/concepts/source/appendices/books-referenced|EIP]], [[wiki/concepts/source/appendices/books-referenced|MP]]\] which provides a unified means of communication and implements some cross\-cutting concerns like the persisting or logging of messages\.
- A *Deployment Manager* \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\] which collects telemetry and manages service instances for error recovery and dynamic scaling\.


As *Middleware* is ubiquitous and does not affect business logic, it is usually omitted from structural diagrams\.

### Performance

A *Middleware* may negatively affect performance when compared to direct communication between services\. Old implementations \(star topology\) relied on a *Broker* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]], [[wiki/concepts/source/appendices/books-referenced|EIP]]\] that used to add an extra network hop for each message and limited scalability\. Newer [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\-based variants avoid those drawbacks but are very complex and may have consistency issues \(according to the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)\)\.

A more subtle drawback is that transports which a *Middleware* supports or uses by default may be suboptimal for some of the interactions in your system, causing programmers to hack around the limitations or build higher\-level protocols on top of your *Middleware*\. Both cases can be ameliorated by adding means for direct communication between the services to bypass the *Middleware* or by using multiple specialized kinds of *Middleware*\. However, that adds to the complexity of the system – the very issue the *Middleware* promised to help with\.

### Dependencies

Each service depends both on the *Middleware* and on the API of every service it communicates with\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Dependencies/Middleware.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Dependencies/Middleware.png" alt="Each service depends on the middleware and on every service which it uses." loading="lazy" width=100%/>
</a>
</div>

You may decide to use an [[wiki/concepts/source/extension-metapatterns/proxy|*Anticorruption Layer*]] over your *Middleware* just in case you may need to change its vendor in the future\. That will trade performance for flexibility\.

### Applicability

*Middleware* <ins>helps</ins>:

- *Multi\-component systems\.* When a service has several instances deployed which need to be accessed, its clients must know the addresses of \(or have channels to\) its instances and use an algorithm for instance selection\. As the number of services grows, so does the amount of information about the instances of other services that each service needs to track\. Even worse, services sometimes crash or are being redeployed, requiring complicated algorithms that queue messages to deliver them in order once the recipient service returns to life\. It makes all the sense in the world to use a dedicated component to take care of all of that\.
- *Dynamic scaling\.* It is good to have a single, even if virtual, component that manages routes for interservice messaging to account for newly deployed \(or destroyed\) service instances\.
- [*Blue\-green deployment*](https://martinfowler.com/bliki/BlueGreenDeployment.html)*,* [*canary release*](https://martinfowler.com/bliki/CanaryRelease.html)*, or* [*dark launching*](https://martinfowler.com/bliki/DarkLaunching.html) *\(traffic mirroring\)*\. It is easier to switch, whether fully or in part, to a new version of a service when the communication is centralized\.
- *System stability\.* Most implementations of *Middleware* guarantee message delivery with unstable networks and failing components\. Many persist messages to be able to recover from failures of the *Middleware* itself\.


*Middleware* <ins>hurts</ins>:

- *Critical real\-time paths\.* An extra layer of message processing is bad for latency\. Such messages may need to bypass the *Middleware*, likely via pre\-established message channels\.


### Relations

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Middleware.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Relations/Middleware.png" alt="Middleware for Services, Shards, and Service-Oriented Architecture." loading="lazy" width=100%/>
</a>
</div>

*Middleware*:

- Extends [[wiki/concepts/source/basic-metapatterns/services|*Services*]], [*Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)>) or, in rare cases, [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]] or [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]\.
- Can participate in a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Bus of Buses*]] \([[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]\) or be merged with other *extension metapatterns*\.
- Is closely related to [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\. A persistent *Middleware* employs a *Shared Repository*\.
- Is usually implemented by a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] or [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] \(which is often based on a *Mesh*\)\.


## Variants by functionality

There are several dimensions of freedom with a *Middleware*, some of them may be configurable:

### By addressing \(channels, [[wiki/concepts/source/implementation-metapatterns/mesh|actors]], pub/sub, gossip\)

Systems vary in the way their components address each other:

- *Channels* \(one to one\) – components which need to communicate establish a message channel between them\. Once created, the channel accepts messages or a data stream on its input end and transparently delivers them to its output end\. Examples: sockets, Unix pipes, and private chats\.
- *Actors* \(many to one\) – each component has a public mailbox\. Any other component that knows its address or name may push a message into it\. Examples: e\-mail\.
- *Publish/subscribe* \(one to many\) – a component can publish events to topics\. Other components subscribe to those topics and one or all of the subscribers receive copies of a published event\. Examples: IP multicast and subscriptions for e\-mail notifications\.
- [*Gossip*](https://highscalability.com/gossip-protocol-explained/) \(many to many\) – an instance of a component periodically synchronizes its version of the system's state with random other instances, which further spread the updates\. As time passes, more and more participants become aware of the changes in the system, leading to eventual consistency of the [[wiki/concepts/source/basic-metapatterns/shards|*replicas*]] of the system's state\.


### By flow \(notifications, request/confirm, RPC\)

Control flow may take one or more of the following approaches:

- *Notifications* – a component sends a message about an event that occurred and does not really care about the further consequences or wait for a response\.
- *Request/confirm* – a component sends a message which requests that another component does something and sends back the result\. The sender may execute other tasks meanwhile\. A request usually includes a unique id that will be added to the confirmation for the *Middleware* to know which of the requests in progress the confirmation belongs to\.
- *Remote procedure call* \(RPC\) is usually built on top of a request/confirm protocol\. The difference is that the sender blocks on the *Middleware* while waiting for the confirmation, thus to the application code the whole process of sending the request and waiting for the confirmation looks like a single method call\.


### By delivery guarantee

If the transport \(network\) or the destination fails, a message may not be processed, or may be processed twice because of retries\. A *Middleware* may [promise to deliver messages](https://blog.bytebytego.com/p/at-most-once-at-least-once-exactly):

- *Exactly once*\. This is the slowest case which is [implemented through distributed transactions](https://docs.confluent.io/kafka/design/delivery-semantics.html)\. If the network, *Middleware* itself, or the message handler fails, there is no side effect, and the whole process of delivering and executing the message is repeated\. The *exactly once* contract is used for financial systems and accounting where money should never disappear or duplicate during a transfer\.
- *At least once*\. On failure the message is redelivered, but the previous message could have already been processed \(if only the confirmation was lost\), thus there is a chance for a message to be processed twice\. If the message is *idempotent* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\], meaning that it sets a value \(x = 42\) instead of incrementing or decrementing it \(x = x \+ 2\), then we can more or less safely process it multiple times \(x = 42; x = 42; x = 42;\) and use the relatively fast *at least once* guarantee\.
- *At most once*\. If anything fails, the message is lost and never retried\. This is the fastest of the three guarantees, suitable for such monitoring applications as weather sensors – it is not too bad if a single temperature measurement disappears when you receive hundreds of them every day\.
- *At will* \(no guarantee\)\. As with the bare [UDP transport](https://en.wikipedia.org/wiki/User_Datagram_Protocol#Reliability_and_congestion_control), a message may disappear, become duplicated, or arrive out of order\. That fits real\-time streaming protocols \(video or audio calls\) where it is acceptable to skip a frame while a frame coming too late is of no use at all\. Each frame contains its sequence number, and it is up to the application to reorder and deduplicate the frames it receives\.


### By persistence

A *Middleware* with a delivery guarantee needs to store messages whose delivery has not yet been confirmed\. They may be:

- Written to a data store of the *broker*\.
- Persisted in a distributed data store in brokerless \([[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\) systems\.
- Replicated over an in\-memory *Mesh* storage \(like [[wiki/concepts/source/extension-metapatterns/shared-repository|*Data Grid*]]\)\.


If the messages are stored indefinitely, the *Middleware* [becomes](#persistent-event-log-shared-event-store) a *Persistent* [*Event Log*](https://medium.com/sundaytech/event-sourcing-audit-logs-and-event-logs-deb8f3c54663) or even a *Shared* [*Event Store*](https://cloudnative.ly/event-driven-architectures-edas-vs-event-sourcing-c8582578e87) with the schemas of the stored events coupling the involved services \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] just like the database schema does in [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\.

### By structure \([[wiki/concepts/source/implementation-metapatterns/microkernel|Microkernel]], [[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]], Broker\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Middleware%20-%20Structure.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Middleware%20-%20Structure.png" alt="In middleware each service is co-located with a generic component which may either be a node of a mesh or forward the service's requests to a centralized broker as a proxy." loading="lazy" width=100%/>
</a>
</div>

A *Middleware* may be:

- Implemented by an underlying operating or virtualization system \(see [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]]\)\.
- Run as a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] of identical modules co\-deployed with the distributed components in their [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]]\.
- Rely on a single *broker* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]], [[wiki/concepts/source/appendices/books-referenced|EIP]]\] for coordination\.


The last configuration is simpler but features a single point of failure unless multiple instances of the broker are deployed and kept synchronized\.

## Examples

There are several patterns which extend *Middleware* with other functions:

- A [*Persistent Event Log*](#persistent-event-log-shared-event-store) allows for replaying past events\.
- A [*Service Mesh*](#service-mesh) adds a *Sidecar* with shared libraries to every service instance it hosts\.
- A [*Message Bus*](#message-bus) uses *Adapters* to support a variety of protocols\.
- An [*Event Mediator*](#event-mediator) orchestrates request processing for the services it connects\.
- An [*Enterprise Service Bus*](#enterprise-service-bus-esb) both supports multiple protocols and orchestrates request processing\.


### [[wiki/concepts/source/extension-metapatterns/shared-repository|Persistent Event Log, Shared Event Store]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Middleware%20-%20Shared%20Event%20Store.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Middleware%20-%20Shared%20Event%20Store.png" alt="Both persistent event log and shared event store merge the functionality of middleware and shared repository." loading="lazy" width=100%/>
</a>
</div>

When a *Middleware* persists messages, it takes on the function \(and drawbacks\) of a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\. A *Persistent Event Log* allows to replay events incoming to a given service \(to help a debug session or fix data corrupted by a bug\) while a *Shared Event Store* also captures changes of the internal states of the services \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\], thus [replacing their private databases](https://cloudnative.ly/event-driven-architectures-edas-vs-event-sourcing-c8582578e87)\. However, with either approach, changing an event field impacts all the services that use the event and may involve rewriting the entire event log \(the system’s history\) \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\]\.

### [[wiki/concepts/source/implementation-metapatterns/mesh|Service Mesh]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Microservices.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/1/Microservices.png" alt="Multiple instances of several services connected to their sidecars which are connected to a shared mesh engine. Instances of each service access its single database." loading="lazy" width=100%/>
</a>
</div>

*Service Mesh* \[[wiki/concepts/source/appendices/books-referenced|[FSA]], [[wiki/concepts/source/appendices/books-referenced|MP]]\] is a smart [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]]\-based *Middleware* that manages service instances and employs at least one co\-located [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] \(called [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecar*]]\) per service instance deployed\. The *Sidecars* may provide protocol translation and cover cross\-cutting concerns such as encryption or logging\. They make a good place for shared libraries\.

The internals of [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]] are discussed in the [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh* chapter]]\.

### Message Bus

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Message%20Bus.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Message%20Bus.png" alt="A message bus has an adapter per service to allow each service to use its own protocol." loading="lazy" width=100%/>
</a>
</div>

A *Message Bus* \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\] employs one or more [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] per service to let the services intercommunicate even if they differ in protocols\. That helps to integrate legacy services without major changes to their code but it degrades the overall performance as up to two protocol translations per message are involved\.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|Event Mediator]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Event%20Mediator.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Event%20Mediator.png" alt="An event mediator calls event processors one by one." loading="lazy" width=100%/>
</a>
</div>

*Event Mediator* \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], which pervades both [[wiki/concepts/source/basic-metapatterns/pipeline|*Event\-Driven Architecture*s]] and [[wiki/concepts/source/basic-metapatterns/pipeline|*Nanoservices*]], combines a *Middleware* \(used for the delivery of messages\) and an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] \(that coordinates high\-level use cases\)\. A message arrives to a service and is responded to without any explicit support on the service’s side – it appears *out of thin Middleware* which implements the entire integration logic\.

Slightly more details on the *Event Mediator* are [[wiki/concepts/source/extension-metapatterns/orchestrator|provided in the *Orchestrator* chapter]]\.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|Enterprise Service Bus]] \(ESB\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Enterprise%20Service%20Bus.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Variants/2/Enterprise%20Service%20Bus.png" alt="An Enterprise Service Bus is between the fragmented task and entity layers of Service-Oriented Architecture. It mediates all calls and messages between the system components." loading="lazy" width=100%/>
</a>
</div>

[*Enterprise Service Bus*](https://www.confluent.io/learn/enterprise-service-bus/) \(*ESB*\) \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] is a mixture of *Message Bus* and *Event Mediator*\. A *ESB* blends a *Middleware* and an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and adds an [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] per service as a topping\. It emerged to connect components that originated in incompatible networks of organizations that had been acquired by a corporation\.

See the [chapter about *Service\-Oriented Architecture*](<Service-Oriented Architecture (SOA)#enterprise-soa>)\.

## [[wiki/concepts/source/appendices/evolutions-of-a-middleware|Evolutions]]

A *Middleware* is unlikely to be removed \(though it may be replaced\) once it is built into a system\. There are [[wiki/concepts/source/appendices/evolutions-of-a-middleware|few evolutions for *Middleware*]] because it is usually a third\-party product and thus unlikely to be modified in\-house:

- If the *Middleware* in use does not fit the preferred mode of communication between some of your services, there is the option to deploy a second, specialized *Middleware*\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Middleware%20add%20Middleware.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Middleware%20add%20Middleware.png" alt="A specialized middleware added to a system that already has a generic middleware." loading="lazy" width=100%/>
</a>
</div>

- If several existing systems need to be merged, that is accomplished by adding yet another layer of *Middleware*, resulting in a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Bottom\-up Hierarchy*]] *\(Bus of Buses\)*\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Middleware%20to%20Bus%20of%20Buses.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/2/Middleware%20to%20Bus%20of%20Buses.png" alt="A low-level middleware interconnects several higher-level middlewares." loading="lazy" width=100%/>
</a>
</div>

## Summary

A *Middleware* is a ready\-to\-use component that provides a system of services with means of communication, scalability, and error recovery\. It is very common in distributed backends\.

| \<\< [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|Extension metapatterns]] | ^ [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|Extension metapatterns]] ^ | [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]] \>\> |
| --- | --- | --- |
