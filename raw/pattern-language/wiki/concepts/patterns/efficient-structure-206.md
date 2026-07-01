---
title: "Efficient Structure (206)"
created: 2026-07-01
updated: 2026-07-01
type: concept
status: compiled
namespace: pattern-language
pattern_number: 206
pattern_name: "Efficient Structure"
source_repository: https://github.com/zenodotus280/apl-md
source_url: https://github.com/zenodotus280/apl-md/blob/master/Patterns/Efficient%20Structure%20%28206%29.md
license_note: Non-commercial reuse with attribution; see namespace README and source LICENSE.md.
related_patterns:
  - "Structure Follows Social Spaces (205)"
  - "Floor and Ceiling Layout (210)"
  - "Floor-Ceiling Vaults (219)"
  - "Roof Layout (209)"
  - "Roof Vaults (220)"
  - "Final Column Distribution (213)"
  - "Columns at the Corners (212)"
  - "Perimeter Beams (217)"
  - "Box Columns (216)"
  - "Wall Membranes (218)"
  - "Frames as Thickened Edges (225)"
  - "Column Connections (227)"
---

# Efficient Structure (206)

> Source pattern from the abridged `apl-md` corpus. Use as a design reference and constraint seed; do not treat as commercial-clean training data.

### Problem
>Some buildings have column and beam structures; others have load-bearing walls with slab floors; others are vaulted structures, or domes, or tents. But which of these, or what mixture of them, is actually the most efficient? What is the best way to distribute materials throughout a building, so as to enclose the space, strongly and well, with the least amount of material?

### Solution
>Conceive the building as a building made from one continuous body of compressive material. In its geometry, conceive it as a three-dimensional system of individually vaulted spaces, most of them roughly rectangular; with thin load-bearing walls, each stiffened by columns at intervals along its length, thickened where walls meet walls and where walls meet vaults and stiffened around the openings.

### Related Patterns
... this pattern complements the pattern [[Structure Follows Social Spaces (205)]]. Where that pattern defines the relationship between the social spaces and the structure, this pattern lays down the kind of structure which is dictated by pure engineering. As you will see, it is compatible with [[Structure Follows Social Spaces (205)]], and will help to create it.

The layout of the inner vaults is given in [[Floor and Ceiling Layout (210)]] and [[Floor-Ceiling Vaults (219)]]; the layout of the outer vaults which form the roof is given in [[Roof Layout (209)]] and [[Roof Vaults (220)]]. The layout of the stiffeners which make the walls is given in [[Final Column Distribution (213)]]; the layout of the thickening where walls meet walls is given by [[Columns at the Corners (212)]]; the thickening where walls meet vaults is given by [[Perimeter Beams (217)]]; the construction of the columns and the walls is given by [[Box Columns (216)]] and [[Wall Membranes (218)]]; the thickening of doors and window frames is given by [[Frames as Thickened Edges (225)]]; and the non- right-angled connection between columns and beams by [[Column Connections (227)]] ...

---

> [!cite]- Alexander, Christopher. _A Pattern Language: Towns, Buildings, Construction_. Oxford University Press, 1977, p. 946.
> #APL/confidence/medium
>
> #APL/Construction-Patterns/Emergent-Structure
