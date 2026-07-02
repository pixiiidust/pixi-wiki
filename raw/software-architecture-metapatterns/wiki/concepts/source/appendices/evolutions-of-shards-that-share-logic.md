---
title: "Evolutions of Shards that share logic"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of Shards that share logic.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20Shards%20that%20share%20logic
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of Shards that share logic

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of Shards that share logic.md`.

Other cases are better solved by extracting the logic that manipulates multiple [[wiki/concepts/source/basic-metapatterns/shards|*shards*]]:

- Splitting a [[wiki/concepts/source/basic-metapatterns/services|*service*]] \(as discussed [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-data|above]]\) yields a component that represents both shared data and shared logic\.
- Adding a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] lets the shards communicate with each other without keeping direct connections\. It also may do housekeeping: error recovery, replication, and scaling\.
- A [[wiki/concepts/source/extension-metapatterns/proxy|*Sharding Proxy*]] hides the existence of the shards from clients\.
- An [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] calls \(or messages\) multiple shards to serve a user request\. That relieves the shards of the need to coordinate their states and actions by themselves\.


## Add a Middleware

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Middleware.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Middleware.png" alt="A middleware manages shards and lets them communicate to each other." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Shards]], [[wiki/concepts/source/extension-metapatterns/middleware|Middleware]], [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: simplify the communication between shards, their deployment, and recovery\.

<ins>Prerequisite</ins>: many shards need to exchange information, some may fail\.

A *Middleware* transports messages between shards, checks their health, and recovers ones which have crashed\. It may manage data replication and deployment of software updates as well\.

<ins>Pros</ins>:

- The shards become simpler because they don’t need to track each other\.
- Many good third\-party implementations are readily available\.


<ins>Cons</ins>:

- Performance may degrade\.
- The components of the *Middleware* are new points of failure\.


## Add a Sharding Proxy

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Load%20Balancer.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20add%20Load%20Balancer.png" alt="A sharding proxy relieves clients from the need to find the appropriate shard." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Shards]], [[wiki/concepts/source/extension-metapatterns/proxy|Sharding Proxy]] \([[wiki/concepts/source/extension-metapatterns/proxy|Proxy]]\), [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: simplify the code on the client side, hide your implementation from clients\.

<ins>Prerequisite</ins>: each client connects directly to the shard which owns their data\.

The client application may know the address of the shard which serves it and connect to it without intermediaries\. That is the fastest means of communication, but it prevents you from changing the number of shards or other details of your implementation without updating all the clients, which may be unachievable\. An intermediary may help\.

<ins>Pros</ins>:

- Your system becomes isolated from its clients\.
- You can put generic aspects into the *Proxy* instead of implementing them in the shards\.
- *Proxies* are readily available\.


<ins>Cons</ins>:

- The extra network hop increases latency unless you deploy the *Sharding Proxy* as an [[wiki/concepts/source/extension-metapatterns/proxy|*Ambassador*]] co\-located with every client which, however, brings back the issue of client software updates\.
- The *Sharding Proxy* is a single point of failure unless [[wiki/concepts/source/basic-metapatterns/shards|*replicated*]]\.


## Move the integration logic into an Orchestrator

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20use%20Orchestrator.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Evolutions/Shards/Shards%20use%20Orchestrator.png" alt="The high-level logic of shards moves to a shared orchestrator which integrates the data stored within and processed by individual shards." loading="lazy" width=100%/>
</a>
</div>

<ins>Patterns</ins>: [[wiki/concepts/source/basic-metapatterns/shards|Shards]], [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]], [[wiki/concepts/source/basic-metapatterns/layers|Layers]]\.

<ins>Goal</ins>: isolate the shards and eliminate their awareness of each other\.

<ins>Prerequisite</ins>: the shards are coupled through their high\-level logic\.

When a high\-level scenario uses multiple shards \([[wiki/concepts/source/extension-metapatterns/orchestrator|*Scatter\-Gather* and *MapReduce*]] are the simplest examples\), the way to follow is to extract all such scenarios into a dedicated stateless component\. That makes the shards independent of each other\.

<ins>Pros</ins>:

- The shards don’t need to be aware of each other\.
- The high\-level logic can be written in a high\-level language by a dedicated team\.
- The high\-level logic can be deployed independently\.
- The main bulk of the code should become much simpler\.


<ins>Cons</ins>:

- Latency will increase\.
- The *Orchestrator* becomes a single point of failure which has a good chance to corrupt your data\.


<ins>Further steps</ins>:

- [[wiki/concepts/source/extension-metapatterns/orchestrator|*Shard* or *replicate* the *Orchestrator*]] to support higher load and to remain online if it fails\.
- *Persist* the *Orchestrator* \(give it a dedicated database\) to make sure that it does not leave half\-committed transactions upon failure\.
- *Divide* the *Orchestrator* [[wiki/concepts/source/appendices/evolutions-of-layers-to-gain-flexibility|into *Backends for Frontends*]] or a [[wiki/concepts/source/extension-metapatterns/orchestrator|*SOA*\-style layer]] if you have multiple kinds of clients or workflows, respectively\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-shards-that-share-data|Evolutions of Shards that share data]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-layers-that-make-more-layers|Evolutions of Layers that make more layers]] \>\> |
| --- | --- | --- |
