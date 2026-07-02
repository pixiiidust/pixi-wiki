---
title: "Evolutions of a Middleware"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Middleware.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Middleware
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Middleware

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Middleware.md`.

A [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] is unlikely to be removed \(though it still may be replaced\) once it is built into a system\. There are few evolutions as a *Middleware* is a third\-party product and is unlikely to be messed with:

- If the *Middleware* in use does not fit the preferred mode of communication between some of your services, there is an option to deploy a second specialized *Middleware*\.
- If several existing systems need to be merged, that is accomplished by adding yet another layer of *Middleware*, resulting in a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Bottom\-Up Hierarchy \(Bus of Buses\)*]]\.


## Add a secondary Middleware


![A specialized middleware added to a system that already has a generic middleware.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Middleware%20add%20Middleware.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]]\.

<ins>Goal</ins>: support specialized communication between [[wiki/concepts/source/basic-metapatterns/shards|scaled]] services\.

<ins>Prerequisite</ins>: the system relies on a *Middleware* for scaling\.

If the current *Middleware* is too generic for the system’s needs, you can add another one for specialized communication\. The new *Middleware* does not manage the instances of the services\.

<ins>Pros</ins>:

- Supports specialized communication with no need to write code for tracking the instances of services\.


<ins>Cons</ins>:

- You still need to notify the new *Middleware* when an instance of a service is created or dies\.
- There is an extra component to administer\.


## Merge two systems by building a Bottom\-Up Hierarchy


![A low-level middleware interconnects several higher-level middlewares.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Middleware%20to%20Bus%20of%20Buses.png)


<ins>Patterns</ins>: [[wiki/concepts/source/fragmented-metapatterns/hierarchy|Bottom\-up Hierarchy]] \([[wiki/concepts/source/fragmented-metapatterns/hierarchy|Hierarchy]], [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]]\)\.

<ins>Goal</ins>: integrate two systems without a heavy refactoring\.

<ins>Prerequisite</ins>: both systems use *Middleware*s\.

If we cannot change the way each subsystem’s services use its *Middleware*, we should add a new *Middleware* to connect the existing *Middleware*s\.

<ins>Pros</ins>:

- No need to touch anything in the existing services\.


<ins>Cons</ins>:

- Performance suffers from the double conversion between protocols\.
- There is a new component to fail \(miserably\)\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-pipeline|Evolutions of a Pipeline]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-a-shared-repository|Evolutions of a Shared Repository]] \>\> |
| --- | --- | --- |
