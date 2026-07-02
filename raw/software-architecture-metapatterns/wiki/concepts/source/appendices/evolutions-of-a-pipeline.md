---
title: "Evolutions of a Pipeline"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Appendices/Evolutions of architectures/Evolutions of a Pipeline.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Appendices/Evolutions%20of%20architectures/Evolutions%20of%20a%20Pipeline
source_license_note: "See namespace README; preserve attribution and source links."
---

# Evolutions of a Pipeline

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Appendices/Evolutions of architectures/Evolutions of a Pipeline.md`.

[[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] [[wiki/concepts/source/basic-metapatterns/services|inherits its set of evolutions from *Services*]]\. Components can be added, split in two, merged or replaced\. Many systems employ a [[wiki/concepts/source/extension-metapatterns/middleware|*Middleware*]] \(pub/sub or pipeline framework\), [[wiki/concepts/source/extension-metapatterns/shared-repository|*Shared Repository*]] \(which may be a database or file system\), or [[wiki/concepts/source/extension-metapatterns/proxy|*Proxies*]]\.

There are a couple of *Pipeline*\-specific evolutions:

- The first service of the *Pipeline* can be promoted to [[wiki/concepts/source/extension-metapatterns/orchestrator|*Front Controller*]] which tracks status updates for every request it handles\.
- Adding an [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] turns a [[wiki/concepts/source/basic-metapatterns/pipeline|*Pipeline*]] into [[wiki/concepts/source/basic-metapatterns/services|*Services*]]\. As the high\-level business logic moves to the [[wiki/concepts/source/basic-metapatterns/layers|orchestration layer]], the services don’t need to interact directly anymore, the interservice communication channels disappear, and the system turns into ordinary [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrated Services*]]\.


## Promote a service to Front Controller


![The first service of a pipeline subscribes to notifications from other services and thus becomes a Front Controller.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Pipeline%20promote%20Front%20Controller.png)


<ins>Patterns</ins>: [[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Front Controller]] \([[wiki/concepts/source/fragmented-metapatterns/polyglot-persistence|Polyglot Persistence]], [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]]\), [[wiki/concepts/source/basic-metapatterns/pipeline|Pipeline]] \([[wiki/concepts/source/basic-metapatterns/services|Services]]\)\.

<ins>Goal</ins>: allow for clients to query the state of their requests\.

<ins>Prerequisite</ins>: request processing steps are slow \(may depend on human action\)\.

If the request processing steps require heavy calculations or manual action, then clients may want to query the status of their requests, and analysts may want to see bottlenecks in the *Pipeline*\. Let the first service in the *Pipeline* track the state of all the running requests by subscribing to status notifications from other services\.

<ins>Pros</ins>:

- The state of each running request is readily available\.


<ins>Cons</ins>:

- The first service in the pipeline becomes more complex and starts depending on every other service\.


<ins>Further steps</ins>:

- The *Front Controller* may be further promoted to [[wiki/concepts/source/extension-metapatterns/orchestrator|*Orchestrator*]] if there is a need to support many complex scenarios\.


## Add an Orchestrator


![Adding an orchestrator transforms a pipeline into Orchestrated Services.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Evolutions/Services/Pipeline%20use%20Orchestrator.png)


<ins>Patterns</ins>: [[wiki/concepts/source/extension-metapatterns/orchestrator|Orchestrator]], [[wiki/concepts/source/basic-metapatterns/services|Services]]\.

<ins>Goal</ins>: support many use cases\.

<ins>Prerequisite</ins>: performance degradation is acceptable\.

When a [[wiki/concepts/source/foundations-of-software-architecture/choreography|*choreographed*]] system is gradually extended with more and more use cases, it is very likely to fall into integration hell where nobody understands how its components interrelate\. Extract the [[wiki/concepts/source/basic-metapatterns/layers|workflow logic]] into a dedicated service\.

<ins>Pros</ins>:

- New use cases are easy to add\.
- Complex scenarios are supported\.
- Error handling becomes trivial\.
- The services don’t depend on each other\.
- There is a single client\-facing team, other teams are not under pressure from the business\.
- It is easier to run actions in parallel\.
- Global scenarios become debuggable\.
- The services don’t need to be redeployed when the high\-level logic changes\.


<ins>Cons</ins>:

- The number of messages in the system doubles, thus its performance may degrade\.
- The *Orchestrator* may become a development and performance bottleneck, or a single point of failure\.


<ins>Further steps</ins>:

- If there are several clients that strongly vary in their workflows, you can apply [*Backends for Frontends*](<Backends for Frontends (BFF)>) with an *Orchestrator* per client\.
- If the *Orchestrator* grows too large, it can be [[wiki/concepts/source/extension-metapatterns/orchestrator|divided]] into layers, services, or both, with the latter option resulting in a [[wiki/concepts/source/fragmented-metapatterns/hierarchy|*Top\-Down Hierarchy*]]\.
- The *Orchestrator* can be [[wiki/concepts/source/extension-metapatterns/orchestrator|scaled]] and can have its own database\.


| \<\< [[wiki/concepts/source/appendices/evolutions-of-services-that-add-layers|Evolutions of Services that add layers]] | ^ [[wiki/concepts/source/appendices/evolutions-of-architectures|Evolutions of architectures]] ^ | [[wiki/concepts/source/appendices/evolutions-of-a-middleware|Evolutions of a Middleware]] \>\> |
| --- | --- | --- |
