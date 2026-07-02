---
title: "Format of a metapattern"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Format of a metapattern.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Format%20of%20a%20metapattern
source_license_note: "See namespace README; preserve attribution and source links."
---

# Format of a metapattern

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Format of a metapattern.md`.

The descriptions of most [[wiki/concepts/source/introduction/metapatterns|metapatterns]] follow the same format:

### Diagram

The structural diagram \(in *abstractness\-subdomain\-sharding* [[wiki/concepts/source/introduction/metapatterns|coordinates]]\) of a typical application of the metapattern\. Please note that in practice the number and types of components and their interactions may vary:

- Even though most diagrams show 3 *layers* or *services*, there are many 2\-layered or 4\-layered systems, while the number of services may often be greater than 10\.
- [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|*Extension metapatterns*]] add a *layer* \(or a *layer of services*\) to an existing system, which is shown as [[wiki/concepts/source/basic-metapatterns/services|*Services*]], but may instead comprise [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], or even a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]]\.
- Subtypes of [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] or [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] differ in their [[wiki/concepts/source/introduction/system-topologies|topologies]]\. Only one is shown\.
- Components of metapatterns may communicate in various ways that include in\-process calls, RPC, asynchronous messaging, or streams\. Only one of them is shown\. Optional communication pathways may appear as dashed arrows\.


Most diagrams feature the following colors:

- [[wiki/concepts/source/basic-metapatterns/layers|*Use cases*]] \(aka integration, orchestration, workflow or application logic\) are shown in green\. Those are high\-level scenarios executed by user actions or signals from hardware which keep the system acting as a whole\. Use cases are *what* your software does\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Domain logic*]] \(business rules\), shown in blue, is the set of algorithms that models the real\-world system which your software describes\. It is *how* your system solves its tasks\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Generic code*]] is white\. It stands for tools and libraries unrelated to your business\. Examples include communication protocols, data compression, and common maths\.
- [[wiki/concepts/source/basic-metapatterns/layers|*Data*]] is gray\. It includes business\-critical in\-memory state \(e\.g\. user’s session\) and persistent storage \(in a database or files\)\.


*Use cases* and *domain logic* comprise *business logic* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\] – the code that makes your software different from whatever else is available on the market\. It is this part of the system which your customers pay for, and it usually is much larger than the other parts, which makes business logic the primary focus of development\.

In [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreographed*]] systems use cases are defined by the web of communication channels instead of the code inside the system’s components\. That is represented by green arrows and the overall lack of green areas on the diagrams of system components\.

### Abstract

*Motto* and the design goal\.

<ins>Known as:</ins> the list of aliases for the general metapattern\.

<ins>Structure:</ins> a short description of the structure of the metapattern\.

<ins>Type:</ins> system topology, extension component, or implementation\.

- A *system topology* \([[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], [[wiki/concepts/source/basic-metapatterns/services|*Services*]] and few others derived from them\) makes the backbone of any system\.
- An *extension component* is an addition to a *system topology* which modifies its properties\.
- An *implementation* shows the internal structure of a component, usually hidden from its clients\.


A short *table of benefits and drawbacks*\.

<ins>References:</ins> select articles and books that describe the topic\.

After that, there follow two or three paragraphs of facts and ideas about the metapattern\.

### Performance

This section discusses the performance of the subject metapattern in scenarios of various scope: simple requests or events that relate to a single subsystem are usually processed much faster than those that touch multiple components\.

There are two kinds of performance: latency and throughput\. Low latency is possible only if few components are involved because inter\-component communication, especially in distributed systems, increases latency\. Contrariwise, throughput depends on the number of components that work in parallel, thus it scales together with the system\.

This section may also discuss optimization techniques that apply to the metapattern\.

### Dependencies

Some components of the metapattern depend on other components\. If a component changes, everything that depends on it may need to be re\-tested with the updated version\. If a component’s interface changes, all the components that depend on it must be updated\. Therefore, components that evolve quickly should depend on others, not the other way around\.

Some patterns, such as [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]], use [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] to [[wiki/concepts/source/analytics/indirection-in-commands-and-queries|break dependencies]]\. An *Adapter* depends on components on both sides of itself, making those components independent of each other\. The *Adapters* are small enough to update quickly, and may easily be replaced with stubs for testing or running a component in isolation\.

### Applicability

Here follows a list of types of projects which may benefit from applying the architecture under review, and another list of those which it is more likely to hurt\.

### Relations

These are illustrated through an optional sequence of diagrams, showing the \(*extension* or *implementation*\) metapattern applied to various kinds of architectures, followed by a list of relations between the current and other metapatterns\.

### Variants and examples

A metapattern usually unites many variations of several patterns\. Here we may have a section per dimension of variability, and often another section with well\-known patterns and architectures that match the metapattern\.

When a pattern is listed under several metapatterns \(as often seen with *extension components*\), the headers of the multiple pattern descriptions cross\-link to each other\.

In other cases I had to include several variants that do not properly belong to the metapattern under review, just to avoid confusion with terminology and point the reader to the right chapter\. For example, [[wiki/concepts/source/basic-metapatterns/monolith|*Modular Monolith*]] has a module per subdomain, thus it belongs to [[wiki/concepts/source/basic-metapatterns/services|*Services*]] rather than [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]]\. Still, when the chapter on *Monolith* was not mentioning it, I was blamed for misunderstanding the *Monolithic Architecture*\. Such patterns are marked as \(misapplied\) or \(inexact\)\.

I tried to show the difference between synonymous names for every variant or example whenever I could identify one\.

### Evolutions

This section covers a brief summary of possible changes to the architecture under review\. Each change leads to a new architecture which usually belongs to another metapattern\.

[[wiki/concepts/source/appendices/evolutions-of-architectures|Appendix E]] discusses many evolutions in greater detail:

- A diagram that shows the original and resulting structures\.
- The list of patterns, present in the resulting architecture\. More general forms of each pattern are given in parentheses, i\.e\. Pattern \(Metapattern \(Parent Metapattern\)\)\.
- The goal\(s\) of the transition\.
- The prerequisites that enable the change\.
- A short description of the change and the resulting system\.
- Lists of pros and cons of the evolution\.
- An optional list of metapatterns that the resulting system may evolve into and their benefits in the context of the current evolution\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-sandwich|Evolutions of a Sandwich]] | ^ [[wiki/concepts/source/appendices/appendices|Appendices]] ^ | [[wiki/concepts/source/appendices/glossary|Glossary]] \>\> |
| --- | --- | --- |
