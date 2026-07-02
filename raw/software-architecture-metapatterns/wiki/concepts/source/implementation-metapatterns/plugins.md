---
title: "Plugins"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Implementation metapatterns/Plugins.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Implementation%20metapatterns/Plugins
source_license_note: "See namespace README; preserve attribution and source links."
---

# Plugins

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Implementation metapatterns/Plugins.md`.


![A diagram for Plugins Architecture, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Plugins.png)


*Overspecialize, and you breed in weakness\.* Customize the system through attachable modules\.

<ins>Known as:</ins> Plug\-In Architecture \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\], [Extension Architecture](https://www.uber.com/en-UA/blog/microservice-architecture/), \(misapplied\) Microkernel \(Architecture\) \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]], [[wiki/concepts/source/appendices/books-referenced|SAP]], [[wiki/concepts/source/appendices/books-referenced|FSA]]\], Plugin \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\], [Strategy](https://refactoring.guru/design-patterns/strategy) \[[wiki/concepts/source/appendices/books-referenced|[GoF]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\], Reflection \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\], Aspects, Hooks\.

<ins>Structure:</ins> A [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or subsystem extended with one or more modules that customize its behavior\.

<ins>Type:</ins> Implementation, extension components\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Some aspects are easy to customize | Testability is poor \(too many combinations\) |
| The customized system is relatively light\-weight | Performance is suboptimal |
| Platform\-specific optimizations are supported | Designing good SPIs for plugins is hard |
| The custom pieces may be written in a different programming language or DSL |  |

<ins>References:</ins> \[[wiki/concepts/source/appendices/books-referenced|[SAP]]\] and \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] [[wiki/concepts/source/analytics/ambiguous-patterns|mistakenly]] call this pattern *Microkernel* and dedicate chapters to it\.

Most systems require some extent of customizability that may range from the basic codec selection by a video player to the screens full of tools and wizards unlocked once you upgrade your subscription plan\. This is achieved by keeping the *core* functionality separate from its extensions, which are developed by either your team or external enthusiasts to fine\-tune the behavior of the system\. The cost of flexibility is paid in complexity of design – the need to predict which aspects should be customizable and which *SPI*s \([*Service Provider Interfaces*](https://en.wikipedia.org/wiki/Service_provider_interface)\) are good for both known and still unknown uses by the extensions\. If the communication between the core and *plugins* is heavy, performance may suffer\.

### Performance

Using plugins usually degrades performance\. The effect may be negligible for in\-process plugins \(such as strategies or codecs\) but it becomes noticeable if inter\-process communication or networking is involved\.

The only case for a plugin to improve performance of a system that I can think of is when a part of the client’s business logic moves to a lower layer of a system or to another service forming an [*Ambassador Plugin*](#ambassador-plugin-logic-extension)\. That is similar to the [[wiki/concepts/source/basic-metapatterns/layers|strategy injection optimization for *Layers*]]\. Real\-world examples include:

- The use of *stored procedures* in databases,
- HFT rules and price tables [uploaded](https://www.youtube.com/watch?v=sX2nF1fW7kI) to a network card or FPGA,
- Customization of a supplier [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]] for varying needs of its client *Cells* in [*Domain\-Oriented Microservice Architecture*](<Service-Oriented Architecture (SOA)#domain-oriented-microservice-architecture-doma>)\.



![Business logic injection in Layers and Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Plugins-injection.png)


### Dependencies

Each *plugin* depends on the *core*’s *API* \(for *Addons*\) or *SPI* \(for *Plugins*\) for the functionality it extends\. That makes the APIs and SPIs nearly impossible to modify, only to extend, as there tend to be many plugins in the field, some of them out of active development, that rely on any given method of the already published interfaces\.


![Each plugin depends on an interface of the core.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Plugins.png)


### Applicability

*Plugins* are <ins>good</ins> for:

- *Product lines\.* The shared *core* functionality and some *plugins* are reused by many flavors of the product\. Per\-client customizations are largely built using existing plugins\.
- *Frameworks\.* A framework is a functional core to be customized by its users\. When shipped with a set of plugins it becomes ready\-to\-use\.
- *Platform\-specific customizations\. Plugins* allow both for native look and feel \(e\.g\. desktop vs mobile vs console\) and for the use of platform\-specific hardware\.


*Plugins* <ins>do not perform well</ins> in:

- *Highly optimized applications\.* Any generic code tends to be inefficient\. A generic *SPI* that serves a family of plugins is unlikely to be optimized for the use by any one of them\.


### Relations


![A monolith with plugins; layers with plugins; a Cell with a plugin.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Plugins.png)


*Plugins*:

- Implement [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]]\.
- Extend [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], or [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]] with one or two layers of services\.


## Variants

*Plugins* are omnipresent if we take [*Strategy*](https://refactoring.guru/design-patterns/strategy) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] for a kind of plugin\. They vary:

### By the direction of communication

A plugin may:

- Provide input to the core \(as UI screens and [CLI](https://en.wikipedia.org/wiki/Command-line_interface) connections do\)\.
- Receive output from the core \(e\.g\. collection of statistics\)\.
- Participate in both input and output \(like health check instrumentation\)\.
- Take the role of [[wiki/concepts/source/extension-metapatterns/orchestrator|*Controller*]] \(*Orchestrator*\) – the plugin processes events from the core and decides on the core’s further behavior\.
- Be a data processor – the plugin implements a part of a [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|data processing]] algorithm which is run by the core\. This enables platform\-specific optimizations, like SIMD or DSP\.


### By linkage

Plugins may be *built in* or selected dynamically:

- Every *flavor* \(e\.g\. free, lite, pro, premium\) of a product line incorporates a single set of plugins \(configuration\) built into the application\. Web services often use this kind of customization for [[wiki/concepts/source/basic-metapatterns/shards|*Multitenancy*]]\.
- Other systems choose and initiate their plugins on startup according to their configuration files or licenses\.
- Still others support attaching and detaching plugins dynamically at runtime\.


### By granularity

Plugins come in different sizes:

- Small functions or classes are built into the core\. They seem to implement the [*Strategy*](https://refactoring.guru/design-patterns/strategy) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] / *Plugins* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\] design patterns\.
- [*Aspects*](https://en.wikipedia.org/wiki/Aspect_(computer_programming)), such as logging and memory management, pervade a system and are accessed from many places in its code\. *Reflection* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\] probably belongs there\.
- Modules are plugged in as separate system components\. This kind of *Plugins* matches the topic of this book and is further developed by [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] and [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]]\.


### By the number of instances

A plugin may be:

- *Mandatory* \(1 instance\), like a piece of algorithm used by the core for a calculation\.
- *Optional* \(0 or 1 instance\), like a smart coloring scheme for a text editor\.
- *Subscriptional* \(0 or more instances\), like log output which may go to a console, the system log, a log file, socket, or to all of them simultaneously\.


### By execution mode

Plugins may be:

- Linked as a binary code called from within the core\.
- Written in a [*domain\-specific language*](https://en.wikipedia.org/wiki/Domain-specific_language) \(*DSL*\) and [[wiki/concepts/source/implementation-metapatterns/microkernel|interpreted]] by the core\.
- Remote, available as a stand\-alone web service or even hardware component which the core needs to access through a dedicated protocol\.


## Examples

*Plugins* can take different roles and places in the system\. Though their classification and naming has never been well established, we can discern the following kinds of *plugins*, which are non\-exclusive, meaning that a single application may support some or all of them at once:

- A [true *Plugin*](#true-plugin-or-plug-in) provides custom low\-level functionality\.
- An [*Ambassador Plugin*](#ambassador-plugin-logic-extension) injects a part of a given service’s business logic into another service\.
- An [*Extension*](#extension) modifies its target’s workflow \(use cases\)\.
- An [*Addin*](#addin-or-add-in) is a deeply integrated optional part of a system’s core logic\.
- An [*Addon*](#inexact-addon-or-add-on) is an addition that wraps an application to improve user experience\.


### True Plugin \(or Plug\-in\)


![Several low-level plugins are called by a use case running in a system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Plugins.png)


A true *Plugin* is registered with and called by the system’s *core* to provide \(as an algorithm\) or extend \(as a custom step\) a specific low\-level functionality\. It is usually made by a third party\.

Customizable software often exposes multiple interfaces for different kinds of *Plugins*, some of which are *optional* \(0 or 1 instance\) or *subscriptional* \(multiple instances\) as explained [earlier](#by-the-number-of-instances)\.

Examples: codecs in a video player, country\-specific tax calculation rules in accounting software, or filters in a traffic sniffer\.

### [[wiki/concepts/source/extension-metapatterns/proxy|Ambassador]] Plugin, Logic Extension


![An ambassador plugin is a part of one service hosted inside another service. When called, it may consult its origin service or make independent decisions.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Ambassador%20Plugin.png)


A service may accept *Plugins* that [act on behalf of peer services](https://www.uber.com/en-UA/blog/microservice-architecture/) \(are are their [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassadors*]]\) and are implemented by their teams\. That [[wiki/concepts/source/analytics/dependency-inversion-in-architectural-patterns|inverts dependencies]]: whoever wants to affect the behavior of your service uses your SPI to inject their code into your service which apart from that remains self\-contained\. As a result, whatever used to be a system\-wide workflow becomes limited to a single subdomain\.

Though an *Ambassador Plugin* \(aka Uber’s [*Logic Extension*](https://www.uber.com/en-UA/blog/microservice-architecture/)\) may call the service on whose behalf it acts, it is preferable performance\-wise for it to make independent decisions without cross\-service calls \(it works as a smart [[wiki/concepts/source/extension-metapatterns/proxy|*Cache*]] that provides decisions instead of data\)\. For data\-driven decisions the *Ambassador* may need to opaquely receive and store data \([*Data Extension*](https://www.uber.com/en-UA/blog/microservice-architecture/)\) in its host’s data store\.

*Ambassador Plugins* are widely used in Uber’s [*Domain\-Oriented Microservice Architecture*](<Service-Oriented Architecture (SOA)#domain-oriented-microservice-architecture-doma>) to decouple its [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cells*]]\.

### Extension


![An extension is called as a high-level part of a system's use case.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Extension.png)


An *Extension* changes use cases by modifying the application’s business logic, but it is still called by the application’s *core*\. An *Extension* may install a group of low\-level *Plugins* which add to the system’s low\-level functionality whatever tools the *Extension* relies on\.

Examples: IDE customization\.

### Addin \(or Add\-in\)


![An addin is hosted inside a system and implements a part of its control flow.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Addin.png)


An *Add\-in* is deeply integrated with the *core* – the system has been originally designed to provide it thorough access to its internals\. It comes from the system’s creators or external teams that commit to the system *core*’s codebase\.

Examples: complex extensions for web browsers or static website generators\.

### \(inexact\) Addon \(or Add\-on\)


![An addon is a layer between a system and its client. It translates a single client request into multiple calls to the underlying system.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Addon.png)


Though any of the variants of *Plugins* described above may sometimes be called an *addon*, there is a kind of system extension which perfectly matches the meaning of the word\.

A true *Addon* is built on top of the system’s *API* \(not a dedicated *SPI* as with other kinds of *Plugins*\) and calls into the system from outside – it is a kind of an external [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] or even [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] for the system\.

Examples: applications that provide [[wiki/concepts/source/extension-metapatterns/proxy|user interface]] for command\-line tools such as git\.

## Summary

*Plugins* allow for customization of a component’s behavior at the cost of increased complexity, poor testability, and somewhat reduced performance\.

| \<\< [[wiki/concepts/source/implementation-metapatterns/implementation-metapatterns|Implementation metapatterns]] | ^ [[wiki/concepts/source/implementation-metapatterns/implementation-metapatterns|Implementation metapatterns]] ^ | [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Hexagonal Architecture]] \>\> |
| --- | --- | --- |
