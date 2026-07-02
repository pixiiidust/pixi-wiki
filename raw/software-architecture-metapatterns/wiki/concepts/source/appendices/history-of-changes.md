---
title: "History of changes"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/History of changes.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/History%20of%20changes
source_license_note: "See namespace README; preserve attribution and source links."
---

# History of changes

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/History of changes.md`.

0.1 (2020) – Description of my semisynchronous *Proactor* architecture for a VoIP gateway, published by dou.ua. It received very positive feedback and lots of comments from the community.

0.2 (2020) – [The same in a more official style](http://www.hillside.net/plop/2020/papers/poltorak.pdf) for the (Corona-)PLoP’20 conference.

0.3 (2021) – Comparison of choreography and orchestration for dou.ua. No impact.

0.4 (2022) – A series of 5 articles that looked into local and distributed architectures by applying the actor model. Positive feedback from dou.ua, but the series was interrupted by the war.

0.5 (2023) – [The same series in English](https://medium.com/itnext/introduction-to-software-architecture-with-actors-part-1-89de6000e0d3), published by ITNEXT and upvoted by r/softwarearchitecture.

0.6 (2023) – I attempted to rebuild the series for InfoQ but the first article was rejected as impractical (technology-agnostic).

0.7 (09-2024) – [Chapters from this book](https://medium.com/itnext/the-list-of-architectural-metapatterns-ed64d8ba125d), published by ITNEXT. Some of them were boosted by Medium.

0.8 (11-2024) – The complete book as a pdf. Clients were changed to mid-brown. Detailed evolutions were moved to the appendix. Rejected by Manning (the free license and color diagrams make the book unprofitable) and O’Reilly (it would get in the way of their bestsellers). Ignored by Addisson-Wesley.

0.9 (12-2024) – Integrated patterns from \[[wiki/concepts/source/appendices/books-referenced|[DDS]], [[wiki/concepts/source/appendices/books-referenced|LDDD]], [[wiki/concepts/source/appendices/books-referenced|SAHP]]\] and Internet sources, mostly affecting [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]], [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]. Added diagrams for [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Polyglot Persistence* with derived storage]] and detailed evolutions for [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]. Downgraded [[wiki/concepts/source/analytics/comparison-of-architectural-patterns|analytical chapters]] to sections and added a couple of new ones. Extended the [[wiki/concepts/source/analytics/ambiguous-patterns|ambiguous patterns chapter]]. Improved the structure of the variants sections of metapatterns: now each synonym has a short description. Fixed alignment of text and figures. Liked by [r/softwarearchitecture](https://www.reddit.com/r/softwarearchitecture/comments/1hi377v/free_book_architectural_metapatterns_the_pattern/). Rejected by The Pragmatic Programmer (they want “hands-on, actionable content”). Ignored by No Starch Press and Packt.

1.0 (04-2025) – Integrated \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\]. Integration logic (use cases) is now in green. Added [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVC*]]- and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVP*]]-related patterns and a section on [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|Programming and architectural paradigms]]. Replaced the chapter on [control and processing](https://medium.com/itnext/control-and-processing-software-9011fee8bc66) with a new one about [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|Four kinds of software]] and added another one called [[wiki/concepts/source/analytics/the-heart-of-software-architecture|The heart of software architecture]]. Made minor changes all over the book. Now I know how to [generate a table of contents for both EPUB and PDF versions](https://medium.com/@denyspoltorak/guide-on-converting-a-google-docs-text-into-an-ebook-5b1abc65f69d). Ignored by Wikibooks.

1.1 (07-2025) – Lars Noodén edited the book, fixing my poor English. Patterns are now in *Title Case Italics*. [*Domain-Oriented Microservice Architecture*](<Service-Oriented Architecture (SOA)#domain-oriented-microservice-architecture-doma>) was added. There are now short explanation sections (in gray) throughout the book. Rejected by [EuroPLoP](https://www.europlop.net/) and [AsianPLoP](https://plopcon.org/asianplop2026/) because I was unable to attend the conferences in person. Ignored by the [main PLoP](https://plopcon.org/).

1.2 (05-2026) – New chapters: [[wiki/concepts/source/introduction/system-topologies|System topologies]] and [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] (replaced the boring *Combined Component*). Added [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]], [[wiki/concepts/source/basic-metapatterns/layers|*ECB*]], [[wiki/concepts/source/extension-metapatterns/proxy|*User Interface*]], [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Pedestals*]], [[wiki/concepts/source/implementation-metapatterns/plugins|examples of *Plugins*]], and [[wiki/concepts/source/basic-metapatterns/layers|descriptions of layer roles]]. Changed the diagram for [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]. Made many minor alterations. The book passed another cycle of editing.
