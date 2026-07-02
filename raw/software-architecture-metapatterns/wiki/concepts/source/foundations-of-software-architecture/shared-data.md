---
title: "Shared data"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Foundations of software architecture/Arranging communication/Shared data.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Foundations%20of%20software%20architecture/Arranging%20communication/Shared%20data
source_license_note: "See namespace README; preserve attribution and source links."
---

# Shared data

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Foundations of software architecture/Arranging communication/Shared data.md`.

The final approach is integration through shared data \([[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\):

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Services%20to%20Shared%20Data.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Services%20to%20Shared%20Data.png" alt="After a monolith is subdivided into services, a shared database is used to integrate the services." loading="lazy" width=100%/>
</a>
</div>

The shared data is a “blackboard” available for each service to read from and write to\. It is passive \(as controlled by the services\) and does not contain any logic except for the data schema, which represents a part of the domain knowledge\. That makes communication through shared data the antipode of [[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestration]], which also features a shared component, namely an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], which is, however, active \(controls services\) and contains business logic, not data\.

Shared data can be used for storage, messaging, or both:

## Storage

The most common case of shared data is persistent storage \(usually a database, sometimes a file system\) for a \(sub\)domain that comprises functionally independent services which operate on a common dataset\. For example, a ticket purchase service and a ticket refund service share a database of ticket details\. The ticket purchase service reads in the available seats and fills in ticket data for purchases\. The ticket refund service should be able to find all tickets bought by a user and delete the user data from seats refunded\. The only communication between the purchase and refund services is the shared database of tickets or seats, so that one of them sees the changes made by the other the next time it reads the data\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Purchase%20and%20Return.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Purchase%20and%20Return.png" alt="Both purchase and refund services see and edit the entire system's data." loading="lazy" width=100%/>
</a>
</div>

With this model the services don’t depend on each other – instead, they depend on the shared \(domain\) data format and the database technology\. Thus, it is easy to add, modify, or remove services but hard to change the shared data structure or the database vendor\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Shared%20Data%20-%20Dependencies.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Shared%20Data%20-%20Dependencies.png" alt="Each service depends only on the shared database." loading="lazy" width=92%/>
</a>
</div>

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Shared%20Data%20add%20a%20Service.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Shared%20Data%20add%20a%20Service.png" alt="Adding a service to a system integrated through shared data does not require changes to other services." loading="lazy" width=100%/>
</a>
</div>

Services usually need to coordinate their actions\. Commonly, services with a shared database rely on a messaging [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] for communication\. Users of our ticketing system will want to be notified \(through email, SMS or an instant message\) when a free seat that they are interested in appears\. We’re not going to complicate either of the existing services by integration with instant messengers, so we will create a new notification service, which must track each returned ticket to see if any user wants to buy it\. This is easily implemented by the refund service publishing and the notification service subscribing to a ticket refund event, mixing in a bit of choreography into our data\-centric backend\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Notification%20to%20Notification.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Notification%20to%20Notification.png" alt="A diagram of a ticketing service whose components use direct messaging to intercommunicate." loading="lazy" width=100%/>
</a>
</div>

Another case is found with data processing pipelines where an element may periodically read new files from a folder or new records from a database table to avoid implementing notifications\. This increases latency and may cause a little CPU load when the system is idle, but is perfectly ok for long\-running calculations\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Shared%20files.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Shared%20files.png" alt="Stepwise processing of a batch of files." loading="lazy" width=100%/>
</a>
</div>

Finally, there is the rarely used option of an external [[wiki/concepts/source/extension-metapatterns/proxy|*Scheduler*]] which selects the services which should run based on the data available\. This is known as [[wiki/concepts/source/extension-metapatterns/sandwich|*Blackboard System*]], and [[wiki/concepts/source/basic-metapatterns/monolith|something similar]] happens in 3D game engines\. The *Scheduler* \(which in this case serves as an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\) is needed when CPU \(or GPU or RAM\) resources are much lower than what the services would consume if all of them ran in parallel, thus they must be given priorities, and the priorities change based on the context which is regularly estimated from the latest data\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Blackboard.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Blackboard.png" alt="Components of the Blackboard Architecture." loading="lazy" width=100%/>
</a>
</div>

> There is no clear distinction between [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] and [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]], and between [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\. Their [[wiki/concepts/source/introduction/system-topologies|topologies]] are identical, and functionality is often intermixed\. Indeed, a database can be used for messaging, as we see below, and many communication frameworks store the history of messages; while the [[wiki/concepts/source/introduction/system-topologies|managing layer]] can both provide protocol support and implement use cases, as seen with [[wiki/concepts/source/extension-metapatterns/proxy|*API Gateways*]]\. *Scheduler*, which is normally a *Proxy* with a simple [round\-robin](https://micrium.atlassian.net/wiki/spaces/osiiidoc/pages/131360/Round-Robin+Scheduling) or [preemption](https://micrium.atlassian.net/wiki/spaces/osiiidoc/pages/131347/Preemptive+Scheduling) algorithm, in *Blackboard* is delegated complex strategic planning, which turns it into an *Orchestrator*\.

## Messaging

The other, not as obvious, use case for shared data is messaging, which is implemented by the sender writing to a \(shared\) queue \(or log\) while the recipient is waiting to read from it\. Queues can be used for any kind of messages: request/confirm pairs, commands, or notifications\. Each service may have a dedicated queue \(either input for commands mode or output for notifications\), a pair of queues \(messages from the service’s output are duplicated by an underlying distributed [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] to input queues of their destinations\), or there may be a queue per communication channel, or a single queue for the entire system \(or one global\-level queue per message priority\) with each message carrying destination id \(for commands\) or topic \(for notifications\)\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Queues.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Queues.png" alt="Diagrams for: a queue per service, separate input and output queues, a queue per channel, and a single system queue." loading="lazy" width=100%/>
</a>
</div>

The use of shared data for messaging turns our data store into a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]\. The dependencies are identical to [[wiki/concepts/source/foundations-of-software-architecture/choreography|those in choreography]] – each service depends on the APIs of its destinations for commands or its sources for notifications\.

There should be a means for the recipient of a message to know about its arrival so that it starts processing the input\. Usually a messaging *Middleware* implements a receive\(\) method for the service to block on\. However, very low latency applications, like [HFT](https://en.wikipedia.org/wiki/High-frequency_trading), may [busy\-wait](https://en.wikipedia.org/wiki/Busy_waiting) by repeatedly re\-reading the shared memory so that the service starts processing the incoming data immediately on its arrival, bypassing the OS scheduler\. This is the fastest means of communication available in software\.

## Full\-featured

Finally, some \(usually distributed\) data stores implement data change notifications\. That allows for the services to communicate through the data store in near real\-time, removing both the need for an additional *Middleware* and interdependencies for the services\. Such a system follows the [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] pattern of \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] which was rectified as [[wiki/concepts/source/extension-metapatterns/shared-repository|*Space\-Based Architecture*]]\. In our example, the available seats notification service subscribes to changes in the seats data in the database – this way it does not need to be aware of the existence of other services at all\. We can also move the email notifications logic of the ticket purchase service into a separate component which would track purchases in the database and send a printable version of each newly acquired ticket to the buyer’s email address which can be found in the ticket details in the database\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Notification%20inside%20the%20DB.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Notification%20inside%20the%20DB.png" alt="A diagram of a ticketing service whose components rely on database notifications." loading="lazy" width=100%/>
</a>
</div>

## Summary

Communication through shared data is best suited for data\-centric domains \(for example, ticket purchase\)\. It allows for the services to be unaware of each other’s existence, just as they are with orchestration, but the structure of the domain data becomes hard to change as it is referenced all over the code\. Shared data may also be used to implement messaging\.

| \<\< [[wiki/concepts/source/foundations-of-software-architecture/choreography|Choreography]] | ^ [[wiki/concepts/source/foundations-of-software-architecture/arranging-communication|Arranging communication]] ^ | [[wiki/concepts/source/foundations-of-software-architecture/comparison-of-communication-styles|Comparison of communication styles]] \>\> |
| --- | --- | --- |
