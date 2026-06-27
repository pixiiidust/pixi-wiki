---
title: Job Edge
created: 2026-06-27
updated: 2026-06-27
type: entity
status: active-prototype
namespace: ai-native-product-surfaces
source: Projects/Job Edge/Index.md
confidence: high
---
# Job Edge

Job Edge is a prototype for finding **edge in crowded job searches**: freshness, geography, fit, and distribution signals that make a role more worth applying to now.

The first use case is **Ashby PM Radar**, a PM/product-role radar that turns public Ashby job-board data into an apply-action queue.

## Thesis

Most job-search tools optimize for more listings. Job Edge optimizes for better timing and lower competition.

Core question:

> Which roles are worth applying to today because timing, fit, and crowding signals create an edge?

## Current prototype

The private `pixiiidust/job-edge` repo contains:

```text
job_edge/ashby_pm_radar.py      # Ashby use-case CLI/scorer
dashboard.html                  # static interactive dashboard prototype
data/                           # saved discovery + scoring artifacts
docs/                           # product/design notes
tests/                          # unit tests
```

`ashby-pm-radar` is the first use case, not the full product boundary.

## Ashby PM Radar flow

```text
web search → extract Ashby company slugs → fetch public boards → score jobs → dashboard triage
```

Ashby exposes company-scoped public boards, not a global search endpoint:

```text
https://api.ashbyhq.com/posting-api/job-board/{companySlug}?includeCompensation=true
```

Printing Press was inspected but not used for the prototype. Direct Python was enough for the simple endpoint; the product value is the strategy layer on top.

## Edge signals

The current scorer combines:

- **Freshness** — recently posted roles are more actionable.
- **Geographic narrowing** — Toronto/GTA/Canada roles shrink the applicant pool.
- **Role specificity** — niche PM roles can be less crowded than generic product listings.
- **Personal/product fit** — AI, agents, workflow, developer tools, design/product overlap, integrations, platform, and B2B SaaS.
- **Distribution crowding** — public LinkedIn posting presence implies a larger applicant pool.

Competition is inferred. Ashby does not expose applicant counts, and LinkedIn evidence only detects public posting presence; it does not scrape applicant counts.

## Triage buckets

```text
apply_now            high score, fresh/local, no LinkedIn posting found
apply_fast_crowded   high score, found on LinkedIn, likely larger applicant pool
maybe                plausible but weaker timing/fit/competition profile
low_priority         stale or low-score roles
```

Freshness buckets:

```text
new_0_3d
fresh_4_7d
recent_8_14d
aging_15_30d
old_31_90d
stale_90d_plus
```

## Dashboard contract

The dashboard is an action queue, not a generic job board.

It supports:

- Apply and source-job links.
- Mark-applied state in browser local storage.
- Copyable job notes.
- Search by title, company, and location.
- Filters for triage, freshness, and LinkedIn presence.
- Sorting by best triage, freshness, low crowd risk, Canada/Toronto fit, role fit, or score.

Primary workflow:

```text
1. Apply now — fresh/local roles with no LinkedIn evidence.
2. Apply fast — strong roles already visible on LinkedIn.
3. Review maybes — backup queue after the top targets.
```

## Verification snapshot

The initial repository push verified:

- 9 Python unit tests passed.
- CLI package smoke returned current apply-now rows.
- Dashboard served locally with HTTP 200.
- Browser rendered the dashboard, filters/sorts worked, Apply links pointed at real Ashby application URLs, and the console had no JavaScript errors.

## Next slice

Add a refresh pipeline or real search API so discovery and LinkedIn evidence can update without manual Hermes web search. Then add row expansion for reasons/cautions, saved notes, and repost/stale-role detection.
