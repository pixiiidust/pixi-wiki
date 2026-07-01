---
title: "Web of Public Transport (16)"
created: 2026-07-01
updated: 2026-07-01
type: concept
status: compiled
namespace: pattern-language
pattern_number: 16
pattern_name: "Web of Public Transport"
source_repository: https://github.com/zenodotus280/apl-md
source_url: https://github.com/zenodotus280/apl-md/blob/master/Patterns/Web%20of%20Public%20Transport%20%2816%29.md
license_note: Non-commercial reuse with attribution; see namespace README and source LICENSE.md.
related_patterns:
  - "City Country Fingers (3)"
  - "Local Transport Areas (11)"
  - "Interchange (34)"
  - "Mini-Buses (20)"
---

# Web of Public Transport (16)

> Source pattern from the abridged `apl-md` corpus. Use as a design reference and constraint seed; do not treat as commercial-clean training data.

### Problem
>The system of public transportation—the entire web of airplanes, helicopters, hovercraft, trains, boats, ferries, buses, taxis, mini-trains, carts, ski-lifts, moving sidewalks—can only work if all the parts are well-connected. But they usually aren’t, because the different agencies in charge of various forms of public transportation have no incentive to connect to one another.

### Solution
>Treat interchanges as primary and transportation lines as secondary. Create incentives so that all the different modes of public transportation—airplanes, helicopters, ferries, boats, trains, rapid transit, buses, mini-buses, ski-lifts escalators, travelators, elevators—plan the lines to connect the interchanges, with the hope that gradually many different lines, of many different types, will meet at every interchange.
>
>Give the local communities control over their interchanges so that they can implement the pattern by giving contracts only to those transportation companies which are willing to serve these interchanges.


### Related Patterns
... the city, as defined by [[City Country Fingers (3)]], spreads out in a ribbon fashion, throughout the countryside, and is broken into [[Local Transport Areas (11)]]. To connect the transport areas, and to maintain the flow of people and goods along the fingers of the cities, it is now necessary to create a web of public transportation.

Keep all the various lines that converge on a single interchange, and their parking, within 600 feet, so that people can transfer on foot -- [[Interchange (34)]]. It is essential that the major stations are served by a good feeder system, so that people are not forced to use private cars at all -- [[Mini-Buses (20)]] ...

```
The example given at the end references the contrast between the Swiss railways and the French railways. It is clear that the Swiss system is better as it allows the whole of the country to participate in the economy rather than the French model which generates an obligatory relationship to the capital.
```

---

> [!cite]- Alexander, Christopher. _A Pattern Language: Towns, Buildings, Construction_. Oxford University Press, 1977, p. 92
> #APL/confidence/medium
>
> #APL/Town-Patterns/Community-Networking
