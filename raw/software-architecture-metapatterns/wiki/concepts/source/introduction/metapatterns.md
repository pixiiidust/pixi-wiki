---
title: "Metapatterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Introduction/Metapatterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Introduction/Metapatterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Metapatterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Introduction/Metapatterns.md`.

Is there a way to bring the patterns into order? They are way too many, some obscure, others overly specialized\.

We can try\. On a subset\. And the subset should be:

- *Important* enough to matter for the majority of programmers\.
- *Small* enough to fit in one’s memory or in a book\.
- *Complete* enough to assure that we don’t miss anything crucial\.


Is there such a set? I believe so\.

## Architectural patterns

\[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\] defines three categories of patterns:

- *Architectural patterns* which deal with the overall structure of a system and functions of its components\.
- *Design patterns* which describe relations between objects\.
- *Idioms* which provide abstractions on top of a given programming language\.


Architectural patterns are important by [definition](https://martinfowler.com/architecture/) \(*Architecture is about the important stuff\. Whatever that is*\)\. Point 1 \(*importance*\) – checked\.

Any given system has an internal structure\. When its developers talk about *architectural style* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\] or draw structural diagrams that usually boils down to a composition of two or three well\-known architectural patterns\. Choosing architectural patterns as the subject of our study lets us feed on a large body of books and articles that describe similar designs over and over again\. Moreover, as soon as a system no longer follows the latest fashions, it is widely advertised as a novelty \(or its designers are labeled as old\-fashioned and shortsighted\), thus we may expect to have heard of nearly all of the architectures which are used in practice\. Point 3 \(*completeness*\) – we have more than enough examples to analyze\.

To organize a set of patterns we rely on the concept of design space\.

## Design space

*Design space* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA5]]\] is a model that allocates a dimension for each choice made while architecting the system\. Thus it contains all the possible ways for a system to be designed\. The only trouble – it is multidimensional, maybe infinite, and the dimensions will differ from system to system\.

There is a workaround – we can use a projection from the design space into a 2\- or 3\-dimensional space which we are more comfortable with\. However, projection causes a loss of information\. Counterintuitively, that is good for us – similar architectures that differ in minor details become identical as soon as the dimensions they differ in disappear\. If we could only find 2 or 3 most important dimensions that apply equally well to each pattern in the set that we want to research, that is architectural patterns, which cover all the known system designs\.

## Structure determines architecture

Systems tend to have an internal structure\. Those that don’t are derogatively called [*Big Balls of Mud*](http://www.laputan.org/mud/) for their peculiar properties\. Structure is all about components, their roles and interactions\. Many architectural styles, for example, [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], are named after their structures, while others, like [[wiki/concepts/source/basic-metapatterns/pipeline|*Event\-Driven Architecture*]], highlight some of its aspects, hinting that it is the structure which determines principal properties of a system\.

I am not the first person to reach such a conclusion\. *Metapatterns* – clusters of patterns of similar structure – were [defined](https://softwareresearch.net/fileadmin/user_upload/Documents/publications/conference_proceedings/C010.pdf) shortly after the first collections of design patterns had appeared but they never made a lasting impact on software engineering\. I believe that the approach was applied prematurely to analyze the \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] patterns, which make quite a random and incomplete subset of design patterns, resulting in an overgeneralization\. I intend to plot structures of all the architectural patterns I encounter, group patterns of identical structure together into metapatterns, draw relations between the metapatterns, and maybe show how a system’s structure determines its properties\. Quite an ambitious plan for a short book, isn’t it?

Our set of architectural patterns is still not known to be complete, is not small and, moreover, the way structural diagrams are drawn differs from source to source – we cannot compare them unless we make up a universal system of coordinates\.

## The system of coordinates

Inventing a generic coordinate system to fit any pattern’s representation, from [*Iterator*](https://refactoring.guru/design-patterns/iterator) to [[wiki/concepts/source/basic-metapatterns/monolith|*Half\-Sync/Half\-Async*]], may be too hard, but we surely can find something for architectural patterns, as all of them share the scope, namely the system as a whole\. Which dimensions an implementation of a system would usually be plotted along?

1.  *Abstractness* – there are high\-level use cases and low\-level details\. A single highly abstract operation unrolls into many lower\-level ones: Python scripts run on top of a C runtime and assembly drivers; orchestrators call API methods of services, which themselves run SQL queries towards their databases which are full of low\-level computations and disk operations\.
2.  *Subdomain* – any complex system manages multiple subdomains\. An OS needs to deal with a variety of peripheral devices and protocols: a video card driver has very little resemblance to an HDD driver or to the TCP/IP stack\. An enterprise has multiple departments, each operating a software that fits its needs\.
3.  *Sharding* – if several instances of a module are deployed, and that fact is an integral part of the architecture, we should represent the multiple instances on our structural diagram\.


We’ll draw the abstractness axis vertically with higher\-level components positioned towards the upper side of the diagram, the subdomain axis horizontally, and sharding diagonally\. Here is an \(arbitrary\) example of such a diagram:

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Intro/CQRS%20with%20notes.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Intro/CQRS%20with%20notes.png" alt="A diagram of a CQRS system in abstractness-subdomain-sharding coordinates with a detailed legend." loading="lazy" width=100%/>
</a>
</div>

\(A structural diagram for [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]], adapted from [Udi Dahan’s article](https://udidahan.com/2009/12/09/clarified-cqrs/), to introduce the notation\)

> Abstractness is usually inverse to the distance to the system’s clients\. A graphical interface is highly abstract with its intuitive windows, forms, and scrollbars, and it is the part of the software which the users interact with\. The opposite end of the system hosts device drivers which operate in cryptic bits and registers\. Nevertheless, the reality is more complex: to draw UI windows on the screen the software still needs help from graphic card drivers deep inside the OS\. Likewise, there are several layers of routing and proxies between a web page that you see in your browser and the server\-side logic which that page allows you to access\. Even though those intermediate layers are not highly abstract, we still draw them in the upper part of diagrams between a system and its clients to keep the diagrams [simple and stupid](https://en.wikipedia.org/wiki/KISS_principle)\.

## Map and reduce

Now that we have the generic coordinates which seem to fit any architectural pattern, we can start mapping our set of architectural patterns into that coordinate system to reduce the multidimensional design space down to the few dimensions of structural diagrams which we were actually looking for\. Then, after filtering out minor details, our hundred or so published patterns should yield a score of [[wiki/concepts/source/introduction/system-topologies|*topologies*]] – clusters of geometrically equivalent diagrams – just because there are very few simple systems that one can draw on a plane before repeating oneself\. Each topology will represent an *architectural metapattern* – a generalization of architectural patterns of similar structure and function\.

Let’s return for a second to our requirements for classifying a set of patterns\. The importance \(point 1\) of architectural patterns was proved before\. The reasonable size of the resulting classification \(point 2\) is granted by the existence of only a few simple 2D or 3D shapes \(topologies\)\. The completeness of the analysis \(point 3\) comes from, on one hand, the geometrical approach which makes any blank spaces \(possible geometries with no known patterns\) obvious, and on the other – from the large sample of architectural patterns which we are classifying\.

Godspeed\!

## An example of metapatterns

Let’s consider the following structure:

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Intro/Example-Undefined.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Intro/Example-Undefined.png" alt="Two high-level components interact with one low-level component." loading="lazy" width=93%/>
</a>
</div>

It features two \(or more in real life\) high\-level modules that communicate with/via a lower\-level module\. Which patterns does it match?

- [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] – a software that provides means of communication between other components\.
- [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] – a space for other components to store and exchange data\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Model\-View\-Controller*]] – a platform\-agnostic business logic with customized means of input and output\.


<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Intro/Example-Defined.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Intro/Example-Defined.png" alt="Diagrams for Services with a Middleware, Services with a shared database and Model-View-Controller." loading="lazy" width=100%/>
</a>
</div>

My idea of grouping patterns by structure seems to have backfired – we got three distinct patterns that have similar structural diagrams\. The first two of them are related – both implement indirect communication, and their distinction is fading as a *Middleware* may feature a persistent storage for messages while a table in a *Shared Database* may be used to orchestrate services\. The third one is very different – primarily because the bulk of its code, that is its *business logic*, resides in the lower layer, leaving the upper\-level components a minor role\.

Notwithstanding, each of the patterns we found is a part of a distinct cluster:

- *Middleware* is also known as *\(Message\) Broker* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]], [[wiki/concepts/source/appendices/books-referenced|EIP]], [[wiki/concepts/source/appendices/books-referenced|MP]]\] and is an integral part of [[wiki/concepts/source/extension-metapatterns/middleware|*Message Bus*]] \[[wiki/concepts/source/appendices/books-referenced|[EIP]]\], [[wiki/concepts/source/extension-metapatterns/middleware|*Service Mesh*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], [[wiki/concepts/source/extension-metapatterns/middleware|*Event Mediator*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], [[wiki/concepts/source/extension-metapatterns/middleware|*Enterprise Service Bus*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], and [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]] \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\]\.
- *Shared Database* is a kind of [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] \([[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Memory*]], [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared File System*]]\), and the foundation for [[wiki/concepts/source/extension-metapatterns/shared-repository|*Blackboard*]] \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\], [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]] \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\], and [[wiki/concepts/source/extension-metapatterns/sandwich|*Service\-Based Architecture*]] \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\]\.
- *Model\-View\-Controller* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\] is a special kind of [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] \(aka [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Ports and Adapters*]], [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Onion Architecture*, and *Clean Architecture*]]\) which itself is derived from [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\] \(*Addons*, *Plug\-In Architecture* \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], or the [[wiki/concepts/source/analytics/ambiguous-patterns|misnomer]] *Microkernel Architecture* \[[wiki/concepts/source/appendices/books-referenced|[SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\]\)\.


Our touching on a single topology revealed a web of twenty or so pattern names that spreads all around\. With such a pace there is a hope of exploring the whole fabric which is known as *pattern language* \[[wiki/concepts/source/appendices/books-referenced|[GoF]], [[wiki/concepts/source/appendices/books-referenced|POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA2]], [[wiki/concepts/source/appendices/books-referenced|POSA5]]\]\.

There are three lessons to learn:

- The distribution of business logic is a crucial aspect of topologies\.
- Metapatterns are interrelated in multiple ways, forming a pattern language\.
- Each metapattern includes several well\-established patterns\.


## What does that mean

Chemistry has the [periodic table](https://en.wikipedia.org/wiki/Periodic_table)\. Biology has the [tree of life](https://en.wikipedia.org/wiki/Tree_of_life_(biology))\. This book strives towards building something of that kind for software and systems architecture\. You can say “That makes no sense\! Chemistry and biology are empirical sciences while software architecture isn’t\!” Is it?

| \<\< [[wiki/concepts/source/introduction/about-this-book|About this book]] | ^ [[wiki/concepts/source/introduction/introduction|Introduction]] ^ | [[wiki/concepts/source/introduction/system-topologies|System topologies]] \>\> |
| --- | --- | --- |
