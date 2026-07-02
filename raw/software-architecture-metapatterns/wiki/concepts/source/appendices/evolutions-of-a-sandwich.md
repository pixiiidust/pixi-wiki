---
title: "Evolutions of a Sandwich"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Sandwich.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Sandwich
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Sandwich

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Sandwich.md`.

Unique evolutions of a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] involve the system’s domain logic or its topology:

- The [[wiki/concepts/source/basic-metapatterns/layers|*domain\-level*]] *services* are independent enough to be easily added or removed\.
- In most cases they share technologies, allowing for splitting or merging of the services\.
- If the services are found to be strongly coupled, they can be merged into a monolithic layer, likely to be subdivided in a better way later on\.
- Alternatively, the subdomains can be further decoupled\.


## Add or remove a domain\-level service


![One of the domain-level services is removed and another one is added.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20add%20remove%20Service.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/sandwich|Sandwich]]\.

<ins>Goal</ins>: maintain effective development\.

<ins>Prerequisite</ins>: a new subdomain emerges or an old one becomes obsolete\.

Though the *Sandwich* architecture allows for subdomains to be pretty independent in their logic, you should update your system’s high\-level structure whenever there are drastic changes in the domain knowledge or functional requirements\. Creation or deletion of a component often means forming or disbanding a team \(see [*Inverse Conway Maneuver*](https://martinfowler.com/bliki/ConwaysLaw.html)\)\.

<ins>Pros</ins>:

- The system’s architecture remains clear as it follows the domain knowledge\.
- The development teams remain narrowly specialized, thus effective\.
- Dead domain\-level code is easily identified and removed\.


<ins>Cons</ins>:

- You may need to update your database schema\.
- A newly established team takes time to learn its area of responsibility, while disbanding an old team disrupts almost everyone on the project\.


## Split or merge domain\-level services


![One domain-level service is split in half while two other services are merged together.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20split%20merge%20Services.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/sandwich|Sandwich]]\.

<ins>Goal</ins>: maintain effective development\.

<ins>Prerequisite</ins>: the business requirements gradually diverge from your original vision\.

[[wiki/concepts/source/foundations-of-software-architecture/modules-and-complexity|Ideally]], each service should be kept cohesive, while the services should be decoupled from each other\. However, business likes to mess up your plans\. If you ignore the results, your teams will be slowed down by mutual dependencies or become overburdened by the size of the components which they maintain\. Therefore, restructure both the system and teams once the divergence between the domain knowledge and system’s architecture starts to negatively impact development\.

> If an architecture is misaligned with the domain which it models, some components implement functions which don’t properly belong to them, while others need a lot of help from their neighbors\. Many unnecessary dependencies emerge between components and that both increases complexity \(you cannot develop a component without knowing other components\) and slows down the system \(calls between components tend to be inefficient\)\.

<ins>Pros</ins>:

- The system’s architecture is realigned with the domain knowledge\.
- The system components remain internally cohesive and decoupled from each other\.
- The development teams stay narrowly specialized, thus effective\.


<ins>Cons</ins>:

- You will have to update the database schema and integration logic \([[wiki/concepts/source/basic-metapatterns/layers|use cases]]\)\.
- Splitting or merging teams disrupts them\.


## Merge all the domain\-level services together


![The entire domain layer is merged, resulting in Layers.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20to%20Layers.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: improve the system performance and, possibly, development efficiency\.

<ins>Prerequisite</ins>: the project is small but found to be strongly coupled\.

Often the project grows in an unexpected manner\. If you see that the domain\-level services interact intensely, that likely means that you chose a wrong architecture\. Revert to *Layers* to remove the artificial interfaces\. You may also consider merging the domain\-level teams if there are not too many people in them\.

<ins>Pros</ins>:

- Less indirection and boilerplate code\.
- Improved performance which can be further optimized\.


<ins>Cons</ins>:

- Now all the teams face higher system complexity\.
- The teams will share the codebase which means a high level of interdependency\.


## Subdivide both shared layers


![The integration and data layers are divided into subdomains, producing Three-Layered Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Sandwich%20to%20Layered%20Services.png)


<ins>Patterns</ins>: [[wiki/concepts/source/fragmented-metapatterns/layered-services|Three\-Layered Services]] \([[wiki/concepts/source/fragmented-metapatterns/layered-services|Layered Services]]\)\.

<ins>Goal</ins>: fine\-grained scalability, database performance optimization, and limited fault tolerance\.

<ins>Prerequisite</ins>: the subdomains are loosely coupled in both [[wiki/concepts/source/basic-metapatterns/layers|use cases]] and [[wiki/concepts/source/basic-metapatterns/layers|data]]\.

It is natural to divide a *Sandwich* into [[wiki/concepts/source/basic-metapatterns/services|*Services*]], but only if your domain is not [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|data\-centric]] \(built around a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]]\) and your use cases are not too complex \(requiring an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\)\.

<ins>Pros</ins>:

- Independent scaling and deployment of the services\.
- Database technologies can be chosen on a per service basis\.
- Simpler application and database components\.
- Limited fault tolerance – if one of the services fails, others may still respond to clients\.


<ins>Cons</ins>:

- Complex use cases are hard to implement or debug\.
- Poor latency for use cases that involve multiple subdomains\.
- Any coupling in the data impairs performance and increases costs\.
- Now you’ll have much more work for your DevOps\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-an-orchestrator|Evolutions of an Orchestrator]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/format-of-a-metapattern|Format of a metapattern]] \>\> |
| --- | --- | --- |
