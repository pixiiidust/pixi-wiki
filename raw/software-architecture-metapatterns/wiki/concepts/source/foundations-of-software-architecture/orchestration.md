---
title: "Orchestration"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Foundations of software architecture/Arranging communication/Orchestration.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Foundations%20of%20software%20architecture/Arranging%20communication/Orchestration
source_license_note: "See namespace README; preserve attribution and source links."
---

# Orchestration

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Foundations of software architecture/Arranging communication/Orchestration.md`.

The most straightforward way to integrate services is to add a coordinating layer, called [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] after the person that assigns parts in an orchestra, on top of them:

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Services%20to%20Orchestrator.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Services%20to%20Orchestrator.png" alt="After a monolith is subdivided into services, an orchestrator is added to communicate with the client and with each service." loading="lazy" width=100%/>
</a>
</div>

The good thing is that your *Orchestrator* has explicit code for every use case it covers and every running scenario gets an associated thread, coroutine, or object so that you are able to attach to the *Orchestrator* and debug any use case step by step\. Nor do you have to worry about keeping the state of the services consistent as they are passive with all the changes in the system being driven by the *Orchestrator*\.

Orchestration is the default approach for single\-process \(desktop\) applications where it is faster to call into an orchestrated module and return than to send it a message\. However, in distributed systems orchestration doubles the communication overhead \(when compared to [[wiki/concepts/source/foundations-of-software-architecture/choreography|choreography]] or [[wiki/concepts/source/foundations-of-software-architecture/shared-data|shared data]]\) as every method call into an orchestrated service uses two messages: request and confirmation\.

## Roles

In a backend which serves client requests an *Orchestrator* takes the role of [*Facade*](https://refactoring.guru/design-patterns/facade) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] – a module that provides and implements a high\-level interface for a multicomponent system\. It sends requests to the underlying services and waits for their confirmations – the mode of action that can be wrapped in an [*RPC*](https://en.wikipedia.org/wiki/Remote_procedure_call) \(*remote procedure call*\)\. The state of each scenario that the facade runs resides in the associated thread’s or coroutine’s call stack \(for [[wiki/concepts/source/basic-metapatterns/monolith|*Reactor*]] or [[wiki/concepts/source/basic-metapatterns/monolith|*Half\-Sync/Half\-Async*]] implementations, respectively\) or in a dedicated object \(for [[wiki/concepts/source/basic-metapatterns/monolith|*Proactor*]]\)\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Facade.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Facade.png" alt="A facade uses request/confirm pairs of messages to communicate with the services which it orchestrates." loading="lazy" width=100%/>
</a>
</div>

A *Facade* also supports querying the services in parallel and collecting the data returned into a single message through the *Splitter* and *Aggregator* patterns of \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\]\. That reduces latency \(and resource consumption as the whole task is completed faster\) for [scatter\-gather](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/scatter-gather.html) requests when compared to sequential execution\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Facade%20-%20Parallel.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Facade%20-%20Parallel.png" alt="A facade initiates communication with every service that it orchestrates simultaneously in a fan-out manner." loading="lazy" width=90%/>
</a>
</div>

Embedded and systems programming – the areas that deal with automating [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|*control*]] of hardware or distributed software – employ *Orchestrators* as [*Mediators*](https://refactoring.guru/design-patterns/mediator) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\]  – components that keep the state of the whole system \(and, by implication, any hardware it may manage\) consistent by enacting a system\-wide reaction to any observable change in any of the system’s constituents\. A mediator operates in non\-blocking, fire\-and\-forget mode which is more characteristic of choreography, to be discussed [[wiki/concepts/source/foundations-of-software-architecture/choreography|below]]\. This also means that you will not be able to debug a use case as a thread – because [there are no predefined scenarios in control software](https://medium.com/itnext/control-and-processing-software-9011fee8bc66)\!

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mediator.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mediator.png" alt="A mediator receives an input from one component, processes it, and initiates actions in other components." loading="lazy" width=100%/>
</a>
</div>

Such a difference may be rooted in the direction of the control and information flow: in a backend it comes as a complex, high\-level request while a control system reacts to a flood of low\-level events\.

## Dependencies

By default an *Orchestrator* depends on each service which it manages – that means that a change in a service’s interface or contract – caused by fixing a bug, adding a feature, or optimizing performance – requires corresponding changes in the *Orchestrator*\. That is acceptable as the *Orchestrator*’s client\-facing, high\-level logic tends to evolve much faster than the business rules of the lower layer of services, therefore the team behind the *Orchestrator*, unrestricted by other components depending on it, will likely release way more often than any other team\. However, as the number of the managed services and the lengths of their APIs increase, so does the amount of information that the *Orchestrator*’s team must remember and the influx of changes which they must integrate in their code\. For a large project the workload of supporting the *orchestration layer* may paralyze its development – that was a major reason behind the decline of [*Enterprise SOA*](<Service-Oriented Architecture (SOA)#enterprise-soa>) where [[wiki/concepts/source/extension-metapatterns/orchestrator|*ESB*]] used to orchestrate all the interactions in the system, including those between domain\-level services and components of the utility layer\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Orchestrator%20-%20Dependencies.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Orchestrator%20-%20Dependencies.png" alt="An orchestrator depends on every service which it uses." loading="lazy" width=100%/>
</a>
</div>

Another option, which appears in [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] and develops in [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]], stems from [*dependency inversion*](https://en.wikipedia.org/wiki/Dependency_inversion_principle): the *Orchestrator* defines an [*SPI*](https://en.wikipedia.org/wiki/Service_provider_interface) \(*service provider interface*\) for every service\. That makes each service depend on the *Orchestrator* so that a single *Orchestrator*’s team does not need to follow updates of the multiple services’ APIs – instead it initiates the changes at its own pace\. However, with that approach the design of an SPI requires coordination from the teams on both sides of it and the once settled interface becomes hard to change\. The most famous example of modules that implement SPIs are OS drivers\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Microkernel%20-%20Dependencies.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Microkernel%20-%20Dependencies.png" alt="In a Microkernel each managed service depends on a dedicated Service Provider Interface of the microkernel." loading="lazy" width=100%/>
</a>
</div>

Furthermore, some domains develop that idea into a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]: when services implement related concepts, they may match a single SPI, making the *Orchestrator* simpler \(as there is no further need for its developers to remember multiple interfaces\)\. That is the case with telecom or payment gateways and it may also be found with trees of product categories in online marketplaces\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Hierarchy%20-%20Dependencies.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Hierarchy%20-%20Dependencies.png" alt="In a hierarchy each child component depends on the same Service Provider Interface of their parent component." loading="lazy" width=100%/>
</a>
</div>

All kinds of orchestration allow for an easy addition of new use cases which may even involve new services as that changes nothing in the existing code\. However, removing or restructuring \(splitting or merging\) previously integrated services requires much work within the orchestrator, except for in a *Hierarchy* where all the services implement the same interface which means that the code in the *Orchestrator* does not depend \(much\) on any specific child\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Orchestrator%20add%20a%20Use%20Case.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Orchestrator%20add%20a%20Use%20Case.png" alt="Adding a new use case to an orchestrated system changes only the orchestrator." loading="lazy" width=100%/>
</a>
</div>

## Mutual orchestration

In some systems there are several services that have their own kinds of clients \(for example, employees of different departments\)\. Each of the services tries hard to process its clients’ requests on its own but occasionally still needs help from other parts of the system\. This creates a paradoxical case where several services orchestrate each other:

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%201.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%201.png" alt="A set of services which call each other while executing requests from their clients." loading="lazy" width=100%/>
</a>
</div>

As each of the services depends on the APIs of the others, any change to any interface or composition of such a system requires consent and collaboration from every team as it impacts the code of all the services\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%202.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%202.png" alt="Each service depends on every other service which it calls." loading="lazy" width=100%/>
</a>
</div>

In real life [[wiki/concepts/source/fragmented-metapatterns/layered-services|services are likely to be layered]], with their upper layers acting as both internal and external *Orchestrators*\. Layering isolates interdependencies to the relatively small [[wiki/concepts/source/basic-metapatterns/layers|application\-level]] components and resolves, to an extent, the seemingly counterintuitive case of mutual orchestration as now there is an explicit, though fragmented, system\-wide orchestration layer\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%203.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%203.png" alt="In Layered Services only the application layers of the services call each other." loading="lazy" width=100%/>
</a>
</div>

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%204.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Mutual%20Orchestration%20-%204.png" alt="In Layered Services only the application layers of the services are interdependent." loading="lazy" width=100%/>
</a>
</div>

## Summary

Orchestration represents [[wiki/concepts/source/basic-metapatterns/layers|use cases]] as a code, allowing for an orchestrated system to support many complex scenarios\. Dealing with errors is as trivial as properly handling exceptions\. This approach trades performance for clarity\.

| \<\< [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|Programming and architectural paradigms]] | ^ [[wiki/concepts/source/foundations-of-software-architecture/arranging-communication|Arranging communication]] ^ | [[wiki/concepts/source/foundations-of-software-architecture/choreography|Choreography]] \>\> |
| --- | --- | --- |
