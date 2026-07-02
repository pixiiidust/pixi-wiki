---
title: "Comparison of communication styles"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Foundations of software architecture/Arranging communication/Comparison of communication styles.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Foundations%20of%20software%20architecture/Arranging%20communication/Comparison%20of%20communication%20styles
source_license_note: "See namespace README; preserve attribution and source links."
---

# Comparison of communication styles

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Foundations of software architecture/Arranging communication/Comparison of communication styles.md`.

We have briefly discussed three approaches to communication: orchestration, choreography, and shared data\. Let’s recall when it makes the most sense to use each of them\.

- [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*Orchestration*]] is built around [[wiki/concepts/source/basic-metapatterns/layers|use cases]]\. They are easy to program and add, no matter how complex they become\. Thus, if your \(sub\)domain is coupled, or your understanding of it is still evolving, this is the way to go, as you will be able to change the high\-level logic in any imaginable way because you express it as convenient imperative code\.
- [[wiki/concepts/source/foundations-of-software-architecture/shared-data|*Shared data*]] is all about… er… domain data\. If you really \(believe that you\) know your domain, and it deals with coupled data – this is your chance\. You may even add in an *Orchestrator* if there are use cases that involve multiple subdomains\. The business logic is going to be easy to extend while changes to the data schema are sure to cause havoc\.
- [[wiki/concepts/source/foundations-of-software-architecture/choreography|*Choreography*]] pays off for weakly coupled domains with a few simple use cases\. It has good performance and flexibility, but lacks the expressive power of orchestration and becomes very messy as the number of tasks and components grows\. It works best with independent teams and delayed processing – when users are not waiting for the final results of their actions\.


There is advice [from Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography) and \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\] which makes perfect sense: use choreography for communication between *bounded contexts* \(subdomains\) \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] but revert to orchestration \(or maybe shared data\) inside each context\. Indeed, subdomains are likely to be loosely coupled while most user requests don’t traverse subdomain boundaries – which kindles hope that their interactions are few and not time\-critical\. If we follow the advice, we get [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]] \([WSO2 definition](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md)\), which collects the best of two worlds: orchestration and/or shared data for strongly coupled parts and choreography between them\.


![A diagram of the Cell-Based Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Communication/Cell-Based%20Architecture.png)


By the way, you could have noticed a few odd cases:

- An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] in a [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|control system]] does not run scenarios and its mode of action resembles choreography\.
- A choreographed system may use a [[wiki/concepts/source/extension-metapatterns/shared-repository|shared message format]], which makes it resemble a system with shared data, even though no shared database is present\.
- A shared database may be used to [[wiki/concepts/source/extension-metapatterns/shared-repository|implement messaging]] for an orchestrated or choreographed system, effectively becoming a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]\.


That likely means that our distinction between the modes of communication is a bit artificial and there exists a yet unknown deeper model to look for\.

| \<\< [[wiki/concepts/source/foundations-of-software-architecture/shared-data|Shared data]] | ^ [[wiki/concepts/source/foundations-of-software-architecture/arranging-communication|Arranging communication]] ^ | [[wiki/concepts/source/basic-metapatterns/basic-metapatterns|Basic metapatterns]] \>\> |
| --- | --- | --- |
