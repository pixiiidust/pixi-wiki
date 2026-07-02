---
title: "Microkernel"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Implementation metapatterns/Microkernel.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Implementation%20metapatterns/Microkernel
source_license_note: "See namespace README; preserve attribution and source links."
---

# Microkernel

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Implementation metapatterns/Microkernel.md`.


![A diagram for Microkernel, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Microkernel.png)


*Communism.* Share resources among consumers.

<ins>Known as:</ins> Microkernel (Architecture) \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]] but [[wiki/concepts/source/analytics/ambiguous-patterns|not]] [[wiki/concepts/source/appendices/books-referenced|SAP]] and [[wiki/concepts/source/appendices/books-referenced|FSA]]\].

<ins>Structure:</ins> A layer of [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]] over a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] over a layer of [[wiki/concepts/source/basic-metapatterns/services|*Services*]].

<ins>Type:</ins> System topology, implementation.

| *Benefits* | *Drawbacks* |
| --- | --- |
| The system’s complexity is evenly distributed among the components | The API and SPIs are very hard to change |
| The resource providers are easy to replace | Performance is suboptimal |
| The components can have independent qualities | Latency is often unpredictable |
| A resource provider can be implemented and tested in isolation |  |
| Each application is sandboxed by the microkernel |  |
| The system is platform-independent |  |

<ins>References:</ins> the Microkernel pattern in \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\].

While vanilla [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] keep the business logic in their monolithic *core* components, *Microkernel* treats the core as a thin [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] (called *microkernel*) that connects user-facing applications (*external services*) to resource providers (*internal services*). The *resource* in question can be anything ranging from CPU time or RAM to business functions. The external services communicate with the microkernel through its *API* while the internal services implement the microkernel's *service provider interfaces* (*SPIs*) (usually there is one kind of internal service and an SPI per resource type).

On one hand, the pattern is very specific and feels esoteric. On the other – it is indispensable in many domains, with many more real-life occurrences than would be expected. *Microkernel* finds its place where there are a variety of applications that need to use multiple shared resources, with each resource being independent of others and requiring complex management.

### Performance

The *microkernel*, being an extra layer of indirection, degrades performance. The actual extent varies from a few percent for *OSes* and *virtualizers* to an order of magnitude for *scripts*. There is also a more grievous aspect of performance degradation, namely that latency becomes unpredictable as soon as the system runs short of one of the shared resources: memory, disk space, CPU time, or even storage for deleted objects. That is why [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|real-time systems]] rely on extremely minimalistic [real-time OS](https://en.wikipedia.org/wiki/Real-time_operating_system)es or even run on bare metal.

It is common to see system components communicate directly via shared memory or sockets bypassing the *microkernel* to alleviate the performance penalty which it introduces.

### Dependencies

The *applications* depend on the *API* of the *microkernel* while the *providers* depend on its *SPIs*. On one hand, that isolates the applications and providers from each other, letting them develop independently. On the other hand, the microkernel’s API and SPIs should be very stable to support older versions of the components which the microkernel integrates.


![Applications depend on the API of the microkernel. Providers depend on its SPIs.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Microkernel.png)


### Applicability

*Microkernel* is <ins>applicable</ins> in:

- *Systems programming.* You manage system resources and services which will be used by untrusted client applications. Hide the real resources behind a trusted proxy layer. Be ready to change the hardware platform without affecting the existing client code.
- *Frameworks that integrate several subdomains.* The microkernel component coordinates multiple specialized libraries. Its API is a [*Facade*](https://refactoring.guru/design-patterns/facade) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] for the functionality which it organizes.
- *Scripting or* [*DSL*](https://en.wikipedia.org/wiki/Domain-specific_language)*s.* The microkernel is an [*Interpreter*](#interpreter-script-domain-specific-language-dsl) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] which lets your clients’ code manage the underlying system.


*Microkernel* <ins>does not fit</ins>:

- *Coupled domains.* Any degree of coupling between the resource providers complicates the microkernel and its SPIs, and is likely to degrade performance, which, however, may be salvaged by introducing direct communication channels between the providers.


### Relations


![Microkernel as a middleware and as an orchestrator; applications of Microkernel Architecture as Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Microkernel.png)


*Microkernel*:

- Is a specialization of [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]].
- Is related to [*Backends for Frontends*](<Backends for Frontends (BFF)>), which is a layer of [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrators*]] over a layer of [[wiki/concepts/source/basic-metapatterns/services|*Services*]]; *Microkernel* adds a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] in between.
- Is a kind of 2-layered [*SOA*](<Service-Oriented Architecture (SOA)#enterprise-soa>) with an [[wiki/concepts/source/extension-metapatterns/orchestrator|*ESB*]].
- The *microkernel* layer serves as (implements) a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] for the upper (*external*) [[wiki/concepts/source/basic-metapatterns/services|*Services*]] and often makes an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] for the lower (*internal*) *Services*.
- May be implemented by a [[wiki/concepts/source/implementation-metapatterns/mesh|*Mesh*]].


## Examples

*Microkernel* can appear in many forms:

- An [*Operating System*](#operating-system) shares hardware resources among many applications.
- A [*Software Framework*](#software-framework-pluggable-component-framework) provides a unified interface to access several libraries.
- A [*Virtualizer*](#virtualizer-hypervisor-container-orchestrator-distributed-runtime) maintains a generic interface to run guest software on any host OS and hardware.
- An [*Interpreter*](#interpreter-script-domain-specific-language-dsl) executes client scripts in a sandbox.
- A [*Configurator*](#configurator-configuration-file) sets up a system in accordance with a configuration file.
- A [*Saga Engine*](#saga-engine) runs distributed transactions.
- An [*AUTOSAR Classic Platform*](#autosar-classic-platform) provides automotive applications with access to any chip on board.


### Operating System


![Each application communicates with its runtime interfacing the shared operating system kernel which communicates with device drivers that adapt hardware components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/OS.png)


The original inspiration for *Microkernel*, namely *operating systems*, provides an almost perfect example of the pattern, even though their kernels are not that “micro-” (unless you are running [MINIX](https://en.wikipedia.org/wiki/Minix_3#Architecture) or [QNX](https://en.wikipedia.org/wiki/QNX#Technology)). [[wiki/concepts/source/basic-metapatterns/services|Device *drivers*]] (*internal services*) encapsulate available hardware resources (see [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Pedestal*]]) and make them accessible to user-space *applications* (*external services*) via an OS *kernel*. *Drivers* for a given kind of subsystem (e.g. network adapter or disk drive) are polymorphic towards the kernel and match the hardware installed.

### Software Framework, Pluggable Component Framework


![A framework is a facade between a user application and several lower-level components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Framework.png)


In a *Software Framework* or *Pluggable Component Framework* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] the *microkernel* (*abstract core* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]) is a [[wiki/concepts/source/extension-metapatterns/orchestrator|*Facade*]] \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] that integrates a set of libraries and exposes a user-friendly high-level interface. [PAM](https://docs.oracle.com/cd/E23824_01/html/819-2145/pam-01.html) looks like a reasonably good example.

### Virtualizer, Hypervisor, Container Orchestrator, [[wiki/concepts/source/basic-metapatterns/services|Distributed Runtime]]


![A virtualizer stands between user applications and several instances of an operating system each running on a separate computer.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Virtualizer.png)


*Hypervisors* (Xen), PaaS and [FaaS](https://shivangsnewsletter.com/p/why-doesnt-cloudflare-use-containers), *container orchestrators* (Kubernetes) \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\], and distributed *actor frameworks* (Akka, Erlang/Elixir/OTP) use resources of the underlying computer(s) to run guest applications. A hypervisor virtualizes the resources of a single computer while a distributed runtime manages those of multiple servers – in the last case there are several instances of the same kind of an *internal server* which abstracts a host system.

### Interpreter, Script, Domain-Specific Language (DSL)


![Each script runs over its instance of an interprester. All the interpreters share a set of libraries.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Interpreter.png)


User-provided *scripts* are run by an *Interpreter* \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] which also allows them to access a set of installed libraries. The *Interpreter* is a microkernel, and the syntax of the script or [*DSL*](https://en.wikipedia.org/wiki/Domain-specific_language) which it interprets is the microkernel’s API.

### Configurator, Configuration File


![A configurator runs at a system's startup, reads a configuration file, and sets up a system of services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Config%20file.png)


*Configuration files* may be regarded as short-lived [*scripts*](#interpreter-script-domain-specific-language-dsl) that configure the underlying modules at the start of the system. The parser of the configuration file is a transient *microkernel*.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|Saga]] Engine


![A saga engine calls several services while executing multiple short-lived sagas.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Saga%20engine.png)


A [[wiki/concepts/source/extension-metapatterns/orchestrator|*Saga*]] \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] orchestrates distributed transactions. It may be written in a [*DSL*](https://en.wikipedia.org/wiki/Domain-specific_language) which requires a compiler or [interpreter](#interpreter-script-domain-specific-language-dsl), which is a *microkernel*, to execute.

### AUTOSAR Classic Platform


![AUTOSAR Classic defines three segmented layers: applications, runtime environment with a shared Virtual Functional Bus, and basic software with generic and hardware-specific services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/AUTOSAR%20classic.png)


The [notorious](https://www.reddit.com/r/embedded/comments/leq366/comment/gmiq6d0/) [automotive standard](https://www.autosar.org/fileadmin/standards/R20-11/CP/AUTOSAR_EXP_VFB.pdf), though inspired by [*SOA*](<Service-Oriented Architecture (SOA)#misapplied-automotive-soa>), is structured as a distributed / virtualized *Microkernel*. The application layer comprises a network of *software components* spread out over hundreds of chips which are, for some secret reason, called *electronic control units* (*ECU*s). Both communication paths between the software components and much of the system’s code are static (auto-generated at compilation time). A software component may access hardware of its ECU via standard interfaces.

The *microkernel* shows up as *Virtual Functional Bus* (*VFB*) which, as a *distributed* [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]], provides communication between the *applications* by virtualizing multiple *Runtime Environments* (*RTEs*) – the local [system interfaces](https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_EXP_LayeredSoftwareArchitecture.pdf).

## Summary

*Microkernel* is a ubiquitous approach to sharing resources among consumers, where both resource providers and consumers may be written by external companies.
