---
title: "Implementation metapatterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Implementation metapatterns/Implementation metapatterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Implementation%20metapatterns/Implementation%20metapatterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Implementation metapatterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Implementation metapatterns/Implementation metapatterns.md`.

A few architectures focus on implementation of components:

### [[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]]


![A diagram of Plugins Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Plugins.png)


The [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] family of patterns is about separating a system’s main logic from the customizable details of its behavior. That allows for the same codebase to be used for multiple flavors or customers.

*<ins>Includes</ins>*: Plug-In Architecture, Addons, Strategy, Hooks.

### [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal Architecture]]


![A diagram of Hexagonal Architecture, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Hexagonal%20Architecture.png)


[[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] is a specialization of [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] where every external dependency is isolated behind an [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]], making it easy to update or replace third-party components.

*<ins>Includes</ins>*: Ports and Adapters, Onion Architecture, and Clean Architecture; Model-View-Presenter (MVP), Model-View-ViewModel (MVVM), Model-View-Controller (MVC), and Action-Domain-Responder (ADR); Pedestal and Cell (Cluster or Domain).

### [[wiki/concepts/source/implementation-metapatterns/microkernel|Microkernel]]


![A diagram of Microkernel, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Microkernel.png)


[[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]] is another derivation of [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]], featuring a rudimentary *core* component which mediates between resource *consumers* (*applications*) and resource *providers*. The *microkernel* is a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] to the *applications* and an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] to the *providers*.

*<ins>Includes</ins>*: operating system, software framework, virtualizer, distributed runtime, interpreter, configuration file, Saga Engine, and AUTOSAR Classic Platform.

### [[wiki/concepts/source/implementation-metapatterns/mesh|Mesh]]


![A diagram of Services over a mesh, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Mesh.png)


A [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]] consists of intercommunicating shards, each of which may host an application. The shards coalesce into a fault-tolerant distributed [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]].

*<ins>Includes</ins>*: peer-to-peer networks, Leaf-Spine Architecture, Actors, Service Mesh, and Space-Based Architecture.
