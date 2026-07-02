---
title: "Hexagonal Architecture"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Implementation metapatterns/Hexagonal Architecture.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Implementation%20metapatterns/Hexagonal%20Architecture
source_license_note: "See namespace README; preserve attribution and source links."
---

# Hexagonal Architecture

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Implementation metapatterns/Hexagonal Architecture.md`.


![A diagram for Hexagonal Architecture, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Hexagonal%20Architecture.png)


*Trust no one\.* Protect your code from external dependencies\.

<ins>Known as:</ins> Hexagonal Architecture, or originally as Ports and Adapters\.

<ins>Structure:</ins> Monolithic or subdivided business logic extended with a set of \(adapter, component\) pairs that encapsulate external dependencies\.

<ins>Type:</ins> Implementation\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Isolates business logic from external dependencies which thus become expendable | Suboptimal performance |
| The programmers of business logic don’t need to learn any external technologies | The vendor\-independent interfaces must be designed before the start of development |
| Facilitates the use of stubs/mocks for testing and development |  |
| Allows for qualities to vary between the external components and the business logic |  |

<ins>References:</ins> [Herberto Graça’s chronicles](https://herbertograca.com/2017/07/03/the-software-architecture-chronicles/) is the main overview of patterns in this chapter\. For *Hexagonal Architecture* there is  [the original article](https://alistair.cockburn.us/hexagonal-architecture/) and a brief summary of its layered variant in \[[wiki/concepts/source/appendices/books-referenced|[LDDD]]\]\. Most of the *Separated Presentation* patterns are featured on Wikipedia and there are collections of them from [Martin Fowler](https://martinfowler.com/eaaDev/uiArchs.html), [Anthony Ferrara](https://blog.ircmaxell.com/2014/11/alternatives-to-mvc.html), and [Derek Greer](https://lostechies.com/derekgreer/2007/08/25/interactive-application-architecture/)\. *Cells* originate with [WSO2](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) and [Uber](https://www.uber.com/en-UA/blog/microservice-architecture/)\.

*Hexagonal Architecture* \(see the [original article](https://alistair.cockburn.us/hexagonal-architecture/) for the explanation of its name\) is a variation of [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] that aims for self\-sufficiency of a system’s business logic *core*\. It hides external components such as libraries, services, or data stores, which the business logic would normally depend upon, behind [[wiki/concepts/source/extension-metapatterns/proxy|*adapters*]] \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\] that translate from the external component’s interface to an interface \([*API*](#upper-half-separated-presentation-open-host-service) or [*SPI*](#lower-half-pedestal-abstraction-layer-anticorruption-layer)\) defined in terms of the business logic\. This indirection not only makes the bulk of the system’s code easy to port, test, and run in isolation, but also allows for replacing external components and for changing the interfaces or even the internal structure of the business logic late in the [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|project’s life cycle]]\.

Though various kinds of *Hexagonal Architecture* are de facto industry standards, they are not without drawbacks: the [extra layer of indirection](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering) requires careful planning with insights into how the system will evolve and which kinds of external components will need to be integrated or which platforms the system will need to run on\. It also adds boilerplate code and prevents aggressive performance optimization that would rely on peculiarities of the currently integrated external component\.

### Performance

*Hexagonal Architecture* is a strange beast performance\-wise\. The generic interfaces between the *core* and *adapters* stand in the way of whole\-system optimization and may add a context switch\. Still, at the same time, each *adapter* concentrates all the vendor\-specific code for its external dependency, which makes the *adapter* a perfect single place for aggressive optimization by an expert or consultant who is proficient with the adapted third\-party software but does not have time to learn the details of your business logic\. Thus, some opportunities for optimization are lost while others emerge\.

Occasionally, the system may benefit from direct communication between the *adapters*\. However, that requires several of them to be compatible or polymorphic, in which case your *Hexagonal Architecture* may in fact be a kind of a shallow [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]\. Examples include a service which uses several databases which are kept in sync through [*Change Data Capture*](https://www.dremio.com/wiki/change-data-capture/) \(*CDC*\) or a telephony gateway that interconnects various kinds of voice devices\.


![A data stream between adapters of Hexagonal Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Performance/Hexagonal%20Architecture.png)


### Dependencies

Each [[wiki/concepts/source/extension-metapatterns/proxy|*adapter*]] breaks the dependency between the *core* that contains business logic and an adapted component\. This makes all the system’s components mutually independent – and easily interchangeable and evolvable – except for the *adapters* themselves, which are small enough to be rewritten as need arises\.


![In Hexagonal Architecture each adapter depends on the core and the component or protocol it adapts.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Dependencies/Hexagonal%20Architecture.png)


Still, there is a hidden pitfall of designing a [*leaky abstraction*](https://en.wikipedia.org/wiki/Leaky_abstraction) – an interface that looks generic but whose contract matches that of the component it encapsulates, making it much harder than expected to change the external component’s vendor\.

### Applicability

*Hexagonal Architecture* <ins>benefits</ins>:

- *Medium\-sized or larger components\.* The programmers don’t need to learn details of external technologies and may concentrate on the business logic instead\. The code of the *core* becomes smaller as all the details of managing the external components are moved into their *adapters*\.
- *Cross\-platform development\.* The core is naturally cross\-platform as it does not depend on any \(platform\-specific\) libraries or frameworks\.
- *Long\-lived products*\. Technologies come and go, your product remains\. Always be ready to change the technologies it uses\.
- *Unfamiliar domain\.* You don’t know how much load you’ll need your database to support\. You don’t know if the library which you have selected is stable enough for your needs\. Be prepared to replace vendors even after the public release of your product\.
- *Automated testing\.* [Stubs and mocks](https://stackoverflow.com/questions/3459287/whats-the-difference-between-a-mock-stub) are great for reducing load on test servers\. And stubs for the [SPI](#lower-half-pedestal-abstraction-layer-anticorruption-layer)s which you wrote yourself are as easy as a pie\.
- *Zero bug tolerance\.* SPIs allow for event replay\. If your business logic is deterministic, you can [reproduce your user’s bugs in your office](http://ithare.com/chapter-vc-modular-architecture-client-side-on-debugging-distributed-systems-deterministic-logic-and-finite-state-machines/)\.


*Hexagonal Architecture* <ins>is not good</ins> for:

- *Small components\.* If there is little business logic, there is not much to protect, while the overhead of defining [SPI](#lower-half-pedestal-abstraction-layer-anticorruption-layer)s and writing *adapters* for them is high compared to the total development time\.
- *Write\-and\-forget projects\.* You don’t want to waste your time on long\-term survivability of your code\.
- *Quick start*\. You need to show the results right now\. No time for good architecture\.
- *Low latency*\. The *adapters* slow down communication\. This is somewhat alleviated by creating [direct communication channels](#performance) between the *adapters* to bypass the *core*\.


### Relations


![Diagrams of Hexagonal Architecture with a monolithic core, with a layered core, and Cell.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Hexagonal%20Architecture.png)


*Hexagonal Architecture*:

- Is a kind of [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]]\.
- May be a shallow [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]]\.
- Implements [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]\.
- Extends [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]], [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]], or [[wiki/concepts/source/basic-metapatterns/services|*Services*]] with one or two layers of [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]]\.
- The [*MVC* family of patterns](#model-view-controller-mvc-action-domain-responder-adr-resource-method-representation-rmr-model-2-mvc2-game-development-engine) is also [[wiki/concepts/source/analytics/pipelines-in-architectural-patterns|derived]] from [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.


## Variants by placement of adapters

There is a variation in a distributed or asynchronous *Hexagonal Architecture* regarding the deployment of [[wiki/concepts/source/extension-metapatterns/proxy|*adapters*]], which may reside with the components they adapt or stay adjacent to the *core*:

### Adapters on the external component side


![Adapters co-located with external components translate a single message from the core into multiple calls to the adapted components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Hexagonal%20-%20Adapters%20with%20Components.png)


If your team owns the component adapted, the *adapter* may be placed next to it\. That usually makes sense because a single domain message \(designed in the terms of your business logic\) tends to unroll into a series of calls to an external component\. The fewer messages you send, the faster your system is\.

### Adapters on the core side


![Adapters for external services and a shared database are co-located with the core.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Hexagonal%20-%20Adapters%20with%20the%20Core.png)


Sometimes you need to adapt an external service which you don’t control\. In that case the only real option is to place its *adapter* together with your *core* logic\. For a monolithic *core* \([*Ports and Adapters*](#ports-and-adapters-hexagonal-architecture)\) the *adapters* may run in the core’s process as ordinary modules\. A distributed *core* \([*Cell*](#cell-cluster-domain)\) requires the *adapters* to be stand\-alone components, which however can be co\-located and co\-deployed with the *core* as [[wiki/concepts/source/extension-metapatterns/proxy|*Sidecars*]]\.

## Variants by encapsulation

In most cases a component or subsystem is involved in two kinds of communication:

- Input/output from clients, users, or network devices which we [[wiki/concepts/source/introduction/metapatterns|draw on the upper side of diagrams]]\. These events initiate the application’s use cases thus they are called [*primary* or *driving*](https://alistair.cockburn.us/hexagonal-architecture)\.
- The activities and calls initiated by the component itself while executing a use case\. They usually target the infrastructure or external services, are called [*secondary* or *driven*](https://alistair.cockburn.us/hexagonal-architecture), and are drawn on the lower side\.



![The system's core is isolated with adapters for the following communication: data stream, REST, and SSH inputs; database and library access; publish/subscribe output stream.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Hexagonal%20-%20Driving%20and%20Driven.png)


> Client output *adapters*, such as the *view* in [*MVC*](#model-view-controller-mvc-action-domain-responder-adr-resource-method-representation-rmr-model-2-mvc2-game-development-engine) or *responder* in [*ADR*](#model-view-controller-mvc-action-domain-responder-adr-resource-method-representation-rmr-model-2-mvc2-game-development-engine), are treated as *primary* even though they are called by the business logic\. The reason is that such an *adapter* is a part of the client feedback loop which *drives* the system’s behavior\.

We can protect a component from its environment by inserting *adapters* into its *primary*, *secondary*, or both communication pathways:

### Upper half: [[wiki/concepts/source/extension-metapatterns/proxy|Separated Presentation]], [[wiki/concepts/source/extension-metapatterns/proxy|Open Host Service]]


![A component provides an API which is called by a GUI adapter for a system's user, a REST adapter for a web application, and a gRPC adapter for a software client.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Hexagonal%20-%20Driving.png)


Isolation on the input \([*primary*, *driving*](https://alistair.cockburn.us/hexagonal-architecture)\) side is achieved by designing an *Application Programming Interface* \(*API*\) that provides access to your component’s use cases which your software exists to implement and writing *adapters* that translate your *API* into something convenient for every kind of communication used by your clients\. For example, you may need a desktop GUI, mobile GUI, CLI, web application \(REST\), and customer \(JSON or gRPC\) *adapters* all of which are built on top of your component’s API\.

Input side isolation allows for your system to be used in different environments and roles and enables automated testing of its business logic without hard\-to\-support GUI tests\.

> Though it may seem that a system’s business logic cannot depend on its [[wiki/concepts/source/basic-metapatterns/layers|*interface*]] \(GUI or web API\) because it is the *interface* that calls the business logic, in fact the business logic must prepare the data it returns in the format declared by the interface \(for a web protocol\) or output the data queried to a widget \(for a GUI\)\. Therefore, making the business logic independent requires an [[wiki/concepts/source/extension-metapatterns/proxy|*Adapter*]] to translate between the domain terms native to the business logic and the data format used by a web protocol or GUI framework which calls the business logic\.

[*Separated Presentation*](https://martinfowler.com/eaaDev/SeparatedPresentation.html) protects business logic \(*model*\) from a dependency on the [[wiki/concepts/source/extension-metapatterns/proxy|*Presentation Layer*]] \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] \(interactions with the system’s user via a window, command line, or web page\)\. There is a [great variety](https://blog.ircmaxell.com/2014/11/alternatives-to-mvc.html) of such patterns, commonly known as *Model\-View\-Controller* \(*MVC*\) alternatives, which make three structurally distinct groups:

- Bidirectional flow – the *view* \(user\-facing component\) both receives input and produces output, and there is often an extra *adapter* between it and the main system, resulting in [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]]\. These patterns make the [*Model\-View\-Presenter* \(*MVP*\) family](#model-view-presenter-mvp-model-view-adapter-mva-model-view-viewmodel-mvvm-model-1-mvc1-document-view)\.
- Unidirectional flow – the *controller* receives input while the *view* only produces output, [[wiki/concepts/source/analytics/pipelines-in-architectural-patterns|forming]] a kind of [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\. Such patterns are [associated with *Model\-View\-Controller* \(*MVC*\)](#model-view-controller-mvc-action-domain-responder-adr-resource-method-representation-rmr-model-2-mvc2-game-development-engine)\.
- Hierarchical patterns with multiple *models*, [[wiki/concepts/source/fragmented-metapatterns/hierarchy|discussed]] in the [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Hierarchy*]] chapter\.


*Open Host Service* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] is an enterprise pattern about providing functionality for use by other components \(hence the name\) through publishing a stable interface, known as a *Published Language* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\. As the subject service should be able to change, and as its clients may differ in their needs, requiring multiple *Published Languages*, an *Open Host Service* usually involves an *adapter* for every *Published Language* it provides – just like *Separated Presentation* does for supported *UI*s\.

> As is common with patterns, there is a slight difference between what the client\-facing side comprises in *Separated Presentation* and *Open Host Service*, with the last pattern including adapters for *Publish\-Subscribe* interfaces\. Neither of these two patterns provides indirection for input streams of data or events\.

### Lower half: [[wiki/concepts/source/basic-metapatterns/services|Pedestal]], [[wiki/concepts/source/extension-metapatterns/proxy|Abstraction Layer, Anticorruption Layer]]


![The core uses adapters to call a database, a library, and an external service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Hexagonal%20-%20Driven.png)


In many cases you need to protect your component from its dependencies\. If the bulk of your code depends on a certain external service provider or component, you face a major risk, called [*vendor lock\-in*](https://en.wikipedia.org/wiki/Vendor_lock-in), of that provider going out of business, being [acquired and killed by a larger company](https://killedbygoogle.com/), or greatly increasing the price of its services\. Therefore you better define a *Service Provider Interface* \(*SPI*\) in terms of your business logic and write an *adapter* between it and the external provider’s *API*\. This way you will be able to change the external provider by merely rewriting the *adapter*\. It will also be easy to upgrade to new versions of the provider’s API\. The set of *adapters* to the services used by a component is called *Anticorruption Layer* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] because it protects the component from any external changes\.

There is a similar situation in embedded and systems programming where software faces hardware\. A hardware component is normally in production only for a few years before being replaced by a newer, and often incompatible, chip\. You have to make sure that your business logic can run on any hardware that provides the functions it needs – therefore you write hardware\-specific [[wiki/concepts/source/extension-metapatterns/proxy|*drivers*]] which adapt the target hardware’s interface to the expectations of your business logic\. The *drivers* make an [[wiki/concepts/source/extension-metapatterns/proxy|*Hardware Abstraction Layer*]] while the entire architecture is called a [*Pedestal*](#pedestal)\.

Another common case is platform independence – you may need to run your code under different operating systems or cloud orchestrators, which requires an [[wiki/concepts/source/extension-metapatterns/proxy|*OS Abstraction Layer*]] \(*OSAL*\) or a [[wiki/concepts/source/extension-metapatterns/proxy|*Platform Abstraction Layer*]] \(*PAL*\)\. And you may even use a [[wiki/concepts/source/extension-metapatterns/proxy|*Database Abstraction Layer*]] \(*DAL*\) to feel more secure\.

> Embedded software and operating systems [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|don’t run use cases]] – they react to events which come from hardware\. This fact breaks the *Hexagonal Architecture*’s model of [*driving* and *driven* adapters](#variants-by-encapsulation) – any hardware component can *drive* a part of the system’s behavior but none of them initiates use cases\.

The extra benefit of the isolation from infrastructure and external services by using [*secondary* or *driven*](https://alistair.cockburn.us/hexagonal-architecture) *adapters* is the ability to run against [*test doubles*](https://martinfowler.com/bliki/TestDouble.html) – local [*stubs* or *mocks*](https://stackoverflow.com/questions/3459287/whats-the-difference-between-a-mock-stub) that replace an external dependency, saving testing time and money\. They also allow for implementing business logic before the external services which it will use are chosen, and even replacing a service provider late in the [[wiki/concepts/source/analytics/architecture-and-product-life-cycle|project’s life cycle]]\.

> *Stubs* and *mocks* are [*test doubles*](https://martinfowler.com/bliki/TestDouble.html) – simplistic replacements for real\-world components\. They are used to run the business logic in isolation – without the need to deploy any heavyweight libraries or services which the logic may depend upon\. A *stub* supports a single usage scenario in a single test case while a *mock* is more generic – its behavior is programmed on a per test basis\.

### Full encapsulation: [Ports and Adapters](#ports-and-adapters-hexagonal-architecture)


![A system with its core fully isolated by adapters from both inputs and outputs. The core depends only on its own interfaces.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Hexagonal%20-%20Full%20Isolation.png)


Complete isolation of business logic – when both *driving* and *driven* communication is mediated by *adapters* – not only reaps the benefits of both approaches described above but also simplifies the main codebase because the entire business logic is written in its own terms, called *ubiquitous language* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\. It also lowers the cognitive complexity which its programmers face because they don’t need to learn any external technology, and [allows for event replay to reproduce bugs](http://ithare.com/chapter-vc-modular-architecture-client-side-on-debugging-distributed-systems-deterministic-logic-and-finite-state-machines/) \(*any reproducible bug is a dead bug*\) if the business logic is deterministic\.

The pattern for full isolation of business logic is known as [*Ports and Adapters*](https://herbertograca.com/2017/09/14/ports-adapters-architecture/) which is the original [*Hexagonal Architecture*](https://alistair.cockburn.us/hexagonal-architecture)\.

## Examples

Several patterns apply the principles of *Hexagonal Architecture* to different extents:

- The patterns of the [*MVP family*](#model-view-presenter-mvp-model-view-adapter-mva-model-view-viewmodel-mvvm-model-1-mvc1-document-view) add one or two layers of indirection between a GUI or web framework and the business logic\.
- Those of the [*MVC family*](#model-view-controller-mvc-action-domain-responder-adr-resource-method-representation-rmr-model-2-mvc2-game-development-engine) use separate *adapters* for input and output flows\.
- [*Pedestal*](#pedestal) wraps each hardware component with a *driver*\.
- [*Ports and Adapters*](#ports-and-adapters-hexagonal-architecture) fully isolate the system’s business logic from any dependencies\.
- There are a few [related architectures with layered *cores*](#ddd-style-hexagonal-architecture-onion-architecture-clean-architecture)\.
- [*Cell*](#cell-cluster-domain) isolates a group of services from the rest of the system\.


### Model\-View\-Presenter \(MVP\), Model\-View\-Adapter \(MVA\), Model\-View\-ViewModel \(MVVM\), Model 1 \(MVC1\), Document\-View


![The control flow of Model-View-Presenter is a loop that starts with an OS GUI, is handled by the view, passes to the presenter, then down to the model, and all the way back to the OS.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/MVP.png)


*MVP*\-style patterns pass user input and output through one or more [[wiki/concepts/source/extension-metapatterns/proxy|*Presentation Layers*]]\. Each pattern includes:

- *View* – the interface exposed to users\. In *Hexagonal Architecture*’s terms it is an *adapter* for the OS GUI framework\.
- An optional intermediate layer that translates between the *view* and *model*, beneficial for when the internal representation of the domain in the *model* diverges from the way it is presented to users by the *view*\. It is this component which differentiates the patterns, both in name and function\.
- *Model* – the whole system’s business logic and infrastructure, now independent from the method of presentation \(CLI, UI, or web\)\.


*Document\-View* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\] and [*Model 1*](https://stackoverflow.com/questions/796508/what-is-the-actual-difference-between-mvc-and-mvc-model2) \(*MVC1*\) skip the intermediate layer and connect the *view* directly to the *model* \(*document*\)\. These are the simplest [*Separated Presentation*](https://martinfowler.com/eaaDev/SeparatedPresentation.html) patterns for UI and web applications, respectively\.

In a [*Model\-View\-Presenter*](https://herbertograca.com/2017/08/17/mvc-and-its-variants/#model-view-presenter) \(*MVP*\), the *presenter* \([*Supervising Controller*](https://martinfowler.com/eaaDev/SupervisingPresenter.html)\) receives input from the *view*, interprets it as a call to one of the *model*’s methods, retrieves the call’s results, and shows them in the *view*, which is often completely dumb \([*Passive View*](https://martinfowler.com/eaaDev/PassiveScreen.html)\)\. A complex system may feature multiple *view\-presenter* pairs, one per UI screen\.

A [*Model\-View\-Adapter*](https://blog.ircmaxell.com/2014/11/alternatives-to-mvc.html#MVA-Model-View-Adapter) \(*MVA*\) is quite similar to *MVP*, but it chooses the *adapter* on a per session basis while reusing the *view*\. For example, an unauthorized user, a normal user, and an admin would access the *model* through different *adapters* which would show them only the data and actions available under their permissions\.

A [*Model\-View\-ViewModel*](https://herbertograca.com/2017/08/17/mvc-and-its-variants/#model-view-view_model) \(*MVVM*\) uses a stateful intermediary \(*ViewModel* or [*Presentation Model*](https://martinfowler.com/eaaDev/PresentationModel.html)\) which resembles a [[wiki/concepts/source/extension-metapatterns/proxy|*Response Cache*]], [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Materialized View*]], [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Reporting Database*]], or the *Read Model* of [[wiki/concepts/source/fragmented-metapatterns/layered-services|*CQRS*]] – it stores all the data shown in the *view* in a form which is convenient for the *view* to [bind to](https://en.wikipedia.org/wiki/Data_binding)\. Changes in the *view* are propagated to the *ViewModel* which translates them into requests to the underlying application \(the true *model*\)\. Changes in the *model* \(both independent and resulting from user actions\) are propagated to the *ViewModel* and, eventually, to the *view*\.

All those patterns exploit modern OS or GUI frameworks’ widgets which handle and process mouse and keyboard input, thus [removing](https://mvc.givan.se/papers/Twisting_the_Triad.pdf) the need for a separate \(input\) *controller* \(see [below](#model-view-controller-mvc-action-domain-responder-adr-resource-method-representation-rmr-model-2-mvc2-game-development-engine)\)\.


![Diagrams of MVP with a view-presenter pair for each screen, MVA with different adapters for different kinds of users, MVVM with data in ViewModel, and simple Document-View and Model 1.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/MVP%20-%20subtypes.png)


### Model\-View\-Controller \(MVC\), Action\-Domain\-Responder \(ADR\), Resource\-Method\-Representation \(RMR\), Model 2 \(MVC2\), Game Development Engine


![The control flow in Model-View-Controller starts with mouse events handled by the controller which calls the model which calls the view which updates the display.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/MVC.png)


When your presentation’s input and output are of different natures \(raw mouse movement vs 3D graphics in UI, HTTP requests vs HTML pages in websites\), it makes sense to separate the [[wiki/concepts/source/extension-metapatterns/proxy|*Presentation Layer*]] into dedicated components for input and output\.

*Model\-View\-Controller* \(*MVC*\) \[[wiki/concepts/source/appendices/books-referenced|[POSA1]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\] allows for cross\-platform development of hand\-crafted UI applications \(which was necessary before universal UI frameworks emerged\) by abstracting the system’s *model* \(its main logic and data, the *core* of *Hexagonal Architecture*\) from its [[wiki/concepts/source/basic-metapatterns/layers|user interface]] comprised of platform\-specific *controller* \(input\) and *view* \(output\):

- The *controller* translates raw input into calls to the business\-centric model’s API\. It may also hide or lock widgets in the *view* when required by the input or if the *model*’s state changes\.
- The *model* is the bulk of UI\-agnostic code which executes the *controller*’s requests and notifies the *view* and, optionally, *controller* when its data changes\.
- Upon receiving a notification, the *view* reads, transforms, and presents to the user the subset of the *model*’s data which it covers\.


Each widget on the screen [may have](https://martinfowler.com/eaaDev/uiArchs.html#ModelViewController) its own *model\-view* pair\. The absence of an intermediate layer between the *view* and *model* makes the *view* heavyweight as it has to translate the *model*'s data format into something presentable to users – the flaw addressed by the 3\-layered [*MVP* patterns discussed above](#model-view-presenter-mvp-model-view-adapter-mva-model-view-viewmodel-mvvm-model-1-mvc1-document-view)\.

Both [*Action\-Domain\-Responder*](https://github.com/pmjones/adr#action-domain-responder) \(*ADR*\) and [*Resource\-Method\-Representation*](https://herbertograca.com/2018/08/31/resource-method-representation/) \(*RMR*\) are web layer patterns\. An *action* \(*method*\) receives a request, calls into a *domain* \(*resource*\) to make changes and retrieve data, and brings the results to a *responder* \(*representation*\) which prepares the return message or web page\. *ADR* is technology\-agnostic while *RMR* is HTTP\-centric\.

[*Model 2*](https://stackoverflow.com/questions/796508/what-is-the-actual-difference-between-mvc-and-mvc-model2) \(*MVC2*\) is a similar pattern from the Java world with integration logic [implemented](https://github.com/pmjones/adr/blob/master/MVC-MODEL-2.md) in the *controller*\.

A [*game development engine*](https://slideplayer.com/slide/12426213/) creates a higher\-level abstraction over input from mouse / keyboard / joystick and output to sound card and GPU while more powerful engines may also [model physics](https://discussions.unity.com/t/unity3d-architecture/565787) and character interactions\. This role is quite similar to what the original *MVC* did, with a couple of differences:

- Games often have to deal with the low\-level and very chatty interfaces of hardware components, thus the input and output are at the bottom side of the system diagram\.
- The framework itself makes a cohesive layer, becoming a kind of [[wiki/concepts/source/implementation-metapatterns/microkernel|*Microkernel*]]\.


Another difference is that while *MVC* provides for changing target platforms by rewriting its minor components \(the *view* and *controller*\), you are very unlikely to change your game framework – instead, it is the framework itself that makes all the platforms look identical to your code\.


![Diagrams of MVC with a dedicated view-controller pair for each widget, ADR and RMR where the action calls the responder, Model 2 with an orchestrating controller, and a game development engine.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/MVC%20-%20subtypes.png)


### [[wiki/concepts/source/basic-metapatterns/services|Pedestal]]


![A Pedestal has a control layer mediating hardware drivers which wrap each hardware component. An operating system adds a kernel between the drivers and an application that uses them.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Pedestal.png)


[*Pedestal*](https://alistair.cockburn.us/hexagonal-architecture) is named after the shape of its diagram and describes a system that operates multiple hardware components\. On one hand, *software* takes years to write and stabilize\. On the other hand, there are many versions and even vendors for each kind of *hardware* component, and they change over years\. Therefore, the bulk of the *software* that contains the system logic \(called [[wiki/concepts/source/extension-metapatterns/orchestrator|*control*]]\) is decoupled from the *hardware* which it manages through the use of *hardware*\-specific [[wiki/concepts/source/extension-metapatterns/proxy|*drivers*]]\. As a result, changes in *hardware* require updates only to the matching *drivers*, the business logic remaining intact\.

A similar pattern is in use with [[wiki/concepts/source/implementation-metapatterns/microkernel|*OS kernels*]], adjusted for the fact that the business logic now resides in user applications, the *kernel* acting as an [extra layer of indirection](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering)\.

### [Ports and Adapters](#full-encapsulation-ports-and-adapters), Hexagonal Architecture


![Adapters of the Hexagonal Architecture translate between the interfaces of its core and those of the adapted external components.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Monolithic%20Hexagonal.png)


[*Ports and Adapters*](https://alistair.cockburn.us/hexagonal-architecture/) – the original *Hexagonal Architecture* – provides full isolation for its business logic \(*core*\) by injecting *adapters* in all its [communication pathways](#variants-by-encapsulation)\. As a result, the *core* depends only on the interfaces, called *ports* \(hence the name of the pattern\), which it defines, with the benefits discussed [earlier in this chapter](#full-encapsulation-ports-and-adapters)\.

Just like [*MVC*](#model-view-controller-mvc-action-domain-responder-adr-resource-method-representation-rmr-model-2-mvc2-game-development-engine) it is based on, *Ports and Adapters* does not care about the contents or structure of its *core* – it is all about isolating the *core* from its environment\. The *core* may have [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] or [[wiki/concepts/source/basic-metapatterns/services|*Modules*]], or even [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugins*]] inside, but this pattern has nothing to say about them\.

### DDD\-Style Hexagonal Architecture, Onion Architecture, Clean Architecture


![Control flows for changing an entity in puristic Domain-Driven Design, pragmatic Domain-Driven Design, and Onion Architecture.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Layered%20Hexagonal.png)


As *Hexagonal Architecture* built upon the [*Domain\-Driven Design*](https://en.wikipedia.org/wiki/Domain-driven_design)’s \(*DDD*\) idea of isolating business logic with [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] \(see the [[wiki/concepts/source/extension-metapatterns/proxy|*Anticorruption Layer* and *Open Host Service*]] patterns\), it was quickly integrated back into DDD \[[wiki/concepts/source/appendices/books-referenced|[LDDD]]\]\. However, as *Ports and Adapters* appeared later than the original DDD book, namely \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\], there is no universal agreement on how this architecture should work:

- The cleanest way is for the [[wiki/concepts/source/basic-metapatterns/layers|*domain*]] layer to have nothing to do with the database – with this approach the [[wiki/concepts/source/basic-metapatterns/layers|*application*]] asks the [[wiki/concepts/source/extension-metapatterns/proxy|*repository*]] \(the database *adapter*\) to create *aggregates* \(domain objects\), then executes its business actions on the aggregates, and tells the repository to save the changed aggregates back to the database\.
- Others say that in practice the logic inside an aggregate may have to read additional information from the database or even depend on the results of persisting parts of the aggregate\. Thus it is the aggregate, not the *application*, which should save its changes, and the logic of accessing the database leaks into the domain layer\.
- [*Onion Architecture*](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) \(see the [original article](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) for the meaning of the name\) – one of early developments of *Hexagonal Architecture* and DDD – always splits the domain layer into a *domain model* and *domain services*\. The *domain model* layer contains classes with business data and business logic, which are loaded and saved by the mostly stateless *domain services* layer just above it\. And the upper *application services* layer drives use cases by calling into both domain services and the *domain model*\.
- There is also [*Clean Architecture*](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) which seems to generalize the approaches above without delving into practical details – thus the way it saves its aggregates remains a mystery\.


### Cell, Cluster, Domain


![Several intercommunicating subservices are wrapped with a cell gateway that receives client requests, adapters for outgoing communication, and a plugin.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Cell.png)


A [*Cell*](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) \(WSO2 name\), *Cluster* \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\], or [*Domain*](https://www.uber.com/en-UA/blog/microservice-architecture/) \(Uber’s name\) is an encapsulated cluster of [[wiki/concepts/source/basic-metapatterns/services|*services*]] which implements a subdomain and is usually deployed as a single unit\. It is modeled after a living cell whose contents are isolated with a membrane\. [As a rule of thumb](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography) \[[wiki/concepts/source/appendices/books-referenced|[DEDS]]\], the communication inside a *Cell* is synchronous, allowing for complex [[wiki/concepts/source/foundations-of-software-architecture/orchestration|*orchestrated*]] use cases that involve the tightly coupled *Cell* components\. Contrariwise, *Cells* are usually loosely coupled among themselves and the communications between them tend to be asynchronous \([[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreography*]]\)\.

 A *Cell* may naturally emerge when a [[wiki/concepts/source/basic-metapatterns/services|*subdomain service*]] becomes too large for comfortable development, which usually means that at least its [[wiki/concepts/source/basic-metapatterns/layers|*domain* layer]] \(already limited to a single subdomain\) is to be subdivided into sub\-subdomain components\. If other layers remain intact, this leads to a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]], otherwise the result is a subsystem of [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]]\.


![Diagrams for: a Cell with a Sandwich, a Cell with services, and a Cell with a pipeline.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Cell%20-%20Basic%20-%20Subtypes.png)


Another way a *Cell* can arise is when architects have overcommitted themselves to [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]], gradually [introducing hundreds of them](https://www.uber.com/en-UA/blog/microservice-architecture/) and turning their project into a [*Microservice Hell*](https://www.reddit.com/r/programming/comments/10xvltx/microservice_hell/)\. Now they need to group their services to:

- Have a clear high\-level picture of what is going on in the system\.
- Cut accidental dependencies between their services and the teams behind them\.
- Improve latency by co\-locating the services that interact intensely\.



![A layered system transforms into a Sandwich-based Cell. A group of stand-alone services is aggregated into a cell behind a Cell gateway.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Cell%20-%20Basic%20-%20Evolutions.png)


In the simplest implementation, the *Cell*’s contents are hidden from its clients by a [[wiki/concepts/source/extension-metapatterns/proxy|*Cell Gateway*]] which acts as an [[wiki/concepts/source/extension-metapatterns/proxy|*Open Host Service*]], allowing for anything inside the *Cell* to be changed at will with no effect on the outside world\.

> In practice, there are three kinds of outgoing traffic: responses to incoming client requests, pub/sub notifications, and requests to external services\. In a *Cell*, the *responses* are sure to pass through or be generated by the *Cell Gateway*\. Indeed, a response usually reuses the request’s transport, therefore if a request arrives at the *Gateway*, the corresponding response should also start there\. *Notifications* are harder to pinpoint: on one hand, they are a part of the *Cell*’s API which the *Gateway* takes care of\. However, that means that the *Cell*’s internals must be aware of the *Gateway*’s existence to use it for their notifications, thus creating a dependency that violates the [[wiki/concepts/source/basic-metapatterns/layers|normal order for a *layered system*]]\. Finally, *outgoing requests* bypass the *Cell Gateway* whose role is limited to the *Cell*’s API\.

Better developed *Cells* employ [[wiki/concepts/source/extension-metapatterns/proxy|*Adapters*]] for outgoing requests to build an [[wiki/concepts/source/extension-metapatterns/proxy|*Anticorruption Layer*]] that protects the *Cell*’s contents from changes in its environment\. Please note that, unlike in [*Ports and Adapters*](#ports-and-adapters-hexagonal-architecture), there is no *Adapter* for the *Cell*’s database\(s\) as they are inside the *Cell*’s perimeter\.

Another improvement, popularized by Uber’s [*Domains*](https://www.uber.com/en-UA/blog/microservice-architecture/), is the use of [[wiki/concepts/source/implementation-metapatterns/plugins|*Ambassador Plugins*]] which run pieces of business logic that belong to other *Cells* inside a host *Cell*\. That both avoids slow intercell calls and boosts the system’s fault tolerance as each *Cell* can now operate independently\.


![Injecting a part of a Cell's business logic into another Cell as an ambassador plugin improves performance by avoiding expensive intercell calls.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Cell%20-%20Full-Featured%20-%20Plugins.png)


> [In Uber](https://www.uber.com/en-UA/blog/microservice-architecture/), the service responsible for a driver’s status accepts *Plugins* from other services, such as safety checks or compliance, which can block the driver from appearing in the system and responding to ride requests\.

*Cells* facilitate recursive decomposition by subdomain\. They are the building blocks for the following patterns:

- [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Cell\-Based Architecture*]] which is [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*hierarchical*]] [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- [*Domain\-Oriented Microservice Architecture*](<Service-Oriented Architecture (SOA)#domain-oriented-microservice-architecture-doma>) which is a [*SOA*](<Service-Oriented Architecture (SOA)>) boosted by [[wiki/concepts/source/implementation-metapatterns/plugins|*Ambassador Plugins*]]\.


## Summary

*Hexagonal Architecture* isolates the component’s business logic from its external dependencies by inserting *adapters* between them\. It protects from *vendor lock\-in* and allows for late changes of third\-party components but requires all the APIs and SPIs to be designed before programming can start and often hinders performance optimizations\.

| \<\< [[wiki/concepts/source/implementation-metapatterns/plugins|Plugins]] | ^ [[wiki/concepts/source/implementation-metapatterns/implementation-metapatterns|Implementation metapatterns]] ^ | [[wiki/concepts/source/implementation-metapatterns/microkernel|Microkernel]] \>\> |
| --- | --- | --- |
