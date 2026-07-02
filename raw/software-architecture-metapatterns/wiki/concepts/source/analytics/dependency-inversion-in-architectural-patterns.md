---
title: "Dependency inversion in architectural patterns"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Analytics/Comparison of architectural patterns/Dependency inversion in architectural patterns.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Analytics/Comparison%20of%20architectural%20patterns/Dependency%20inversion%20in%20architectural%20patterns
source_license_note: "See namespace README; preserve attribution and source links."
---

# Dependency inversion in architectural patterns

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Analytics/Comparison of architectural patterns/Dependency inversion in architectural patterns.md`.

I am no fan of [*SOLID*](https://en.wikipedia.org/wiki/SOLID) – to the extent of being unable to remember what those five letters mean – thus I was really surprised to notice that one of its principles, namely [*dependency inversion*](https://en.wikipedia.org/wiki/Dependency_inversion_principle), is quite common with architectural patterns, which means that it is much more generic than *OOP* which it is promoted for.

Let’s see how dependency inversion is used at the system level.

## Patterns that build around it


![Plugins depend on the core's SPIs. There are multiple versions of plugins. Adapters of Hexagonal Architecture depend on both the core's SPIs and APIs of the adapted components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/DI-1.png)


Both [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] and the derived [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] rely on dependency inversion for the same reason – to protect the *core*, which contains the bulk of the code, from variability in the external components it uses. The *core* operates interfaces ([*SPI*](https://en.wikipedia.org/wiki/Service_provider_interface)s) which it defines so that it may not care exactly what  is behind the interface.

It is the nature of the polymorphic components that distinguishes those patterns:

- [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] allow for small pieces of code, typically contributed by outside developers, to provide customizable parts of the system’s algorithms and decision making. Oftentimes the core team has no idea of how many diverse plugins will be written for their product.
- [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] is about breaking dependency of the core on external libraries or services by employing [[wiki/concepts/source/extension-metapatterns/proxy|*adapters*]]. Each adapter depends both on the core’s SPI and on the API of the component which it adapts. As interfaces and contracts vary among vendors and even versions of software, which we want to be interchangeable, we need adapters to wrap the external components to make them look identical to our core. Besides that, [*stub* or *mock*](https://stackoverflow.com/questions/3459287/whats-the-difference-between-a-mock-stub) adapters help develop and test the core in isolation.


## Patterns that often rely on it


![In an operating system, device drivers depend on the kernel's SPIs. In a hierarchy, child nodes depend on their parent's SPI. Cell-Based Architecture uses adapters to break dependencies between Cells.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/DI-2.png)


A few more patterns tend to use this approach to earn its benefits, even though dependency inversion is not among their integral features:

- [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]], yet another metapattern derived from [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]], distributes resources of *providers* among *consumers*. Polymorphism is crucial for some of its variants, including [[wiki/concepts/source/implementation-metapatterns/microkernel|*Operating System*]], but may rarely benefit others, such as [[wiki/concepts/source/implementation-metapatterns/microkernel|*Software Framework*]].
- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top-Down Hierarchy*]] distributes responsibility over a tree of components. If the nodes of the tree are polymorphic, they are easier to operate, and there is dependency inversion. However, in practice, a parent node may often be so strongly coupled to the types of its children that polymorphism becomes impractical.
- In another kind of [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]], namely [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell-Based Architecture*]] (aka *Services of Services*), each [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]] [may employ](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) a [[wiki/concepts/source/extension-metapatterns/proxy|*Cell Gateway*]] and outbound [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] or [[wiki/concepts/source/implementation-metapatterns/plugins|*Ambassador Plugins*]] to isolate its business logic from the environment – just like its parent [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] does for a monolithic core.


## Patterns that may use it


![Standard APIs are used between frontend and backend, and backend and database. CQRS views and adapters protect a service from dependencies on other services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Conclusion/DI-3.png)


Finally, two basic architectures, [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] and [[wiki/concepts/source/basic-metapatterns/services|*Services*]], may resort to something similar to dependency inversion to decouple their constituents:

- We often see a higher layer to depend on, and a lower layer to implement a standardized interface, like POSIX or SQL, to achieve *interoperability* with other implementations (which is yet another wording for polymorphism).
- A service may follow the concept of [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]] by using an [[wiki/concepts/source/basic-metapatterns/services|*Anti-Corruption Layer*]] or [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*CQRS Views*]] as [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] that protect it from changes in other system components.


## Summary

Many architectural patterns employ dependency inversion by adding:

- an *interface* to enable polymorphism of their lower-level components or
- [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] to protect a component from changes in its dependencies.


These two approaches apply in different circumstances:

- If you can enforce your rules of the game on the suppliers of the external components, you merely *define an SPI*, and expect the suppliers to implement and obey it.
- If the suppliers are independent and it is your side that adapts to their rules, you should *add Adapters* to translate between your lovely SPI and their whimsical APIs.
