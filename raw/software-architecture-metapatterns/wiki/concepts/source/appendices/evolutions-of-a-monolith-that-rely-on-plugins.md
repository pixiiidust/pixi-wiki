---
title: "Evolutions of a Monolith that rely on Plugins"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Monolith that rely on Plugins.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Monolith%20that%20rely%20on%20Plugins
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Monolith that rely on Plugins

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Monolith that rely on Plugins.md`.

The last group of evolutions which we will review does not really change the monolithic nature of the application\. Instead, its goal is to improve the *customizability* of the [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]]:

- Vanilla [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] are the most direct approach which relies on tailorable bits of logic\.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] is a subtype of *Plugins* which is all about isolating the main code from any third\-party components which it uses\.
- [[wiki/concepts/source/implementation-metapatterns/microkernel|*Scripts*]] is a kind of [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] – yet another subtype of *Plugins* – which gives users of the system full control over its behavior\.


## Support plugins


![Plugins customize the monolith's behavior.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Plugins.png)


<ins>Patterns</ins>: [[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]]\.

<ins>Goal</ins>: simplify the customization of the application’s behavior\.

<ins>Prerequisite</ins>: several aspects need to vary from customer to customer\.

*Plugins* create points of access to the system that allow engineers to collect data and govern select aspects of the system’s behavior without having to learn the system’s implementation\.

<ins>Pros</ins>:

- The system’s behavior can be modified by internal and external programmers who don’t know its internal details\.
- Customized versions become much easier to release and support\.


<ins>Cons</ins>:

- Extensive changes in the code may be required to expose the tunable aspects of the system\.
- Testability becomes poor because of the large number of possible variants\.
- Performance is likely to degrade\.


## Isolate dependencies with Hexagonal Architecture


![The database, external libraries, and a protocol support component are separated from the business logic and isolated with adapters.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Hexagonal.png)


<ins>Patterns</ins>: [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal Architecture]] \([[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]]\)\.

<ins>Goal</ins>: isolate the business logic from its external dependencies\.

<ins>Prerequisite</ins>: there are third\-party or frequently changing components in the system\.

The main business logic will communicate with any external component through an API or SPI defined in the terms of the business logic itself\. This way it will not depend on anything at all, and any component will be replaceable with another implementation or a [stub/mock](https://stackoverflow.com/questions/3459287/whats-the-difference-between-a-mock-stub)\.

<ins>Pros</ins>:

- Vendor lock\-in is ruled out\.
- A component may be replaced through to the very end of the system’s life cycle\.
- Stubs and mocks are supported for testing and local or early development\.
- It is possible to provide multiple implementations of a component\.


<ins>Cons</ins>:

- Some extra effort is required to define and use the interfaces\.
- There is performance degradation, mostly due to lost optimization opportunities\.


## Add an Interpreter \(support Scripts\)


![The high-level logic is rewritten as scripts which are run by an interpreter.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Interpreter.png)


<ins>Patterns</ins>: [[wiki/concepts/source/implementation-metapatterns/microkernel|Scripts aka Interpreter]] \([[wiki/concepts/source/implementation-metapatterns/microkernel|Microkernel]] \([[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]]\)\)\.

<ins>Goal</ins>: allow the system’s users to implement their own business logic\.

<ins>Prerequisite</ins>: the domain is representable in high\-level terms\.

*Interpreter* lets the users develop high\-level business logic from scratch by programming interactions of pre\-defined building blocks, which are implemented in the core of the system\. That provides unparalleled flexibility at the cost of degraded performance and design complexity\.

<ins>Pros</ins>:

- Perfect flexibility and customizability for every user\.
- The high\-level business logic is written in high\-level terms, making it fast to develop and easy to grasp\.


<ins>Cons</ins>:

- Requires much effort to design correctly\.
- There may be a heavy performance penalty if the API is overly fine\-grained\.
- Testability may be an issue\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-monolith-that-make-services|Evolutions of a Monolith that make Services]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-data|Evolutions of Shards that share data]] \>\> |
| --- | --- | --- |
