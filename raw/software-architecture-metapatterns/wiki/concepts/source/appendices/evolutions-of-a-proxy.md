---
title: "Evolutions of a Proxy"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Proxy.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Proxy
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Proxy

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Proxy.md`.

It usually makes little sense to get rid of a [[wiki/concepts/source/extension-metapatterns/proxy|*Proxy*]] once it is integrated into the system\. Its only real drawback is a slight increase in latency for user requests which may be helped through creation of [[wiki/concepts/source/extension-metapatterns/proxy|bypass channels]] between the clients and a service which needs low latency\. The other drawback of the pattern, namely the *Proxy*’s being a single point of failure, is countered by deploying multiple instances of the *Proxy*\.

As *Proxies* are usually third\-party products, there is very little we can change about them:

- We can add another kind of a *Proxy* on top of the existing one\.
- We can use a stack of *Proxies* per client, making [*Backends for Frontends*](<Backends for Frontends (BFF)>)\.


## Add another Proxy


![A proxy is added on top of an existing proxy.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Proxy%20add%20Proxy.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]], [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: avoid implementing generic functionality\.

<ins>Prerequisite</ins>: you don't have this kind of *Proxy* yet\.

A system is not limited to a single kind of *Proxies*\. As a *Proxy* represents your system without changing its function, *Proxies* are transparent, thus they are stackable\.

It often makes sense to colocate software *Proxies* or use a multifunctional *Proxy* to reduce the number of network hops between the clients and the system\. However, in a highly loaded system *Proxies* may be resource\-hungry, thus in some cases colocation strikes back\.

<ins>Pros</ins>:

- You get another aspect of your system implemented for you\.


<ins>Cons</ins>:

- Latency degrades\.
- More work for admins\.
- Another point of possible failure\.


## Deploy a Proxy per client type


![A proxy is subdivided into Backends for Frontends.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/2/Proxy%20to%20Backends%20for%20Frontends.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/proxy|Proxy]], [Backends for Frontends](<Backends for Frontends (BFF)>)\.

<ins>Goal</ins>: let the aspects of communication vary among kinds of clients\.

<ins>Prerequisite</ins>: your system serves several kinds of clients\.

If you have internal and external clients, or admins and users, you may want to vary the setup of *Proxies* for each kind of client, sometimes to the extent of physically separating network communication paths, so that each kind of client is treated according to its bandwidth, priority, and permissions\.

<ins>Pros</ins>:

- It is easy to set up various aspects of communication for a group of clients\.


<ins>Cons</ins>:

- More work for admins as the *Proxies* are duplicated\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-a-shared-repository|Evolutions of a Shared Repository]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-an-orchestrator|Evolutions of an Orchestrator]] \>\> |
| --- | --- | --- |
