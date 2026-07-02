---
title: "Pipelines in architectural patterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/Comparison of architectural patterns/Pipelines in architectural patterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/Comparison%20of%20architectural%20patterns/Pipelines%20in%20architectural%20patterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Pipelines in architectural patterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/Comparison of architectural patterns/Pipelines in architectural patterns.md`.

Several architectural patterns involve a unidirectional data flow – a [*pipeline*](https://en.wikipedia.org/wiki/Pipeline_(software))\. Strictly speaking, every data packet in a pipeline should:

- Move through the system over the same *route* with no loops\.
- Be of the same *type*, as a part of a *data stream*\.
- Retain its *identity* on the way\.
- Retain *temporal order* – the sequence of packets remains the same over the entire pipeline\.


Staying true to all of these points makes *Pipes and Filters* – one of the oldest known architectures\. Yet there are other architectures that discard one or more of those conditions:

## [[wiki/concepts/source/basic-metapatterns/pipeline|Pipes and Filters]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-PipesAndFilters.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-PipesAndFilters.png" alt="Pipes and Filters where a data stream originates with the source, passes several filters, and ends in a sink." loading="lazy" width=100%/>
</a>
</div>

[[wiki/concepts/source/basic-metapatterns/pipeline|*Pipes and Filters*]] is about stepwise [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|processing of a data stream]]\. Each piece of data \(a video frame, a line of text, or a database record\) passes through the entire system\.

This architecture is easy to build and it has a wide range of applications, from hardware to data analytics\. Though each pipeline specializes in a single use case, it is often possible to build many different pipelines from the same set of generic components, which is actually practiced by Linux admins in their use of shell scripts \[[wiki/concepts/source/appendices/books-referenced|[DDIA]]\]\.

## [[wiki/concepts/source/basic-metapatterns/pipeline|Choreographed Event\-Driven Architecture]]

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-EventDrivenArchitecture.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-EventDrivenArchitecture.png" alt="Parcel delivery example with different pipelines for individual parcels and trucks of parcels." loading="lazy" width=100%/>
</a>
</div>

Relaxing the *type* and loosening the *identity* criteria opens the way to [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture*]], in which a service publishes notifications about everything it does which may be of interest to other services\. In such a system:

- There are multiple kinds of events going in different directions, as if several branched pipelines were built over the same set of services\.
- A service may aggregate multiple incoming events to publish a single, seemingly unrelated, event later, when a certain condition is met\. For example, a warehouse delivery collects individual orders till it gets a truckload of them, or until the evening comes and no new orders are accepted\.


This architecture covers way more complex use cases than [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipes and Filters*]], because multiple pipelines are present in the system and because processing an event is allowed to have loosely related consequences \(as with the parcel and truck\)\.

## [[wiki/concepts/source/fragmented-metapatterns/layered-services|Command Query Responsibility Segregation]] \(CQRS\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-CQRS.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-CQRS.png" alt="In CQRS data passes through a pipeline formed of the command backend, OLTP database, OLAP database, and the query backend." loading="lazy" width=100%/>
</a>
</div>

When data from events is stored for a future use \(as with the aggregation above\), both the *type* and the *temporal order* are ignored, but the data *identity* may be retained\. A [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*\-based system]] separates the paths for write \(*command*\) and read \(*query*\) requests, making a kind of data processing pipeline with the database, which stores events for an indeterminate amount of time, in the middle\. It is the database that reshuffles the order of events, as a record it stores may be queried at any time, maybe in a year from its addition – or never at all\.

## [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Model\-View\-Controller]] \(MVC\)

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-MVC.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Conclusion/Pipelineliness-MVC.png" alt="Events from the mouse pass to the controller and the model, and those from the model - to the view and display." loading="lazy" width=100%/>
</a>
</div>

[[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Controller*]] completely neglects the *type* and *identity* limitations\. It is a coarse\-grained pattern where the input source produces many kinds of events that go to the main module which does something and outputs another stream of events which have no obvious relation to the input\. A mouse click does not necessarily result in a screen redraw, while a redraw may happen on timer without any user actions\. In fact, this pattern conjoins two separate, short pipelines\.

## Summary

There are four architectures with unidirectional data flow, which is characteristic of [[wiki/concepts/source/basic-metapatterns/pipeline|*pipelines*]]:

- [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipes and Filters*]],
- [[wiki/concepts/source/basic-metapatterns/pipeline|*Choreographed Event\-Driven Architecture* \(*EDA*\)]],
- [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Command \(and\) Query Responsibility Segregation* \(*CQRS*\)]],
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Controller* \(*MVC*\)]]\.


The first two, being true pipelines, are built around data processing and transformation, while for the others it is just an aspect of implementation – their separation of input and output yields pairs of streams\.

| \<\< [[wiki/concepts/source/analytics/sharing-functionality-or-data-among-services|Sharing functionality or data among services]] | ^ [[wiki/concepts/source/analytics/comparison-of-architectural-patterns|Comparison of architectural patterns]] ^ | [[wiki/concepts/source/analytics/dependency-inversion-in-architectural-patterns|Dependency inversion in architectural patterns]] \>\> |
| --- | --- | --- |
