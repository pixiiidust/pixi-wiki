---
title: Job Edge
created: 2026-06-27
updated: 2026-06-30
type: entity
status: live-public-prototype
namespace: ai-native-product-surfaces
source: Projects/Job Edge/Index.md
confidence: high
---
# Job Edge

Job Edge is a live public prototype for finding **edge in crowded job searches**: freshness, geography, fit, and distribution signals that make a role more worth applying to now.

The first use case is **Ashby PM Radar**, a PM/product-role radar that turns public Ashby job-board data into an apply-action queue.

## Thesis

Most job-search tools optimize for more listings. Job Edge optimizes for better timing and lower competition.

Core question:

> Which roles are worth applying to today because timing, fit, and crowding signals create an edge?

## Current prototype

The public dashboard is live at:

```text
https://pixiiidust.github.io/job-edge/
```

The public `pixiiidust/job-edge` repo contains:

```text
job_edge/ashby_pm_radar.py                # Ashby use-case CLI/scorer
scripts/refresh_ashby_pm_radar.py         # refresh wrapper for local/GitHub Actions use
.github/workflows/refresh-ashby-pm-radar.yml
dashboard.html                            # static interactive dashboard
data/                                     # saved discovery, scoring, dashboard, provenance artifacts
docs/                                     # product/PRD notes
tests/                                    # unit tests
```

`ashby-pm-radar` is the first use case, not the full product boundary.

## Ashby PM Radar flow

Current automatic flow:

```text
saved Ashby company slugs → fetch public boards → score jobs → commit static JSON → publish GitHub Pages
```

Ashby exposes company-scoped public boards, not a global search endpoint:

```text
https://api.ashbyhq.com/posting-api/job-board/{companySlug}?includeCompensation=true
```

GitHub Actions now runs the refresh every 6 hours and on manual workflow dispatch. The browser does not run Python; the dashboard only re-fetches the latest published static JSON.

## Discovery boundary

Job Edge currently refreshes **known Ashby boards** from `data/discovered_slugs.txt`. It does **not yet automatically search the public web for brand-new Ashby companies**.

This means a future run can still show `150` jobs and be healthy. The success signal is a fresh generated timestamp plus current board data, not a changed count.

Next discovery layer:

```text
automated search queries → extract jobs.ashbyhq.com/{slug} → update slug list with provenance → refresh boards
```

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
- Manual `Run Ashby refresh` link to the GitHub Actions workflow.
- `Reload latest published data` button for re-fetching the current static snapshot.

Primary workflow:

```text
1. Apply now — fresh/local roles with no LinkedIn evidence.
2. Apply fast — strong roles already visible on LinkedIn.
3. Review maybes — backup queue after the top targets.
```

## Verification snapshot

2026-06-30 auto-refresh milestone verified:

- PR #10 merged on `pixiiidust/job-edge`.
- GitHub Action run succeeded.
- Pages status returned `built`.
- Live dashboard rendered 150 jobs from the auto-refreshed JSON snapshot.
- Latest verified generated timestamp: `2026-06-30T22:08:53.138975+00:00`.
- Browser smoke confirmed the refresh link, reload button, job rows, and no JavaScript console errors.

## Next slice

Add automated discovery for new Ashby company slugs and a “new / removed / changed since last refresh” diff layer so users can distinguish a healthy refresh from a stable job count.
