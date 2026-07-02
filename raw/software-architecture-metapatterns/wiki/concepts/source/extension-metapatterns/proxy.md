---
title: "Proxy"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Extension metapatterns/Proxy.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Extension%20metapatterns/Proxy
source_license_note: "See namespace README; preserve attribution and source links."
---

# Proxy

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Extension metapatterns/Proxy.md`.


![A diagram for Services with a proxy, in abstractness-subdomain-sharding coordinates.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Main/Proxy.png)


*Should I build the wall?* A layer of indirection between your system and its clients\.

<ins>Known as:</ins> [Proxy](https://refactoring.guru/design-patterns/proxy) \[[wiki/concepts/source/appendices/books-referenced|[GoF]]\]\.

<ins>Structure:</ins> A layer that pre\-processes and/or routes user requests\.

<ins>Type:</ins> Extension component\.

| *Benefits* | *Drawbacks* |
| --- | --- |
| Separates cross\-cutting concerns from the services | A single point of failure |
| Decouples the system from its clients | Most proxies degrade latency |
| Low attack surface |  |
| Several kinds of Proxies are available off the shelf |  |

<ins>References:</ins> Half of \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] is about the use of *Proxies*\. See also: \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] on *Proxy*; [Chris Richardson](https://microservices.io/patterns/apigateway.html) and [Microsoft](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway) on *API Gateway*; [Martin Fowler](https://martinfowler.com/articles/gateway-pattern.html) on *Gateway*, *Facade*, and *API Gateway*\.

A *Proxy* stands between a \(sub\)system’s implementation and its users\. It receives a request from a client, does some pre\-processing, then forwards the request to a lower\-level component\. In other words, a *Proxy* encapsulates selected aspects of the system’s communication with its clients by serving as yet another layer of indirection\. It may also decouple the system’s internals from changes in the public protocol\. The [main functions](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway) of a *Proxy* include:

- *Isolation* – the *Proxy* hides the internals of the system behind it from the clients\. This both improves security because access to other system components is supervised and permits changes to the system’s components or structure as nothing external knows what’s behind the *Proxy*\.
- *Translation* – the *Proxy* may convert between the system’s internal protocol and its published interfaces\. [*User Interface*](#user-interface-presentation-layer-separated-presentation-command-line-interface-cli-graphical-user-interface-gui-frontend-human-machine-interface-hmi-man-machine-interface-mmi-operator-interface) is a translating *Proxy* taken to extremes: it represents the system’s internal data and commands as human\-readable information\.
- *Routing* – the *Proxy* tracks addresses of deployed instances of the system’s components and is able to forward a client’s request to the [[wiki/concepts/source/basic-metapatterns/shards|*shard*]] or [[wiki/concepts/source/basic-metapatterns/services|*service*]] which can handle it\. Clients need to know only the public address of the *Proxy*\. A *Proxy* may also respond on its own if the request is invalid or there is a matching response in the *Proxy*’s cache\.
- *Offloading* – a *Proxy* may implement generic aspects \([*cross\-cutting concerns*](https://en.wikipedia.org/wiki/Cross-cutting_concern)\) of the system’s public interface, such as authentication, authorisation, encryption, or request logging which would otherwise need to be implemented by the underlying system components\. That allows for the services to concentrate on what you write them for – the business logic\.


### Performance

Most kinds of proxies trade latency \(the extra network hop\) for some other quality:

- A [*Firewall*](#firewall-api-rate-limiter-api-throttling) slows down processing of good requests but *protects* the system from attacks\.
- Both a [*Load Balancer*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler) and a [*Dispatcher*](#dispatcher-reverse-proxy-ingress-controller-edge-service-microgateway) allow for the use of multiple servers \(with identical or specialized components, respectively\) to improve the system’s *throughput* but they still increase its minimal latency\.
- An [*Adapter*](#adapter-anticorruption-layer-abstraction-layer-open-host-service-gateway-message-translator-api-service-cell-gateway-inexact-backend-for-frontend-database-access-layer-data-mapper-repository-driver) adds *compatibility* but its latency cost is higher than with other *Proxies* as it not only forwards the original message but also changes its payload – an activity which involves data processing and serialization\.


A [*Cache*](#response-cache-read-through-cache-write-through-cache-write-behind-cache-cache-caching-layer-distributed-cache-replicated-cache) is a bit weird in that respect\. It improves latency and throughput for repeated requests but degrades latency for unique ones\. Furthermore, it is often colocated with some other kind of *Proxy* to avoid the extra network hop between the *Proxies*, which makes caching almost free in terms of latency\.

### Dependencies

*Proxies* widely vary in their functionality and level of intrusiveness\. The most generic proxies, like *Firewalls*, may not know anything about the system or its clients\. A *Response Cache* or *Adapter* must parse incoming messages, thus it depends on the communication protocol and message format\. A *Load Balancer* or *Dispatcher* is aware of both the protocol and system composition\.

In fact, because *Proxies* tend to be configurable \(on startup or through their APIs\), there is no need to modify the code of a *Proxy* each time something changes in the underlying system\.

### Applicability

*Proxy* <ins>helps</ins> with:

- *Multi\-component systems\.* Having multiple types and/or instances of services means that a client needs to know the components’ addresses to access them\. A *Proxy* encapsulates that knowledge and may also provide other common functionality as an extra benefit\.
- *Dynamic scaling or sharding\.* The *Proxy* both knows the system’s structure \(the address of each instance of a service\) and delivers user requests, thus it is the place to implement *sharding* \(when a service instance is [[wiki/concepts/source/basic-metapatterns/shards|dedicated to a subset of users]]\) or *load balancing* \(when any service instance can [[wiki/concepts/source/basic-metapatterns/shards|serve any user]]\) and even manage the size of the *Pool* of service instances\.
- *Multiple client protocols*\. When the *Proxy* is the endpoint for the system’s users it may translate multiple external \(user\-facing\) protocols into a unified internal representation\. See also [*Backends for Frontends*](<Backends for Frontends (BFF)>)\.
- *System security\.* Though a *Proxy* does not make a system more secure, it takes away the burden of security considerations from the services which implement the business logic, improving the separation of concerns and making the system components more simple and stupid\. An off\-the\-shelf *Proxy* may be less vulnerable compared to in\-house services \(but don’t disregard [security through obscurity](https://en.wikipedia.org/wiki/Security_through_obscurity)\!\)\.


*Proxy* <ins>hurts</ins>:

- *Critical real\-time paths\.* It adds an extra hop in request processing, increasing latency for thoroughly optimized use cases\. Such requests may need to bypass *Proxies*\.


### Relations


![A proxy for a monolith, shards, layers, and services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Relations/Proxy.png)


*Proxy*:

- Extends [[wiki/concepts/source/basic-metapatterns/monolith|*Monolith*]] or [[wiki/concepts/source/basic-metapatterns/layers|*Layers*]] \(forming *Layers*\), [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]], or [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\.
- Can be extended with another *Proxy* or merged with an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] into an [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Gateway*]]\.
- Can be a part of a [[wiki/concepts/source/extension-metapatterns/sandwich|*Sandwich*]]\.
- At least one *Proxy* per [[wiki/concepts/source/basic-metapatterns/services|*service*]] is employed by [[wiki/concepts/source/extension-metapatterns/middleware|*Message Bus*]], [[wiki/concepts/source/extension-metapatterns/middleware|*Enterprise Service Bus*]], [[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]], and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]\.
- Is a special case \(when there is a single kind of client\) of [*Backends for Frontends*](<Backends for Frontends (BFF)>)\.


## Variants by transparency

A *Proxy* [may either fully isolate the system which it represents or merely help establish connections](https://community.f5.com/kb/technicalarticles/what-is-a-proxy/282718) between clients and servers\. This resembles [[wiki/concepts/source/basic-metapatterns/layers|closed and open layers]] because a *Proxy* is a [[wiki/concepts/source/basic-metapatterns/layers|layer]] between a system and its clients\.

### Full Proxy


![A full proxy mediates all messages between a client and a server.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Full%20Proxy.png)


A *Full Proxy* processes every message between the system and its clients\. It completely isolates the system and may meddle with the protocols but it is resource\-heavy and adds to latency\. [*Adapters*](#adapter-anticorruption-layer-abstraction-layer-open-host-service-gateway-message-translator-api-service-cell-gateway-inexact-backend-for-frontend-database-access-layer-data-mapper-repository-driver) and [*Response Caches*](#response-cache-read-through-cache-write-through-cache-write-behind-cache-cache-caching-layer-distributed-cache-replicated-cache) are always *Full Proxies*\.

### Half\-Proxy


![A half-proxy intercepts only the session establishment request and is transparent to the following in-session communication between the client and server.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Half%20Proxy.png)


A *Half\-Proxy* intercepts, analyzes, and routes the session establishment request from a client but then goes out of the loop\. It may still forward the subsequent messages without looking into their content or it may even help connect the client and server directly, which is known as [*direct server return*](https://www.haproxy.com/glossary/what-is-direct-server-return-dsr) *\(DSR\)*\. This approach is faster and much less resource\-hungry but is also less secure and less flexible than that of *Full Proxy*\. A [*Firewall*](#firewall-api-rate-limiter-api-throttling), [*Load Balancer*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler), or [*Reverse Proxy*](#dispatcher-reverse-proxy-ingress-controller-edge-service-microgateway) may act as a *Half\-Proxy*\. IP telephony servers often use *DSR*: the server helps call parties find each other and then establish direct media communication\.

## Variants by placement

As a *Proxy* stands between a \(sub\)system and its client\(s\), we can imagine a few ways to deploy it and then generalize our observation to other kinds of system components:

### Separate deployment: Standalone


![A standalone proxy is placed between a client and a layer of services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Proxy%20placement%20-%20Standalone.png)


We can deploy a *Proxy* as a separate system component\. This has the downside of an extra network hop \(higher latency\) in the way of every client request to the system and back but that is unavoidable in the following cases:

- The *Proxy* uses a lot of system resources, thus it cannot be colocated with another component\. This mostly affects [*Firewall*](#firewall-api-rate-limiter-api-throttling) and [*Cache*](#response-cache-read-through-cache-write-through-cache-write-behind-cache-cache-caching-layer-distributed-cache-replicated-cache)\.
- The *Proxy* is stateful and deals with multiple services, which is true for a [*Load Balancer*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler), [*Reverse Proxy*](#dispatcher-reverse-proxy-ingress-controller-edge-service-microgateway), or [*API Gateway*](#api-gateway)\.


### On the system side: Sidecar


![A sidecar is co-located with the services and translates from the client's protocol to the service's API.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Proxy%20placement%20-%20Sidecar.png)


We can often co\-locate a *Proxy* with our system when the latter is not distributed\. That avoids the extra network delay, traffic, and operational complexity and does not add any new hardware which can fail at the most untimely moments\. Such a placement is called *Sidecar* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] \(after the motorcycle add\-on\) and it is mostly applicable to [*Adapters*](#adapter-anticorruption-layer-abstraction-layer-open-host-service-gateway-message-translator-api-service-cell-gateway-inexact-backend-for-frontend-database-access-layer-data-mapper-repository-driver)\.

It should be noted that *Sidecar* – co\-locating a generic component and business logic – is more of a DevOps approach than an architectural pattern, thus we can see it used in a variety of ways \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\]:

- As a *Proxy* between a component and its clients\.
- As an extra [[wiki/concepts/source/basic-metapatterns/services|*service*]] that provides observability or configures the main service\.
- As a [[wiki/concepts/source/basic-metapatterns/layers|*layer*]] containing general\-purpose utilities\.
- As an *Adapter* for [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]]\.



![A proxy between a service and its client; one between a service and a middleware; an extension aside of a service; a utility layer below a service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Sidecars.png)


[[wiki/concepts/source/implementation-metapatterns/mesh|*Service Mesh*]] \(the [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] for [[wiki/concepts/source/basic-metapatterns/services|*Microservices*]]\) makes heavy use of *Sidecars* for co\-locating any kind of generic code with every instance of a *Microservice*\.

### On the client side: Ambassador


![An ambassador runs on the client side and translates the client's protocol into the one in use with the service.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Proxy%20placement%20-%20Ambassador.png)


Finally, a *Proxy* may be co\-located with a component’s clients, making it an *Ambassador*  \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\], which is good for:

- Low\-latency systems with [[wiki/concepts/source/basic-metapatterns/shards|stateful *shards*]] – each client should access the shard that has their data, which only the *Proxy* knows how to choose\.
- [*Adapters*](#adapter-anticorruption-layer-abstraction-layer-open-host-service-gateway-message-translator-api-service-cell-gateway-inexact-backend-for-frontend-database-access-layer-data-mapper-repository-driver) that help client applications use an optimized or secure protocol\.


Notably, a [[wiki/concepts/source/implementation-metapatterns/plugins|*Plugin*]] may act as an *Ambassador* for its origin subsystem\. It makes local decisions in some scenarios while others cause it to communicate with the service it represents\. See [[wiki/concepts/source/implementation-metapatterns/plugins|*Ambassador Plugin*]]\.


![An ambassador plugin is a part of one service hosted inside another service. When called, it may consult its origin service or make independent decisions.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/4/Ambassador%20Plugin.png)


## Examples

*Proxies* are ubiquitous in backend systems as using one or several of them frees the underlying code from the need to provide boilerplate non\-business\-logic functionality\. It is common to have several kinds of *Proxies* deployed sequentially \(e\.g\. [*API Gateways*](#api-gateway) behind [*Load Balancers*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler) behind a [*Firewall*](#firewall-api-rate-limiter-api-throttling)\) with many of them [[wiki/concepts/source/basic-metapatterns/shards|*pooled*]] to improve performance and stability\. It is also possible to employ multiple kinds of *Proxies*, each serving its own kind of client, in parallel, resulting in [*Backends for Frontends*](<Backends for Frontends (BFF)>)\.

As *Proxies* are used for many purposes, there are a variety of their specializations and names\. Below is a very rough categorization, complicated by the fact that real\-world *Proxies* often implement several categories at once:

> For example, NGINX claims to be: an HTTP web server, [*Reverse Proxy*](#dispatcher-reverse-proxy-ingress-controller-edge-service-microgateway), content [*Cache*](#response-cache-read-through-cache-write-through-cache-write-behind-cache-cache-caching-layer-distributed-cache-replicated-cache), [*Load Balancer*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler), TCP/UDP *Proxy* server, and mail *Proxy* server – all at once\.

- A [*Firewall*](#firewall-api-rate-limiter-api-throttling) defends a system from attacks\.
- A [*Response Cache*](#response-cache-read-through-cache-write-through-cache-write-behind-cache-cache-caching-layer-distributed-cache-replicated-cache) reuses a system’s responses to reduce load on the system\.
- A [*Load Balancer*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler) evenly distributes requests over several instances of a service\.
- A [*Reverse Proxy*](#dispatcher-reverse-proxy-ingress-controller-edge-service-microgateway) dispatches requests that come through a single entry point to several internal services\.
- An [*Adapter*](#adapter-anticorruption-layer-abstraction-layer-open-host-service-gateway-message-translator-api-service-cell-gateway-inexact-backend-for-frontend-database-access-layer-data-mapper-repository-driver) translates between a pair of protocols or interfaces\.
- An [*API Gateway*](#api-gateway) parses a client protocol, interprets compound requests, and forwards the subrequests to multiple internal services\.
- A [*User Interface*](#user-interface-presentation-layer-separated-presentation-command-line-interface-cli-graphical-user-interface-gui-frontend-human-machine-interface-hmi-man-machine-interface-mmi-operator-interface) represents a system in a way convenient for human interaction\.


### Firewall, \(API\) Rate Limiter, API Throttling


![A firewall lets a request from a good client pass through while requests from a malicious client are blocked.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Firewall.png)


The *Firewall* is a component for white\- and black\-listing network traffic, mostly to protect against attacks\. It is possible to use both generic hardware *Firewalls* on the external perimeter for brute force \(D\)DoS protection and more complex access rules at a second layer of software *Firewalls* to protect critical data and services from unauthorized access\.

[*Rate Limiting*](https://testfully.io/blog/api-rate-limit/) makes sure that no single client uses too much of the system’s resources – it sets a limit on how many requests from a single source the system can process over a unit of time\. Any requests over the limit are rejected\.

*Throttling* differs from *Rate Limiting* in that over\-the\-limit requests are queued for later processing, effectively slowing down communication by overly active clients\.

### Response Cache, Read\-Through Cache, Write\-Through Cache, Write\-Behind Cache, Cache, Caching Layer, [[wiki/concepts/source/extension-metapatterns/shared-repository|Distributed Cache, Replicated Cache]]


![A cache proxies requests and remembers responses to shortcircuit the processing of future requests.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Cache.png)


If a system often receives identical requests, it is possible to remember its responses to most frequent of them and return the cached response without fully re\-processing the request\. The real thing is more complicated because users tend to change the data which the system stores, necessitating a variety of *cache refresh policies*\. A *Response Cache* may be co\-located with a [*Load Balancer*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler) or it may be \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] [[wiki/concepts/source/basic-metapatterns/shards|*sharded*]] \(each *Cache* processes a unique subset of requests\) and/or [[wiki/concepts/source/basic-metapatterns/shards|*replicated*]] \(all the *Caches* are similar\) and thus require a *Load Balancer* of its own\.

This kind of component is called *Response Cache* because it stores the system’s responses to requests of its users or just *Cache* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] because it is the most common kind of a *Cache* in systems architecture\.

If the cached subsystem is a database, we can discern between read and write requests:

- [*Read\-Through Cache*](https://www.enjoyalgorithms.com/blog/read-through-caching-strategy) is when the *Cache* is updated on a miss for a read request but is transparent to or invalidated by write requests\.
- [*Write\-Through Cache*](https://www.enjoyalgorithms.com/blog/write-through-caching-strategy) is when the *Cache* is updated by write requests that pass through it\.
- [*Write\-Behind*](https://www.enjoyalgorithms.com/blog/write-behind-caching-pattern) is when the *Cache* aggregates multiple write requests to later send them to the database as a batch, saving bandwidth and possibly merging multiple updates of the same key\.


It is possible to combine multiple servers into a virtual *Caching Layer* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\]:

- In the simplest case, which does not require any additional instrumentation aside from a [*Load Balancer*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler), the instances of the *Caches* are independent and may return stale results\.
- In a *Distributed Cache*, driven by a [*Sharding Proxy*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler), every server \([[wiki/concepts/source/basic-metapatterns/shards|*shard*]]\) holds a subset of the cached data, thus allowing for caching datasets which don’t fit in a single computer’s memory\.
- In a *Replicated Cache* the datasets of all the servers are identical and synchronized on any modification\. This scales the cache’s throughput but requires a kind of synchronization engine, e\.g\. a [[wiki/concepts/source/extension-metapatterns/shared-repository|*Data Grid*]]\.


### Load Balancer, Sharding Proxy, Cell Router, Messaging Grid, Scheduler


![A load balancer forwards a client's request to any idle instance of a stateless service. A sharding proxy forwards a client's request to the shard that contains the client's data.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Load%20Balancer.png)


Here we have a hardware or software component which distributes user traffic among multiple [[wiki/concepts/source/basic-metapatterns/shards|instances]] of a service:

- A *Sharding Proxy* \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] selects a [[wiki/concepts/source/basic-metapatterns/shards|*shard*]] based on specific data which is present in a request \(OSI level 7 request routing\) for a system where each shard owns a part of the system’s state, therefore only one \(or a few for [[wiki/concepts/source/basic-metapatterns/shards|*replicated*]] *shards*\) of the shards has the data required to process the client’s request\.
- A [*Load Balancer*](https://en.wikipedia.org/wiki/Load_balancing_(computing)) \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\] for a [[wiki/concepts/source/basic-metapatterns/shards|*Pool of stateless instances*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Replicas*]], or a *Messaging Grid* \[[wiki/concepts/source/appendices/books-referenced|[FSA]]\] of [[wiki/concepts/source/extension-metapatterns/sandwich|*Space\-Based Architecture*]] evenly distributes the incoming traffic over identical request processors \([OSI level](https://en.wikipedia.org/wiki/OSI_model) 4 load balancing\) to protect any instance of the underlying system from overload\. In some cases it needs to be session\-aware \(process OSI level 7\) to assure that all the requests from a client are forwarded to the same instance of the service \[[wiki/concepts/source/appendices/books-referenced|[DDS]]\]\.
- It may forward read requests to [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|*Read\-Only Replicas*]] of the data while write requests are sent to the *leader* database \([*CQRS*](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)\-like behavior\)\.
- A [*Cell Router*](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/cell-routing.html) chooses a data center which is the closest to the user’s location\.


*Load Balancers* are very common in high\-load backends\. High\-availability systems deploy multiple instances of a *Load Balancer* in parallel to remain functional if one of the *Load Balancers* fails\. CPU\-intensive applications \(e\.g\. 3D games\) often post asynchronous tasks for execution by *Thread Pools* under the supervision of a *Scheduler*\. A similar pattern is found in OS kernels and *fiber* or *actor* frameworks where a limited set of CPU\-affined threads is scheduled to run a much larger number of tasks\.

### Dispatcher, Reverse Proxy, Ingress Controller, Edge Service, Microgateway


![A dispatcher exposes an interface which merges the interfaces of the services below the dispatcher.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Dispatcher.png)


A [*Reverse Proxy*, *Ingress Controller*](https://traefik.io/blog/reverse-proxy-vs-ingress-controller-vs-api-gateway/), [*Edge Service*](https://medium.com/knerd/api-infrastructure-at-knewton-whats-in-an-edge-service-51a3777aeb41), or [*Microgateway*](https://github.com/wso2/reference-architecture/blob/master/event-driven-api-architecture.md) is a router that stands between the Internet and the organization’s internal network\. It allows clients to use a public address for the system without knowing how and where their requests are processed\. It parses user requests and forwards them to an internal server based on the requests’ bodies\. A *Reverse Proxy* can be extended with a [*firewall*](#firewall-api-rate-limiter-api-throttling), *SSL termination*, [*load balancing*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler), and [*caching*](#response-cache-read-through-cache-write-through-cache-write-behind-cache-cache-caching-layer-distributed-cache-replicated-cache) functionality\. Examples include Nginx\.

*Dispatcher* \[[wiki/concepts/source/appendices/books-referenced|[POSA1]]\] is a similar component for a single\-process application\. It serves a complex command line interface by receiving and preprocessing user commands only to forward each command to a module which knows how to handle it\. The modules may register their commands with the *Dispatcher* at startup or there may be a static dispatch table in the code\.

You could have noticed that *Dispatcher* or *Reverse Proxy* is quite similar to [*Load Balancer* or *Sharding Proxy*](#load-balancer-sharding-proxy-cell-router-messaging-grid-scheduler) – they differ mostly in what kind of system lies below them: [[wiki/concepts/source/basic-metapatterns/services|*Services*]] or [[wiki/concepts/source/basic-metapatterns/shards|*Shards*]]\.

### Adapter, [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Anticorruption Layer, Abstraction Layer]], [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Open Host Service]], Gateway, Message Translator, API Service, Cell Gateway, \(inexact\) Backend for Frontend, Database Access Layer, Data Mapper, Repository, [[wiki/concepts/source/basic-metapatterns/services|Driver]]


![An adapter between a client and a service provider translates between their protocols.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/Adapter.png)


An [*Adapter*](https://refactoring.guru/design-patterns/adapter) \[[wiki/concepts/source/appendices/books-referenced|[GoF]], [[wiki/concepts/source/appendices/books-referenced|DDS]]\] is a mostly stateless *Proxy* that translates between an internal and public protocol and API formats\. It may often be co\-located with a [*Reverse Proxy*](#dispatcher-reverse-proxy-ingress-controller-edge-service-microgateway)\. When it adapts messages, it is called a *Message Translator* \[[wiki/concepts/source/appendices/books-referenced|[EIP]], [[wiki/concepts/source/appendices/books-referenced|POSA4]]\]\.

*Adapters* are often found between two system components \(in [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]\) or between a component and [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] \(in [[wiki/concepts/source/extension-metapatterns/middleware|*Enterprise Service Bus*]] and [[wiki/concepts/source/extension-metapatterns/middleware|*Service Mesh*]]\)\.

In \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\], when one component \(*consumer*\) depends on another \(*supplier*\), there may be an *Adapter* in between to [[wiki/concepts/source/analytics/indirection-in-commands-and-queries|decouple them]]\. It is called *Anticorruption Layer* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] \(as it protects its host from changes in its dependencies\) when owned by the *consumer*’s team or *Open Host Service* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] \(for its readiness to serve any clients\) if the *supplier* adds it to grant one or more stable interfaces \(*Published Languages* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\)\.

A *Gateway* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\] or an [*API Service*](https://backendless.com/what-is-api-as-a-service/) often implies an *Adapter* with extra functionality, like *Reverse Proxy*, authorization, and authentication\. [*Cell Gateway*](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) is a *Gateway* for a [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Cell*]]\.

When a *Gateway* translates a single public API method into several calls towards internal services, it becomes an [*API Gateway*](#api-gateway) \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] which is an aggregate of *Proxy* \(protocol translation\) and [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] \(integration of the lower\-level services\)\.

An *Adapter* between an end\-user client \(web interface, mobile application, etc\.\) and the system’s API is often called [*Backend for Frontend*](<Backends for Frontends (BFF)>)\. It decouples the UI from the backend\-owned system’s API, giving the teams behind both components the freedom to work more independently as changes in one component no longer directly affect the other\.

Adapters between software and hardware components are called \(*device*\) *Drivers*\.

There is also a whole bunch of *Abstraction Layers* that aim to protect the business logic from its environment, the idea which [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|is perfected]] by [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]:

- [*Hardware Abstraction Layer*](https://en.wikipedia.org/wiki/Hardware_abstraction) \(*HAL*\) hides details of hardware to make the code which controls it portable\.
- [*Operating System Abstraction Layer*](https://en.wikipedia.org/wiki/Operating_system_abstraction_layer) \(*OSAL*\) or *Platform Abstraction Layer* \(*PAL*\) abstracts the OS to make the application cross\-platform\.
- [*Database Abstraction Layer*](https://en.wikipedia.org/wiki/Database_abstraction_layer) \(*DBAL* or *DAL*\), *Database Access Layer* \[[wiki/concepts/source/appendices/books-referenced|[POSA4]]\] or *Data Mapper* \[[wiki/concepts/source/appendices/books-referenced|[PEAA]]\] attempts to help building database\-agnostic applications by making all the databases look the same\.
- [*Repository*](https://martinfowler.com/eaaCatalog/repository.html) \[[wiki/concepts/source/appendices/books-referenced|[PEAA]], [[wiki/concepts/source/appendices/books-referenced|DDD]]\] provides methods to access a record stored in a database as if it were an object in the application’s memory\.


> An *Adapter* creates a [layer of indirection](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering) between your code and a library or service which it uses\. If the external component’s interface changes, or you need to substitute a component with an incompatible implementation from another vendor, and your code accesses the component directly, you will have to make many changes throughout your code\. However, if there is an *Adapter* in\-between, your code depends only on the interface of the *Adapter*\. And when the external component changes or is replaced, only the relatively small *Adapter*’s implementation needs to change while your main code is blessed with ignorance of what lies beyond the *Adapter*’s borders\.

### [[wiki/concepts/source/extension-metapatterns/orchestrator|API Gateway]]


![An API Gateway both translates from the client's to the system's protocol and calls services in parallel.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/API%20Gateway.png)


*API Gateway* \[[wiki/concepts/source/appendices/books-referenced|[MP]]\] is a fusion of [*Gateway*](#adapter-anticorruption-layer-abstraction-layer-open-host-service-gateway-message-translator-api-service-cell-gateway-inexact-backend-for-frontend-database-access-layer-data-mapper-repository-driver) \(*Proxy*\) and [[wiki/concepts/source/extension-metapatterns/orchestrator|*API Composer*]] \([[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]]\)\. The *Gateway* aspect encapsulates the external \(public\) protocol while the *API Compose*r translates the system’s high\-level public API methods into multiple \(usually parallel\) calls to the APIs of internal components, collects the results, and conjoins them into a response\.

*API Gateway* is [[wiki/concepts/source/extension-metapatterns/orchestrator|discussed in more detail]] under *Orchestrator*\.

### User Interface, Presentation Layer, [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|Separated Presentation]], Command Line Interface \(CLI\), Graphical User Interface \(GUI\), Frontend, Human\-Machine Interface \(HMI\), Man\-Machine Interface \(MMI\), Operator Interface


![A user interface stands between a human and software. It receives mouse input and produces output on a display.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Variants/2/User%20Interface.png)


An *Adapter* between a human and a computer system is called a [[wiki/concepts/source/basic-metapatterns/layers|*User Interface*]] \(*UI*\) or *Presentation Layer* \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\]\. Though a *UI* mainly translates user actions into commands to the underlying system and presents the results which the system returns and other information supposedly important to the user, it may also include [[wiki/concepts/source/basic-metapatterns/layers|*integration logic*]] \(use cases\) which are occasionally tightly coupled to the visual behavior\. *UI* comes in several flavors:

- *Command Line Interface* \(*CLI*\) is text\-based and sequential – it executes one command at a time\. It’s the simplest kind of *UI*\.
- *Graphical User Interface* \(*GUI*\) is built around graphical representation of information and controls\. It may rely on the windowing system of the underlying OS, a third\-party framework, or build something unique, which takes place in games\.
- *Frontend* is an [*Ambassador*](#on-the-client-side-ambassador) executed by a client’s browser on the system’s behalf\.
- [*Human\-Machine Interface*](https://en.wikipedia.org/wiki/User_interface#Terminology) \(*HMI*\) or *Man\-Machine Interface* \(*MMI*\) is usually used for human interaction with an embedded system\. Sometimes this term may include both input / output hardware \(e\.g\. mouse and display, or touch screen\) and software that operates it\.
- [*Operator Interface*](https://en.wikipedia.org/wiki/User_interface#Terminology) is an *HMI* that grants its user access to a system of several embedded devices\.


[*Separated Presentation*](https://martinfowler.com/eaaDev/SeparatedPresentation.html) is, basically, another name for *User Interface* except that this pattern focuses on dispensability of any implementation of a *UI*: the same system can be driven by a *CLI*, *GUI*, or *Frontend* without noticing any difference\. Many variants of *Separated Presentation* are known as [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVP*]] and [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*MVC*]] families of patterns discussed under [[wiki/concepts/source/implementation-metapatterns/hexagonal-architecture|*Hexagonal Architecture*]]\.

## [[wiki/concepts/source/appendices/evolutions-of-a-proxy|Evolutions]]

It usually makes little sense to get rid of a *Proxy* once it has been integrated into a system\. The only real drawback to using a *Proxy* is a slight increase in latency for user requests which may be mitigated through the creation of [bypass channels](#half-proxy) between the clients and a service which needs low latency\. The other drawback of the pattern, the *Proxy* being a single point of failure, is countered by deploying multiple instances of the *Proxy*\.

As *Proxies* are usually third\-party products, there is not much that [[wiki/concepts/source/appendices/evolutions-of-a-proxy|we can change about them]]:

- We can add another kind of a *Proxy* on top of an existing one\.



![A proxy is added on top of an existing proxy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Proxy%20add%20Proxy.png)


- We can use a stack of *Proxies* per client, making [*Backends for Frontends*](<Backends for Frontends (BFF)>)\.



![A proxy is subdivided into Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Proxy%20to%20Backends%20for%20Frontends.png)


## Summary

 A *Proxy* represents your system to its clients and takes care of some aspects of the communication\. It is common to see multiple *Proxies* deployed sequentially as they are often stackable\.

| \<\< [[wiki/concepts/source/extension-metapatterns/shared-repository|Shared Repository]] | ^ [[wiki/concepts/source/extension-metapatterns/extension-metapatterns|Extension metapatterns]] ^ | [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]] \>\> |
| --- | --- | --- |
