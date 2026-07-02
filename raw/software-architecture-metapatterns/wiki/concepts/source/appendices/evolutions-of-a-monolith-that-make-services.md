---
title: "Evolutions of a Monolith that make Services"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Monolith that make Services.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Monolith%20that%20make%20Services
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Monolith that make Services

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Monolith that make Services.md`.

The final major drawback of [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] is the cohesiveness of its code. The rapid start of development begets a major obstacle for project growth: every developer needs to know the entire codebase to be productive, and changes made by individual developers overlap and may break each other. Such distress is usually solved by dividing the project into components along *subdomain boundaries* (which tend to match [*bounded contexts*](https://martinfowler.com/bliki/BoundedContext.html) \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]). However, that requires a lot of work, and good boundaries and APIs are [hard to design](https://martinfowler.com/bliki/MonolithFirst.html). Thus many organizations prefer a slower iterative transition.

- A *Monolith* can be split into [[wiki/concepts/source/basic-metapatterns/services|*Services*]] right away.
- Or only the new features may be added as new services.
- Or the weakly coupled parts of existing functionality may be separated, one at a time.
- Some domains allow for sequential [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|data processing]] best described by [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]].



![In Services a single component executes a client request while in Pipeline there is no use case owner.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith_%20Services%20and%20Pipeline.png)


## Divide into Services


![A monolith is subdivided into services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Services.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/services|Services]].

<ins>Goal</ins>: facilitate development by multiple teams, improve the code, and decouple the qualities of subdomains.

<ins>Prerequisite</ins>: there is a natural way to split the business logic into loosely coupled subdomains, and the subdomain boundaries are sure to never change in the future.

Splitting a [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] into *Services* by subdomain [is risky in the early stages of a project](https://martinfowler.com/bliki/MonolithFirst.html) while the domain understanding is evolving ([[wiki/concepts/source/basic-metapatterns/services|in-process *modules*]] are less risky but provide fewer benefits). However, this is the way to go as soon as the codebase becomes unwieldy due to its size.

<ins>Pros</ins>:

- Supports multiple, relatively independent and specialized development teams.
- Lowers the penalty imposed by the project’s size and complexity on the velocity of development and product quality.
- Each team may choose the best fitting technologies for its component.
- The services can differ in their [qualities](https://en.wikipedia.org/wiki/List_of_system_quality_attributes).
- Flexible deployment and scaling.
- A certain degree of error tolerance for asynchronous systems.


<ins>Cons</ins>:

- It takes a lot of work to split a *Monolith*.
- Any future changes to the overall structure of the domain will be hard to implement.
- Sharing data between services is complicated and error-prone.
- System-wide use cases are hard to understand and debug.
- There is a moderate performance penalty for system-wide use cases.


## Add or split a service


![A service is split from a monolith.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20Split%20Service.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/services|Services]].

<ins>Goal</ins>: [stop digging](https://en.wikipedia.org/wiki/Law_of_holes), get some work for novices who don’t know the entire project.

<ins>Prerequisite</ins>: the new functionality you are adding or the part you are splitting is weakly coupled to the bulk of the existing *Monolith*.

If your [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] is already hard to manage, but a new functionality is needed, you can try dedicating a separate service to the new feature(s). This way the *Monolith* does not become larger – it is even possible that you will move a part of its code to the newly established service.

If you are not adding a new feature but need to change an old one – use the chance to make the existing *Monolith* smaller by first separating the functionality which you are going to change from its bulk. At the very minimum this two-step process lowers the probability of breaking something unrelated to the required changes of behavior.

<ins>Pros</ins>:

- The legacy code does not increase in size and complexity.
- The new service is transferred to a dedicated team which does not need to know the legacy system or use the old technologies.
- The new service can be experimented with and even rewritten from scratch.
- The likely faults of the new service won’t crash the main application.
- The new service can be tested and deployed in isolation.
- The new service can be scaled independently.


<ins>Cons</ins>:

- The new service will have a hard time sharing data or code with the main application.
- Use cases that involve both the new service and the old application are hard to debug.
- There is a moderate performance penalty for using the service.


<ins>Further steps</ins>:

- [Continue disassembling](https://martinfowler.com/bliki/StranglerFigApplication.html) the *Monolith*.


## Divide into a Pipeline


![A Monolith is transformed into a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Pipeline.png)


<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/pipeline|Pipeline]] ([[wiki/concepts/source/basic-metapatterns/services|Services]]).

<ins>Goal</ins>: decrease the complexity of the code, make it easy to experiment with the steps of data processing, and distribute the task over multiple CPU cores, processors, or computers.

<ins>Prerequisite</ins>: the domain can be represented as a sequence of coarse-grained data processing steps.

If you can treat your application as a chain of independent steps that transform the input data, you can rely on the OS to schedule them, and you can also dedicate a development team to each of the steps. This is the default solution for a system that [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|processes a stream]] of a single type of data (video, audio, or measurements). It has excellent flexibility.

<ins>Pros</ins>:

- Nearly abolishes the influence of the project size on development velocity.
- The project’s teams become almost independent.
- Flexible deployment and scaling.
- Naturally supports event replay for reproducing bugs, testing, or benchmarking individual components.
- It is possible to have multiple implementations for each of the steps of data processing.
- Does not require any manual scheduling or thread synchronization.


<ins>Cons</ins>:

- Latency may skyrocket.
- As the number of supported scenarios grows, so does the number of components and *pipelines*. Soon there’ll be nobody who understands the system as a whole.


## Further steps

As your knowledge of the domain and your business requirements change, you may need to move some functionality between the services to keep them loosely coupled. Sometimes you have to merge two or three services together. So it goes.

Systems of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipelines*]] are quite often extended with special kinds of [[wiki/concepts/source/basic-metapatterns/layers|*layers*]]:

- [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] takes care of deployment, [[wiki/concepts/source/basic-metapatterns/layers|intercommunication]], and scaling of services.
- [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] lets services operate on and communicate through [[wiki/concepts/source/foundations-of-software-architecture/shared-data|shared data]].
- [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]] are ready-to-use components that add generic functionality to the system.
- [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] encapsulates [[wiki/concepts/source/basic-metapatterns/layers|use cases]] that involve multiple services, so that the services don’t need to know about each other.



![Diagrams of Services with a proxy, Services with an orchestrator, Services with a middleware, and Services with a shared database.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Services%20-%20Further%201.png)


Each service, being a smaller *Monolith*, may evolve on its own. Most of the evolutions of [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] are applicable. The most common examples include:

- [[wiki/concepts/source/basic-metapatterns/services|*Scaled (Sharded) Service*]] with a [[wiki/concepts/source/extension-metapatterns/proxy|*Load Balancer*]] and [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Database*]] to support high load.
- [[wiki/concepts/source/basic-metapatterns/services|*Layered Service*]] to improve the code structure and decouple the deployment of parts of the service.
- [[wiki/concepts/source/basic-metapatterns/services|*Cell*]] (*Service of Services*) to involve multiple teams and technologies within a single subdomain.
- [[wiki/concepts/source/basic-metapatterns/services|*Hexagonal Service*]] to escape vendor lock-in.



![Diagrams of a scaled service, layered service, Cell, and a service that implements Hexagonal Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Monolith/Monolith%20to%20Services%20-%20Further%202.png)
