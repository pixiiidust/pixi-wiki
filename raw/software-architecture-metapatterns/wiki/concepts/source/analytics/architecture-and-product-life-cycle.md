---
title: "Architecture and product life cycle"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/Architecture and product life cycle.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/Architecture%20and%20product%20life%20cycle
source_license_note: "See namespace README; preserve attribution and source links."
---

# Architecture and product life cycle

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/Architecture and product life cycle.md`.

In my practice, a product’s architecture changes over its lifetime\. For a R&D, when there is nobody with relevant experience on the team, it starts small, gradually gains flexibility through fragmentation, grows and restructures itself according to the ever\-changing domain knowledge and business requirements, then it solidifies as the project matures, and dies because of performance optimizations and loss of experience as the seasoned programmers leave\. In more mundane projects the first stages may be omitted, as little research needs to be done, and oftentimes a project is canceled way before its architecture succumbs under its own weight\. Anyway, let’s observe the full life cycle\.

### Infancy \(proof of concept\) – Monolith


![A diagram of a monolith.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Lifecycle-1.png)


A project in an unknown domain starts humble and small, likely as a proof of concept\. You need to write quickly to check your ideas about how the domain works without investing much time – as you may oftentimes be wrong here or there, making you rethink and rewrite\.

### Childhood \(prototype\) – Layers


![Diagrams of Layers and Hexagonal Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Lifecycle-2.png)


When you have the thing working, you may start reflecting on the rules and the code which you wrote\. What belongs where, what can be subject to change, which tests will you need? At this point you clearly see the levels of abstractness: the high\-level [[wiki/concepts/source/basic-metapatterns/layers|*application*]] \(integration, orchestration\) logic, the lower\-level [[wiki/concepts/source/basic-metapatterns/layers|*domain*]] \(business\) rules, and the generic *infrastructure* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\. Now that you know better the whats and the hows, you divide the code \(either old or rewritten from scratch\) into [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] to make it both structured and flexible, yet still without a heavy development overhead caused by interfaces between subdomains\.

### Youth \(development of features\) – fragmented architectures


![Diagrams of Layered Services, Orchestrated Services, and Top-Down Hierarchy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Lifecycle-3.png)


As you acquire domain experience, you start discerning subdomains \(or *bounded contexts* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\) and isolating them to reduce the [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|complexity]] of your code\. The layered structure turns into a system of subdomain\-dedicated components: [[wiki/concepts/source/basic-metapatterns/services|modules]], [[wiki/concepts/source/basic-metapatterns/services|services]], [[wiki/concepts/source/basic-metapatterns/services|device drivers]] – whatever you used to name them throughout your career\. The actual architecture follows the structure of the domain, with [[wiki/concepts/source/fragmented-metapatterns/layered-services|*Layered Services*]], [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrated Services*]], and [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top\-Down Hierarchy*]] among common options\. The fragmentation of the system enables development by multiple teams with diverse technologies and styles, reduces the ripple effects of changes, and helps testability\. However, use cases for the system as a whole become harder to understand and fix – if only because they traverse the parts of the code owned by multiple teams – which is not extremely bad given you have enough humanpower to do the work\.

### Adulthood \(production\) – ad\-hoc composition


![Layered Services evolve into a pragmatic architecture where the application layers of some services are merged while the domain layer of another service is subdivided.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Lifecycle-4.png)


As the product enters the market, its development tends to slow down with more attention given to corner cases and user experience\. Some \(often the most active\) people are going to get bored and leave the project, while your understanding of the domain changes again based on user experience and real\-life business needs \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\. You may find that some of the components which you have designed as independent become strongly coupled, and you are lucky if they are small enough to be merged together – this is where the fragmentation from the previous stage pays off\. Other parts of the system may outgrow the comfort zone of programmers and need to be subdivided\. The architecture becomes asymmetrical and pragmatic\.

### Old age \(support\) – back to Layers


![A diagram of Layers with multiple databases.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Lifecycle-5.png)


When active development ceases, you lose even more people and funding as you drift into the support phase\. You are unlikely to retain your best programmers – you’ll get novices or even an outsourced team instead\. They will struggle to retain the structure of the system – with its mass of hacks from the previous years – against progressively more weird requests from the business and customers whose natural desires have already been satisfied\. That will cause many more hacks to be added – and components coupled or merged for the hacks to land – bringing the architecture back to [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], though this time heavily oversized layers\.

### Death \(the ultimate release\) – Monolith


![A diagram of a monolith with multiple databases.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/Lifecycle-6.png)


If the project is allowed to die, it may still have a chance for a final release which aims at improving performance and leaving a golden standard for the generations of users to come\. Heavy optimizations will likely require merging the layers to avoid all kinds of communication overhead, reverting the system back to [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]]\.

### So it goes

Even though I have observed the cycle of architecture expanding and collapsing in embedded software, I believe that these forces apply to most kinds of systems\. First you need to go quickly and interfaces are a burden\. Then you need the extra flexibility that they provide to reserve space for future design changes\. And as the flow of changes ceases, you may optimize the flexibility away to make programming easier and the code smaller and faster\. However, the last transition is not always applicable: a distributed system will oppose compacting if it was written in diverse programming languages or needs specialized hardware setups for proper operation\.

### Going back in time

It can happen that you need to step back through the life cycle – for example, when the domain itself changes drastically: a new standard emerges or the management decides that your application for washing machines fits coffee machines pretty well, as they are basically doing the same things: heating water, adding powder, and stirring – yet you have never wrote software for coffee machines before, thus you are back to the R&D phase\.

In such cases it may be easier to rewrite the affected components from scratch rather than try to rejuvenate and refit the old code\. Remember that you keep your experience – what was originally implemented as an improvised hack will be accounted for in the redesigned architecture\. This means that every time a component is rewritten adds to its longevity as its architecture fits the domain more closely and needs fewer hacks \(which are inflexible and confusing by definition\) to get to production\.

| \<\< [[wiki/concepts/source/analytics/ambiguous-patterns|Ambiguous patterns]] | ^ [[wiki/concepts/source/analytics/analytics|Analytics]] ^ | [[wiki/concepts/source/analytics/real-world-inspirations-for-architectural-patterns|Real\-world inspirations for architectural patterns]] \>\> |
| --- | --- | --- |
