---
title: "Arranging communication"
created: 2026-07-02
updated: 2026-07-02
type: source-page
status: imported
namespace: software-architecture-metapatterns
source_repository: https://github.com/denyspoltorak/metapatterns
source_wiki: https://github.com/denyspoltorak/metapatterns/wiki
source_path: "Foundations of software architecture/Arranging communication/Arranging communication.md"
source_url: https://github.com/denyspoltorak/metapatterns/wiki/Foundations%20of%20software%20architecture/Arranging%20communication/Arranging%20communication
source_license_note: "See namespace README; preserve attribution and source links."
---

# Arranging communication

> Imported source page from Denys Poltorak's *Architectural Metapatterns* wiki. Source path: `Foundations of software architecture/Arranging communication/Arranging communication.md`.

As a project grows, it tends to become subdivided into services, modules, or whatever you call the [[wiki/concepts/source/basic-metapatterns/services|components that match its subdomains]] \(or *bounded contexts*, if you prefer the \[[wiki/concepts/source/appendices/books-referenced|[DDD]]\] convention\)\. Still, there remain system\-wide use cases that require collaboration from many or all of the system’s parts – otherwise the components don’t even form a single system\. Let’s see how they can be integrated\.

<div align="center">
<a href="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Monolith%20to%20Services.png">
<img src="https://raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Communication/Monolith%20to%20Services.png" alt="A monolithic system is subdivided into several services but it is an open question how the resulting components should be integrated." loading="lazy" width=100%/>
</a>
</div>

As integration is not unique to distributed systems – it is present even in smaller programs that need to make data, functions, and classes work together – we’ll take a look at programming and architectural paradigms next\.

## Contents:

- [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|Programming and architectural paradigms]]
- [[wiki/concepts/source/foundations-of-software-architecture/orchestration|Orchestration]]
- [[wiki/concepts/source/foundations-of-software-architecture/choreography|Choreography]]
- [[wiki/concepts/source/foundations-of-software-architecture/shared-data|Shared data]]
- [[wiki/concepts/source/foundations-of-software-architecture/comparison-of-communication-styles|Comparison of communication styles]]

| \<\< [[wiki/concepts/source/foundations-of-software-architecture/four-kinds-of-software|Four kinds of software]] | ^ [[wiki/concepts/source/foundations-of-software-architecture/foundations-of-software-architecture|Foundations of software architecture]] ^ | [[wiki/concepts/source/foundations-of-software-architecture/programming-and-architectural-paradigms|Programming and architectural paradigms]] \>\> |
| --- | --- | --- |
