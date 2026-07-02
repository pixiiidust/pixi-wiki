---
title: "Evolutions of Layers that make more layers"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Layers that make more layers.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Layers%20that%20make%20more%20layers
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Layers that make more layers

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Layers that make more layers.md`.

Not all the layered architectures are equally layered\. A [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] with a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] or [[wiki/concepts/source/basic-metapatterns/layers|database]] has already stepped into the realm of [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] but is still far from reaping all of its benefits\. It may continue its journey in a few ways that [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-result-in-layers|were earlier discussed]] for *Monolith*:

- Employing a [[wiki/concepts/source/basic-metapatterns/layers|*database*]] \(if you don’t use one\) lets you rely on a thoroughly optimized state\-of\-the\-art subsystem for data processing and storage\.
- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] are similarly reusable generic components to be added at will\.
- Implementing an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] on top of your system may improve the programming experience and runtime performance for your clients\.



![A diagram of calls in a layered system. A single request from a client is translated by an Orchestrator into multiple calls to lower layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20to%20Layers.png)


It is also common to:

- Segregate the business logic into two [[wiki/concepts/source/basic-metapatterns/layers|*layers*]]\.


## Split the business logic into two layers


![A backend is subdivided into application and domain layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Layers/Layers%20Split%20in%20Two.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: let parts of the business logic vary in their qualities, improve the structure of the code\.

<ins>Prerequisite</ins>: the high\-level and low\-level parts of the business logic are loosely coupled\.

It is often possible to split a backend into [[wiki/concepts/source/basic-metapatterns/layers|integration]] \([[wiki/concepts/source/foundations-of-software-architecture/orchestration|orchestration]]\) and [[wiki/concepts/source/basic-metapatterns/layers|domain]] layers\. That allows for one team to specialize in customer use cases while the other one delves deep into the domain knowledge and infrastructure\.

<ins>Pros</ins>:

- You get an extra development team\.
- The high\-level use cases may be deployed separately from business rules\.
- The layers may diverge in technologies and styles\.
- The code may [[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|become less complex]]\.


<ins>Cons</ins>:

- There is a small performance penalty\.
- In\-depth debugging becomes harder\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-logic|Evolutions of Shards that share logic]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-layers-that-help-large-projects|Evolutions of Layers that help large projects]] \>\> |
| --- | --- | --- |
