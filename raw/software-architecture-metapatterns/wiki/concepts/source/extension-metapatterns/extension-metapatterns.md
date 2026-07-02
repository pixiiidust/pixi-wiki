---
title: "Extension metapatterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Extension metapatterns/Extension metapatterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Extension%20metapatterns/Extension%20metapatterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Extension metapatterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Extension metapatterns/Extension metapatterns.md`.

These patterns extend [[wiki/concepts/source/basic-metapatterns/services|*Services*]], [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], or even a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] with a layer that provides an aspect or two of the system’s behavior and often glues other components together\.

### [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]]


![A diagram of Services with a middleware, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Middleware.png)


A [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] is a layer which provides communication with instances of the system’s components and it may also manage those instances\. This way each instance is relieved of the need to track the other instances which it accesses\.

*<ins>Includes</ins>*: \(Message\) Broker and Deployment Manager; Message Bus, Event Mediator, Enterprise Service Bus, and Service Mesh\.

### [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]]


![A diagram of Services with a shared repository, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Shared%20Repository.png)


A [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] stores the system’s data, maintains its integrity through transactions, and may support subscriptions to changes in subsets of the data\. That lets other system components concentrate on implementing the business logic\.

*<ins>Includes</ins>*: Shared Database, Blackboard, Data Grid of Space\-Based Architecture, Shared Memory, and Shared File System\.

### [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]


![A diagram of Services with a proxy, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Proxy.png)


A [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] mediates between a system and its clients, transparently taking care of some generic functionality\.

*<ins>Includes</ins>*: Full Proxy and Half\-Proxy; Sidecar and Ambassador; Firewall, Response Cache, Load Balancer, Reverse Proxy and various Adapters, e\.g\. Anticorruption Layer, Open Host Service, many Abstraction Layers, Repository, and even User Interface\.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]


![A diagram of Services with an orchestrator, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Orchestrator.png)


An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] implements use cases as sequences of calls to the underlying components which are usually left unaware of each other’s existence\.

*<ins>Includes</ins>*: Workflow Owner, Application Layer, Facade, Mediator; API Composer, Scatter\-Gather, MapReduce, Process Manager, Saga Execution Component, and Integration \(Micro\-\)Service\.

### [[wiki/concepts/source/extension-metapatterns/sandwich|Sandwich]]


![A diagram of Sandwich Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Sandwich.png)


[[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]] subdivides the largest and loosely coupled [[wiki/concepts/source/basic-metapatterns/layers|*domain* layer]] into modules or services while the other layers remain monolithic\.

*<ins>Includes</ins>*: Service\-Based Architecture, Space\-Based Architecture, Blackboard Architecture, Nanoservices, and Command Query Responsibility Segregation \(CQRS\)\.

| \<\< [[wiki/concepts/source/basic-metapatterns/pipeline|Pipeline]] | ^ [[wiki/concepts/source/root/home|Home]] ^ | [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]] \>\> |
| --- | --- | --- |
