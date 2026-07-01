---
title: "Mini-Buses (20)"
created: 2026-07-01
updated: 2026-07-01
type: concept
status: compiled
namespace: pattern-language
pattern_number: 20
pattern_name: "Mini-Buses"
source_repository: https://github.com/zenodotus280/apl-md
source_url: https://github.com/zenodotus280/apl-md/blob/master/Patterns/Mini-Buses%20%2820%29.md
license_note: Non-commercial reuse with attribution; see namespace README and source LICENSE.md.
related_patterns:
  - "Local Transport Areas (11)"
  - "Web of Public Transport (16)"
  - "Parallel Roads (23)"
  - "Interchange (34)"
  - "Bus Stop (92)"
---

# Mini-Buses (20)

> Source pattern from the abridged `apl-md` corpus. Use as a design reference and constraint seed; do not treat as commercial-clean training data.

### Problem
>Public transportation must be able to take people from any point to any other point within the metropolitan area.

### Solution
>Establish a system of small taxi-like buses, carrying up to six people each, radio-controlled, on call by telephone, able to provide point-to-point service according to the passengers’ needs, and supplemented by a computer system which guarantees minimum detours, and minimum waiting times. Make bus stops for the mini-buses every 600 feet in each direction, and equip these bus stops with a phone for dialing a bus.

### Related Patterns
... this pattern helps complete the [[Local Transport Areas (11)]] and the [[Web of Public Transport (16)]]. The local transport areas rely heavily on foot traffic, and on bikes and carts and horses. The web of public transportation relies on trains and planes and buses. Both of these patterns need a more flexible form of public transportation to support them.

Place the stops mainly along major roads, as far as this can be consistent with the fact that no one ever has to walk more than 600 feet to the nearest one -- [[Parallel Roads (23)]]; put one in every [[Interchange (34)]]; and make each one a place where a few minutes' wait is pleasant -- [[Bus Stop (92)]] ...

---

> [!cite]- Alexander, Christopher. _A Pattern Language: Towns, Buildings, Construction_. Oxford University Press, 1977, p. 110
> #APL/confidence/medium
>
> #APL/Town-Patterns/Community-Networking
